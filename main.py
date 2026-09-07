#!/usr/bin/env pybricks-micropython

import rotations
import turns
import moves
import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

ev3 = EV3Brick()
base_motor = Motor(Port.B)
arm_motor = Motor(Port.A)
sensor_motor = Motor(Port.C)


base_motor.run_angle(500, 360)
time.sleep(1)
print(rotations.state)
moves.execute(["r'", "u", "l", "u'"])
print(rotations.state)
