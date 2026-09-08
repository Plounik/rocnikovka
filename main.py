#!/usr/bin/pybricks-micropython
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import arm_motor
import base_motor
import rotations
import sensor_motor
import turns
import moves
import time

ev3 = EV3Brick()
sensor_motor.initialize()
# arm_motor.initialize()
# sensor_motor.scan_position_edge()
# sensor_motor.scan_position_corner()
# sensor_motor.color_detect()
def scan_side():
    sensor_motor.scan_position_center()
    base_motor.base_motor.reset_angle(0)
    for _ in range(4):
        sensor_motor.scan_position_edge()
        base_motor.r45()
        sensor_motor.scan_position_corner()
        base_motor.r45()
        if _ % 2 == 1:
            base_motor.fix()
    sensor_motor.default()
def scan_cube():
    sides_to_scan = ["D", "B", "L", "F", "R", "U"]
    for i in sides_to_scan:
        moves.execute(i, False)
        scan_side()
        print(sensor_motor.colors)
        sensor_motor.colors = []


scan_cube()
time.sleep(1)
print(sensor_motor.colors)
print(base_motor.base_motor.angle())
# sensor_motor.scan_position_center()
# time.sleep(1)
# sensor_motor.scan_position_edge()
# time.sleep(2)
# base_motor.r45()
# sensor_motor.scan_position_corner()
# time.sleep(1)
# base_motor.r45()
# time.sleep(1)
# sensor_motor.scan_position_edge()
# time.sleep(2)
# sensor_motor.default()
# print(sensor_motor.colors)









# for i in range(5):
#     moves.execute(
#     [
#         "R", "U2", "F'", "L", "D", "B2", "R'", "U",
#         "F2", "D'", "L2", "B", "U'", "R2", "F",

#         "F'", "R2", "U", "B'", "L2", "D", "F2", "U'",
#         "R", "B2", "D'", "L'", "F", "U2", "R'"
#     ]
#     )
#     ev3.speaker.beep(500, 3000)
#     time.sleep(10)

