import scan_cube
scan_cube.scan()
default_state = {"top":"yellow", "bottom":"white", "front":"green", "back":"blue", "right":"orange", "left":"red"}
state = default_state
def left_turn():
    global state
    state = {
        "top":state.get("top"),
        "bottom":state.get("bottom"),
        "front":state.get("right"),
        "back":state.get("left"),
        "right":state.get("back"),
        "left":state.get("front")
        }

def right_turn():
    global state
    state = {
        "top":state.get("top"),
        "bottom":state.get("bottom"),
        "front":state.get("left"),
        "back":state.get("right"),
        "right":state.get("front"),
        "left":state.get("back")
        }

def up_turn():
    global state
    state = {
        "top":state.get("front"),
        "bottom":state.get("back"),
        "front":state.get("bottom"),
        "back":state.get("top"),
        "right":state.get("right"),
        "left":state.get("left")
        }

def down_turn():
    global state
    state = {
        "top":state.get("back"),
        "bottom":state.get("front"),
        "front":state.get("top"),
        "back":state.get("bottom"),
        "right":state.get("right"),
        "left":state.get("left")
        }
