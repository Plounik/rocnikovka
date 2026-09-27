from pybricks.hubs import PrimeHub
from pybricks.pupdevices import (ColorSensor,Motor)
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.tools import StopWatch, wait
# import pybrics

import motors
import rotations
import turns
import moves
import scan_cube
# import files



hub = PrimeHub()
hub.speaker.volume(100)
hub.speaker.beep(1000, 100)
# signal hub is connected



if hub.battery.voltage() < 8000:
    print(f"the battery voltage is {hub.battery.voltage()/1000}V")
# checks battery status



def convert_white(cube):
    face_order = ["U", "R", "F", "D", "L", "B"]
    position = ((face_order.index(scan_cube.yellow_face)+3)%6 * 9) + 4
    cube = cube[:position] + "W" + cube[position+1:]
    return cube
# converts white center


def cube_scan():
    cube = ""
    cube += scan_cube.scan_side("U")
    turns.execute(["left","up"])
    cube += scan_cube.scan_side("R")
    turns.execute(["down","right","up"])
    cube += scan_cube.scan_side("F")
    turns.execute(["up"])
    cube += scan_cube.scan_side("D")
    turns.execute(["left","down"])
    cube += scan_cube.scan_side("L")
    turns.execute(["up","left","down"])
    cube += scan_cube.scan_side("B")
    turns.execute(["down","left","left"])
    print(cube)
    return cube
# scanning the cube

def cube_convert(cube):
    cube = convert_white(cube)
    print(cube)
    final_cube = ""
    for i in cube:
        final_cube += scan_cube.faces[i]
    print(final_cube)
# coverting to desired format

def cube_solve():
    import solve
    moves_list = solve.solve(final_cube)
    moves.execute(moves_list)
# imputs cube state to solver, get moves list as and output

# motors.scan()
# h1, s1, v1 = 0, 0, 0
# for i in range(10):
#     h, s, v = scan_cube.main_sensor.hsv()
#     h1 += h
#     s1 += s
#     v1 += v
# print(h1/10, s1/10, v1/10)

motors.setup_up()
cube = cube_scan()
print(scan_cube.faces)


final_cube = cube_convert(cube)

cube_solve(final_cube)


