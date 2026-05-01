"""
ball.py - Ball with proper swept collision detection.

Instead of checking which cell the ball occupies (broken),
we check the LINE the ball travels each frame and find
the first block it actually crosses. This is how real games work.
"""

import math
from config import BALL_SPEED, GRAVITY, GRID_COLS, GRID_ROWS

TRAIL_LENGTH = 10


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
        self.trail = []   # list of (x, y) for drawing trail

    def move(self, dt: float, grid_w: float, grid_h: float,
             cell: float, blocks: dict) -> tuple:
        """
        Move the ball using swept collision detection.

        - Moves ball in one step
        - Checks every block the ball's path could intersect
        - Bounces off the correct face
        - Returns (col, row) of hit block or (None, None)

        blocks: dict of (col, row) -> Block from grid
        """
        # Save trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

        # Apply gravity
        self.vy -= GRAVITY * dt

        # Target position
        nx = self.x + self.vx * dt
        ny = self.y + self.vy * dt

        # ── Wall collisions first ──────────────────────────────────────────
        if nx < 0:
            nx  = 0.0
            self.vx = abs(self.vx)
        if nx > grid_w:
            nx  = grid_w
            self.vx = -abs(self.vx)
        if ny > grid_h:
            ny  = grid_h
            self.vy = -abs(self.vy)
        if ny < 0:
            self.alive = False
            return None, None

        # ── Swept block collision ──────────────────────────────────────────
        # Find which cells the ball might pass through this frame
        hit_col, hit_row, hit_time, hit_face = self._sweep(
            self.x, self.y, nx, ny, cell, blocks, grid_w, grid_h
        )

        if hit_col is not None:
            # Move ball to just before the collision point
            self.x = self.x + (nx - self.x) * hit_time
            self.y = self.y + (ny - self.y) * hit_time

            # Bounce off correct face
            if hit_face == 'left' or hit_face == 'right':
                self.vx = -self.vx
                # Push out
                if hit_face == 'left':
                    self.x = hit_col * cell - 2
                else:
                    self.x = (hit_col + 1) * cell + 2
            else:  # top or bottom
                self.vy = -self.vy
                if hit_face == 'bottom':
                    self.y = hit_row * cell - 2
                else:
                    self.y = (hit_row + 1) * cell + 2

            return hit_col, hit_row
        else:
            # No block hit — move freely
            self.x = nx
            self.y = ny
            return None, None

    def _sweep(self, x0, y0, x1, y1, cell, blocks, grid_w, grid_h):
        """
        Find the first block the ball's path (x0,y0)->(x1,y1) intersects.
        Returns (col, row, time, face) or (None, None, None, None).
        time is 0..1 along the path.
        face is 'left', 'right', 'top', 'bottom'.
        """
        best_t    = 1.1
        best_col  = None
        best_row  = None
        best_face = None

        # Find range of cells to check
        min_col = max(0, int(min(x0, x1) // cell) - 1)
        max_col = min(GRID_COLS - 1, int(max(x0, x1) // cell) + 1)
        min_row = max(0, int(min(y0, y1) // cell) - 1)
        max_row = min(GRID_ROWS - 1, int(max(y0, y1) // cell) + 1)

        for col in range(min_col, max_col + 1):
            for row in range(min_row, max_row + 1):
                if (col, row) not in blocks:
                    continue

                # Block bounds
                bx0 = col * cell
                bx1 = (col + 1) * cell
                by0 = row * cell
                by1 = (row + 1) * cell

                t, face = self._ray_vs_rect(
                    x0, y0, x1 - x0, y1 - y0,
                    bx0, by0, bx1, by1
                )
                if t is not None and t < best_t:
                    best_t    = t
                    best_col  = col
                    best_row  = row
                    best_face = face

        if best_col is not None:
            return best_col, best_row, best_t, best_face
        return None, None, None, None

    def _ray_vs_rect(self, rx, ry, rdx, rdy, bx0, by0, bx1, by1):
        """
        Ray vs axis-aligned rectangle intersection.
        Ray starts at (rx, ry) with direction (rdx, rdy).
        Returns (t, face) where t is 0..1, or (None, None).
        """
        if rdx == 0 and rdy == 0:
            return None, None

        # Time of intersection with each side
        if rdx != 0:
            tx0 = (bx0 - rx) / rdx
            tx1 = (bx1 - rx) / rdx
        else:
            tx0 = -math.inf
            tx1 =  math.inf

        if rdy != 0:
            ty0 = (by0 - ry) / rdy
            ty1 = (by1 - ry) / rdy
        else:
            ty0 = -math.inf
            ty1 =  math.inf

        # Sort so t_min < t_max for each axis
        if tx0 > tx1: tx0, tx1 = tx1, tx0
        if ty0 > ty1: ty0, ty1 = ty1, ty0

        # Find overlap
        t_enter = max(tx0, ty0)
        t_exit  = min(tx1, ty1)

        if t_enter > t_exit:
            return None, None   # no intersection
        if t_exit < 0:
            return None, None   # behind ray
        if t_enter > 1:
            return None, None   # beyond destination

        t = max(0.0, t_enter)

        # Which face did we hit?
        if tx0 > ty0:
            face = 'left' if rdx > 0 else 'right'
        else:
            face = 'bottom' if rdy > 0 else 'top'

        return t, face
