import rotations
def execute_moves(moves_list):
    for i in moves_list:
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
  
print(rotations.state)
execute_moves(["down", "left", "up", "left", "down", "right"])
print(rotations.state)
