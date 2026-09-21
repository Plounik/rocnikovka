import motors
default_state = {"top":"yellow", "bottom":"white", "front":"green", "back":"blue", "right":"orange", "left":"red"}
state = default_state
def move_left():
    global state
    state = {
        "top":state["top"],
        "bottom":state["bottom"],
        "front":state["right"],
        "back":state["left"],
        "right":state["back"],
        "left":state["front"]
        }
    motors.turn_90()

def move_right():
    global state
    state = {
        "top":state["top"],
        "bottom":state["bottom"],
        "front":state["left"],
        "back":state["right"],
        "right":state["front"],
        "left":state["back"]
        }
    motors.turn_270()
def move_up():
    global state
    state = {
        "top":state["front"],
        "bottom":state["back"],
        "front":state["bottom"],
        "back":state["top"],
        "right":state["right"],
        "left":state["left"]
        }
    motors.turn_up()

def move_down():
    global state
    state = {
        "top":state["back"],
        "bottom":state["front"],
        "front":state["top"],
        "back":state["bottom"],
        "right":state["right"],
        "left":state["left"]
        }
    motors.turn_down()
