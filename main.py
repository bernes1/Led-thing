import os
import time
import ssl
import wifi
import board
import terminalio
import socketpool
from adafruit_matrixportal.matrixportal import MatrixPortal
import adafruit_requests

SCROLL_DELAY = 0.05
time_interval = 5

BASE_URL = "https://api.duky.dev/api/message/"


# --- Wi-Fi setup ---
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")

# --- Display setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL,debug=True)

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    text_scale=1.5,
    scrolling=True,
    
)

# --- Networking setup ---
context = ssl.create_default_context()

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, context)

DATA_SOURCE = BASE_URL

# --- Main Loop ---
APIDATA = {"messsage": "connecting....","color":"0xffffff"}
try:
   APIDATA = requests.get(DATA_SOURCE).json()

except:
   pass

while True:
    print("Fetching json from", DATA_SOURCE)
    try:
        APIDATA = requests.get(DATA_SOURCE).json()
    except:
        pass
    text = APIDATA["message"]
    color = APIDATA["color"]
    print(color,text)
    matrixportal.set_text(text)
    matrixportal.set_text_color(color)
    matrixportal.scroll_text(SCROLL_DELAY)
    

    time.sleep(time_interval)
