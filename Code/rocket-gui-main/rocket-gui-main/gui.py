from math import sqrt
from time import sleep
from threading import Thread

from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd

import serialReader
import alert

# Start a new thread to init the serial reader
th = Thread(target=serialReader.init)
th.start()
sleep(1)
# Get the list of columns from the CSV file
col_list = open("./data.csv", "r").readline().replace("\n", "").split(",")
# Hide the matplotlib toolbar
rcParams["toolbar"] = "None"
# Create a 3x2 grid of charts
gs = GridSpec(3, 3)
# Change the window's size
fig = plt.figure(figsize=(16, 9))
# Change the window's title
fig.canvas.manager.set_window_title("Astroknights Live Rocket GUI")
# Change the window's icon
thismanager = plt.get_current_fig_manager()
thismanager.window.wm_iconbitmap("icon.ico")


def animate(i):
    """Redraw the charts with new data from the CSV file"""
    try:
        # Clear the chart of existing data
        plt.clf()
        data = pd.read_csv("./data.csv", usecols=col_list)
        # Get various data points
        time_vals = data["time"].astype(float)
        status = "Burning"
        time = round(data["time"].tolist()[-1], 2)
        altitude = round(data["alt"].tolist()[-1], 2)
        acceleration = round(
            sqrt(
                data["aX"].tolist()[-1] ** 2
                + data["aY"].tolist()[-1] ** 2
                + data["aZ"].tolist()[-1] ** 2
            ),
            2,
        )
        temperature = data["temp"].tolist()[-1]
        lat, lon = round(data["lat"].tolist()[-1], 5), round(
            data["lon"].tolist()[-1], 5
        )
        gX, gY, gZ = (
            round(data["gX"].tolist()[-1], 2),
            round(data["gY"].tolist()[-1], 2),
            round(data["gZ"].tolist()[-1], 2),
        )

        diag = alert.checkSafeTrajectory(altitude, temperature, gX, gY, gZ)
        
        # Subplot that shows various statistics as text
        ax = plt.subplot(gs[0:1, 0])
        ax.set_title("Flight Data")
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Text of the subplot
        text = f"""
Status: {status}
Time: {time}s
Altitude: {altitude}m
Acceleration:{acceleration}m/s
Temperature: {temperature}C
Coordinates: ({lat}, {lon})
Rotation: ({gX}, {gY}, {gZ})
{diag}"""

        ax.annotate(
            text,
            (0.025, 1),
            xycoords="axes fraction",
            va="top",
            fontsize=13,
            linespacing=1.5,
        )
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Altitude & Pressure subplot
        ax = plt.subplot(gs[0, 1:])
        plt.plot(time_vals, data["alt"].astype(float), label="Altitude", color="red")
        plt.plot(time_vals, data["pres"].astype(float), label="Pressure", color="blue")
        ax.set_title("Altitude & Pressure")
        ax.legend(loc="upper left")

        # Atmospheric Data subplot
        ax = plt.subplot(gs[1, 0:2])
        plt.plot(time_vals, data["temp"].astype(float), label="Temperature", color="red")
        plt.plot(time_vals, data["humid"].astype(float), label="Humidity", color="blue")
        ax.set_title("Atmospheric Data")
        ax.legend(loc="upper left")

        # Coordinates subplot
        ax = plt.subplot(gs[1, 2])
        plt.plot(time_vals, data["lat"].astype(float), label="Latitude", color="red")
        plt.plot(time_vals, data["lon"].astype(float), label="Longitude", color="blue")
        ax.set_title("Coordinates")
        ax.legend(loc="upper left")

        # Gyroscope subplot
        ax = plt.subplot(gs[2, 0:2])
        plt.plot(time_vals, data["gX"].astype(float), label="x", color="red")
        plt.plot(time_vals, data["gY"].astype(float), label="y", color="green")
        plt.plot(time_vals, data["gZ"].astype(float), label="z", color="blue")
        ax.set_title("Gyroscope")
        ax.legend(loc="upper left")

        # Accelerometer subplot
        ax = plt.subplot(gs[2, 2])
        plt.plot(time_vals, data["aX"].astype(float), label="x", color="red")
        plt.plot(time_vals, data["aY"].astype(float), label="y", color="green")
        plt.plot(time_vals, data["aZ"].astype(float), label="z", color="blue")
        ax.set_title("Accelerometer")
        ax.legend(loc="upper left")

        plt.tight_layout()
    except Exception as e:
        print(e)
        sleep(1)


# Run animate every 250 ms
ani = FuncAnimation(plt.gcf(), animate, interval=250)
plt.tight_layout()
plt.show()
