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
import solve
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
    index_W = (face_order.index(scan_cube.yellow_face) + 3) % 6
    index_R = (face_order.index(scan_cube.orange_face) + 3) % 6
    scan_cube.faces["W"] = face_order[index_W]
    scan_cube.faces["R"] = face_order[index_R]
    position = (index_W * 9) + 4
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
    turns.execute(["down","180"])
    print(cube)
    return cube
# scanning the cube

def cube_convert(cube):
    cube = convert_white(cube)
    print(cube)
    final_cube = ""
    for i in cube:
        final_cube += str(scan_cube.faces[i])
    print(final_cube)
    return final_cube
# coverting to desired format

def cube_solve(final_cube):
    moves_list = solve.solve(final_cube)
    print(moves_list)
    return moves_list
# imputs cube state to solver, get moves list as and output



for attempt in range(3):
    motors.setup_up()
    rotations.state = rotations.default_state.copy()
    scan_cube.faces.clear()
    scan_cube.scan_readings.clear()
    scan_cube.yellow_face = None
    scan_cube.orange_face = None
    print("scan", attempt + 1, "of 3")
    try:
        cube = cube_scan()
        if len(cube) != 54 or any(cube.count(color) != 9 for color in "WYROGB"):
            raise ValueError("wrong number of stickers")
        final_cube = cube_convert(cube)
        moves_list = cube_solve(final_cube)
        break
    except (ValueError, KeyError, AttributeError) as error:
        print("scan failed:", error)
        print("scan HSV readings:", scan_cube.scan_readings)
else:
    raise RuntimeError("cube scan failed three times")

print(scan_cube.faces)
moves.execute(moves_list)


