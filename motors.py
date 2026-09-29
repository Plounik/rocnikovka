from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait


motor_b = Motor(Port.B)
motor_d = Motor(Port.D)
motor_e = Motor(Port.E)
motor_f = Motor(Port.F)
motor_b.control.limits(1000, 4000, 400)
motor_f.control.limits(1000, 4000, 400)
def _absolute_angle(motor):
    return motor.angle() % 360


def _target_delta(motor, target, direction="shortest"):
    current = _absolute_angle(motor)
    target %= 360

    if direction == "clockwise":
        return (target - current) % 360

    if direction == "counterclockwise":
        return -((current - target) % 360)

    return (target - current + 180) % 360 - 180


def _go_to_position(motor, target, direction="shortest", wait_for_finish=True):
    delta = _target_delta(motor, target, direction)
    motor.run_angle(
        500,
        delta,
        then=Stop.HOLD,
        wait=wait_for_finish,
    )


def _wait_until_done(motor):
    while not motor.done():
        wait(1)


def hold():
    _go_to_position(motor_b, 315, "clockwise", False)
    _go_to_position(motor_f, 315, "clockwise", True)
    _wait_until_done(motor_b)


def release():
    _go_to_position(motor_d, 100, "shortest")
    _go_to_position(motor_d, 0, "counterclockwise")


def scan():
    _go_to_position(motor_d, 100, "shortest")
    _go_to_position(motor_d, 185, "clockwise")
    motor_d.hold()
    wait(300)

def scan_center():
    _go_to_position(motor_d, 135, "shortest")
    wait(300)


def scan_center_fast():
    motor_d.run_angle(10000, _target_delta(motor_d, 135), then=Stop.HOLD)


def release_fast():
    motor_d.run_angle(10000, _target_delta(motor_d, 0), then=Stop.HOLD)


def setup_up():
    release()

    current_e = _absolute_angle(motor_e)
    target_e = round(current_e / 90) * 90 - 5
    _go_to_position(motor_e, target_e, "shortest")

    _go_to_position(motor_f, 150, "shortest", False)

    _go_to_position(motor_b, 150, "shortest", True)

    _wait_until_done(motor_f)


def left_and_right(angle):
    _go_to_position(motor_f, angle, "shortest", False)
    _go_to_position(motor_b, angle, "shortest", True)
    _wait_until_done(motor_f)


def turn_up():
    left_and_right(150)
    _go_to_position(motor_b, 35, "clockwise", True)
    _go_to_position(motor_f, 330, "clockwise", True)
    left_and_right(150)
    wait(300)


def turn_down():
    left_and_right(150)
    _go_to_position(motor_f, 35, "clockwise", True)
    _go_to_position(motor_b, 330, "clockwise", True)
    left_and_right(150)
    wait(300)


def turn_90():
    motor_e.run_angle(10000, -280, then=Stop.HOLD)
    motor_e.run_angle(10000, 10, then=Stop.HOLD)


def turn_180():
    motor_e.run_angle(10000, 550, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)


def turn_270():
    motor_e.run_angle(10000, 280, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)


def move_90():
    hold()
    motor_e.run_angle(10000, -280, then=Stop.HOLD)
    motor_e.run_angle(10000, 10, then=Stop.HOLD)
    left_and_right(150)


def move_180():
    hold()
    motor_e.run_angle(10000, 550, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)
    left_and_right(150)


def move_270():
    hold()
    motor_e.run_angle(10000, 280, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)
    left_and_right(150)
