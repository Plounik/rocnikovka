from pybricks.ev3devices import Motor
from pybricks.parameters import Port
base_motor = Motor(Port.B)

def r90():
    base_motor.run_angle(1000, 270)
def r270():
    base_motor.run_angle(1000, -270)
def r180():
    base_motor.run_angle(1000, 540)

