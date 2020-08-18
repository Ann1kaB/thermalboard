#!/usr/bin/python3
import os
import time

red = "/sys/devices/platform/faustus/kbbl/kbbl_red"
green = "/sys/devices/platform/faustus/kbbl/kbbl_green"
blue = "/sys/devices/platform/faustus/kbbl/kbbl_blue"

f=open("/sys/devices/platform/faustus/kbbl/kbbl_flags", 'w')
f.write("2a")

f=open("/sys/devices/platform/faustus/kbbl/kbbl_mode", 'w')
if f != "0":
    f.write("0")

while True:
    temp = open("/sys/class/thermal/thermal_zone0/temp", 'r').read().splitlines()[0]
    temp = temp[:2]
    if int(temp) >= 50:
        redbase = (int(temp) - 50) * 10
        if redbase <= 255:
            rval = hex(redbase)
            r=open(red, 'w')
            r.write(rval)
        elif redbase > 255:
            r=open(red, 'w')
            r.write("ff")
    elif int(temp) <= 50:
        r=open(red, 'w')
        r.write("00")

    if int(temp) <= 95:
        incgreenbase = (int(temp) - 95) * -10
        if incgreenbase <= 255:
            incgval = hex(incgreenbase)
            ig=open(green, 'w')
            ig.write(incgval)
        elif incgreenbase > 255:
            ig=open(green, 'w')
            ig.write("ff")
    elif int(temp) >= 95:
        ig=open(green, 'w')
        ig.write("00")

    if int(temp) >= 20 and int(temp) <= 50:
        decgreenbase = (int(temp) - 20) * 10
        if decgreenbase <= 255:
            decgval = hex(decgreenbase)
            dg=open(green, 'w')
            dg.write(decgval)

    if int(temp) <= 50:
        bluebase = (int(temp) - 50) * -10
        if bluebase <= 255:
            bval = hex(bluebase)
            b=open(blue, 'w')
            b.write(bval)
        elif bluebase > 255:
            b=open(blue, 'w')
            b.write("ff")
    elif int(temp) >= 60:
        b=open(blue, 'w')
        b.write("00")
    s=open("/sys/devices/platform/faustus/kbbl/kbbl_set", 'w')
    s.write("1")
    time.sleep(0.5)


