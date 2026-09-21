import rotations
def execute(turns_list):
    for i in turns_list:
            print(i)
            if i == "up":
                rotations.move_up()
            elif i == "down":
                rotations.move_down()
            elif i == "left":
                rotations.move_left()
            elif i == "right":
                rotations.move_right()
  
