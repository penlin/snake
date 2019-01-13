from game import GameStatus, Game
from utils import same_pos
from simple_ai import SimpleAI
from smart_ai import get_smart_ai
from bfs_ai import get_bfs_ai
from trace_tail_ai import get_trace_tail_ai
import cv2
import sys
import argparse
import pickle
import random as rand


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

    def win(self):
        return (self.size[0] * self.size[1] - 1) == len(self.tail)

    def dead(self):
        return not (0 <= self.x < self.size[0] and 0 <= self.y < self.size[1] and (self.x, self.y) not in self.tail)

    def create_candy(self):
        getNum = lambda pt: pt[1] * self.size[0] + pt[0]
        max_num = self.size[0] * self.size[1] - 1
        invalid = list(map(getNum, self.tail)) + [getNum((self.x, self.y))]
        num = rand.randint(0, max_num)
        while num in invalid:
            num = rand.randint(0, max_num)
        self.candy = (num % self.size[0], int(num/ self.size[0]))

    def eat(self):
        if same_pos((self.x, self.y), self.candy):
            if len(self.tail) > 0:
                self.tail.insert(0, self.tail[0])
            else:
                self.tail.append((self.x, self.y))
            self.create_candy()


class SnakeGame(Game):
    def __init__(self, size=(50, 50), frame_rate=60, scale=10, controller=None):
        super().__init__('Snake Game', size, frame_rate=frame_rate, scale=scale, controller=controller)

    def update(self, game_inst):
        game_inst.update()
        if game_inst.win():
            self.status = GameStatus.EGameVictory
            return
        elif game_inst.dead():
            self.status = GameStatus.EGameOver
            return
        game_inst.eat()

    def draw(self, game_inst):
        for pt in game_inst.tail:
            self.screen.grid(pt, (90, 100, 150))
        if len(game_inst.tail) > 1:
            self.screen.grid(game_inst.tail[0], (60, 100, 60))
        self.screen.grid((game_inst.x , game_inst.y), (255, 255, 255))
        self.screen.ball(game_inst.candy, (0, 0, 255))
        score_msg = 'Score:{}'.format(len(game_inst.tail))
        self.screen.text(score_msg, (2, (self.height + self.size[1]) // 2 + 1), (200, 200, 255))

    def onKeyPressed(self, key, game_inst):
        if key == ord('i'):
            game_inst.dir(0, -1)
        elif key == ord('k'):
            game_inst.dir(0, 1)
        elif key == ord('j'):
            game_inst.dir(-1, 0)
        elif key == ord('l'):
            game_inst.dir(1, 0)


def get_ai(name, size):
    controller = None
    if name == 'SimpleAI':
        controller = SimpleAI
    elif name == 'SmartAI':
        controller = get_smart_ai(size)
    elif name == 'BFSAI':
        controller = get_bfs_ai(size)
    elif name == 'TraceTailAI':
        controller = get_trace_tail_ai(size)
    return controller

def get_snake_obj(args):
    size = tuple(map(int, args.size.split('x')))
    if args.record:
        with open(args.record, 'rb') as fin:
            obj = pickle.load(fin)
        size = obj.size
    else:
        obj = Snake(size)
    return obj


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Snake Game')
    parser.add_argument('--resume', dest='record',
                         help='resume from the specified saved record')
    parser.add_argument('--fps', default=8, type=int, help='frame rate')
    parser.add_argument('--size', default='30x30', help='game board size')
    parser.add_argument('--scale', default=15, type=int, help='grid size')
    parser.add_argument('--ai', help='AI name to run the Snake Game')
    args = parser.parse_args()
    key = ord('r')
    while key == ord('r'):
        obj = get_snake_obj(args)
        controller = get_ai(args.ai, obj.size)
        game = SnakeGame(size=obj.size, frame_rate=args.fps, scale=args.scale, controller=controller)
        key = game.start(obj)