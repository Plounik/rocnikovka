import rotations
def execute(turns_list):
    for i in turns_list:
            if i == "up":
                rotations.move_up()
            elif i == "down":
                rotations.move_down()
            elif i == "left":
                rotations.move_left()
            elif i == "right":
                rotations.move_right()
            elif i == "180":
                rotations.move_180()