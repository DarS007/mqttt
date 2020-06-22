# mqttt - MQTT Terminal

MQTT is a real backbone of IoT. Lighweight, scalable, popular, etc. If you're IoT fanatic, you've perhaps collected a decent set of MQTT tools in your workbench. Me too. But I was always missing a portable, standalone, small, always-on display that could connect to MQTT broker and show the circulating messages. Yeah, I know... I can fire up MQTT.fx or XXX (enter here your preference) on my desktop. But this is not always handy or comfortable.

Therefore here you go... **MQTT Terminal** is a small, relatively dumb, standalone device to display rolling MQTT messages. It can be build with Raqspberry Pi Zero W (and any other single board computer/SBC) and 3.5" (or bigger) LCD. You can place it on your desk, next to your laptop, and discretely watch whether MQTT messaging works as expected. Great for targeted troubleshooting or ad hoc diagnosis.

Screenshots of **MQTT Terminal** with different fonts and sizes:

| <img src="https://github.com/DarS007/mqttt/blob/master/PICTURES/mqttt_screenshot.01-arial.png" width="240"> | <img src="https://github.com/DarS007/mqttt/blob/master/PICTURES/mqttt_screenshot.02-noteserif.png" width="240"> | <img src="https://github.com/DarS007/mqttt/blob/master/PICTURES/mqttt_screenshot.03-noteserif-smaller.png" width="240"> |

You can configure:
* display type (usually 3.5" LCD via video framebuffer, but the code can be also run on Linux and MS Windows desktops, etc.)
* LCD size (tested with 3.5" 480x320 LCD, but the code will work for smaller and bigger displays)
* font type (*font name* for system fonts, *font location* for other fonts)
* font size (separately for *title* and for *MQTT messages*)
* colors for background and message font
* number of displayed MQTT messages (one message equals one line of text), usually between 8 and 15
* rotation 'upside down' (180 degree) for reverted LCD screens

## HARDWARE
*Raspberry Pi Zero W* is perhaps the most optimal (cost and performance) platform. It's even too beefy for such easy task, but come on... You can spend $9 for RPi or $3 on ESP8266 - small difference for a singular DIY quantities. And with RPi you have a comfort of full Linux distribution, fully functional Python, flawless WiFi, etc. 

For display, you can use any small LCD screen HAT you wish. It has to work with Raspberry Pi, of course. But this is the only limitation. **MQTT Terminal** uses *framebuffer* for graphics so it DOES NOT need X Server to be installed. When selecting OS distribution for your Raspberry Pi, do not install fully featured *desktop* version. Choose *server* flavor. It is much lighter anyway.

## INSTALLATION
On Linux, install Paho MQTT Python client library and some fonts (assuming you run headless server without X Server and without any fancy fonts, incl. system fonts). Then just clone this repository, configure *mqtttcfg.json* file and run the code. I propose to make './bin' directory to keep this code there.
```
> sudo pip3 install paho-mqtt
> sudo apt-get install ttf-mscorefonts-installer fonts-liberation
> mkdir bin
> cd bin
> git clone https://github.com/DarS007/mqttt.git
```

## TO DO
- MQTT authentication - it is currently lacking, as the code was developed for in-house usage where local MQTT broker was open to everyone (in the subnet)
