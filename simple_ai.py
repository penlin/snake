
def SimpleAI(inst):
    if inst.xspeed == 0:
        if (inst.y + inst.yspeed) < 0 or (inst.y + inst.yspeed) >= inst.size[1]:
            return ord('j') if inst.x > 0 else ord('l')
    else:
        if (inst.x + inst.xspeed) < 0 or (inst.x + inst.xspeed) >= inst.size[0]:
            return ord('i') if inst.y > 0 else ord('k')
    return 0xFF

