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

if hub.charger.connected():
    print(f"the charging current is {hub.charger.current()/1000}A")
# checks charging status


def cube_scan():
    global cube
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
# scanning the cube

def cube_convert():
    print(cube)
    global final_cube
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



motors.setup_up()








# cube_scan()

# cube_convert()

# cube_solve()