from ubinascii import hexlify
import machine
from umqttsimple import MQTTClient
import utime

# MQTT Stuff
CLIENT_ID = hexlify(machine.unique_id()) #To create an MQTT client, we need to get the PICOW unique ID
MQTT_BROKER = "io.adafruit.com" # MQTT broker IP address or DNS
PORT = 1883
ADAFRUIT_USERNAME = "michelow"
ADAFRUIT_PASSWORD = "aio_xnAU80fke1w7PYPBzSyxLnQZYAwO"
PUBLISH_TOPIC = b"michelow/f/gate"

#print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
mqttClient.connect()
#print(f"Connected to MQTT  Broker :: {MQTT_BROKER} successfully!")

# pins
led_onboard = machine.Pin("LED", machine.Pin.OUT)
hall = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
gateOpen = False

# Callback function to handle interrupt event
def interrupt_callback(pin):
    publishGateState()

# MQTT message with gate info    
def publishGateState():
    led_onboard.toggle()
    utime.sleep_ms(20)
    led_onboard.toggle()
    gateOpen = bool(hall.value())
    mqttClient.publish(PUBLISH_TOPIC, str(gateOpen).encode()) # type: ignore
    #print(f"Message published: Gate open: {gateOpen}.")

# Configure pin 14 as an input pin with an interrupt
hall.irq(trigger=(machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING), handler=interrupt_callback)
publishGateState()
#print("Initial message done, starting routine.")

while True:
    utime.sleep(30)
    publishGateState()

