import rotations
def execute(turns_list):
    for i in turns_list:
        print(i)
        if i == "up":
            rotations.up_turn()
        elif i == "down":
            rotations.down_turn()
        elif i == "left":
            rotations.left_turn()
        elif i == "right":
            rotations.right_turn()
  
