import rotations
import turns
import moves

print(rotations.state)
moves.execute(["u'", "D", "l'", "b", "r", "f'", "U"])
rotations.up_turn()
turns.execute(["down", "left", "up", "left", "down", "right"])
print(rotations.state)
