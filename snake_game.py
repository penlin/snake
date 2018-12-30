from game import GameStatus, Game
import cv2
import random as rand

def dist(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def same_pos(p1, p2):
    return dist(p1, p2) < 1

class Snake():
    def __init__(self, x=rand.randint(0, 10), y=rand.randint(0, 10)):
        self.x = x
        self.y = y
        self.tail = []
        self.xspeed = 1
        self.yspeed = 0
    
    def dir(self, x, y):
        if self.xspeed == -x and self.yspeed == -y:
            return 
        self.xspeed = x
        self.yspeed = y
    
    def update(self, size):
        if len(self.tail) > 0:
            self.tail = self.tail[1:] + [(self.x, self.y)]
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        if self.x < 0 or self.y < 0 or self.x >= size[0] or self.y >= size[1]:
            return False
        return True

    def eat(self, x, y):
        if same_pos((self.x, self.y), (x, y)):
            self.tail.append((self.x, self.y))
            return True
        return False

class SnakeGame(Game):
    candy = (0, 0)
    score = -1

    def __init__(self, size=(50, 50), frame_rate=60, scale=10):
        super().__init__('Snake Game', size, frame_rate=frame_rate, scale=scale)
        self.create_candy()        

    def create_candy(self):
        self.candy = (rand.randint(0, self.size[0]-1), rand.randint(0, self.size[1]-1))
        self.score += 1

    def update(self, game_inst):
        if not game_inst.update(self.size):
            self.status = GameStatus.EGameOver
            return
        if game_inst.eat(self.candy[0], self.candy[1]):
            self.create_candy()

    def draw(self, canvas, game_inst):
        for pt in game_inst.tail:
            self.rect(canvas, pt[0], pt[1], (150, 160, 200))
        self.rect(canvas, game_inst.x , game_inst.y, (200, 210, 255))
        self.rect(canvas, self.candy[0], self.candy[1], (0, 0, 255))
        win_w = int(self.size[0] * self.scl)
        win_h = int((self.size[1] * self.scl + self.h)/2)
        cv2.putText(canvas, 'Score:{}'.format(self.score), (win_w - 100, win_h), cv2.FONT_HERSHEY_PLAIN, 1, (200, 200, 255), 1)

    def onKeyPressed(self, key, game_inst):
        if key == ord('i'):
            game_inst.dir(0, -1)
        elif key == ord('k'):
            game_inst.dir(0, 1)
        elif key == ord('j'):
            game_inst.dir(-1, 0)
        elif key == ord('l'):
            game_inst.dir(1, 0)


if __name__ == '__main__':
    game = SnakeGame(frame_rate=10)
    obj = Snake()
    game.start(obj)