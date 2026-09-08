import sensor_motor
import base_motor
import arm_motor
default_state = {"top":"yellow", "bottom":"white", "front":"green", "back":"blue", "right":"orange", "left":"red"}
state = default_state
def left_turn():
    global state
    state = {
        "top":state["top"],
        "bottom":state["bottom"],
        "front":state["right"],
        "back":state["left"],
        "right":state["back"],
        "left":state["front"]
        }
    base_motor.r90()


def right_turn():
    global state
    state = {
        "top":state["top"],
        "bottom":state["bottom"],
        "front":state["left"],
        "back":state["right"],
        "right":state["front"],
        "left":state["back"]
        }
    base_motor.r270()

def up_turn():
    global state
    state = {
        "top":state["front"],
        "bottom":state["back"],
        "front":state["bottom"],
        "back":state["top"],
        "right":state["right"],
        "left":state["left"]
        }

def down_turn():
    global state
    state = {
        "top":state["back"],
        "bottom":state["front"],
        "front":state["top"],
        "back":state["bottom"],
        "right":state["right"],
        "left":state["left"]
        }
    arm_motor.turn()
