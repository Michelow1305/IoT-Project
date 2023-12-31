# Pico G, the one on my gate
from ubinascii import hexlify
import machine
from umqttsimple import MQTTClient
import utime

## pins
led_onboard = machine.Pin("LED", machine.Pin.OUT)
hall = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
gateOpen = False

## MQTT Stuff
CLIENT_ID = hexlify(machine.unique_id()) #To create an MQTT client, we need to get the PICOW unique ID
MQTT_BROKER = "io.adafruit.com" # MQTT broker IP address or DNS
PORT = 1883
ADAFRUIT_USERNAME = "michelow"
ADAFRUIT_PASSWORD = "aio_xnAU80fke1w7PYPBzSyxLnQZYAwO"
PUBLISH_TOPIC_1 = b"michelow/f/gate"
PUBLISH_TOPIC_2 = SUBSCRIBE_TOPIC = b"michelow/f/alive"

def sendAliveStatus():
    mqttClient.publish(topic=PUBLISH_TOPIC_2, msg=str("G").encode(), qos=1) # type: ignore
    
def sendRestartRequest():
    mqttClient.publish(topic=PUBLISH_TOPIC_2, msg=str("restart").encode(), qos=1) # type: ignore
    

## MQTT publish function with gate info    
def publishGateState():
    try:
        global gateOpen
        gateOpen = bool(hall.value())
        mqttClient.publish(topic=PUBLISH_TOPIC_1, msg=str(int(gateOpen)).encode(), qos=1) # type: ignore
        
        # blink
        led_onboard.toggle()
        utime.sleep_ms(20)
        led_onboard.toggle()
    except:
        machine.reset()

## Callback function to handle interrupt event
def interrupt_callback(pin):
    for i in range(0, 3):
        publishGateState()
        utime.sleep(i*2+1)

def MQTT_subscribe_callback(topic, msg):
    if msg.decode() == "D":
        global picoDLastSeen
        picoDLastSeen = utime.time()
    elif msg.decode() == "restart":
        sendRestartRequest()
        utime.sleep(2)
        machine.reset()


#print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=120)
try:
    mqttClient.set_callback(MQTT_subscribe_callback)
    mqttClient.connect()
    utime.sleep(2)
    mqttClient.subscribe(SUBSCRIBE_TOPIC, qos=1)
except:
    machine.reset()
#print(f"Connected to MQTT  Broker :: {MQTT_BROKER} successfully!")

## Configure pin 14 as an input pin with an interrupt
hall.irq(trigger=(machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING), handler=interrupt_callback)

publishGateState() # inital publish
#print("Initial publish done, starting routine.")

global picoDLastSeen
picoDLastSeen = utime.time()

while True:
    try:
        mqttClient.check_msg()

        if(utime.time() - picoDLastSeen > 35):
            sendRestartRequest()
            utime.sleep(2)
            machine.reset()

        utime.sleep(5)
        sendAliveStatus()
        utime.sleep(5)
        publishGateState()
    except:
        machine.reset()

vsc