"""
this script runs on ev3, listens for commands from raspi.
Commands should be a 1 byte int, signifying different movements to perform
after performing a command, ev3 should send back the same int, indicating finish
"""
import ev3dev.ev3 as ev3
from time import sleep
import socket
from ev3_commands import EV3Commands

ma = ev3.LargeMotor('outA')
mb = ev3.LargeMotor('outB')
mc = ev3.LargeMotor('outC')
md = ev3.LargeMotor('outD')

SPEED = 300
TIME_MOVE_TO_1_4 = 850
TIME_MOVE_TO_2_5 = 2100

PORT = 54321

# bucket 1:
# TIME = 850
# BUCKET 2:
# TIME = 2100, BUT NEEDS TO TURN COUTER CLOCKWISE A BIT TO BE AT CENTER

# ma.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_1_4)
# mb.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_1_4)
# mc.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_1_4)
# md.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_1_4)
#
# sleep(2)
#
# ma.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_2_5+200)
# mb.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_2_5+200)
# mc.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_2_5+200)
# md.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_2_5+200)
#####

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', PORT))
sock.listen()
pi_socket, pi_address = sock.accept()
print("ev3 listening for command")

while True:
    command = int.from_bytes(pi_socket.recv(1), 'big')
    if command == EV3Commands.MOVE_TO_BUCKET_1_4:
        print("MOVE_TO_BUCKET_1_4")
        ma.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_1_4)
        mb.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_1_4)
        mc.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_1_4)
        md.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_1_4)
        sleep((TIME_MOVE_TO_1_4 + 300) / 1000)
        pi_socket.send(command.to_bytes(1, 'big'))

    elif command == EV3Commands.MOVE_TO_BUCKET_2_5:
        print("MOVE_TO_BUCKET_2_5")
        ma.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_2_5)
        mb.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_2_5)
        mc.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_2_5)
        md.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_2_5)
        sleep((TIME_MOVE_TO_2_5 + 300) / 1000)
        pi_socket.send(command.to_bytes(1, 'big'))

    elif command == EV3Commands.MOVE_BACK_FROM_1_4:
        print("MOVE_BACK_FROM_1_4")
        ma.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_1_4 + 200)
        mb.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_1_4 + 200)
        mc.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_1_4 + 200)
        md.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_1_4 + 200)
        sleep((TIME_MOVE_TO_1_4 + 500) / 1000)
        pi_socket.send(command.to_bytes(1, 'big'))

    elif command == EV3Commands.MOVE_BACK_FROM_2_5:
        print("MOVE_BACK_FROM_2_5")
        ma.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_2_5 + 200)
        mb.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_2_5 + 200)
        mc.run_timed(speed_sp=-SPEED, time_sp=TIME_MOVE_TO_2_5 + 200)
        md.run_timed(speed_sp=SPEED, time_sp=TIME_MOVE_TO_2_5 + 200)
        sleep((TIME_MOVE_TO_2_5 + 500) / 1000)
        pi_socket.send(command.to_bytes(1, 'big'))
