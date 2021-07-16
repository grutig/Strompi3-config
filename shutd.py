#!/usr/bin/python3

import serial
import os
import sys

#
# shutd.py
# shutdown daemon for Joy-it StromPi 3
#
#
# This is free software released under MIT License
# Copyright 2021 Giorgio L. Rutigliano
# (www.iltecnico.info, www.i8zse.eu, www.giorgiorutigliano.it)
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# shdely sets the delay between the powerfail event and the start of the shutdown process
# must be set to the value of StrimPi3 shutdown-timer less the time required to end the shutdown process

shdelay = 30  # shutdown delay in seconds

#
# Serial port
# since StrompPI3 uses a rather high comm speed (btw: why?), it requires that /dev/serial0 on raspberry 3 and 4
# is assigned to /dev/ttyAMA0
# to do so, put
# dtoverlay=pi3-miniuart-bt
# in /boot/config.txt
#

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

pfail = False
pftimer = 0
while True:
    msg = ser.readline().decode().strip()
    if msg == 'xxxShutdownRaspberryPixxx':
        print("poerfail")
        pfail = True
    if msg == 'xxx--StromPiPowerBack--xxx':
        print("powerback")
        pfail = False
        pftimer = 0
    if pfail:
        pftimer +=1
        if pftimer > shdelay:
            print("shutdown")
            os.system("shutdown -h now")
            sys.exit(10)
