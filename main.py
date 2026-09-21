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

motors.setup_up()
moves.execute(["U", "D2", "F", "L'"])
