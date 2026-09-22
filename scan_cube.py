import motors
faces = {}
def scan(sensor):
    if sensor == "main":
        pass
    else:
        pass
    color = None
    return color



def scan_side(face):
    order = "476501238"
    side = ""
    motors.scan_center()
    side += scan("main")
    faces[side] = face
    motors.scan()
    for i in range(4):
        side += scan("main")
        side += scan("side")
        motors.move_90()
    side_final = ""
    for i in range(9):
        side_final += side[int(order[i])]
    return side_final 