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
import turns
import moves
import time

ev3 = EV3Brick()
sensor_motor = Motor(Port.C)



for i in range(5):
    moves.execute(
    [
        "R", "U2", "F'", "L", "D", "B2", "R'", "U",
        "F2", "D'", "L2", "B", "U'", "R2", "F",

        "F'", "R2", "U", "B'", "L2", "D", "F2", "U'",
        "R", "B2", "D'", "L'", "F", "U2", "R'"
    ]
    )
    ev3.speaker.beep(500, 3000)
    time.sleep(10)

