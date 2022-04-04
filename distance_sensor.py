import serial
import threading
from collections import deque
from pickup_action import PickupAction


class Sensor:
    """Sensors should be arranged in such an order:
    top left is 1, top right is 2, bottom left is 3, bottom right is 4"""
    # threshold for distance detection for upper/lower
    # if <= this, perform action grab upper
    THRESHOLD_UPPER = 16
    # if <= this but >= THRESHOLD_UPPER, grab lower
    THRESHOLD_LOWER = 19
    # else, treat as no fabric there

    def __init__(self):
        # dequeue for 4 sensors' data
        self.data1, self.data2, self.data3, self.data4 =\
            deque(maxlen=20), deque(maxlen=20), deque(maxlen=20), deque(maxlen=20)
        self.data_lock = threading.Lock()

        self.ser = serial.Serial('/dev/ttyACM0')
        self.ser.flushInput()
        read_thread = threading.Thread(target=self._read_sensors)
        read_thread.start()

    def _read_sensors(self):
        """This is a background running thread pulling values from arduino"""
        while True:
            readings = self.ser.readline()[:-2].decode("utf-8").split(" ")
            print('values from arduino', readings)
            readings = list(map(int, readings))
            if any(map(lambda v: v > 35, readings)):
                print("outliers found, skipping")
                continue
            print(readings)
            if len(readings) != 4:
                print("not reading 4 values from sensors, ignoring")
                continue
            with self.data_lock:
                self.data1.append(int(readings[0]))
                self.data2.append(int(readings[1]))
                self.data3.append(int(readings[2]))
                self.data4.append(int(readings[3]))

    def get_sensor_values(self):
        """return a 4 tuple of averaged sensor readings"""
        with self.data_lock:
            average1 = sum(self.data1) / len(self.data1)
            average2 = sum(self.data2) / len(self.data2)
            average3 = sum(self.data3) / len(self.data3)
            average4 = sum(self.data4) / len(self.data4)
            # print(average1,average2,average3,average4)
        return average1, average2, average3, average4

    def get_pickup_action(self):
        """Returns an int representing the action for the arm"""
        averages = self.get_sensor_values()
        # print("averaged distances from sensors:", averages)
        sensor_distance_tuples = [(i+1, dist) for i, dist in enumerate(averages)]
        uppers = list(filter(lambda t: t[1] < self.THRESHOLD_UPPER, sensor_distance_tuples))
        lowers = list(filter(lambda t: self.THRESHOLD_LOWER > t[1] > self.THRESHOLD_UPPER, sensor_distance_tuples))
        if uppers:
            sensor = uppers[0][0]  # between 1 to 4
            if sensor == 1:
                return PickupAction.TOP_LEFT_UPPER
            if sensor == 2:
                return PickupAction.TOP_RIGHT_UPPER
            if sensor == 3:
                return PickupAction.BOTTOM_LEFT_UPPER
            if sensor == 4:
                return PickupAction.BOTTOM_RIGHT_UPPER
        elif lowers:
            sensor = lowers[0][0]
            if sensor == 1:
                return PickupAction.TOP_LEFT_LOWER
            if sensor == 2:
                return PickupAction.TOP_RIGHT_LOWER
            if sensor == 3:
                return PickupAction.BOTTOM_LEFT_LOWER
            if sensor == 4:
                return PickupAction.BOTTOM_RIGHT_LOWER

