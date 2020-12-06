#!/usr/bin/python3
import os
import time
import sys

colors = {
"RED":"/sys/devices/platform/faustus/kbbl/kbbl_red",
"GREEN":"/sys/devices/platform/faustus/kbbl/kbbl_green",
"BLUE":"/sys/devices/platform/faustus/kbbl/kbbl_blue"}

MAX_TEMP = 95
MIN_TEMP = 20
MID_TEMP = 50

BR_MULT = 10

KB_FLAGS = open("/sys/devices/platform/faustus/kbbl/kbbl_flags", 'w')
KB_FLAGS.write("2a")
KB_FLAGS.close()

SET_KB = "/sys/devices/platform/faustus/kbbl/kbbl_set"

with open("/sys/devices/platform/faustus/kbbl/kbbl_mode", 'w') as KB_MODE:
    KB_MODE_R = open("/sys/devices/platform/faustus/kbbl/kbbl_mode", 'r')
    if KB_MODE_R.read() != "00":
        KB_MODE.write("00")

debug = True

def current_config():
    prev_config = []
    for color in colors:
        prev_config.append(open(colors[color], 'r').read().strip('\n'))
    return prev_config

def restore_config(prev_config):
    _c = 0
    for color in colors:
        with open(colors[color], 'w') as prev_color:
            prev_color.write(prev_config[_c])
        _c += 1
    with open(SET_KB, 'w') as set_kb:
        set_kb.write("1")

def get_temp():
    CPU_TEMP = open("/sys/class/thermal/thermal_zone0/temp", 'r').read().splitlines()[0]
    cputemp = int(CPU_TEMP[:2])
    return cputemp


def over_max_temp():
# reset KB B and G color
    for color in colors:
        with open(colors[color], 'w') as color_w:
            color_w.write("00")
    with open(SET_KB, 'w') as set_kb:
        set_kb.write("1")
    time.sleep(1)
# ON
    with open(colors["RED"], 'w') as red_w:
        red_w.write("ff")
    with open(SET_KB, 'w') as set_kb:
        set_kb.write("1")
    time.sleep(1)


def red(cputemp):
    redbase = (cputemp - MID_TEMP) * BR_MULT
    if redbase <= 255 and redbase >= 0:
        rval = hex(redbase)
    elif redbase > 255:
        rval = "ff"
    else:
        rval = "00"
    return rval


def inc_green(cputemp):
    incgreenbase = (cputemp - MAX_TEMP) * -BR_MULT
    if incgreenbase <= 255 and incgreenbase >= 0:
        incgval = hex(incgreenbase)
    elif incgreenbase > 255:
        incgval = "ff"
    else:
        incgval = "00"
    return incgval


def dec_green(cputemp):
    decgreenbase = (cputemp - MIN_TEMP) * BR_MULT
    if decgreenbase <= 255 and decgreenbase >= 0:
        decgval = hex(decgreenbase)
    else:
        decgval = "ff"
    return decgval


def blue(cputemp):
    bluebase = (cputemp - MID_TEMP) * -BR_MULT
    if bluebase <= 255 and bluebase >= 0:
        bval = hex(bluebase)
    elif bluebase > 255:
        bval = "ff"
    else:
        bval = "00"
    return bval


def main():

    prev_config = current_config()

    while True:
        cputemp = get_temp()
        try:
            while cputemp > MAX_TEMP:
                over_max_temp()
                cputemp = get_temp()

            if cputemp >= MID_TEMP:
                with open(colors["RED"], 'w') as red_w:
                    rval = red(cputemp)
                    if debug:
                        print("rval: %s" % rval, cputemp)
                    red_w.write(rval)

            elif cputemp <= MID_TEMP:
                with open(colors["RED"], 'w') as red_w:
                    if debug:
                        print("rval: 00")
                    red_w.write("00")

            if cputemp >= MID_TEMP and cputemp <= MAX_TEMP:
                with open(colors["GREEN"], 'w') as green_w:
                    incgval = inc_green(cputemp)
                    if debug:
                        print("incgval: %s" % incgval, cputemp)
                    green_w.write(incgval)

            elif cputemp <= MIN_TEMP:
                with open(colors[GREEN], 'w') as green_w:
                    if debug:
                        print("incgval: 00")
                    green_w.write("00")

            if cputemp >= MIN_TEMP and cputemp <= MID_TEMP:
                with open(colors["GREEN"], 'w') as green_w:
                    decgval = dec_green(cputemp)
                    if debug:
                        print("decgval %s" % decgval, cputemp)
                    green_w.write(decgval)

            if cputemp <= MID_TEMP:
                with open(colors["BLUE"], 'w') as blue_w:
                    bval = blue(cputemp)
                    if debug:
                        print("bval: %s" % bval, cputemp)
                    blue_w.write(bval)

            if cputemp >= MID_TEMP:
                with open(colors["BLUE"], 'w') as blue_w:
                    if debug:
                        print("bval: 00")
                    blue_w.write("00")
            with open(SET_KB, 'w') as set_kb:
                set_kb.write("1")
            time.sleep(0.5)

        except KeyboardInterrupt:
            restore_config(prev_config)
            print("Exiting.")
            sys.exit(0)
main()

