from ubinascii import hexlify
import machine
from umqttsimple import MQTTClient
from utime import sleep_ms, sleep, time

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
SUBSCRIBE_TOPIC_1 = b"michelow/f/gate"
SUBSCRIBE_TOPIC_2 = PUBLISH_TOPIC = b"michelow/f/alive"

## MQTT subscribe callback (gate info)    
def MQTT_subscribe_callback(topic, msg):
    global currentGateStatus
    if msg.decode() == "1":
        currentGateStatus = True
        if(led.value() is 0): # only beep when the gate just opened
            led.value(1)
            beep()
    elif msg.decode() == "0":
        currentGateStatus = False
        led.value(0)
    elif msg.decode() == "G":
        global picoGLastSeen
        picoGLastSeen = time()
    elif msg.decode() == "restart":
        sendRestartRequest()
        sleep(2)
        machine.reset()

    # blink
    onboard_LED.toggle()
    sleep_ms(100)
    onboard_LED.toggle()

def sendRestartRequest():
    mqttClient.publish(topic=PUBLISH_TOPIC, msg=str("restart").encode(), qos=1) # type: ignore

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

def sendAliveStatus():
    mqttClient.publish(topic=PUBLISH_TOPIC, msg=str("D").encode(), qos=1) # type: ignore

mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=120)
try:
    #print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
    # whenever a new message comes (to picoW), execute callback function
    mqttClient.set_callback(MQTT_subscribe_callback)
    mqttClient.connect()
    sleep(1)
    mqttClient.subscribe(SUBSCRIBE_TOPIC_1, qos=1)
    mqttClient.subscribe(SUBSCRIBE_TOPIC_2, qos=1)
except:
    machine.reset()
#print(f"Connected to MQTT  Broker :: {MQTT_BROKER} successfully!")

global picoGLastSeen
picoGLastSeen = time()

while True:
    try:
        mqttClient.check_msg()

        if(time() - picoGLastSeen > 45):
            sendRestartRequest()
            sleep(1)
            machine.reset()

        sleep(2)
        mqttClient.check_msg()
        sleep(2)
        mqttClient.check_msg()
        sleep(2)
        mqttClient.check_msg()
        sleep(2)
        mqttClient.check_msg()
        sleep(2)
        sendAliveStatus()
    except:
        machine.reset()
