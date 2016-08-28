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

vc.dump(window='-1')
init_view = vc.findViewWithText(u'''Tap here\nto set alarm''')
touch(init_view)
sleep(65) # sleep for 10 minutes
touch(init_view)
vc.dump(window='-1')
onoff_switch = vc.findViewById("id/no_id/19") or vc.findViewById("id/no_id/9") #19 for odroid and 9 for nexus
ampm_switch = vc.findViewWithText(u'OFF') or vc.findViewWithText(u'ON')
more_button = vc.findViewById("id/no_id/21") or vc.findViewById("id/no_id/11") #21 for odroid and 11 for nexus
for i in range(200):
    touch(ampm_switch)
touch(onoff_switch)    
next_theme = 'Dark'
for i in range(12):
    vc.dump(window='-1')
    touch(init_view)
    touch(onoff_switch)
    touch(init_view)
    touch(ampm_switch)
    touch(ampm_switch)
    touch(ampm_switch)
    touch(onoff_switch)
    touch(more_button)
    vc.dump(window='-1')
    settings = vc.findViewWithText(u'''Settings''')
    touch(settings)
    vc.dump(window='-1')
    touch(vc.findViewWithText(u'''Theme'''))
    vc.dump(window='-1')
    touch(vc.findViewWithText(next_theme))
    if next_theme == 'Dark':
        next_theme = 'Light'
    else:
        next_theme = 'Dark'
    back(device)

save_interaction(serialno,"talalarmo_cache.json")
