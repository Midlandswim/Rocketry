import utils


MAX_PITCH = 20
MAX_ALT = 20
MAX_TEMP = 50


def checkSafeTrajectory(alt, temp, gX, gY, gZ):
    pitch = utils.angle((gX, gY, gZ), (0.01, 0.01, 0.01))
    
    output = ""
    output += f"\n[WARN] Altitude out of range: {alt}!" if alt > MAX_ALT else ""
    output += f"\n[WARN] Pitch out of range: {pitch}!" if pitch > MAX_PITCH else ""
    output += f"\n[WARN] Temperature out of range: {temp}!" if temp > MAX_TEMP else ""

    return output