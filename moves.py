import rotations
import motors
reference = {"U": "top", "D": "bottom", "F": "front", "B": "back", "R": "right", "L": "left"}
 

def execute(turns_list):
    for i in turns_list:
        original_color = rotations.default_state[reference[str(i[0])]]
        reverse_state = {v: k for k, v in rotations.state.items()}
        current_position = reverse_state[original_color]

        if current_position == "top":
            rotations.move_up()
            rotations.move_up()
        elif current_position == "bottom":
            pass
        elif current_position == "front":
            rotations.move_180()
            rotations.move_up()
        elif current_position == "back":
            rotations.move_up()
        elif current_position == "right":
            rotations.move_right()
            rotations.move_up()
        elif current_position == "left":
            rotations.move_left()
            rotations.move_up()

        if i[0] == i[-1]:
            motors.move_90()

        elif i[-1] == "'":
            motors.move_270()

        elif i[-1] == "2":
            motors.move_180()
