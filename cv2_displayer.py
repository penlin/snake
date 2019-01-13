import cv2
import numpy as np


class CV2_Screen(object):
    def __init__(self, title, width, height, scale=50):
        self.title = title
        self.w = width
        self.h = height
        self.scl = scale
        self._grid_width = int(self.scl * 3 /4)
        self._ball_radius = int(self.scl / 2)
        self._canvas = np.zeros((self.h * self.scl, self.w * self.scl, 3), dtype=np.int8)
        cv2.namedWindow(self.title)
        cv2.moveWindow(self.title, 200, 0)

    def __del__(self):
        cv2.destroyWindow(self.title)

    def _to_grid_cord(self, pt):
        return tuple(map(lambda v: int(v * self.scl), pt))

    def _to_grid_center(self, pt):
        return tuple(map(lambda v: int(v * self.scl + self.scl / 2), pt))

    def grid(self, pt, color, linewidth=-1):
        lt_ = self._to_grid_cord(pt)
        left, top = lt_
        cv2.rectangle(self._canvas, lt_, (left + self._grid_width, top + self._grid_width), color, linewidth)
    
    def ball(self, center, color, linewidth=-1):
        c = self._to_grid_center(center)
        cv2.circle(self._canvas, c, self._ball_radius, color, linewidth)

    def rect(self, lt, br, color, linewidth=-1):
        _lt = self._to_grid_cord(lt)
        _br = self._to_grid_center(br)
        cv2.rectangle(self._canvas, _lt, _br, color, linewidth)
    
    def text(self, msg, pos, color):
        location = self._to_grid_cord(pos)
        cv2.putText(self._canvas, msg, location, cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

    def show(self):
        cv2.imshow(self.title, self._canvas)

    def waitKey(self, timeout=0):
        return cv2.waitKey(timeout)


