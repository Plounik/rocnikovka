from pybricks.hubs import PrimeHub
from pybricks.tools import StopWatch
# import pybrics

import motors
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
    turns.execute(["up"])
    cube += scan_cube.scan_side("F")
    turns.execute(["left","up"])
    cube += scan_cube.scan_side("R")
    turns.execute(["up"])
    cube += scan_cube.scan_side("B")
    turns.execute(["up"])
    cube += scan_cube.scan_side("L")
    turns.execute(["right","up"])
    cube += scan_cube.scan_side("D")
    turns.execute(["down","180"])
    return cube
# scanning the cube

def cube_convert(cube):
    f_cube = ""
    for i in cube:
        f_cube += str(scan_cube.faces[i])
    source = list(f_cube)
    final_cube = source[:] 

    final_cube[9:18] = source[18:27]
    final_cube[18:27] = source[9:18]
    final_cube[27:36] = source[45:54]
    final_cube[45:54] = source[27:36]

    final_cube = "".join(final_cube)
    return final_cube
# coverting to desired format

def cube_solve(final_cube):
    global moves_list
    moves_list = solver.solve(final_cube).split()
    return moves_list
# imputs cube state to solver, get moves list as and output

def scan():
    global cube
    print("Scanning...")
    scanning_timer = StopWatch()
    cube = cube_scan()
    final_cube = cube_convert(cube)
    scanning_timer.pause()
    print("\x1b[1A\r\x1b[2K", end="")
    print(f"The scanning finished in {scanning_timer.time()/1000}s")
    return final_cube
# scans and converts the cube to desired format

def calculate(final_cube):
    print("Calculating...")
    calculate_timer = StopWatch()
    moves_list = cube_solve(final_cube)
    calculate_timer.pause()
    print("\x1b[1A\r\x1b[2K", end="")
    print(f"Calculating the solution took {calculate_timer.time()/1000}s")
    return moves_list
# gives the position to solver, returns moves list

def solve(moves_list):
    print("Solving...")
    solving_timer = StopWatch()
    moves.execute(moves_list)
    solving_timer.pause()
    print("\x1b[1A\r\x1b[2K", end="")
    print(f"Solving the cube finished in {solving_timer.time()/1000}s")
# executing moves_list



motors.setup_up()

timer = StopWatch()

final_cube = scan()
moves_list = calculate(final_cube)
solve(moves_list)

timer.pause()

print(f"Executed in {timer.time()/1000}s\n\n")
print(cube)
print(moves_list)