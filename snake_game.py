from game import GameStatus, Game
import cv2
import sys
import argparse
import pickle
import random as rand
import time

def dist(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def same_pos(p1, p2):
    return dist(p1, p2) < 1

class Snake():
    def __init__(self, size, x=-1, y=-1):
        self.size = size
        if x < 0 or x > (self.size[0]-2):
            self.x  = rand.randint(0, self.size[0]-2)
        else:
            self.x = x
        if y < 0 or y > (self.size[1]-2):
            self.y = rand.randint(0, self.size[1]-2)
        else:
            self.y = y
        self.tail = []
        self.xspeed = 1
        self.yspeed = 0
        self.create_candy()

    def dir(self, x, y):
        if self.xspeed == -x and self.yspeed == -y:
            return 
        self.xspeed = x
        self.yspeed = y
    
    def update(self):
        if len(self.tail) > 0:
            self.tail = self.tail[1:] + [(self.x, self.y)]
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        return self.dead()

    def dead(self):
        return 0 <= self.x < self.size[0] and 0 <= self.y < self.size[1] and (self.x, self.y) not in self.tail

    def create_candy(self):
        num = rand.randint(0, self.size[0] * self.size[1]-1)
        while num != (self.x * self.size[0] + self.y):
            num = rand.randint(0, self.size[0] * self.size[1]-1)
        self.candy = (num % self.size[0], int(num/ self.size[0]))

    def eat(self):
        if same_pos((self.x, self.y), self.candy):
            self.tail.append((self.x, self.y))
            self.create_candy()
            return True
        return False

class SnakeGame(Game):
    def __init__(self, size=(50, 50), frame_rate=60, scale=10, controller=None):
        super().__init__('Snake Game', size, frame_rate=frame_rate, scale=scale, controller=controller)

    def update(self, game_inst):
        if not game_inst.update():
            self.status = GameStatus.EGameOver
            return
        game_inst.eat()

    def draw(self, canvas, game_inst):
        for pt in game_inst.tail:
            self.rect(canvas, pt[0], pt[1], (150, 160, 200))
        self.rect(canvas, game_inst.x , game_inst.y, (200, 210, 255))
        self.rect(canvas, game_inst.candy[0], game_inst.candy[1], (0, 0, 255))
        win_w = int(self.size[0] * self.scl)
        win_h = int((self.size[1] * self.scl + self.h)/2)
        cv2.putText(canvas, 'Score:{}'.format(len(game_inst.tail)), (win_w - 100, win_h), cv2.FONT_HERSHEY_PLAIN, 1, (200, 200, 255), 1)

    def onKeyPressed(self, key, game_inst):
        if key == ord('s'):
            with open('record.tmp', 'wb') as ftmp:
                pickle.dump(game_inst, ftmp)
        elif key == ord('i'):
            game_inst.dir(0, -1)
        elif key == ord('k'):
            game_inst.dir(0, 1)
        elif key == ord('j'):
            game_inst.dir(-1, 0)
        elif key == ord('l'):
            game_inst.dir(1, 0)


def SimpleAI(inst):
    key = cv2.waitKey(1)
    if key in [ord('q'), ord('p'), 27]:
        return key
    if inst.xspeed == 0:
        if (inst.y + inst.yspeed) < 0 or (inst.y + inst.yspeed) >= inst.size[1]:
            return ord('j') if inst.x > 0 else ord('l')
    else:
        if (inst.x + inst.xspeed) < 0 or (inst.x + inst.xspeed) >= inst.size[0]:
            return ord('i') if inst.y > 0 else ord('k')
    return 0xFF


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Snake Game')
    parser.add_argument('--resume', dest='record',
                         help='resume from the specified saved record')
    parser.add_argument('--fps', default=8, type=int, help='frame rate')
    parser.add_argument('--size', default='30x30', help='game board size')
    parser.add_argument('--scale', default=15, type=int, help='grid size')
    parser.add_argument('--ai', help='AI name to run the Snake Game')
    args = parser.parse_args()
    size = tuple(map(int, args.size.split('x')))
    if args.record:
        with open(args.record, 'rb') as fin:
            obj = pickle.load(fin)
        size = obj.size
    else:
        obj = Snake(game.size)

    controller = None
    if args.ai:
        controller = SimpleAI

    game = SnakeGame(size=size, frame_rate=args.fps, scale=args.scale, controller=controller)
    game.start(obj)