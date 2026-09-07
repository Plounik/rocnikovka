import rotations
reference = {"u": "top", "d": "bottom", "f": "front", "b": "back", "r": "right", "l": "left"}
 

def execute(turns_list, base_motor=None):
    for i in turns_list:
        original_color = rotations.default_state[reference[str(i[0]).lower()]]
        reverse_state = {v: k for k, v in rotations.state.items()}
        current_position = reverse_state[original_color]

        if current_position == "top":
            rotations.up_turn()
            rotations.up_turn()
        elif current_position == "bottom":
            pass
        elif current_position == "front":
            rotations.down_turn()
        elif current_position == "back":
            rotations.up_turn()
        elif current_position == "right":
            rotations.left_turn()
            rotations.down_turn()
        elif current_position == "left":
            rotations.right_turn()
            rotations.down_turn()

        if i[0] == i[0].upper():
            # rotate 180
            pass
        elif i[-1] != "'":
            # rotate 90
            pass
        elif i[-1] == "'":
            if base_motor is None:
                raise ValueError("base_motor is required for inverse turns")
            base_motor.run_angle(500, 270)
            pass
