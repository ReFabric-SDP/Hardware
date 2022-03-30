# Arduino Distance Sensor Guide

- Instruction source:
  - https://www.instructables.com/How-to-Use-the-Sharp-IR-Sensor-GP2Y0A41SK0F-Arduin/
- the type of our selected sensor is **GP2Y0A41SK0F**
  - (not exact the name in the sensor surface but the name should be similar to this)

## Procedure

### Step 1: to connect the board to a PC

- For a DICE machine:

  - detailed guide is given in https://wiki.inf.ed.ac.uk/SDP/ArduinoGuide

  - 1: Connect the Arduino to the USB port on the DICE machine

  - 2: From a terminal window on your DICE machine, enter the following to check whether the board is connected

    ```
    ls /dev
    ```

    - This will display all the devices that are currently connected to the DICE machine.
    - typically the board we use have name like **TTYACM0** or **TTYACM1** and it should be shown in the list of devices

  - 3: from the command line, input

    - ```
      arduino &
      ```

    - To make sure **we select the correct board**, make sure the **board, port and programmer** are like below:

      - ![image-20220330153822036](C:\Users\Morphling\AppData\Roaming\Typora\typora-user-images\image-20220330153822036.png)
      - Check these in the Arduino IDE:
        - ![image-20220330153850784](C:\Users\Morphling\AppData\Roaming\Typora\typora-user-images\image-20220330153850784.png)

- In personal laptop (take my windows as an example)

  - after connecting the board to USB port of my laptop, directly open the IDE and set the Tools-Port to the correct one

### Step 2 Connect the sensor to the board

![image-20220330153006887](C:\Users\Morphling\AppData\Roaming\Typora\typora-user-images\image-20220330153006887.png)

- Connect the sensor and the Arduino board shown above
  - the leftmost cable connects to `A0`
  - the middle cable connects to `GND`
  - the rightmost cable connects `5V`

### Step 3  run the code

- The code has been committed to our github 
  - https://github.com/ReFabric-SDP/Hardware/blob/main/distance_detector.ino
  - The first commented part is for another type of sensor 

![image-20220330154233562](C:\Users\Morphling\AppData\Roaming\Typora\typora-user-images\image-20220330154233562.png)

- Click Upload as above and the code is running with the `Serial` class reading values from the analogue port
- The distance values can be monitored in **`Tools -> Serial Monitor`**
  - the values are essentially from the `analogRead(sensor)` with float type