#!/usr/bin/env python
import ctypes
import os
import time
import sys

class XScreenSaverInfo(ctypes.Structure):
  """ typedef struct { ... } XScreenSaverInfo; """
  _fields_ = [('window',      ctypes.c_ulong), # screen saver window
              ('state',       ctypes.c_int),   # off,on,disabled
              ('kind',        ctypes.c_int),   # blanked,internal,external
              ('since',       ctypes.c_ulong), # milliseconds
              ('idle',        ctypes.c_ulong), # milliseconds
              ('event_mask',  ctypes.c_ulong)] # events

xlib = ctypes.cdll.LoadLibrary('libX11.so')
dpy = xlib.XOpenDisplay(os.environ['DISPLAY'])
root = xlib.XDefaultRootWindow(dpy)
xss = ctypes.cdll.LoadLibrary('libXss.so')
xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
xss_info = xss.XScreenSaverAllocInfo()
playing = True
while True:
    try:
        xss.XScreenSaverQueryInfo(dpy, root, xss_info)
        idle_time_seconds = xss_info.contents.idle / 1000.0
        if idle_time_seconds > 30:
            if playing:
                os.system("mocp -P")
                playing = False
        else:
            if not playing:
                os.system("mocp -U")
                playing = True
        time.sleep(0.2)
    except KeyboardInterrupt:
        sys.exit(0)
