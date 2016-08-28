from test_helper import *
import re
import sys
import os

from com.dtmilano.android.viewclient import ViewClient

TAG = 'CULEBRA'

_s = 5
_v = '--verbose' in sys.argv

kwargs1 = {'ignoreversioncheck': False, 'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True, 'autodump': False, 'startviewserver': True, 'compresseddump': True}
vc = ViewClient(device, serialno, **kwargs2)

def add_habit(habit_name):
    print("Creating habit %s"%habit_name)
    vc.dump(window='-1')
    sleep(1)
    touch(vc.findViewWithContentDescription(u'''Add habit'''))
    vc.dump(window='-1')
    type_text(device,habit_name)
    vc.dump(window='-1') # in case the keyboard changed layout
    save_button= vc.findViewWithText(u'Save')
    #go to reminder view and go back
    # touch(vc.findViewWithText(u'Off'))
    # vc.dump(window='-1')
    # touch(vc.findViewWithText(u'Clear'))
    touch(save_button)
    #Main window
    vc.dump(window='-1')
    touch(vc.findViewWithTextOrRaise(habit_name))
    vc.dump(window='-1')
    swipeUp(device)
    swipeUp(device)
    touch(vc.findViewWithContentDescription(u'''Navigate up'''))


vc.dump(window='-1')
next_button=vc.findViewById("org.isoron.uhabits:id/next") or vc.findViewById("id/no_id/23")
touch(next_button)
touch(next_button)
touch(next_button)
touch(next_button)

#Main window
vc.dump(window='-1')
touch(vc.findViewWithContentDescription(u'''More options'''))
vc.dump(window='-1')
touch(vc.findViewWithText(u'About'))
swipeUp(device)
swipeUp(device)
back(device)


for k in range(10):
    print("Set %d"%k)
    for i in range(7):
        add_habit("H%d"%i)
        swipeUp(device)
        swipeUp(device)

    #Main window
    vc.dump(window='-1')
    for i in range(7):
        habit_name = "H%d"%i
        hold(vc.findViewWithText(habit_name))
    touch(vc.findViewWithContentDescription(u'''More options'''))
    vc.dump(window='-1')
    touch(vc.findViewWithText('Delete'))
    vc.dump(window='-1')
    touch(vc.findViewWithText('OK'))

#Main window

save_interaction(serialno,"uhabits_cache.json")
