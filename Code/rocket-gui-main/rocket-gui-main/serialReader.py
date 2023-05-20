"""Serial Reader
Methods to read lines from the serial port and then write them to a CSV file
"""

from time import sleep
from threading import Thread

import serial


def __retryConnection():
    """Automatically retry to connect to serial port after some time"""
    # Wait five seconds
    sleep(5)
    try:
        # Try to set ser to the serial port
        global ser
        ser = serial.Serial(SERIAL_PORT)
        print(f"Connected to {SERIAL_PORT}")
        return True
    except:
        return False


# All the columns in the CSV file
HEADERS = "time,alt,pres,temp,humid,lat,lon,gX,gY,gZ,aX,aY,aZ\n"
# The Serial Port the Arduino is connected to
SERIAL_PORT = "COM3"
# Whether the program is able to connect to the serial port or not
portBusy = False

# Try to connect to the serial port
try:
    ser = serial.Serial(SERIAL_PORT)
    print(f"Connected to {SERIAL_PORT}")
except:
    # If not able to connect try three times to reconnect
    connected = False
    for i in range(3):
        print(f"Error connecting to {SERIAL_PORT}, automatic retry ({i + 1}/3)...")
        if __retryConnection():
            connected = True
            break
    if not connected:
        print(
            "Error reading from serial port!\nMake sure port "
            + SERIAL_PORT
            + " is not busy, and that the Arduino IDE and Serial Monitor"
            "/Plotter are closed."
        )
        portBusy = True


def init():
    """Write the headers to the csv file and start a new thread
    to read from the serial port"""
    with open("./data.csv", "w") as f:
        f.write(HEADERS)
        f.close()
    th = Thread(target=readSerial)
    th.start()


def readSerial():
    """Read the output on the serial port"""
    while True:
        if portBusy:
            return
        # Clean up the output
        data = str(ser.readline())[2:-1].replace("\\r\\n", "")
        if data.startswith("!!"):
            # If the Arduino has been restarted
            if data.endswith("REC_RESET"):
                init()
                return
        else:
            # If it is normal data write it to the CSV file
            if __isfloat(data.split(",")[0]):
                with open("./data.csv", "a") as f:
                    f.write(data + "\n")


def __isfloat(value):
    """Check if a value can be parsed to a float"""
    try:
        float(value)
        return True
    except ValueError:
        return False
