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
allow = vc.findViewWithText(u'Allow')
if allow:
    touch(allow)
dir = None
media_item = None
for _ in range(100):
    if dir is None:
        vc.dump(window='-1')
        dir = vc.findViewById("com.simplemobiletools.gallery:id/dir_name") or vc.findViewById("id/no_id/18")
    touch(dir)
    if media_item is None:
        vc.dump(window='-1')
        media_item = vc.findViewById("com.simplemobiletools.gallery:id/media_item_holder") or vc.findViewById("id/no_id/11")
    touch(media_item)
    back(device)
    for _ in range(15):
        swipeUp(device)
    back(device)

save_interaction(serialno,"simplegallery_cache.json")
