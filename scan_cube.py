import motors
def scan(sensor):
    if sensor == "main":
        pass
    else:
        pass
    color = None
    return color



def scan_side():
    order = "729814563"
    side = ""
    motors.scan_center()
    side += scan("main")
    motors.scan()
    for i in range(4):
        side += scan("main")
        side += scan("side")
        motors.move_90()
    side_final = ""
    for i in range(9):
        side_final += side[order[i]]
    return side_final 