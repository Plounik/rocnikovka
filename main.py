import rotations
state = {"up":"yellow", "front":"green", "right":"orange", "left":"red","back":"blue", "bottom":"white"}
print(state)
state = rotations.left_turn(state)
print(state)
state = rotations.right_turn(state)
print(state)