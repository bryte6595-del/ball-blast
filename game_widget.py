"""
game_widget.py - Draws the game with stylish visuals.
Handles touch input for aiming.
"""

import math
from kivy.uix.widget import Widget
from kivy.graphics import (
    Color, Rectangle, RoundedRectangle,
    Ellipse, Line, Triangle,
)
from kivy.core.text import Label as CoreLabel
from config import (
    GRID_COLS, GRID_ROWS, BALL_RADIUS,
    DANGER_ROW,
    C_BG_TOP, C_BG_BOT, C_GRID_BG, C_GRID_LINE,
    C_DANGER_LINE, C_BALL_GLOW, C_POWERUP_RING,
)


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_angle_update  = None
        self.on_angle_release = None
        self._touching        = False
        self._aim_angle       = 270.0
        # Grid geometry — updated each draw call
        self._ox = self._oy = 0.0
        self._cell = self._grid_w = self._grid_h = 0.0

    # ── Public draw ───────────────────────────────────────────────────────────

    def draw(self, grid, balls, aiming=False, aim_angle=None,
             cannon_x=None, cannon_y=None):
        self.canvas.clear()

        cell   = min(self.width / GRID_COLS, self.height / GRID_ROWS)
        grid_w = cell * GRID_COLS
        grid_h = cell * GRID_ROWS
        ox = self.x + (self.width  - grid_w) / 2
        oy = self.y + (self.height - grid_h) / 2

        # Store for touch calculations
        self._ox = ox; self._oy = oy
        self._cell = cell; self._grid_w = grid_w; self._grid_h = grid_h

        with self.canvas:

            # ── Full background ───────────────────────────────────────────────
            Color(*C_BG_BOT)
            Rectangle(pos=self.pos, size=self.size)
            # Fake vertical gradient with two rects
            Color(*C_BG_TOP)
            Rectangle(pos=(self.x, oy + grid_h * 0.5),
                      size=(self.width, self.height - grid_h * 0.5))

            # ── Grid background ───────────────────────────────────────────────
            Color(*C_GRID_BG)
            Rectangle(pos=(ox, oy), size=(grid_w, grid_h))

            # ── Grid lines (subtle) ───────────────────────────────────────────
            Color(*C_GRID_LINE)
            for c in range(GRID_COLS + 1):
                Rectangle(pos=(ox + c * cell, oy), size=(1, grid_h))
            for r in range(GRID_ROWS + 1):
                Rectangle(pos=(ox, oy + r * cell), size=(grid_w, 1))

            # ── Danger line ───────────────────────────────────────────────────
            dy = oy + DANGER_ROW * cell
            Color(*C_DANGER_LINE)
            Line(points=[ox, dy, ox + grid_w, dy],
                 width=2, dash_offset=10, dash_length=14)

            # ── Blocks ────────────────────────────────────────────────────────
            for col, row, block in grid.all_blocks():
                bx = ox + col * cell
                by = oy + row * cell
                cx = bx + cell * 0.5
                cy = by + cell * 0.5
                r  = cell * 0.40

                # Block fill
                Color(*block.color())
                self._fill_shape(block.shape, cx, cy, r)

                # Block border — slightly lighter
                Color(*block.border_color())
                self._stroke_shape(block.shape, cx, cy, r, lw=1.5)

                # Power-up ring and inner glow
                if block.is_powerup:
                    Color(*C_POWERUP_RING)
                    Line(circle=(cx, cy, r * 0.65), width=2)
                    Color(1, 1, 1, 0.4)
                    Ellipse(pos=(cx - r*0.3, cy - r*0.3),
                            size=(r*0.6, r*0.6))
                else:
                    # HP label
                    self._hp_label(str(block.hp), cx, cy, int(cell * 0.26))

            # ── Balls ─────────────────────────────────────────────────────────
            ball_r = cell * BALL_RADIUS
            for ball in balls:
                if not ball.alive:
                    continue
                bx = ox + ball.x
                by = oy + ball.y
                # Glow ring
                Color(*C_BALL_GLOW)
                Ellipse(pos=(bx - ball_r*1.6, by - ball_r*1.6),
                        size=(ball_r*3.2, ball_r*3.2))
                # Ball body
                Color(*ball.color)
                Ellipse(pos=(bx - ball_r, by - ball_r),
                        size=(ball_r*2, ball_r*2))
                # Highlight
                Color(1, 1, 1, 0.4)
                hr = ball_r * 0.35
                Ellipse(pos=(bx - ball_r*0.55 - hr*0.5,
                             by + ball_r*0.3 - hr*0.5),
                        size=(hr, hr))

            # ── Cannon base ───────────────────────────────────────────────────
            if cannon_x is not None and cannon_y is not None:
                cbx = ox + cannon_x
                cby = oy + cannon_y
                cr  = cell * 0.28
                Color(0.6, 0.6, 0.7, 0.6)
                Ellipse(pos=(cbx - cr, cby - cr), size=(cr*2, cr*2))
                Color(0.9, 0.9, 1.0, 0.9)
                Line(circle=(cbx, cby, cr), width=1.5)

            # ── Aiming line (only while touching) ────────────────────────────
            if aiming and self._touching and aim_angle is not None:
                rad = math.radians(aim_angle)
                sx  = ox + (cannon_x or grid_w / 2)
                sy  = oy + (cannon_y or grid_h * 0.9)
                ln  = grid_h * 0.55

                # Draw dotted line in segments
                Color(1, 1, 1, 0.7)
                Line(points=[sx, sy,
                             sx + ln * math.cos(rad),
                             sy + ln * math.sin(rad)],
                     width=2,
                     dash_offset=8, dash_length=14)

                # Arrow tip
                tip_x = sx + ln * math.cos(rad)
                tip_y = sy + ln * math.sin(rad)
                Color(1, 0.6, 0.1, 0.9)
                Ellipse(pos=(tip_x - 5, tip_y - 5), size=(10, 10))

    # ── Shape drawing ─────────────────────────────────────────────────────────

    def _fill_shape(self, shape, cx, cy, r):
        if shape == 'circle':
            Ellipse(pos=(cx - r, cy - r), size=(r*2, r*2))
        elif shape == 'triangle':
            pts = self._poly_pts(cx, cy, r, 3, offset=90)
            Triangle(points=pts)
        elif shape == 'pentagon':
            self._filled_poly(cx, cy, r, 5, offset=90)
        elif shape == 'hexagon':
            self._filled_poly(cx, cy, r, 6, offset=0)

    def _stroke_shape(self, shape, cx, cy, r, lw=1.5):
        if shape == 'circle':
            Line(circle=(cx, cy, r), width=lw)
        elif shape == 'triangle':
            pts = self._poly_pts(cx, cy, r, 3, offset=90)
            Line(points=pts + pts[:2], width=lw)
        elif shape == 'pentagon':
            pts = self._poly_pts(cx, cy, r, 5, offset=90)
            Line(points=pts + pts[:2], width=lw)
        elif shape == 'hexagon':
            pts = self._poly_pts(cx, cy, r, 6, offset=0)
            Line(points=pts + pts[:2], width=lw)

    def _poly_pts(self, cx, cy, r, sides, offset=0):
        pts = []
        for i in range(sides):
            a = math.radians(offset + i * 360 / sides)
            pts += [cx + r * math.cos(a), cy + r * math.sin(a)]
        return pts

    def _filled_poly(self, cx, cy, r, sides, offset=0):
        for i in range(sides):
            a1 = math.radians(offset + i * 360 / sides)
            a2 = math.radians(offset + (i+1) * 360 / sides)
            Triangle(points=[
                cx, cy,
                cx + r * math.cos(a1), cy + r * math.sin(a1),
                cx + r * math.cos(a2), cy + r * math.sin(a2),
            ])

    def _hp_label(self, text, cx, cy, font_size):
        lbl = CoreLabel(text=text, font_size=max(8, font_size), bold=True)
        lbl.refresh()
        tex = lbl.texture
        Color(1, 1, 1, 1)
        Rectangle(texture=tex,
                  pos=(cx - tex.width/2, cy - tex.height/2),
                  size=tex.size)

    # ── Touch input ───────────────────────────────────────────────────────────

    def on_touch_down(self, touch):
        self._touching = True
        self._update_angle(touch.pos)
        return True

    def on_touch_move(self, touch):
        if not self._touching:
            return False
        self._update_angle(touch.pos)
        return True

    def on_touch_up(self, touch):
        if not self._touching:
            return False
        self._touching = False
        angle = self._calc_angle(touch.pos)
        if angle is not None and self.on_angle_release:
            self.on_angle_release(angle)
        return True

    def _update_angle(self, pos):
        angle = self._calc_angle(pos)
        if angle is not None and self.on_angle_update:
            self.on_angle_update(angle)

    def _calc_angle(self, pos):
        # Cannon sits at top-centre of grid
        cannon_x = self._ox + self._grid_w / 2
        cannon_y = self._oy + self._grid_h * 0.92
        dx = pos[0] - cannon_x
        dy = pos[1] - cannon_y
        if abs(dx) < 3 and abs(dy) < 3:
            return None
        angle = math.degrees(math.atan2(dy, dx))
        # Normalize to 0-360
        angle = angle % 360
        # Force downward: allow 185 to 355
        if angle < 185:
            angle = 185
        if angle > 355:
            angle = 355
        self._aim_angle = angle
        return angle
