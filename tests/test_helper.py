import time
import os
import json

PERSIST_SCRIPT=True

if PERSIST_SCRIPT:
    interaction = []

def touch(view):
    view.touch()
    if PERSIST_SCRIPT:
        (x,y) = view.getXY()
        touch_coord = (x+view.getWidth()/2, y+view.getHeight()/2)
        interaction.append({'type':'touch','position':touch_coord})

def type_text(device, text):
    device.type(text)
    if PERSIST_SCRIPT:
        interaction.append({'type':'type_text','text':text})

def back(device):
    device.shell('input keyevent KEYCODE_BACK')
    if PERSIST_SCRIPT:
        interaction.append({'type':'back'})

def sleep(duration):
    time.sleep(duration)
    if PERSIST_SCRIPT:
        interaction.append({'type':'wait','duration':duration})

def hold(view):
    (x,y) = view.getXY()
    (x,y) = (x+view.getWidth()/2, y+view.getHeight()/2)
    # view.device.drag((x,y), (x,y), 2000, 1)
    os.system('monkeyrunner hold.py %s %d %d'%(view.device.serialno,x,y))
    if PERSIST_SCRIPT:
        interaction.append({'type':'hold','position':(x,y)})

def swipeUp(device):
    w13 = device.display['width'] / 3
    h = device.display['height']
    s = (w13, h/2)
    e = (w13, h/4)
    device.drag(s, e, 500, 20, -1)
    if PERSIST_SCRIPT:
        interaction.append({'type':'swipe_up'})

#save
def save_interaction(serialno, filename):
    if not os.path.isfile(filename):
        json_data = {}
    else:
        with open(filename,'r') as data_file:
            json_data = json.load(data_file)
    json_data.update({serialno:interaction})
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile)
