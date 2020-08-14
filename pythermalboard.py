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
            f=open(red, 'w')
            f.write(rval)
        elif redbase > 255:
            f=open(red, 'w')
            f.write("ff")

    if int(temp) <= 95:
        incgreenbase = (int(temp) - 95) * -10
        if incgreenbase <= 255:
            incgval = hex(incgreenbase)
            f=open(green, 'w')
            f.write(incgval)
        elif incgreenbase > 255:
            f=open(green, 'w')
            f.write("ff")

    if int(temp) >= 20 and int(temp) <= 50:
        decgreenbase = (int(temp) - 20) * 10
        if decgreenbase <= 255:
            decgval = hex(decgreenbase)
            f=open(green, 'w')
            f.write(decgval)

    if int(temp) <= 50:
        bluebase = (int(temp) - 50) * -10
        if bluebase <= 255:
            bval = hex(bluebase)
            f=open(blue, 'w')
            f.write(bval)
        elif bluebase > 255:
            f=open(blue, 'w')
            f.write("ff")
    f=open("/sys/devices/platform/faustus/kbbl/kbbl_set", 'w')
    f.write("1")
    time.sleep(0.5)


