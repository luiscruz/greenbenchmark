#! /usr/bin/env python

import re
import sys
import os
from time import sleep
import json
import argparse
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

parser = argparse.ArgumentParser(description='Run Android user interaction that is described in a json file.')
parser.add_argument('json_file', help='the json file with interaction data')
args = parser.parse_args()
PERSIST_SCRIPT_FILENAME=args.json_file
del sys.argv[-1]

def swipeDown():
    w13 = device.display['width'] / 3
    h = device.display['height']
    s = (w13, h/3)
    e = (w13, h/2)
    device.drag(s, e, 500, 20, -1)

def swipeUp():
    w13 = device.display['width'] / 3
    h = device.display['height']
    s = (w13, h/2)
    e = (w13, h/4)
    device.drag(s, e, 500, 20, -1)

def hold(x,y):
    os.system('monkeyrunner tests/hold.py "%s" %d %d'%(serialno,x,y))
    # device.drag((x,y), (x,y), 2000, 1)

_v = '--verbose' in sys.argv
kwargs1 = {'ignoreversioncheck': False, 'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True, 'autodump': False, 'startviewserver': True, 'compresseddump': True}
vc = ViewClient(device, serialno, **kwargs2)


with open(PERSIST_SCRIPT_FILENAME) as data_file:
    interaction = json.load(data_file).get(serialno)

for action in interaction:
    action_type=action.get("type")
    if action_type == "touch":
        (x,y) = action.get("position")
        vc.touch(x,y)
    elif action_type == "type_text":
        device.type(action.get('text'))
    elif action_type == "wait":
        sleep(action.get('duration'))
    elif action_type == 'swipe_down':
        swipeDown()
    elif action_type == 'swipe_up':
        swipeUp()
    elif action_type == 'hold':
        (x,y) = action.get("position")
        hold(x,y)
    elif action_type == 'back':
        device.shell('input keyevent KEYCODE_BACK')
