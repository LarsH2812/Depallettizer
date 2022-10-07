def moveTo(x, y, r, o):
    instruction = f"G1 X{x} Y{y} R{r} O{o}"
    return instruction


def getCoords():
    instruction = f"M1"
    return instruction


def sendLabel(present=False):
    labelPresent = 1 if present else 0
    instruction = f"M2 B{labelPresent}"
    return instruction


def stop():
    instruction = f"Q0"
    return instruction


def start():
    instruction = f"S0"
    return instruction
    