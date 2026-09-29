import motors
from pybricks.parameters import Port
from pybricks.pupdevices import (ColorSensor,Motor)
from pybricks.tools import wait


main_sensor = ColorSensor(Port.A)
side_sensor = ColorSensor(Port.C)
faces = {}
scan_readings = []


def check_face():
    motors.scan()
    h1, s1, v1 = 0, 0, 0
    for i in range(10):
        h, s, v = main_sensor.hsv()
        h1 += h
        s1 += s
        v1 += v
    print(h1/10, s1/10, v1/10)

def scan(sensor):
    wait(200)
    h, s, v = 0, 0, 0
    for i in range(10):
        hsv = sensor.hsv()
        h += hsv[0]
        s += hsv[1]
        v += hsv[2]
    h /= 10
    s /= 10
    v /= 10
    scan_readings.append((h, s, v))
    if v < 30:
        return "R"
    if s < 30:
        return "W"
    if h >= 300 or h < 35:
        return "O"
    if h < 100:
        return "Y"
    if h < 175:
        return "G"
    return "B"
    
    
    

def scan_center_fast():
    motors.scan_center_fast()
    h, s, v = 0, 0, 0
    for i in range(5):
        hsv = main_sensor.hsv()
        h += hsv[0]
        s += hsv[1]
        v += hsv[2]
    h /= 5
    s /= 5
    v /= 5
    scan_readings.append((h, s, v))
    motors.release_fast()
    if v < 30:
        return "R"
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
    order = "836501274"
    side = ""
    motors.scan_center()
    side += scan(main_sensor)
    if side == "Y":
        global yellow_face
        yellow_face = face
    elif side == "O":
        global orange_face
        orange_face = face
    faces[side] = face
    motors.scan()
    print(face, main_sensor.hsv())
    for i in range(4):
        side += scan(main_sensor)
        side += scan(side_sensor)
        motors.turn_90()
    side_final = ""
    for i in range(9):
        side_final += side[int(order[i])]
    motors.release()
    return side_final 
