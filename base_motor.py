from pybricks.ev3devices import Motor
from pybricks.parameters import Port
base_motor = Motor(Port.B)

def r90():
    base_motor.run_angle(1000, 270)
    base_motor.hold()
    
def r270():
    base_motor.run_angle(1000, -270)
    base_motor.hold()
    
def r180():
    base_motor.run_angle(1000, 540)
    base_motor.hold()
    
def r45():
    base_motor.run_angle(1000, -135)
    base_motor.hold()
def fix():
    base_motor.run_target(1000, -540)
    base_motor.reset_angle(0)
