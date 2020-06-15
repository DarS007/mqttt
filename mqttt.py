#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 2020/06/15 - DarS
#  - final version (rel.1.0) is ready
#  - you need 'paho-mqtt' and some TTF fonts (if you don't like the default font)
# 2020/06/12 - DarS
# source: https://stackoverflow.com/questions/51807052/mqtt-subscribing-and-reading-from-multiple-topics
"""MQTT terminal to display MQTT messages on a Raspberry Pi (or other SBC) with small LCD or OLED
"""

import argparse
import gettext
import importlib
import json
import locale
import logging
import os
import paho.mqtt.client as mqtt
import pygame, sys
import time

# initialize logger
parser = argparse.ArgumentParser(description=__file__)
parser.add_argument("--debug",
                    "-d",
                    action="store_const",
                    const=True,
                    default=False)
parser.add_argument("--fonts",
                    "-f",
                    help='check what system fonts are accessible to Pygame', 
                    action="store_const",
                    const=True,
                    default=False)
args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                    stream=sys.stdout,
                    format="%(asctime)s %(levelname)s %(message)s")
if args.fonts:
    print("=====================================================================")
    print("List of System Fonts that are accessible to Pygame.")
    print("You can configure this app (via 'MQTTtermcfg.json' file) to use one of these fonts:")
    print(pygame.font.get_fonts())
    print("Please note that Linux systems with framebuffer LCDs and without X Server (without desktop env)")
    print("do NOT have any System Fonts installed/available. But you can install TTF fonts on your own!")
    print("Just invoke 'sudo apt-get install fonts-liberation' and several TTF fonts will be installed in")
    print("'/usr/share/fonts/truetype/liberation/' directory. You can then adjust your 'MQTTtermcfg.json' file")
    print("to include ")
    print("   - 'font_name: /usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf,' ")
    print("or any other font you wish.")
    sys.exit('Quitting... Available system fonts were listed')

# initialize thread
timer_thread = None

try:
    # load config file
    file = "/etc/MQTTtermcfg.json"
    if not os.path.exists(file):
        file = "{}/MQTTtermcfg.json".format(sys.path[0])
    with open(file, "r") as f:
        config = json.loads(f.read())
    logging.info("config %s loaded", file)

    # initialize pygame
    if "DISPLAY_NO" in config:
        os.putenv("DISPLAY", config["DISPLAY_NO"])
    if "SDL_FBDEV" in config:
        os.putenv("SDL_FBDEV", config["SDL_FBDEV"])
    pygame.init()
    pygame.mouse.set_visible(False)
    display = screen = pygame.display.set_mode(config["display"])
    DISPLAY_SLEEP = pygame.USEREVENT + 1
    DISPLAY_WAKEUP = pygame.USEREVENT + 2
    RESTART = pygame.USEREVENT + 3
    logging.debug("pygame initialized. display:%s screen:%s",
                 display.get_size(), screen.get_size())
except Exception as e:
    logging.error(e, exc_info=True)

# define the list (buffer) for MQTT messages and clear the message counter
mqtt_msg_list = ["Waiting for MQTT messages..."]
mqtt_msg_counter = 1

# create display background
background = pygame.Surface(screen.get_size())
background.fill(config["screen_bkg"])

# define the font objects for title and MQTT messages
# (select non-System Font for framebuffer LCD because such system, most likely, 
#  does NOT HAVE any System Font installed)
if config["SDL_FBDEV"]:
    titlefont = pygame.font.Font(config["font_name"], config["fontsize_title"])
    msgfont = pygame.font.Font(config["font_name"], config["fontsize_msg"])
    msgfont_m = pygame.font.Font(config["font_name"], int(config["fontsize_msg"]*0.8))
    msgfont_s = pygame.font.Font(config["font_name"], int(config["fontsize_msg"]*0.6))
else:
    titlefont = pygame.font.SysFont(config["font_name"], config["fontsize_title"])
    msgfont = pygame.font.SysFont(config["font_name"], config["fontsize_msg"])
    msgfont_m = pygame.font.SysFont(config["font_name"], int(config["fontsize_msg"]*0.8))
    msgfont_s = pygame.font.SysFont(config["font_name"], int(config["fontsize_msg"]*0.6))

# get ready for MQTT connection
broker_url = config["MQTTbroker_url"]
broker_port = config["MQTTbroker_port"]
logging.debug("MQTT broker config read: %s:%s",
             broker_url, broker_port)

ss=''

def onConnect(client, userdata, flags, rc):
#   print("Connected With Result Code "+rc)
    logging.debug("connected to MQTT broker with Result Code: %s", rc)

def onMessage(client, userdata, message):
    logging.debug("MQTT message from : %s", message.topic)
    global ss, mqtt_msg_counter
    ss=(str(time.strftime("%H:%M:%S", time.localtime())+": "+message.topic+" - "+message.payload.decode("utf-8")))
    mqtt_msg_list.append(ss) 
    mqtt_msg_counter += 1
	# trim the list if it is too long
    while (len(mqtt_msg_list) > config["MQTT_max_messages"]):
        mqtt_msg_list.pop(0)

# connect to MQTT broker and subscribe to everything (#)
client = mqtt.Client()
client.on_connect = onConnect
client.on_message = onMessage
client.connect(broker_url, broker_port)
client.loop_start()
client.subscribe("#")

# main loop for receiving and displaying MQTT messages
while True:
    screen.blit(background, (0,0))
    tmp_pos_y = config["MQTT_window_bottom"]
	
	# render title
    title=titlefont.render("Broker %s" %broker_url, True, config["fontcolor_title"])
    titleRect = title.get_rect(topleft=(5,5))
    screen.blit(title,titleRect)
    pygame.draw.rect(screen, config["fontcolor_title"], (0, 0, screen.get_width(), int(config["fontsize_title"]*1.4)), 1)

    # render MQTT message list with a diminishing tail (tail goes first and is placed at the bottom)
    for x in mqtt_msg_list:
        if tmp_pos_y == config["MQTT_window_bottom"]:
            text=msgfont_s.render(" %s" %x, True, (160, 160, 160))
            textRect = text.get_rect(topleft=(25,tmp_pos_y))
            screen.blit(text,textRect)
            tmp_pos_y = int(tmp_pos_y-config["fontsize_msg"]/1.5)
        elif tmp_pos_y >= 0.9*config["MQTT_window_bottom"]:
            text=msgfont_m.render(" %s" %x, True, (192, 192, 192))
            textRect = text.get_rect(topleft=(12,tmp_pos_y))
            screen.blit(text,textRect)
            tmp_pos_y = int(tmp_pos_y-config["fontsize_msg"]/1.2)
        else:
            text=msgfont.render(" %s" %x, True, config["fontcolor_msg"])
            textRect = text.get_rect(topleft=(5,tmp_pos_y))
            screen.blit(text,textRect)
            tmp_pos_y = tmp_pos_y-0.93*config["fontsize_msg"]

    # render MQTT message counter
    msg_counter=msgfont.render(" %s" %mqtt_msg_counter, True, (0,255,0))
    msg_counterRect = msg_counter.get_rect(topleft=(410,280))
    screen.blit(msg_counter,msg_counterRect)

    # rotate text for upside down LCD if necessary
    if "rotate_upside_down" in config:
        screen.blit(pygame.transform.rotate(screen, 180), (0, 0))

    time.sleep(0.2)    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
pygame.quit()
sys.exit()