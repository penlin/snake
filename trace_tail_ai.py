import cv2
import numpy as np
from utils import dist
from queue import Queue  

def tail_bfs(res, size, tail):
    q = Queue()
    res[tail[1]][tail[0]] = 2
    q.put(tail)
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while not q.empty():
        pt = q.get()
        for d in dirs:
            n = (pt[0] + d[0], pt[1] + d[1])
            if 0 <= n[0] < size[0] and 0 <= n[1] < size[1]:
                if res[n[1]][n[0]] == 0:
                    res[n[1]][n[0]] = 2
                    q.put(n)


def tail_bfs_map(size, inst):
    if len(inst.tail) < 2:
         return [[3 for _ in range(size[0])] for _ in range(size[1])]
    res = [[0 for _ in range(size[0])] for _ in range(size[1])]
    for pt in [(inst.x, inst.y)] + inst.tail[1:]:
        res[pt[1]][pt[0]] = 1
    tail_bfs(res, size, inst.tail[1])
    return res

def get_trace_tail_ai(size):
    def trace_tail_ai(inst):
        key = cv2.waitKey(1)
        if key in [ord('q'), ord('p'), ord('s'), 27]:
            return key
        candidate = {ord('j'): (-1, 0), ord('i'): (0, -1), ord('l'): (1, 0), ord('k'): (0, 1)}
        valid_candidate = {}
        tail_map = tail_bfs_map(size, inst)
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
            if tail_map[pos[1]][pos[0]] != 2 and val < 1:
                return key
            if tail_map[pos[1]][pos[0]] == 2 and val < min_val:
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
    return trace_tail_ai