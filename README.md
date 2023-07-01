# Smart security project
by Michel Jensen (mj225aj)

## Introduction
Hello there! Welcome to my home security project I did for my IoT course in summer 2023.

I made a little system to notify me when someone enters my property, even when I am not home. It logs the activity online, to let me see when exactly someone entered.

## Objective
Since neighbors, parents or eventually intruders could show up any second at my doorstep, being able to see my living room before I even realize someone is there, I wanted to do something about that. So, I thought of the following:

The only way to my door is to go through that one gate outside. What if I attach something to the gate to notify me when someone enters? 
I even wanted to go a step further: it should log when someone enters, because I want to see when it happened, not only the moment it happens.

And that seemed to be quite feasible! I thought all that would be done in a couple of days, but it turned out later that there are more difficulties than I thought there would be.

## Material
-	2x Raspberry Pi Pico
  	- Sending/receiving the data
-	Hall effect sensor + magnet
    - Sensing if gate is open or closed
-	Buzzer and/or LED
    - Notifying if gate was just opened

  
I bought everything (except the LED) on electrokit. Here are more details and links:


### Raspberry Pi Pico:
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/a9d88325-777f-4e42-92da-18889ea736e5)

www.electrokit.com/produkt/raspberry-pi-pico                                
65.00 SEK / p

### Hall effect Sensor (digital):
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/5d5abcda-51ee-4a2e-a733-9fbaf1f751ab)

www.electrokit.com/produkt/tlv49645-sip-3-hall-effektsensor-digital                                
18.00 SEK / p

### Magnet:
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/b3c7140a-e5a4-427e-831a-769c2149311c)

www.electrokit.com/produkt/magnet-neo35-o8mm-x-4mm 		                
25.00 SEK / p

### Buzzer:
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/0293e102-e3fd-40c4-89e4-379af04f46ec)

www.electrokit.com/produkt/summer-3-8-khz  				                    
37.50 SEK / p

## Computer Setup
I chose Visual Studio Code as my main IDE. It provides a ton of features, and I was already used to it before. Of course, if not already done, Python needs to be installed on the computer. For me, that was already done. I updated the version of Python and Visual Studio Code, which I can only recommend.


To program the Pico’s, there are a few steps I needed to take:
### Set up the pico
First, when I had my pico fresh out of the box, I had to install firmware. I got the latest firmware from:

www.raspberrypi.com/documentation/microcontrollers/micropython.html

I used the “Raspberry Pi Pico W with Wi-Fi and Bluetooth LE support” option, and downloaded the file.

While plugging the pico in the first time, one needs to hold the white “BOOTSEL” button down. That opens a folder like the pico was a USB stick. Dragging and dropping the downloaded file results in the window closing and the pico restarting, and the pico is flashed!
### Setting up Visual Studio Code
I can recommend starting with a new project with a new workspace in Visual Studio Code. Making a new file called “main.py” is the next step. No need for any code for now.

After that, install the extension “Pico-W-Go”.

Pressing “CTRL-SHIFT-P” opens all the commands that are usable. Type “project” and select the option “Configure Project”. This should create a file called “.picowgo”. When you see that file, well done! You are ready to code. Make sure that the pico is connected (look at the bottom left corner).

One more thing to note here is that one can’t just press the play button. It’s important to always press “CTRL-SHIFT-P” and choose the “upload project to pico” or “run current file on pico”. Otherwise, the code will be executed on the PC, which is not what we want.

## Putting everything together
After learning about how to set up a Wi-Fi connection with a Raspberry Pi Pico, and my router being in the living room (which is close enough to the gate), I decided to attach a pico on the gate. I also need a second pico to receive data and turn on a buzzer, to let me know when someone enters.

First, I will go into detail on the pico attached next to the Gate (referred to as “Pico G”):
### Pico G
To know, If the gate is open or not, I connected a hall sensor and attached a magnet to the gate. That way, the pico would always know if the gate is currently closed or open. I enabled a pull-up resistor digitally, to make the output of the hall effect sensor even more reliable. If that feature is not be available to you (because youre maybe on an Arduino?), I can recommend to wire it differently and add that pull-up resistor to the circuit.

I first thought about making that pico battery powered, but I have an outdoor plug one meter away from the gate. So, I decided to use that one old USB adapter that doesn’t charge quickly anymore, obliterate a small old USB mini cable, and solder a long wire to the power cables, which went smoothly. I put the cable under the steppingstones to avoid anyone falling over it. Here is a connection diagram for you to see where I soldered what: (I know, its ugly...)

![Pico G wiring diagram](https://github.com/Michelow1305/IoT-Project/assets/19593240/d30f21ff-9034-4465-871c-b83b5c4aee5c)

For now, to protect the pico against rain, I put it in a plastic bag. I will 3D-print a nice case for it when everything is done, but for now I need to keep it this way to make eventual adjustments easy.

Now, I want to describe the other pico on my living room desk, referred to as “Pico D”:

### Pico D
This pico just needs a buzzer and an LED. It is connected as follows:

![Pico D wiring diagram](https://github.com/Michelow1305/IoT-Project/assets/19593240/6318ab0a-f2f2-475a-9a43-0acb42eaea93)

## Platform
The platform I used was the cloud based Adafruit MQTT broker. It is easy to set up and worked very well for me. I use the free plan, since it is enough for my project. 

If someone wanted this on a bigger scale, a paid subscription would probably be needed. Otherwise, one could set up a local MQTT broker, maybe on a Raspberry Pi 4. That would have been my next option, if the Adafruit broker had not worked well.

One can set up multiple MQTT feeds to subscribe and publish to and monitor the activity using any web browser. I also set up a Dashboard to see the live activity and history.

## Code
First, I want to explain how I implemented the MQTT functionality on the Pico’s.

Fortunately, I had a library given called “umqttsimple”. You can find the file on my repository or on the internet. I had to make a few adjustments to make Pylance shut up, mainly putting “assert x not None” statements, but it would have worked without those adjustments.
Here is some code that I wrote to set up the MQTT broker:
```
# defines
CLIENT_ID = hexlify(machine.unique_id()) #To create an MQTT client, we need to get the PICOW unique ID
MQTT_BROKER = "io.adafruit.com" # MQTT broker IP address or DNS
PORT = 1883
ADAFRUIT_USERNAME = "michelow"
ADAFRUIT_PASSWORD = "aio_xxxxxxxxxxxxxxxx" # (your key goes here)
SUBSCRIBE_TOPIC = b"michelow/f/gate"
PUBLISH_TOPIC = b"michelow/f/alive"
# setup connection
mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
# set ”MQTT_subscribe_callback()“ as the callback function to execute when a message comes in
mqttClient.set_callback(MQTT_subscribe_callback)
mqttClient.connect()
mqttClient.subscribe(SUBSCRIBE_TOPIC)
```
This first defines a few things for your pico to know Your username, password and where to connect to etc. One also needs to define what the feeds names are to subscribe - or publish to.

Here, I have two feeds that I use: one for seeing if the devices are connected and alive and to send reset commands, and one for the status if the gate is open or not.

The pico on the gate sends a message to the gate feed when the gate is either closed or opened, and again after 1, 3 and 5 seconds to be sure the other pico gets the message, even when it is restarting at any moment. When the Pico in the living room receives, that the gate just opened, it makes the buzzer beep three times and lights the LED. The LED stays on until the gate is closed again.

“Why should it restart? Why do you make everything so complicated?”, you may think. But I tried the easy and straightforward way, sending only one message, even trying out every QoS level. But it was unreliable and simply didn’t work very well.

I ran into a few issues, where one of the two Pico’s would just not respond anymore, and restarting the pico always fixed the issue temporarily. Restarting regularly was my first idea, but that didn’t work out.

After days of trying to fix that issue, I thought of a neat way to work around any failures: Both Pico’s send an alive message every 10 seconds. When one pico does not get any alive message from the other over 45 seconds, it can make the other pico restart, by simply sending the restart command to the alive feed. That pico will then also restart itself.

This fixed all the issues I had with MQTT, and I also had the possibility to see which pico was not alive and when, and restarting the Pico’s remotely, which made my life a lot easier. Now, after testing the system all the time for the last days, I can be sure it is reliable. A restart only happens once or maximum twice a day, which is reasonable for me.

Another tip one might want to consider is don’t be as stupid as me and publish your code with your Adafruit password and leak that kind of sensitive information. Change the line to a blank one or just leave it as it is and regenerate the key when uploading.

## Connectivity
For me, data is sent all the time, at the latest every five seconds. Both Pico’s send their alive messages every ten seconds, and Pico G is additionally sending the gate status every ten seconds as well, right between the alive messages. So, every 5 seconds, when the gate is not moved, otherwise even more than that. 

As I mentioned earlier, the messages are sent and received over Wi-Fi, specifically over a socket to the Adafruit MQTT broker. 

I chose the Wi-Fi option, because my router is in the living room. The Pico D has a very good connection, as there is nothing in between except air with a 2-meter distance, and the Pico G’s distance is around 6-8 meters with a wooden wall in between. Since the Wi-Fi functionality is inbuilt in the Pico W, this was the easiest choice to make for me.

When one of the Pico’s boots and try to connect to my Wi-Fi, the onboard LED blinks rapidly to let me know it’s doing something, and if the connection is not established after 10 seconds, the pico restarts. Otherwise, they stop blinking. They do blink once, if they receive or send a message, also just for me to see if something actually arrives or gets sent. I can only recommend doing this, it makes debugging so much easier, especially in the beginning of a project like this.

## Presenting the Data
I made a Dashboard on IO.Adafruit, that is directly linked to my feeds. It contains the history of the gate status for the past 24 hours, and one for the last hour to see some more details. 

Although one can’t see the older history on the dashboard, the history is saved for about 6 days, until the space runs out. I don’t know the full extent yet since there is still a lot of data left from the debugging phase, all I know is that it’s longer than 48 hours, which is enough for my purposes. 

One can also see a big slider, which tells you if the gate is now open or closed. I also added a reset button to remotely reset the Pico’s, which is a nice thing to have to debug. Lastly, I added a small Stream Block, that lets me see when the last messages were sent in the alive feed. This allows me to see if one of the Pico’s is dead, or if they restarted recently.

Here is how it looks like:

![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/cdff2017-1b2d-4e61-a2c4-a420e638f0a9)

As we can see, the gate was opened today at 2:43 pm, and 3:38 pm. It is closed now, and the Pico's are both alive!


## Finalizing the Design
This project was a lot of fun and gave me a very nice feeling of privacy, since I always know beforehand when someone wants to come to my doorstep. Learning about micro python opened up a whole new world for me, after spending months on writing C for embedded systems, this was a nice and fun thing to do!
Although one can't see a lot on them, here are some pictures, if you want to take a look: 

![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/02d14ffc-041c-4ffa-b553-1e48c90256bc)
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/cb326f4c-abd7-4209-966b-3b0f2331afa8)
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/9110f15f-a3cc-4da6-bc7e-fc41c19f87d2)
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/3feaf8df-35e7-422e-beb0-6cb88a892eab)
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/c41aa891-1e17-4661-8f69-67daacf2a2df)
![grafik](https://github.com/Michelow1305/IoT-Project/assets/19593240/45f91eaa-f954-466a-8cfc-0b02964517c0)





