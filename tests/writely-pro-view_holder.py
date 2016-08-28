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

    

def create_folder(name):
    print "creating folder %s"%name
    vc.dump(window='-1')
    expand_menu_button = vc.findViewById("me.writeily:id/fab_expand_menu_button") or vc.views[-1]
    touch(expand_menu_button)
    vc.dump(window='-1')
    touch(vc.findViewById("me.writeily:id/create_folder") or vc.views[-2])
    vc.dump(window='-1')
    type_text(device,name)
    touch(vc.findViewWithText(u'Create'))
    print "creating folder %s: done"%name

def create_note(name):
    print "creating note %s"%name
    vc.dump(window='-1')
    expand_menu_button = vc.findViewById("me.writeily:id/fab_expand_menu_button") or vc.views[-1]
    touch(expand_menu_button)
    vc.dump(window='-1')
    create_note_button = vc.findViewById("me.writeily:id/create_note") or vc.views[-3]
    touch(create_note_button)
    vc.dump(window='-1')
    type_text(device,name)
    touch(vc.findViewById("me.writeily:id/note_content") or vc.findViewById("id/no_id/14"))
    type_text(device,'# Title\n\n_one thing is italic_. **Another thing is bold**.\n\n[Link](Link)\n----\nEnd\n')
    touch(vc.findViewWithContentDescription(u'''Navigate up'''))

vc.dump(window='-1')
touch(vc.findViewWithContentDescription(u'''More options'''))
vc.dump(window='-1')
touch(vc.findViewWithText(u'Settings'))
vc.dump(window='-1')
touch(vc.findViewWithContentDescription(u'''Navigate up'''))


    
number_of_repeats = 2
for i in range(number_of_repeats):
    create_folder("folder-one")
    

    
    vc.dump(window='-1')
    touch(vc.findViewWithText("folder-one"))
    for folder_one_i in range(20):
        create_folder("folder-one-%d"%folder_one_i)
    
    create_note("note-one")
    
    # root folder
    
    create_folder("folder-two")
    
    vc.dump(window='-1')
    touch(vc.findViewWithText("folder-two"))
    create_note("note-two")
    
    vc.dump(window='-1')
    touch(vc.findViewWithText("folder-two"))
    create_note("note-three")
    
    vc.dump(window='-1')
    touch(vc.findViewWithText("folder-two"))
    create_note("note-four")
    
    #root
    for folder_one_i in range(10):
        vc.dump(window='-1')
        touch(vc.findViewWithText("folder-one"))
        back(device)
    # loop to enter and exit folder-one
    
    #root
    
    vc.dump(window='-1')
    touch(vc.findViewWithText("folder-two"))
    
    vc.dump(window='-1')
    #seleect folder two three and four
    hold(vc.findViewWithText(u'note-two'))
    touch(vc.findViewWithText(u'note-three'))
    touch(vc.findViewWithText(u'note-four'))
    
    vc.dump(window='-1')
    touch(vc.findViewWithContentDescription(u'''Move'''))
    vc.dump(window='-1')
    touch(vc.findViewWithText(u'folder-one'))
    vc.dump(window='-1')
    touch(vc.findViewWithText(u'Move here'))
    vc.dump(window='-1')
    create_note("note-five")
    
    create_folder("folder-three")
    
    vc.dump(window='-1')
    #seleect folder one and two
    hold(vc.findViewWithText(u'folder-one'))
    
    vc.dump(window='-1')
    touch(vc.findViewWithContentDescription(u'''Move'''))
    vc.dump(window='-1')
    touch(vc.findViewWithText(u'folder-three'))
    vc.dump(window='-1')
    touch(vc.findViewWithText(u'Move here'))
    
    vc.dump(window='-1')
    hold(vc.findViewWithText(u'folder-three'))
    
    vc.dump(window='-1')
    touch(vc.findViewWithContentDescription(u'''Delete'''))
    vc.dump(window='-1')
    touch(vc.findViewWithText(u'OK'))

save_interaction(serialno,"writely-pro-view_holder_cache.json")

    

