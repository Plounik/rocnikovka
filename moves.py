import rotations
import motors
reference = {"U": "top", "D": "bottom", "F": "front", "B": "back", "R": "right", "L": "left"}


def execute(turns_list):
    for number, i in enumerate(turns_list, 1):
        if i != 0:print("\x1b[1A\r\x1b[2K" * 2, end="")
        print("move", number, "of", len(turns_list))
        print(f"currently performing move {i}")
        original_face = rotations.default_state[reference[str(i[0])]]
        reverse_state = {v: k for k, v in rotations.state.items()}
        current_position = reverse_state[original_face]

        if current_position == "top":
            rotations.move_up()
            rotations.move_up()
        elif current_position == "bottom":
            pass
        elif current_position == "front":
            rotations.move_down()
        elif current_position == "back":
            rotations.move_up()
        elif current_position == "right":
            rotations.move_right()
            rotations.move_up()
        elif current_position == "left":
            rotations.move_left()
            rotations.move_up()

        if i[0] == i[-1]:
            motors.move_270()

        elif i[-1] == "'":
            motors.move_90()

        elif i[-1] == "2":
            motors.move_180()
