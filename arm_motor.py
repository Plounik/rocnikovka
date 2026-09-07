from pybricks.ev3devices import Motor
from pybricks.parameters import Port
import time
arm_motor = Motor(Port.A)

def hold():
    arm_motor.run_target(3000, 100)
def turn():
    arm_motor.run_target(1000, 205)
    arm_motor.run_target(1000, 0)
def release():
    arm_motor.run_target(3000, 0)
