#!/usr/bin/python3
import serial
from time import sleep, clock_settime, CLOCK_REALTIME
from datetime import datetime

#
# ssetup.py
# boot configuration for Joy-it StromPi 3
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
    timeout=.1
)

def sendserial(msg):
    """
    send msg over serial channel
    """
    print(msg)
    for uch in msg:
        ser.write(uch.encode('UTF-8', 'replace'))
    sleep(.1)


def sendcmd(cmd):
    """
    send a command over serial channel
    """
    sendserial(cmd)
    sleep(.5)
    sendserial('\x0D')
    sleep(.1)


def setconfig(item, val):
    """
    set a configuration value
    """
    sendcmd("set-config " + str(item) + " " + str(val) + "\n")


def getserial(tout=10):
    """
    get a line from serial channel
    """
    buf = ''
    while True:
        chr = ser.read().decode()
        if chr == '\r':
            continue
        if chr == '\n':
            return buf + "\n"
        if len(chr) == 0 and len(buf) > 0:
            return buf
        if len(chr) > 0:
            buf += chr
        else:
            tout -= 1
            if tout < 0:
                return ''


def getans():
    """
    get a response from serial channel
    """
    while True:
        buf = getserial(4)
        if len(buf) > 0:
            #print("buf ->", len(buf), buf)
            continue
        else:
            return


def getconf():
    """
    retrieva configuration values and store all in a dictionary
    """
    cnf = {}
    sendcmd('status-rpi')
    cnf['time'] = getserial().strip()
    cnf['date'] = getserial().strip()
    cnf['weekday'] = getserial().strip()
    cnf['modus'] = getserial().strip()
    cnf['alarm_enable'] = getserial().strip()
    cnf['alarm_mode'] = getserial().strip()
    cnf['alarm_hour'] = getserial().strip()
    cnf['alarm_min'] = getserial().strip()
    cnf['alarm_day'] = getserial().strip()
    cnf['alarm_month'] = getserial().strip()
    cnf['alarm_weekday'] = getserial().strip()
    cnf['alarmPoweroff'] = getserial().strip()
    cnf['alarm_hour_off'] = getserial().strip()
    cnf['alarm_min_off'] = getserial().strip()
    cnf['shutdown_enable'] = getserial().strip()
    cnf['shutdown_time'] = getserial().strip()
    cnf['warning_enable'] = getserial().strip()
    cnf['serialLessMode'] = getserial().strip()
    cnf['intervalAlarm'] = getserial().strip()
    cnf['intervalAlarmOnTime'] = getserial().strip()
    cnf['intervalAlarmOffTime'] = getserial().strip()
    cnf['batLevel_shutdown'] = getserial().strip()
    cnf['batLevel'] = getserial().strip()
    cnf['charging'] = getserial().strip()
    cnf['powerOnButton_enable'] = getserial().strip()
    cnf['powerOnButton_time'] = getserial().strip()
    cnf['powersave_enable'] = getserial().strip()
    cnf['poweroffMode'] = getserial().strip()
    cnf['poweroff_time_enable'] = getserial().strip()
    cnf['poweroff_time'] = getserial().strip()
    cnf['wakeupweekend_enable'] = getserial().strip()
    cnf['ADC_Wide'] = float(getserial().strip()) / 1000
    cnf['ADC_BAT'] = float(getserial().strip()) / 1000
    cnf['ADC_USB'] = float(getserial().strip()) / 1000
    cnf['ADC_OUTPUT'] = float(getserial().strip()) / 1000
    cnf['output_status'] = getserial().strip()
    cnf['powerfailure_counter'] = getserial().strip()
    cnf['firmwareVersion'] = getserial().strip()
    return cnf


#
# flush serial channel
#
ser.reset_input_buffer()
ser.reset_output_buffer()
sleep(.5)
# quit console if left open
sendserial("quit\r")
getans()
#
# ## sync rtc
#
sendcmd("date-rpi")
srtc = getserial(5)
if len(srtc) == 6 and srtc.isnumeric():
    # exctract date from response
    yrtc = int(srtc[0:2]) + 2000
    mrtc = int(srtc[2:4])
    drtc = int(srtc[4:6])
else:
    # invalid format
    print("Hat date: invalid format " + srtc)
    yrtc = 2000
    mrtc = 1
    drtc = 1
sendcmd("time-rpi")
srtc = (6 * "0" + getserial(5))[-6:]
if srtc.isnumeric():
    # exctract time from response
    Hrtc = int(srtc[0:2])
    Mrtc = int(srtc[2:4])
    Srtc = int(srtc[4:6])
    print(Hrtc, Mrtc, Srtc)
else:
    print("Hat time: invalid format " + srtc)
    Hrtc = 0
    Mrtc = 0
    Srtc = 0
hrtc = datetime(yrtc, mrtc, drtc, Hrtc, Mrtc, Srtc)
rrtc = datetime.now()
if rrtc > hrtc:  # set hat clock to system time
    sdate = rrtc.strftime("%d %m %y 0") + str(rrtc.isoweekday())
    sendcmd("set-date " + sdate)
    stime = rrtc.strftime("%H %M %S")
    sendcmd("set-clock " + stime)
else: # set system time to hat clock - needs clock setting privileges
    clock_settime(CLOCK_REALTIME, hrtc.timestamp())
#
# set hat configuration
#
setconfig(1, 4)  # modus
setconfig(13, 0)  # alarm enable
setconfig(14, 1)  # shutdown enable
setconfig(15, 90)  # shutdown timer
setconfig(16, 1)  # warning enable
setconfig(22, 1)  # PowerButton
setconfig(25, 0)  # PowerOff mode
setconfig(27, 55)  # PowerOff time

setconfig(0, 1)  # write config

#cnf = getconf()
#print(cnf)
