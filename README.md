# mqttt - MQTT Terminal

MQTT is a real backbone of IoT. Lighweight, scalable, popular, etc. If you're IoT fanatic, you've perhaps collected a decent set of MQTT tools in your workbench. Me too. But I was always missing a portable, standalone, small, always-on display that could connect to MQTT broker and show the circulating messages. Yeah, I know... I can fire up MQTT.fx or XXX (enter here your preference) on my desktop. But this is not always handy or comfortable.

Therefore here you go... **MQTT Terminal** is a small, relatively dumb, standalone device to display rolling MQTT messages. It can be build with Raqspberry Pi Zero W (and any other single board computer/SBC) and 3.5" (or bigger) LCD. You can place it on your desk, next to your laptop, and discretely watch whether MQTT messaging works as expected. Great for targeted troubleshooting or ad hoc diagnosis.

## HARDWARE
*Raspberry Pi Zero W* is perhaps the most optimal (cost and performance) platform. It's even too beefy for such easy task, but come on... You can spend $9 for RPi or $3 on ESP8266 - small difference for a singular DIY quantities. And with RPi you have a comfort of full Linux distribution, fully functional Python, flawless WiFi, etc. 

For display, you can use any small LCD screen HAT you wish. It has to work with Raspberry Pi, of course. But this is the only limitation. **MQTT Terminal** uses *framebuffer* for graphics so it DOES NOT need X Server to be installed. When selecting OS distribution for your Raspberry Pi, do not install fully featured *desktop* version. Choose *server* flavor. It is much lighter anyway.



## TO DO
- MQTT authentication - it is currently lacking, as the code was developed for in-house usage where local MQTT broker was open to everyone (in the subnet)
