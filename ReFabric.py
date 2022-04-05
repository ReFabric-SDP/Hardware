import socket
import requests
import serial
from time import sleep
from pickup_action import PickupAction
from ev3_commands import EV3Commands
from drop_off_action import DropOffAction
import threading


class ReFabric:
    ev3_port = 54321  # corresponds to that in ev3.py
    # ev3_addr = "IP_ADDR_HERE"
    # vision_pi_addr = "IP_ADDR_HERE"

    def __init__(self, ev3_addr, vision_pi_addr, hardcode=True):
        self.pickup_actions_hardcoded = [PickupAction.TOP_LEFT_UPPER, PickupAction.TOP_LEFT_LOWER, PickupAction.TOP_RIGHT_LOWER, PickupAction.BOTTOM_LEFT_LOWER, PickupAction.BOTTOM_RIGHT_LOWER]
        self.hardcode = hardcode

        self.ev3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ev3_socket.connect((ev3_addr, self.ev3_port))
        self.vision_pi_addr = vision_pi_addr  # the other pi
        self.vision_pi_url = "http://" + vision_pi_addr + ":5000"

        self.ser = serial.Serial('/dev/ttyACM0')  # connects to the arm
        self.ser.flushInput()

        self.app_data = None
        self.is_started = False
        self.main_loop_thread = None
        self.main_lock = threading.Lock()

    def on_app_sync(self, sync_data):
        """Relay sync data to vision pi"""
        self.app_data = sync_data
        requests.post(self.vision_pi_url, json=sync_data)

    def start(self):
        if not self.main_loop_thread:
            # vision will need to take a picture of the background
            requests.get(self.vision_pi_url + "/take_background")
            self.is_started = True
            self.main_loop_thread = threading.Thread(target=self.run)
            self.main_loop_thread.start()
        else:
            with self.main_lock:
                self.is_started = True

    def stop(self):
        with self.main_lock:
            self.is_started = False

    def run(self):
        """main running loop"""
        # 0. check self.is_started, if so do the following
        # 1. get pick up location from vision pi
        # 2. send command to arduino
        # 3. wait for arduino pick up action to finish
        # 4. call do_classification on vision pi, get bucket for drop off
        # 5. send command to ev3, wait for movement to finish
        # 6. send command to arm for dropping off, wait for finish
        # 7. send command to ev3 to move back, wait for finish, loop done
        while True:
            if not self.is_started:
                sleep(0.1)
                continue
            # hardcoded magic goes here
            if self.hardcode:
                if len(self.pickup_actions_hardcoded) == 0:
                    action = 0
                else:
                    action = self.pickup_actions_hardcoded.pop(0)
            else:
                # action should be an int from 1 to 8 inclusive, representing actions to be performed by the arm
                action = int(requests.get(self.vision_pi_url + "/get_pickup_action").text)
                print("got action %d from vision pi" % action)

            if action == 0:  # nothing left to grab
                print("nothing left to grab, stopping")
                with self.main_lock:
                    self.is_started = False
                    continue

            # send to arm
            self.ser.write(action.to_bytes(1, 'big'))
            self.ser.flush()
            print("sent action %d to arm" % action)

            # await confirmation of action finish
            # TODO: arm needs to perform said action, and raise to camera position
            confirmation = int.from_bytes(self.ser.read(), 'big')
            if confirmation != action:
                print("ERROR, arm action %d different from command %d" % (confirmation, action))
                continue
            else:
                # okay, go to standby position before dropping/moving car
                print("action %d finished by arm, moving to standby position" % action)
                self.ser.write(PickupAction.STANDBY.to_bytes(1, 'big'))
                self.ser.flush()
                standby_done = int.from_bytes(self.ser.read(), 'big')
                if standby_done != 99:  # this is hardcoded
                    print("ERROR, standby confirmation %d, should be 99" % standby_done)
                    continue

            # get bucket to go to from vision pi, move there and wait for finish
            bucket_to_go = int(requests.get(self.vision_pi_url + "/do_classification").text)
            if bucket_to_go == 0 or bucket_to_go == 3:  # then not moving
                pass
            if bucket_to_go == 1 or bucket_to_go == 4:
                self.ev3_socket.send(EV3Commands.MOVE_TO_BUCKET_1_4.to_bytes(1, 'big'))
            elif bucket_to_go == 2 or bucket_to_go == 5:
                self.ev3_socket.send(EV3Commands.MOVE_TO_BUCKET_2_5.to_bytes(1, 'big'))
            else:
                print("ERROR, bucket to go is %d" % bucket_to_go)
                continue
            move_confirmation = int.from_bytes(self.ev3_socket.recv(1), 'big')
            print("move to bucket confirmation:", move_confirmation)

            # perform drop off action with arm
            if bucket_to_go == 0 or bucket_to_go == 1:
                self.ser.write(DropOffAction.DROP_OFF_01.to_bytes(1, 'big'))
                self.ser.flush()
            elif not (bucket_to_go == 3 or bucket_to_go == 4):
                self.ser.write(DropOffAction.DROP_OFF_34.to_bytes(1, 'big'))
                self.ser.flush()
            elif bucket_to_go == 2:
                self.ser.write(DropOffAction.DROP_OFF_2.to_bytes(1, 'big'))
                self.ser.flush()
            elif bucket_to_go == 5:
                self.ser.write(DropOffAction.DROP_OFF_5.to_bytes(1, 'big'))
                self.ser.flush()
            else:
                print("ERROR: got drop off action for bucket", bucket_to_go)
                continue

            # wait for drop off action finish
            drop_off_confirmation = int.from_bytes(self.ser.read(), 'big')
            if drop_off_confirmation != 1 or drop_off_confirmation != 2:
                print("ERROR: UNEXPECTED drop off confirmation", drop_off_confirmation)
                continue

            # tell ev3 to come back, wait for finish
            if bucket_to_go == 0 or bucket_to_go == 3:  # then not moving
                pass
            if bucket_to_go == 1 or bucket_to_go == 4:
                self.ev3_socket.send(EV3Commands.MOVE_BACK_FROM_1_4.to_bytes(1, 'big'))
            elif bucket_to_go == 2 or bucket_to_go == 5:
                self.ev3_socket.send(EV3Commands.MOVE_BACK_FROM_2_5.to_bytes(1, 'big'))
            else:
                print("ERROR, bucket to go is %d" % bucket_to_go)
                continue
            move_back_confirmation = int.from_bytes(self.ev3_socket.recv(1), 'big')
            print("move back from bucket confirmation:", move_back_confirmation)
            # move to safe ready position
            self.ser.write(PickupAction.READY.to_bytes(1, 'big'))
            self.ser.flush()
            ready_confirmation = int.from_bytes(self.ser.read(), 'big')
            if ready_confirmation != 98:
                print("ERROR, EXPECTED ready position confirmation 98, got %d" % ready_confirmation)
