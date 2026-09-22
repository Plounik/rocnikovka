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
cube += scan_cube.scan_side()
turns.execute("right","up")
cube += scan_cube.scan_side()
turns.execute("down","left","up")
cube += scan_cube.scan_side()
turns.execute("up")
cube += scan_cube.scan_side()
turns.execute("left","down")
cube += scan_cube.scan_side()
turns.execute("up","left","down")
cube += scan_cube.scan_side()
turns.execute("down","left","left")



import solve
moves_list = solve.solve(cube)
moves.execute(moves_list)
