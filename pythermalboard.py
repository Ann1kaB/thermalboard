#!/usr/bin/python3
import os
import time
import sys

red = "/sys/devices/platform/faustus/kbbl/kbbl_red"
green = "/sys/devices/platform/faustus/kbbl/kbbl_green"
blue = "/sys/devices/platform/faustus/kbbl/kbbl_blue"

f=open("/sys/devices/platform/faustus/kbbl/kbbl_flags", 'w')
f.write("2a")

debug = True

f=open("/sys/devices/platform/faustus/kbbl/kbbl_mode", 'w')
if f != "0":
    f.write("0")

# fucking NVIDIA
present = os.popen("xrandr --listproviders | grep -o \"NVIDIA.*\"").read()

while True:
    try:
        cputemp = open("/sys/class/thermal/thermal_zone0/temp", 'r').read().splitlines()[0]
        if present:
            gputemp = os.popen("nvidia-smi | awk '{print $3}' | xargs | awk '{print $7}' | sed 's/C//'").read()
            gputemp = gputemp.split()[0]
        else:
            gputemp = 0
        cputemp = cputemp[:2]
        if int(cputemp) >= 50 and int(gputemp) >= 40:
            if int(cputemp) > int(gputemp):
                redbase = (int(cputemp) - 50) * 10
            elif int(cputemp) < int(gputemp):
                redbase = (int(gputemp) - 40) * 10
            if redbase <= 255 and redbase > 0:
                rval = hex(redbase)
                if debug:
                    print("rval: %s" % rval, cputemp, gputemp)
                r=open(red, 'w')
                r.write(rval)
            elif redbase > 255:
                r=open(red, 'w')
                r.write("ff")
        elif int(cputemp) <= 60 and int(gputemp) <= 60:
            r=open(red, 'w')
            r.write("00")

        if int(cputemp) <= 95 and int(gputemp) <= 85:
            if int(cputemp) > int(gputemp):
                incgreenbase = (int(cputemp) - 95) * -10
            elif int(cputemp) < int(gputemp):
                incgreenbase = (int(gputemp) - 85) * -10
            if incgreenbase <= 255 and incgreenbase > 0:
                incgval = hex(incgreenbase)
                if debug:
                    print("incgval: %s" % incgval)
                ig=open(green, 'w')
                ig.write(incgval)
            elif incgreenbase > 255:
                ig=open(green, 'w')
                ig.write("ff")
        elif int(cputemp) >= 95 and int(gputemp) >= 85:
            ig=open(green, 'w')
            ig.write("00")

        if int(cputemp) >= 20 and int(cputemp) <= 50 and int(gputemp) >= 20 and int(gputemp) <= 40:
            if int(cputemp) > int(gputemp):
                decgreenbase = (int(cputemp) - 20) * 10
            elif int(cputemp) < int(gputemp):
                decgreenbase = (int(gputemp) - 20) * 10
            if decgreenbase <= 255 and decgreenbase > 0:
                decgval = hex(decgreenbase)
                if debug:
                    print("decgval %s" % decgval)
                dg=open(green, 'w')
                dg.write(decgval)

        if int(cputemp) <= 50 and int(gputemp) <= 50:
            if int(cputemp) > int(gputemp):
                bluebase = (int(cputemp) - 50) * -10
            elif int(cputemp) < int(gputemp):
                bluebase = (int(gputemp) - 50) * -10
            if bluebase <= 255 and bluebase > 0:
                bval = hex(bluebase)
                if debug:
                    print("bval: %s" % bval)
                b=open(blue, 'w')
                b.write(bval)
            elif bluebase > 255:
                b=open(blue, 'w')
                b.write("ff")
        elif int(cputemp) >= 50 and int(gputemp) >= 40:
            b=open(blue, 'w')
            b.write("00")
        s=open("/sys/devices/platform/faustus/kbbl/kbbl_set", 'w')
        s.write("1")
        time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting.")
        sys.exit(0)


