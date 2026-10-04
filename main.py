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
import solver
# import files


hub = PrimeHub()
hub.speaker.volume(100)
hub.speaker.beep(1000, 100)
# signal hub is connected


if hub.battery.voltage() < 8000:
    print(f"the battery voltage is {hub.battery.voltage()/1000}V")
# checks battery status


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
    print(cube)
    final_cube = ""
    for i in cube:
        final_cube += str(scan_cube.faces[i])
    print(final_cube)
    return final_cube
# coverting to desired format

def cube_solve(final_cube):
    moves_list = solver.solve(final_cube).split()
    print(moves_list)
    return moves_list
# imputs cube state to solver, get moves list as and output


motors.setup_up()

timer = StopWatch()
scanning_timer = StopWatch()
cube = cube_scan()
final_cube = cube_convert(cube)
scanning_timer.pause()
print(f"The scanning finished in {scanning_timer.time()/1000}s")

solve_timer = StopWatch()
moves_list = cube_solve(final_cube)
print(scan_cube.faces)
solve_timer.pause()
print(f"Calculating the solution took {solve_timer.time()/1000}s")

solving_timer = StopWatch()
moves.execute(moves_list)
solve_timer.pause()
timer.pause()
print(f"Solving the cube finished in {solving_timer.time()/1000}s")

print(f"Executed in {timer.time()/1000}s")