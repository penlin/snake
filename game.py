import abc
import enum
from cv2_displayer import CV2_Cursor

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
    scl = 5
    _status_bar_height = 5
    _title = 'A New Game'
    _time = 0

    def __init__(self, title, size, frame_rate=50, scale=50, controller=None):
        self._title = title
        self.size = size
        self.status = GameStatus.EGameReady
        self.scl = scale
        self.fps = frame_rate
        self.controller = controller

    def start(self, game_inst, start_time=0):
        self.status = GameStatus.EGameStart
        self._init_io()
        self._time = start_time
        while self.status != GameStatus.EGameStop:
            if self.status == GameStatus.EGameStart:
                self._time = self._time + 1
                self.update(game_inst)
                if self.status in [GameStatus.EGameOver, GameStatus.EGameVictory]:
                    break
            self.display(game_inst)
            key = self.controller(game_inst)
            if key == ord('p'):
                if self.status == GameStatus.EGamePause:
                    self.status = GameStatus.EGameStart
                elif self.status == GameStatus.EGameStart:
                    self.status = GameStatus.EGamePause
            elif key in [ord('q'), 27]:
                self.status = GameStatus.EGameStop
            elif (key & 0xFF) != 0xFF:
                self.onKeyPressed(key, game_inst)

        self.show(game_inst)
        return self.screen.waitKey(0)

    def _init_io(self):
        self.width = self.size[0]
        self.height = self.size[1] + self._status_bar_height
        if self.fps <= 0:
            self.display = lambda *x: None
        else:
            self.display = self.show

        self.screen = CV2_Cursor(self._title, self.width, self.height, self.scl)
        if self.controller is None:
            delay = int(1000/self.fps)
            self.controller = lambda inst: self.screen.waitKey(delay)

    def show(self, game_inst):
        self.drawMain()
        self.draw(game_inst)
        self.screen.show()

    def drawMain(self):
        self.screen.rect((0, 0), self.size, (0, 0, 0))
        self.screen.rect((0, self.size[1]), (self.size[0], self.height), (30, 30, 30))
        if self.status != GameStatus.EGameStop:
            status = '[{}]: {}'.format(self._time, self.status)
        else:
            status = '[{}]: Game Ended, press any key to exit ...'.format(self._time)
        self.screen.text(status, (2, (self.size[1] + self.height) // 2), (255, 255, 255))

    @abc.abstractmethod
    def update(self, game_inst):
        pass

    @abc.abstractmethod
    def draw(self, game_inst):
        pass

    @abc.abstractmethod
    def onKeyPressed(self, key, game_inst):
        pass
