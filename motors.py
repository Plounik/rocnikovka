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
        10000,
        delta,
        then=Stop.HOLD,
        wait=wait_for_finish,
    )


def _wait_until_done(motor):
    while not motor.done():
        wait(1)


def left_arm(angle, wait_for_finish=True):
    current = _absolute_angle(motor_b)
    if round((current-10) / 20) * 20 == angle - 10:
        direction = "shortest"
    elif angle - 60 > current:
        direction = "clockwise"
    else:
        direction = "counterclockwise"

    _go_to_position(motor_b, angle, direction, wait_for_finish)


def right_arm(angle, wait_for_finish=True):
    current = _absolute_angle(motor_f)

    if round((current-10) / 20) * 20 == angle - 10:
        direction = "shortest"
    elif angle - 60 > current:
        direction = "clockwise"
    else:
        direction = "counterclockwise"

    _go_to_position(motor_f, angle, direction, wait_for_finish)


def hold():
    _go_to_position(motor_b, 325, "clockwise", False)
    _go_to_position(motor_f, 350, "clockwise", True)
    _wait_until_done(motor_b)


def release():
    _go_to_position(motor_d, 100, "shortest")
    _go_to_position(motor_d, 0, "counterclockwise")


def scan():
    _go_to_position(motor_d, 100, "shortest")
    _go_to_position(motor_d, 190, "clockwise")


def setup_up():
    release()

    current_e = _absolute_angle(motor_e)
    target_e = round(current_e / 90) * 90 - 5
    _go_to_position(motor_e, target_e, "shortest")

    current_f = _absolute_angle(motor_f)
    direction_f = "counterclockwise" if 270 < current_f else "shortest"
    _go_to_position(motor_f, 90, direction_f, False)

    current_b = _absolute_angle(motor_b)
    direction_b = "counterclockwise" if 170 < current_b else "shortest"
    _go_to_position(motor_b, 90, direction_b, True)

    _wait_until_done(motor_f)


def left_and_right(angle):
    right_arm(angle, False)
    left_arm(angle, True)
    _wait_until_done(motor_f)


def turn_up():
    left_and_right(90)
    motor_b.run_angle(2000, 180, then=Stop.HOLD)
    motor_b.run_angle(350, 180, then=Stop.HOLD)
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
    left_and_right(90)


def move_180():
    hold()
    motor_e.run_angle(10000, 550, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)
    left_and_right(90)


def move_270():
    hold()
    motor_e.run_angle(10000, 280, then=Stop.HOLD)
    motor_e.run_angle(10000, -10, then=Stop.HOLD)
    left_and_right(90)
