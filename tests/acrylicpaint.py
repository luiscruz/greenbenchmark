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
touch(vc.findViewWithTextOrRaise(u'Continue'))
vc.dump(window='-1')
color_button = vc.findViewWithContentDescription(u'''Color''')

for _ in range(20):
    for _ in range(10):
        swipeUp(device)
    
    touch(color_button)
    vc.dump(window='-1')
    color_menu = vc.findViewById("id/no_id/1")
    
    for _ in range(10):
        touch(color_menu)
    back(device)

save_interaction(serialno,"acrylicpaint_cache.json")
