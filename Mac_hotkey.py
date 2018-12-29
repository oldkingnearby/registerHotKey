# -*- coding: utf8 -*-

# 主要参考: https://gist.github.com/nevyn/764542/73e53a77dc59d7c78510069d9215f4a0a17c6cb8
# mac 平台

import Quartz
from AppKit import NSKeyUp, NSSystemDefined, NSEvent, NSKeyDownMask


def keyboardTapCallback(proxy, type_, event, refcon):
    keyEvent = NSEvent.eventWithCGEvent_(event)
    if (keyEvent.subtype() == 8):
        key_code = (keyEvent.data1() & 0xFFFF0000) >> 16
        key_state = (keyEvent.data1() & 0xFF00) >> 8
        if key_code is 16 or key_code is 19 or key_code is 20:
            # 16 for play-pause, 19 for next, 20 for previous
            return None  # 截取到事件，其他程序将不会收到该事件。如果之前是listen only就不能截取
    return event

# Set up a tap, with type of tap, location, options and event mask
tap = Quartz.CGEventTapCreate(
    Quartz.kCGSessionEventTap, # Session level is enough for our needs
    Quartz.kCGHeadInsertEventTap, # Insert wherever, we do not filter
    Quartz.kCGEventTapOptionListenOnly, # (如果是default就可以截取事件, 现在只能监听)
    Quartz.CGEventMaskBit(NSSystemDefined), # NSSystemDefined for media keys
    keyboardTapCallback,
    None
)


runLoopSource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
Quartz.CFRunLoopAddSource(
    Quartz.CFRunLoopGetCurrent(),
    runLoopSource,
    Quartz.kCFRunLoopDefaultMode
)
# Enable the tap
Quartz.CGEventTapEnable(tap, True)
# and run! This won't return until we exit or are terminated.
Quartz.CFRunLoopRun()
