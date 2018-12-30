import cv2
import numpy as np
import abc
import enum

class GameStatus(enum.Enum):
    EGameNotInit = 'NotInit',
    EGameReady = 'Ready',
    EGameStart = 'Start, press \'p\' to pasue',
    EGamePause = 'Pause, press \'p\' to resume',
    EGameOver = 'Game Over!',
    EGameVictory = 'Congradulation! You Win',
    EGameStop = 'Stop',


class Game(abc.ABC):
    size = (250, 250)
    status = GameStatus.EGameNotInit
    frame_rate = 50
    scl = 5
    _status_bar_height = 5
    _title = 'A New Game'
    _time = 0

    def __init__(self, title, size, frame_rate=50, scale=50):
        self._title = title
        self.size = size
        self.frame_rate=frame_rate
        self.scl = scale
        self.status = GameStatus.EGameReady

    def start(self, game_inst):
        self.status = GameStatus.EGameStart
        delay = int(1000/self.frame_rate)
        cv2.namedWindow(self._title)
        cv2.moveWindow(self._title, 200, 0)
        self.w = int(self.size[0] * self.scl)
        self.h = int((self.size[1] + self._status_bar_height) * self.scl)
        canvas = np.zeros((self.h, self.w, 3), dtype=np.int8)
        while self.status != GameStatus.EGameStop:
            if self.status == GameStatus.EGameStart:
                self._time = self._time + 1
                self.update(game_inst)
                if self.status in [GameStatus.EGameOver, GameStatus.EGameVictory]:
                    break
            self.show(canvas, game_inst)
            key = cv2.waitKey(delay)                
            if key == ord('p'):
                if self.status == GameStatus.EGamePause:
                    self.status = GameStatus.EGameStart
                elif self.status == GameStatus.EGameStart:
                    self.status = GameStatus.EGamePause
            elif key in [ord('q'), 27]:
                self.status = GameStatus.EGameStop
            elif (key & 0xFF) != 0xFF:
                self.onKeyPressed(key, game_inst)

        self.show(canvas, game_inst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show(self, canvas, game_inst):
        self.drawMain(canvas)
        self.draw(canvas, game_inst)
        cv2.imshow(self._title, canvas)

    def rect(self, canvas, x, y, color):
        left = int(x * self.scl)
        top = int(y * self.scl)
        cv2.rectangle(canvas, (left, top), (left + self.scl, top + self.scl), color, -1)

    def drawMain(self, canvas):
        win_w = int(self.size[0] * self.scl)
        win_h = int(self.size[1] * self.scl)
        cv2.rectangle(canvas, (0, 0), (win_w, win_h), (0, 0, 0), -1)
        cv2.rectangle(canvas, (0, win_h), (win_w, self.h), (30, 30, 30), -1)
        if self.status != GameStatus.EGameStop:
            status = '[{}]: {}'.format(self._time, self.status)
        else:
            status = '[{}]: Game Ended, press any key to exit ...'.format(self._time)
        cv2.putText(canvas, status, (self.scl * 5, int((win_h + self.h)/2)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

    @abc.abstractmethod
    def update(self, game_inst):
        pass

    @abc.abstractmethod
    def draw(self, canvas, game_inst):
        pass

    @abc.abstractmethod
    def onKeyPressed(self, key, game_inst):
        pass
