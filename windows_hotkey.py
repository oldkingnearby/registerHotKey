# -*- coding: utf8-*-
# windows 平台
# 这段代码很久之前测试过，或许会有些许bug

import sys
import time
from ctypes import *
from ctypes.wintypes import *

delta = 0.3
lastTime = 0

WM_HOTKEY   = 0x0312
MOD_ALT     = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT   = 0x0004
WM_KEYUP    = 0x0101
class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pt', POINT)]
key = 192 # ~ 键
hotkeyId = 1
if not windll.user32.RegisterHotKey(None, hotkeyId, None, key):
    sys.exit("Cant Register Hotkey")

msg = MSG()
while True:
    if (windll.user32.GetMessageA(byref(msg), None, 0, 0) != 0):
        if msg.message == WM_HOTKEY and msg.wParam == hotkeyId:
            if (time.time() - lastTime) < delta:
                print "down"
            else:
                pass
            lastTime = time.time()
        if msg.message == WM_KEYUP:
            print "up"
        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageA(byref(msg))
