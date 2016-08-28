import sys
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyView
print sys.argv
serialno=sys.argv[1]
(x,y) = (int(sys.argv[2]),int(sys.argv[3]))
device = MonkeyRunner.waitForConnection(timeout = 60, deviceId = serialno)

no_of_seconds=2
device.touch(x, y,MonkeyDevice.DOWN)
MonkeyRunner.sleep(no_of_seconds)
# to release the hold
device.touch(x, y,MonkeyDevice.UP)