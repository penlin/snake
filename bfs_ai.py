import cv2
import numpy as np
from queue import Queue

def gen_bfs_map(res, size, root):
    q = Queue()
    res[root[1]][root[0]] = 2
    q.put(root)
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while not q.empty():
        pt = q.get()
        dist = res[pt[1]][pt[0]]
        for d in dirs:
            n = (pt[0] + d[0], pt[1] + d[1])
            if 0 <= n[0] < size[0] and 0 <= n[1] < size[1]:
                if res[n[1]][n[0]] == 0:
                    res[n[1]][n[0]] = dist + 1
                    q.put(n)


def candy_bfs_map(size, inst):
    res = [[0 for _ in range(size[0])] for _ in range(size[1])]
    for pt in [(inst.x, inst.y)] + inst.tail[1:]:
        res[pt[1]][pt[0]] = 1
    gen_bfs_map(res, size, inst.candy)
    return res


def get_bfs_ai(size):
    def bfs_ai(inst):
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
        candy_map = candy_bfs_map(size, inst)
        for key, pos in valid_candidate.items():
            val = candy_map[pos[1]][pos[0]]
            if val > 0 and val < min_val:
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
    return bfs_ai