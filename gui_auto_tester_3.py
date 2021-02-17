#!/usr/bin/env python3


import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
import sys
import subprocess
import time
import random

def get_screen_resolution():
    return

def pixel_at(x, y):
    w = Gdk.get_default_root_window()
    pb = Gdk.pixbuf_get_from_window(w, x, y, 1, 1)
    return pb.get_pixels()

def call_xdotool(call):
    call = "xdotool " + call
    cmd_list = call.split()
#    print(cmd_list)
    subprocess.call(cmd_list)


def activate_bsps():
    call_xdotool("search --class bsps_client_launcher windowactivate %@")

def check_pixel_color(x, y, color):
    print("Check if pixel at x={} y={} is RGB={}".format(x, y, color))
    if list(pixel_at(x, y)) == color:
        return True
    else:
        return False


def click_bw():
    print("Click write button")
    while True:
        if check_pixel_color(BW_X, BW_Y, BW_COLOR):
            call_xdotool("mousemove {} {} click 1".format(BW_X, BW_Y))
            return
        else:
            time.sleep(1)

def click_snd():
    while True:
        if check_pixel_color(SND_X, SND_Y, SND_COLOR):
            call_xdotool("mousemove {} {} click 1".format(SND_X, SND_Y))
            return
        else:
            time.sleep(1)
        

def type_message(msg):
    print("Typing message")
    call_xdotool("mousemove {} {} click 1".format(412, 227))
    time.sleep(ACTION_PAUSE)
    subprocess.call(["xdotool", "type", "--delay", "100", msg])
    #call_xdotool("type --delay 100 " + msg)
    time.sleep(ACTION_PAUSE)

def change_in_selector(sel_type, num, sel_x, sel_y):
    print("Changing {} level of message to {}".format(sel_type, num))
    num_to_yoffset = {
                1: 30,
                2: 60,
                3: 90,
                4: 120,
            }
    call_xdotool("mousemove {} {} click 1".format(sel_x, sel_y))
    time.sleep(ACTION_PAUSE)
    call_xdotool("mousemove {} {}".format(sel_x, sel_y + num_to_yoffset[num]))
    time.sleep(ACTION_PAUSE)
    call_xdotool("click 1")
    time.sleep(ACTION_PAUSE)



#def change_urgency(urg):
#    print("Changing urgency level of message to {}".format(urg))
#    urg_coords = {
#                1: 30,
#                2: 60,
#                3: 90,
#                4: 120,
#            }
#    call_xdotool("mousemove {} {} click 1".format(MAC_SELECTOR_X, MAC_SELECTOR_Y))
#    time.sleep(ACTION_PAUSE)
#    call_xdotool("mousemove {} {}".format(MAC_SELECTOR_X, MAC_SELECTOR_Y + mac_coords[mac]))
#    time.sleep(ACTION_PAUSE)
#    call_xdotool("click 1")
#    time.sleep(ACTION_PAUSE)
#


def attach_file(file_att):
    print("Attaching file {} to message".format(file_att))
    call_xdotool("mousemove {} {} click 1".format(FILE_ATT_BTN_X, FILE_ATT_BTN_Y))
    time.sleep(ACTION_PAUSE)
    while True:
        if check_pixel_color(FILE_ATT_WIN_X, FILE_ATT_WIN_Y, FILE_ATT_WIN_COLOR):
            for i in range(0,3):
                call_xdotool("key Tab")
                time.sleep(ACTION_PAUSE)
            for i in file_att.split("/"):
                if i != "":
                    call_xdotool("key 0x002f")
                    subprocess.call(["xdotool", "type", "--delay", "100", i])
            #0x002f
            #subprocess.call(["xdotool", "type", "--delay", "100", file_att])
            time.sleep(ACTION_PAUSE)
            call_xdotool("key Return")
            time.sleep(ACTION_PAUSE)
            return
        else:
            time.sleep(1)
 


def generate_mac():
    mac = random.randint(1,4)
    return mac

def generate_urgency():
    urg = random.randint(1,4)
    return urg

def generate_file_attachment():
    file_att = random.randint(0,3)
    return file_att


ITER=100000

BW_X=27
BW_Y=114
BW_COLOR=[220, 223, 227]

SND_X=410
SND_Y=48
SND_COLOR=[216, 216, 216]

MAC_SELECTOR_X=632
MAC_SELECTOR_Y=136

URG_SELECTOR_X=506
URG_SELECTOR_Y=136

FILE_ATT_BTN_X=268
FILE_ATT_BTN_Y=915

FILE_ATT_WIN_X=374
FILE_ATT_WIN_Y=631
FILE_ATT_WIN_COLOR=[234, 234, 234]

# Pause between actions
ACTION_PAUSE=0.3
# Pause between interations
PAUSE=0.3

i = 0
#i = 5000
activate_bsps()

mac_to_filepath = {
        1: "/1/НС/",
        2: "/1/ДСП/",
        3: "/1/С/",
        4: "/1/СС/",
        }




while i < ITER:
    click_bw()
    mac = generate_mac();
    change_in_selector("mac", mac, MAC_SELECTOR_X, MAC_SELECTOR_Y)
    time.sleep(ACTION_PAUSE)
    change_in_selector("urgency", generate_urgency(), URG_SELECTOR_X, URG_SELECTOR_Y)
    time.sleep(ACTION_PAUSE)
    file_att = generate_file_attachment()
    if (file_att > 0):
        attach_file(mac_to_filepath[mac] + "{}.txt".format(file_att))

    type_message("from 70 number {}".format(i))
    click_snd()
    i += 1
    time.sleep(PAUSE)


#type_message("num {}".format(i))

#print(list(pixel_at(int(sys.argv[1]), int(sys.argv[2]))))



# x
# x   = 27
# 100 = 1920
# 
# perc=1.4
# 
# y
# x   = 110
# 100 = 1200
# perc = 9.1
# 
