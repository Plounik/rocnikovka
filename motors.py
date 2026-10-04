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
# motor_e.control.target_tolerances(50, 5)


def _go_to_position(motor, target, speed=500, wait_for_finish=True):
    # Choose the equivalent target nearest to the accumulated motor angle.
    target += 360 * ((motor.angle() - target + 180) // 360)
    motor.run_target(
        speed,
        target,
        then=Stop.HOLD,
        wait=wait_for_finish,
    )


def base_motor(angle, target_angle):
    angle += target_angle
    motor_e.run_target(1000, angle + 5)
    motor_e.run_target(1000, angle, Stop.HOLD)
    return angle

def hold():
    _go_to_position(motor_b, 30, 1000, False)
    _go_to_position(motor_f, 30, 1000)
    _go_to_position(motor_b, 30, 1000)


def release():
    if (motor_d.angle()%360) > 175 and (motor_d.angle()%360) < 280:
        motor_d.run_angle(1000, -165)
        motor_d.reset_angle(motor_d.angle()%360)
        motor_d.run_target(1000, 0, wait=False)
    else:
        motor_d.run_target(1000, 0)


def scan():
    motor_d.run_target(1000, 195)
    motor_d.hold()
    wait(100)

def scan_center():
    motor_d.run_target(1000, 135)
    wait(100)



def setup_up():
    release()
    motor_e.run_target(400, 0)
    global current_angle
    current_angle = 0
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
    global current_angle
    _go_to_position(motor_b, 350, 500, False)
    _go_to_position(motor_f, 350)
    current_angle = base_motor(current_angle, 90)


def turn_180():
    global current_angle
    _go_to_position(motor_b, 350, 500, False)
    _go_to_position(motor_f, 350)
    current_angle = base_motor(current_angle, 180)


def turn_270():
    global current_angle
    _go_to_position(motor_b, 350, 500, False)
    _go_to_position(motor_f, 350)
    current_angle = base_motor(current_angle, -90)


def move_90():
    global current_angle
    hold()
    current_angle = base_motor(current_angle, 90)
    left_and_right(0)


def move_180():
    global current_angle
    hold()
    current_angle = base_motor(current_angle, 180)
    left_and_right(0)


def move_270():
    global current_angle
    hold()
    current_angle = base_motor(current_angle, -90)
    left_and_right(0)
