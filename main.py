from ubinascii import hexlify
import machine
from umqttsimple import MQTTClient
from utime import sleep_ms, time

## pins
led = machine.Pin(20, machine.Pin.OUT)
onboard_LED = machine.Pin("LED", machine.Pin.OUT)
buzzer = machine.Pin(15, machine.Pin.OUT)
currentGateStatus = True # True to prevent beeping while restart
previousGateStatus = True 

## MQTT Stuff
CLIENT_ID = hexlify(machine.unique_id()) #To create an MQTT client, we need to get the PICOW unique ID
MQTT_BROKER = "io.adafruit.com" # MQTT broker IP address or DNS
PORT = 1883
ADAFRUIT_USERNAME = "michelow"
ADAFRUIT_PASSWORD = "aio_xnAU80fke1w7PYPBzSyxLnQZYAwO"
SUBSCRIBE_TOPIC = b"michelow/f/gate"

## MQTT subscribe callback (gate info)    
def MQTT_subscribe_callback(topic, msg):
    global currentGateStatus
    if msg.decode() == "1":
        currentGateStatus = True
        if(led.value() is 0): # only beep when the gate just opened
            led.value(1)
            beep()
    else:
        currentGateStatus = False
        led.value(0)

    # blink
    onboard_LED.toggle()
    sleep_ms(100)
    onboard_LED.toggle()

# long beep, short beep, short beep
def beep():
    buzzer.toggle()
    sleep_ms(600)
    buzzer.toggle()

    sleep_ms(100)

    buzzer.toggle()
    sleep_ms(200)
    buzzer.toggle()

    sleep_ms(100)

    buzzer.toggle()
    sleep_ms(200)
    buzzer.toggle()

mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=120)
try:
    #print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
    # whenever a new message comes (to picoW), execute callback function
    mqttClient.set_callback(MQTT_subscribe_callback)
    mqttClient.connect()
    mqttClient.subscribe(SUBSCRIBE_TOPIC, qos=1)
except:
    machine.reset()
#print(f"Connected to MQTT  Broker :: {MQTT_BROKER} successfully!")

startTime_s = time()

while True:
    mqttClient.check_msg()

    timeElapsed_s = time() - startTime_s
    if(timeElapsed_s > 120 and currentGateStatus is False):
        machine.reset()

    sleep_ms(500)