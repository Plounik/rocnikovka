from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
import time

color_sensor = ColorSensor(Port.S2)
sensor_motor = Motor(Port.C)

colors = []
def color_detect(red):
    r = 0
    g = 0
    b = 0 
    for i in range(10):
        time.sleep(0.05)
        r += color_sensor.rgb()[0]
        g += color_sensor.rgb()[1]
        b += color_sensor.rgb()[2]
    color_rgb = [r/10, g/10, b/10]
    if color_rgb[2] >= 40:
        colors.append("W")
    elif color_rgb[0]<= 10:
        if color_rgb[0] + color_rgb[1]<= 18:
            colors.append("B")
        else:
            colors.append("G")
    elif color_rgb[0] <= 26.5 and red:
        colors.append("R")
    elif color_rgb[0] <= 23:
        colors.append("R")
    elif color_rgb[0] + color_rgb[1] + color_rgb[2]<= 65:
        colors.append("O")  
    else:
        colors.append("Y")



def initialize():
    sensor_motor.run_until_stalled(300)
    sensor_motor.reset_angle(0)
    sensor_motor.run_target(500, -360)
    sensor_motor.reset_angle(0)



def default():
    sensor_motor.run_target(500, 0)
def scan_position_center():
    sensor_motor.run_target(500, -395)
    color_detect(False)


def scan_position_edge():
    if sensor_motor.angle() <= -245:
        sensor_motor.run_target(200, -250)
    else:
        sensor_motor.run_target(200, -275)
    color_detect(False)

def scan_position_corner():
    sensor_motor.run_target(200, -195)
    color_detect(True)



        # r = 0
    # g = 0
    # b = 0 
    # for i in range(100):
    #     time.sleep(0.1)
    #     r += color_sensor.rgb()[0]
    #     g += color_sensor.rgb()[1]
    #     b += color_sensor.rgb()[2]
    # print(r/100, g/100, b/100)

