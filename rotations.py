def left_turn(state):
    new_state = {
        "up":"yellow", 
        "front":state.get("right"), 
        "right":state.get("back"), 
        "left":state.get("front"), 
        "back":state.get("left"), 
        "bottom":"white"
        }
    return new_state
def right_turn(state):
    new_state = {
        "up":"yellow", 
        "front":state.get("left"), 
        "right":state.get("front"), 
        "left":state.get("back"), 
        "back":state.get("right"), 
        "bottom":"white"
        }
    return new_state