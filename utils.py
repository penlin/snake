def dist(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def same_pos(p1, p2):
    return dist(p1, p2) < 1
