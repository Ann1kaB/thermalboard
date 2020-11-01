#!/usr/bin/python3
import os
import time
import sys

RED = "/sys/devices/platform/faustus/kbbl/kbbl_red"
GREEN  = "/sys/devices/platform/faustus/kbbl/kbbl_green"
BLUE  = "/sys/devices/platform/faustus/kbbl/kbbl_blue"

MAX_TEMP = 95
MIN_TEMP = 20
MID_TEMP = 50

KB_FLAGS = open("/sys/devices/platform/faustus/kbbl/kbbl_flags", 'w')
KB_FLAGS.write("2a")

SET_KB = "/sys/devices/platform/faustus/kbbl/kbbl_set"

KB_MODE = open("/sys/devices/platform/faustus/kbbl/kbbl_mode", 'w')
KB_MODE_R = open("/sys/devices/platform/faustus/kbbl/kbbl_mode", 'r')
if KB_MODE_R != "0":
    KB_MODE.write("0")

debug = False


def get_temp():
    CPU_TEMP = open("/sys/class/thermal/thermal_zone0/temp", 'r').read().splitlines()[0]
    cputemp = int(CPU_TEMP[:2])
    return cputemp


def over_max_temp():
# reset KB B and G color
    blue_w = open(BLUE, 'w')
    blue_w.write("00")
    green_w = open(GREEN, 'w')
    green_w.write("00")
# OFF
    red_w = open(RED, 'w')
    red_w.write("00")
    set_kb = open(SET_KB, 'w')
    set_kb.write("1")
    time.sleep(1)
# ON
    red_w = open(RED, 'w')
    red_w.write("ff")
    set_kb = open(SET_KB, 'w')
    set_kb.write("1")
    time.sleep(1)


def red(cputemp):
    redbase = (cputemp - MID_TEMP) * 10
    rval = "00"
    if redbase <= 255 and redbase > 0:
        rval = hex(redbase)
    elif redbase > 255:
        rval = "ff"
        if debug:
            print("rval: ff")
    return rval


def inc_green(cputemp):
    incgreenbase = (cputemp - MAX_TEMP) * -10
    incgval = "00"
    if incgreenbase <= 255 and incgreenbase > 0:
        incgval = hex(incgreenbase)
    elif incgreenbase > 255:
        incgval = "ff"
    return incgval


def dec_green(cputemp):
    decgreenbase = (cputemp - MIN_TEMP) * 10
    decgval = "00"
    if decgreenbase <= 255 and decgreenbase > 0:
        decgval = hex(decgreenbase)
    return decgval


def blue(cputemp):
    bluebase = (cputemp - MID_TEMP) * -10
    bval = "00"
    if bluebase <= 255 and bluebase > 0:
        bval = hex(bluebase)
    elif bluebase > 255:
        bval = "ff"
    return bval


def main():

    while True:
        cputemp = get_temp()
        try:
            while cputemp > MAX_TEMP:
                over_max_temp()
                cputemp = get_temp()

            if cputemp >= MID_TEMP:
                red_w = open(RED, 'w')
                rval = red(cputemp)
                if debug:
                    print("rval: %s" % rval, cputemp)
                red_w.write(rval)

            elif cputemp <= MID_TEMP:
                red_w = open(RED, 'w')
                if debug:
                    print("rval: 00")
                red_w.write("00")

            if cputemp <= MAX_TEMP:
                green_w = open(GREEN, 'w')
                incgval = inc_green(cputemp)
                if debug:
                    print("incgval: %s" % incgval, cputemp)
                green_w.write(incgval)

            if cputemp >= MIN_TEMP and cputemp <= MID_TEMP:
                green_w = open(GREEN, 'w')
                decgval = dec_green(cputemp)
                if debug:
                    print("decgval %s" % decgval, cputemp)
                green_w.write(decgval)

            if cputemp <= MID_TEMP:
                blue_w = open(BLUE, 'w')
                bval = blue(cputemp)
                if debug:
                    print("bval: %s" % bval, cputemp)
                blue_w.write(bval)

            if cputemp >= MID_TEMP:
                blue_w = open(BLUE, 'w')
                if debug:
                    print("bval: 00")
                blue_w.write("00")
            time.sleep(0.5)
            set_kb = open(SET_KB, 'w')
            set_kb.write("1")

        except KeyboardInterrupt:
            print("Exiting.")
            sys.exit(0)
main()

