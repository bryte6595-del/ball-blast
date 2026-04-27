"""
ball.py - Ball with realistic physics and accurate collision.
"""

import math
from config import BALL_SPEED, GRAVITY, GRID_COLS, GRID_ROWS


class Ball:
    def __init__(self, x: float, y: float, angle_deg: float, color=None):
        from config import C_BALL
        self.x     = float(x)
        self.y     = float(y)
        self.color = color or C_BALL
        self.alive = True
        rad        = math.radians(angle_deg)
        self.vx    = BALL_SPEED * math.cos(rad)
        self.vy    = BALL_SPEED * math.sin(rad)

    def step(self, sub_dt: float, grid_w: float, grid_h: float,
             cell: float) -> tuple:
        """
        Move one sub-step with gravity applied.
        Returns (col, row) or (None, None) if exited bottom.
        """
        # Gravity pulls downward (negative y direction in Kivy)
        self.vy -= GRAVITY * sub_dt

        self.x += self.vx * sub_dt
        self.y += self.vy * sub_dt

        # Left wall
        if self.x < 0:
            self.x  = 0.0
            self.vx = abs(self.vx)

        # Right wall
        if self.x > grid_w:
            self.x  = grid_w
            self.vx = -abs(self.vx)

        # Top wall — bounce back down
        if self.y > grid_h:
            self.y  = grid_h
            self.vy = -abs(self.vy)

        # Bottom — ball exits
        if self.y < 0:
            self.alive = False
            return None, None

        col = int(self.x // cell)
        row = int(self.y // cell)
        col = max(0, min(col, GRID_COLS - 1))
        row = max(0, min(row, GRID_ROWS - 1))
        return col, row

    def bounce_off_block(self, col: int, row: int, cell: float):
        """
        Accurate face detection using axis overlap.
        Smaller overlap axis = the face that was hit.
        """
        cx = (col + 0.5) * cell
        cy = (row + 0.5) * cell
        dx = self.x - cx
        dy = self.y - cy
        half = cell * 0.48   # slightly less than 0.5 to avoid edge ambiguity

        ox = half - abs(dx)  # overlap on x axis
        oy = half - abs(dy)  # overlap on y axis

        if ox < oy:
            # Hit left or right face — flip vx, push out horizontally
            self.vx = -self.vx
            push    = (half + 2) * (1 if dx >= 0 else -1)
            self.x  = cx + push
        else:
            # Hit top or bottom face — flip vy, push out vertically
            self.vy = -self.vy
            push    = (half + 2) * (1 if dy >= 0 else -1)
            self.y  = cy + push
