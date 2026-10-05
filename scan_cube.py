import motors
from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait


main_sensor = ColorSensor(Port.A)
side_sensor = ColorSensor(Port.C)
faces = {}


def scan(sensor):
    h, s, v = 0, 0, 0
    for i in range(10):
        hsv = sensor.hsv()
        h += hsv[0]
        s += hsv[1]
        v += hsv[2]
    h /= 10
    s /= 10
    v /= 10
    if v < 30:
        if sensor.reflection() < 30:
            return "R"
        else:
            return "W"
    if s < 30:
        return "W"
    if h >= 300 or h < 35:
        return "O"
    if h < 100:
        return "Y"
    if h < 175:
        return "G"
    return "B"
    


def scan_side(face):
    if face == "F" or face == "U":
        order = "836501274"
    else:
        order = "614307852"
    side = ""
    motors.scan_center()
    side += scan(main_sensor)
    faces[side] = face
    motors.scan()
    for i in range(4):
        side += scan(main_sensor)
        side += scan(side_sensor)
        motors.turn_90()
        wait(20)
    side_final = ""
    for i in range(9):
        side_final += side[int(order[i])]
    motors.release()
    return side_final 