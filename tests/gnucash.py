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
next =vc.findViewWithTextOrRaise(u'Next') 
touch(next)
touch(next)
touch(next)
vc.dump(window='-1')
touch(vc.findViewWithTextOrRaise(u'Disable crash reports'))
touch(next)
touch(next)
vc.dump(window='-1')
allow = vc.findViewWithText(u'Allow')
if allow:
    touch(allow)
vc.dump(window='-1')
touch(vc.findViewWithTextOrRaise(u'Assets'))
vc.dump(window='-1')
more_options = vc.findViewWithContentDescriptionOrRaise(u'''More options''')
touch(more_options)
vc.dump(window='-1')
edit_account = vc.findViewWithTextOrRaise(u'Edit Account')
touch(edit_account)
back(device)
back(device)
account = 'Assets'
for _ in range(10):
    vc.dump(window='-1')
    touch(vc.findViewWithTextOrRaise(account))
    for _ in range(20):
        touch(more_options)
        touch(edit_account)
        back(device)
    back(device)
    if account == 'Assets':
        account = 'Equity'
    else:
        account = 'Assets'

save_interaction(serialno,"gnucash_cache.json")
