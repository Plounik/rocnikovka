import rotations
def execute(turns_list):
    for i in turns_list:
            print(i)
            match i:
                case "up":
                    rotations.up_turn()
                case "down":
                    rotations.down_turn()
                case "left":
                    rotations.left_turn()
                case "right":
                    rotations.right_turn()
  