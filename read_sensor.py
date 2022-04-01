import serial
import csv

ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()

CSV_FILE = "test_data.csv"

def main():
    with open("test_data.csv","a") as f:
        writer = csv.writer(f,delimiter=",")

        while True:
            ser_bytes = ser.readline()
            distances = ser_bytes[0:len(ser_bytes)-2].decode("utf-8").split(" ")
            if len(distances) != 4:
                continue
            writer.writerow(distances)
            print(distances)

if __name__ == '__main__':
    main()
