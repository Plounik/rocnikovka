import motors
from pybricks.parameters import Port
from pybricks.pupdevices import (ColorSensor,Motor)

main_sensor = ColorSensor(Port.A)
side_sensor = ColorSensor(Port.C)
faces = {}

def scan(sensor):
    if sensor == "main":
        hsv = main_sensor.hsv()
    else:
        hsv = side_sensor.hsv()
    print(hsv)
    
    return "f"



def scan_side(face):
    order = "476501238"
    side = ""
    motors.scan_center()
    side += scan("main")
    faces[side] = face
    motors.scan()
    for i in range(4):
        side += scan("main")
        side += scan("side")
        motors.turn_90()
    side_final = ""
    for i in range(9):
        side_final += side[int(order[i])]
    motors.release()
    return side_final 