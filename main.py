from pybricks.hubs import PrimeHub
from pybricks.pupdevices import (ColorSensor,Motor)
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.tools import StopWatch, wait

hub = PrimeHub()
hub.speaker.volume(100)
hub.speaker.beep(1000, 100)
wait(150)

import motors
import rotations
import turns
import moves
import scan_cube
motors.setup_up()
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

for i in cube:
    cube[i] = scan_cube.faces[cube[i]]

print(cube)

import solve
moves_list = solve.solve(cube)
moves.execute(moves_list)
