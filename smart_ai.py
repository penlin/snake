import cv2
import numpy as np
from utils import dist


def get_smart_ai(size):
    def smart_ai(inst):
        key = cv2.waitKey(1)
        if key in [ord('q'), ord('p'), ord('s'), 27]:
            return key
        candidate = {ord('j'): (-1, 0), ord('i'): (0, -1), ord('l'): (1, 0), ord('k'): (0, 1)}
        valid_candidate = {}
        for key, speed in candidate.items():
            if speed[0] == -inst.xspeed and speed[1] == -inst.yspeed:
                continue
            pos = (inst.x + speed[0], inst.y + speed[1])
            if 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]:
                if len(inst.tail) <= 1 or pos not in inst.tail[1:]:
                    valid_candidate[key] = pos
        min_val = size[0] * size[1]
        min_key = 0xFF
        for key, pos in valid_candidate.items():
            val = dist(pos, inst.candy)
            if val < min_val:
                min_val = val
                min_key = key
        if min_key == 0xFF:
            if inst.xspeed == 0:
                if (inst.y + inst.yspeed) < 0 or (inst.y + inst.yspeed) >= inst.size[1]:
                    return ord('j') if inst.x > 0 else ord('l')
            else:
                if (inst.x + inst.xspeed) < 0 or (inst.x + inst.xspeed) >= inst.size[0]:
                    return ord('i') if inst.y > 0 else ord('k')
        return min_key
    return smart_ai