"""
cannon.py - Fires balls one at a time at regular intervals.
"""

from config import FIRE_INTERVAL
from ball import Ball


class Cannon:
    def __init__(self):
        self._firing     = False
        self._angle      = 270.0
        self._timer      = 0.0
        self._balls_left = 0
        self._color      = None
        self.new_balls   = []

    def start_firing(self, angle: float, count: int, color):
        self._firing     = True
        self._angle      = angle
        self._balls_left = count
        self._color      = color
        self._timer      = FIRE_INTERVAL  # fire first ball immediately
        self.new_balls   = []

    def tick(self, dt: float, start_x: float, start_y: float) -> bool:
        """
        Called every frame. Populates self.new_balls.
        Returns True when all balls have been fired.
        """
        self.new_balls = []
        if not self._firing:
            return True

        self._timer += dt
        while self._timer >= FIRE_INTERVAL and self._balls_left > 0:
            self._timer      -= FIRE_INTERVAL
            self._balls_left -= 1
            self.new_balls.append(
                Ball(start_x, start_y, self._angle, color=self._color)
            )

        if self._balls_left <= 0:
            self._firing = False
            return True
        return False

    @property
    def is_firing(self):
        return self._firing
