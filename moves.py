import rotations
import motors
import scan_cube
reference = {"U": "top", "D": "bottom", "F": "front", "B": "back", "R": "right", "L": "left"}
 

def same_center(color, expected):
    return color == expected or (color in ("R", "W") and expected in ("R", "W"))


def check_top(direction):
    expected = None
    for center, face in scan_cube.faces.items():
        if face == rotations.state["top"]:
            expected = center
    for attempt in range(6):
        color = scan_cube.scan_center_fast()
        if same_center(color, expected):
            return
        color = scan_cube.scan(scan_cube.main_sensor)
        motors.release()
        if same_center(color, expected):
            return
        print("top center should be", expected, "but is", color)
        if attempt == 5:
            raise RuntimeError("cube failed to find the right top face")
        if direction == "up":
            motors.turn_up()
        else:
            motors.turn_down()


def execute(turns_list):
    for number, i in enumerate(turns_list, 1):
        print("move", number, "of", len(turns_list), i)
        original_face = rotations.default_state[reference[str(i[0])]]
        reverse_state = {v: k for k, v in rotations.state.items()}
        current_position = reverse_state[original_face]

        if current_position == "top":
            rotations.move_up()
            check_top("up")
            rotations.move_up()
            check_top("up")
        elif current_position == "bottom":
            pass
        elif current_position == "front":
            rotations.move_down()
            check_top("down")
        elif current_position == "back":
            rotations.move_up()
            check_top("up")
        elif current_position == "right":
            rotations.move_right()
            rotations.move_up()
            check_top("up")
        elif current_position == "left":
            rotations.move_left()
            rotations.move_up()
            check_top("up")

        if i[0] == i[-1]:
            motors.move_270()

        elif i[-1] == "'":
            motors.move_90()

        elif i[-1] == "2":
            motors.move_180()
