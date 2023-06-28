# boot.py -- run on boot-up
import network, utime
from machine import Pin

onboard_LED = Pin("LED", Pin.OUT)
onboard_LED.toggle()

# Replace the following with your WIFI Credentials
SSID = "Michis WLAN"
SSID_PASSWORD = "youstink"


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        #print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD) # type: ignore
        while not sta_if.isconnected():
            #print("Attempting to connect....")
            utime.sleep(1)
    #print('Connected! Network config:', sta_if.ifconfig())
    
#print("Connecting to your wifi...")
do_connect()
onboard_LED.toggle()