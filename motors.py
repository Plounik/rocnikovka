from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import StopWatch, wait


motor_b = Motor(Port.B)
motor_d = Motor(Port.D)
motor_e = Motor(Port.E)
motor_f = Motor(Port.F)


motor_b.control.limits(1500, 4000, 1000)
motor_f.control.limits(1500, 4000, 1000)
motor_d.control.limits(1500, 4000, 1000)


def _go_to_position(motor, target, speed=500, wait_for_finish=True):
    # Choose the equivalent target nearest to the accumulated motor angle.
    target += 360 * ((motor.angle() - target + 180) // 360)
    motor.run_target(
        speed,
        target,
        then=Stop.HOLD,
        wait=wait_for_finish,
    )


def hold():
    _go_to_position(motor_b, 30, 1000, False)
    _go_to_position(motor_f, 30, 1000)
    _go_to_position(motor_b, 30, 1000)


def release():
    motor_d.run_target(1000, 0)


def scan():
    motor_d.run_target(1000, 190)
    motor_d.hold()
    wait(100)

def scan_center():
    motor_d.run_target(1000, 135)
    wait(100)



def setup_up():
    release()



    left_and_right(350)


def left_and_right(angle=14):
    _go_to_position(motor_f, angle, 1000, False)
    _go_to_position(motor_b, angle, 1000)
    _go_to_position(motor_f, angle, 1000)


def turn_up():
    _go_to_position(motor_f, -15, 800, False)
    wait(30)
    motor_b.run(1000)
    wait(170)
    _go_to_position(motor_f, 14, 800, False)
    wait(10)
    _go_to_position(motor_b, 0, 600)
    wait(30)


def turn_down():
    _go_to_position(motor_b, -15, 800, False)
    wait(30)
    motor_f.run(1000)
    wait(170)
    _go_to_position(motor_b, 14, 800, False)
    wait(10)
    _go_to_position(motor_f, 0, 400)
    wait(30)

    


def turn_90():
    _go_to_position(motor_b, 350, 500, False)
    _go_to_position(motor_f, 350)
    motor_e.run_angle(10000, -136, then=Stop.HOLD)
    motor_e.run_angle(10000, 10, then=Stop.HOLD)


def turn_180():
    _go_to_position(motor_b, 350, 500, False)
    _go_to_position(motor_f, 350)
    motor_e.run_angle(10000, 262, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)


def turn_270():
    _go_to_position(motor_b, 350, 500, False)
    _go_to_position(motor_f, 350)
    motor_e.run_angle(10000, 136, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)


def move_90():
    hold()
    motor_e.run_angle(10000, -136, then=Stop.HOLD)
    motor_e.run_angle(10000, 10, then=Stop.HOLD)
    left_and_right(0)


def move_180():
    hold()
    motor_e.run_angle(10000, 262, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)
    left_and_right(0)


def move_270():
    hold()
    motor_e.run_angle(10000, 136, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)
    left_and_right(0)
