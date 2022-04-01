from pyserial_test import *
import numpy as np
import csv

def processLine(lines):
    lines = [line.split(",") for line in lines]
    print("lines",lines)
    for i in range(0, 5):
        for j in range(0, 4):
            lines[i][j] = int(lines[i][j])
    return lines

class Sensor(object):
    def __init__(self, ser):
        self.ser = ser

    def getDistances(self, window_size=5):
        with open(CSV_FILE, 'r') as f:
            last_lines = f.readlines()[-window_size:]
        print("last_lines", last_lines)
        last_lines = processLine(last_lines)
        print(last_lines)
        return list(np.mean(last_lines, axis=0))

def main():
    sensor = Sensor(ser)
    print(sensor.getDistances())

if __name__ == "__main__":
    main()
