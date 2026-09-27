import motors
from pybricks.parameters import Port
from pybricks.pupdevices import (ColorSensor,Motor)
from pybricks.tools import wait


main_sensor = ColorSensor(Port.A)
side_sensor = ColorSensor(Port.C)
faces = {}


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
    if h > 300 or h < 25:
        if s < 30:
            return "W"
        else:
            return "O"
    elif h > 25 and h < 100:
        return "Y"
    elif h > 100 and h < 175:
        return "G"
    else:
        if s < 30:
            return "R"
        else:
            return 
    
    
    

def scan_side(face):
    order = "476501238"
    side = ""
    motors.scan_center()
    side += scan(main_sensor)
    if side == "Y":
        global yellow_face
        yellow_face = face
    faces[face] = side
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
