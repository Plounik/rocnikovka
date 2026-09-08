import rotations
import base_motor
import arm_motor
reference = {"U": "top", "D": "bottom", "F": "front", "B": "back", "R": "right", "L": "left"}
 

def execute(turns_list, turn):
    for i in turns_list:
        original_color = rotations.default_state[reference[str(i[0])]]
        reverse_state = {v: k for k, v in rotations.state.items()}
        current_position = reverse_state[original_color]

        if current_position == "top":
            rotations.down_turn()
            rotations.down_turn()
        elif current_position == "bottom":
            pass
        elif current_position == "front":
            rotations.down_turn()
        elif current_position == "back":
            rotations.left_turn()
            rotations.left_turn()
            rotations.down_turn()
        elif current_position == "right":
            rotations.left_turn()
            rotations.down_turn()
        elif current_position == "left":
            rotations.right_turn()
            rotations.down_turn()
        if turn:
            arm_motor.hold()
            if i[-1] == i[0]:
                base_motor.r90()
            elif i[-1] == "'":
                base_motor.r270()
            elif i[-1] == "2":
                base_motor.r180()
            arm_motor.release()
