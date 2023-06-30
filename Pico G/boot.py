# boot.py -- run on boot-up
import network, utime
from machine import Pin, reset

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
        counter = 0
        while not sta_if.isconnected():
            #print("Attempting to connect....")
            onboard_LED.toggle()
            utime.sleep_ms(100)
            counter += 1
            if(counter > 150):
                reset()
    #print('Connected! Network config:', sta_if.ifconfig())
    
#print("Connecting to your wifi...")
do_connect()
onboard_LED.value(0)
