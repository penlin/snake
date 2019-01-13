from utils import dist
from queue import Queue  
from random import choice

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


def bfs_maps(size, inst, blocks):
    candy_map = [[0 for _ in range(size[0])] for _ in range(size[1])]
    for pt in blocks:
        candy_map[pt[1]][pt[0]] = 1
    gen_bfs_map(candy_map, size, inst.candy)

    if len(inst.tail) < 2:
         tail_map = [[2 for _ in range(size[0])] for _ in range(size[1])]
    else:
        tail_map = [[0 for _ in range(size[0])] for _ in range(size[1])]
        for pt in blocks:
            tail_map[pt[1]][pt[0]] = 1
        gen_bfs_map(tail_map, size, inst.tail[1])
    return candy_map, tail_map

def get_trace_tail_ai(size):
    def trace_tail_ai(inst):
        candidate = {ord('j'): (-1, 0), ord('i'): (0, -1), ord('l'): (1, 0), ord('k'): (0, 1)}
        valid_candidate = {}
        blocks = [(inst.x, inst.y)] + inst.tail[1:]
        candy_map, tail_map = bfs_maps(size, inst, blocks)
        for key, speed in candidate.items():
            if speed[0] == -inst.xspeed and speed[1] == -inst.yspeed:
                continue
            pos = (inst.x + speed[0], inst.y + speed[1])
            if 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]:
                if len(inst.tail) <= 1 or pos not in blocks:
                    valid_candidate[key] = pos
        min_val = size[0] * size[1]
        availible_key = []
        for key, pos in valid_candidate.items():
            val = candy_map[pos[1]][pos[0]]
            if tail_map[pos[1]][pos[0]] > 1 and val > 1:
                if val < min_val:
                    min_val = val
                    availible_key = [key]
                elif val == min_val:
                    availible_key.append(key)
        if len(availible_key) == 0:
            for key, pos in valid_candidate.items():
                if tail_map[pos[1]][pos[0]] > 1:
                    availible_key.append(key)
        if len(availible_key) == 0:
            if inst.xspeed == 0:
                if (inst.y + inst.yspeed) < 0 or (inst.y + inst.yspeed) >= inst.size[1]:
                    return ord('j') if inst.x > 0 else ord('l')
            else:
                if (inst.x + inst.xspeed) < 0 or (inst.x + inst.xspeed) >= inst.size[0]:
                    return ord('i') if inst.y > 0 else ord('k')
            return 0xFF
        return choice(availible_key)
    return trace_tail_ai