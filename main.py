from ubinascii import hexlify
import machine
from umqttsimple import MQTTClient
from utime import sleep_ms

# MQTT Stuff
CLIENT_ID = hexlify(machine.unique_id()) #To create an MQTT client, we need to get the PICOW unique ID
MQTT_BROKER = "io.adafruit.com" # MQTT broker IP address or DNS
PORT = 1883
ADAFRUIT_USERNAME = "michelow"
ADAFRUIT_PASSWORD = "aio_xnAU80fke1w7PYPBzSyxLnQZYAwO"
SUBSCRIBE_TOPIC = b"michelow/f/gate"

# pins
led = machine.Pin(20, machine.Pin.OUT)
onboard_LED = machine.Pin("LED", machine.Pin.OUT)

currentGateStatus = False
messageCounter = 0

# MQTT subscribe callback (gate info)    
def MQTT_subscribe_callback(topic, msg):
    onboard_LED.toggle()
    global messageCounter
    messageCounter += 1
    if msg.decode() == "True":
        currentGateStatus = True
        led.value(1)
    else:
        currentGateStatus = False
        led.value(0)
    sleep_ms(100)
    onboard_LED.toggle()

#print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
# whenever a new message comes (to picoW), execute callback function
mqttClient.set_callback(MQTT_subscribe_callback)
mqttClient.connect()
mqttClient.subscribe(SUBSCRIBE_TOPIC)
#print(f"Connected to MQTT  Broker :: {MQTT_BROKER} successfully!")

while True:
    mqttClient.check_msg()
    if(messageCounter > 5 and currentGateStatus is False):
        machine.soft_reset()
    sleep_ms(100)