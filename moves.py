import rotations
reference = {"u": "top", "d": "bottom", "f": "front", "b": "back", "r": "right", "l": "left"}
 

def execute(turns_list):
    for i in turns_list:
        original_color = rotations.default_state[reference[str(i[0]).lower()]]
        reverse_state = {v: k for k, v in rotations.state.items()}
        current_position = reverse_state[original_color]

        match current_position:
            case "top":
                rotations.up_turn()
                rotations.up_turn()
            case "bottom":
                pass
            case "front":
                rotations.down_turn()
            case "back":
                rotations.up_turn()
            case "right":
                rotations.left_turn()
                rotations.down_turn()
            case "left":
                rotations.right_turn()
                rotations.down_turn()

        if i[0] == i[0].upper():
            # rotate 180
            pass
        elif i[-1] != "'":
            # rotate 90
            pass
        elif i[-1] == "'":
            # rotate -90
            pass