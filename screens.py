"""
screens.py - All screens for Ball Blast.
Uses separate screens instead of overlays to avoid touch issues on Android.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle

from config import (
    GRID_COLS, GRID_ROWS,
    C_HUD_BG, C_BTN_PLAY, C_BTN_DARK, C_BTN_DANGER,
)
from save import (
    load_high_score, save_high_score,
    load_ball_count, save_ball_count, reset_all,
)
from grid import Grid
from ball import Ball
from cannon import Cannon
from game_widget import GameWidget


# ── Helper ────────────────────────────────────────────────────────────────────

def make_btn(text, bg, font_size='20sp', bold=False,
             size_hint=(1, None), height=52):
    return Button(
        text=text, font_size=font_size, bold=bold,
        background_color=bg, background_normal='',
        size_hint=size_hint, height=height,
    )


# ── Home Screen ───────────────────────────────────────────────────────────────

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()
        with root.canvas.before:
            Color(0.04, 0.07, 0.18, 1)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda w, v: setattr(self._bg, 'pos', v),
            size=lambda w, v: setattr(self._bg, 'size', v),
        )

        layout = BoxLayout(
            orientation='vertical', padding=50, spacing=22,
            size_hint=(0.85, 0.85),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        self.hs_label = Label(
            text=f'Best: {load_high_score()}',
            font_size='18sp', color=(0.95, 0.85, 0.10, 1),
            halign='right', text_size=(400, None),
        )
        layout.add_widget(self.hs_label)

        layout.add_widget(Label(
            text='BALL BLAST',
            font_size='52sp', bold=True,
            color=(1.0, 0.55, 0.10, 1),
            halign='center', size_hint=(1, 0.35),
        ))

        layout.add_widget(Label(
            text='[i][color=4499ff]By Bryte[/color][/i]',
            font_size='22sp', markup=True,
            halign='center', size_hint=(1, None), height=36,
        ))

        layout.add_widget(Widget(size_hint=(1, 0.05)))

        play_btn = make_btn('PLAY', C_BTN_PLAY,
                            font_size='30sp', bold=True, height=64)
        play_btn.bind(on_press=lambda *_: setattr(
            self.manager, 'current', 'game'))
        layout.add_widget(play_btn)

        settings_btn = make_btn('Settings', C_BTN_DARK, height=50)
        settings_btn.bind(on_press=lambda *_: setattr(
            self.manager, 'current', 'settings'))
        layout.add_widget(settings_btn)

        root.add_widget(layout)
        self.add_widget(root)

    def on_pre_enter(self, *_):
        self.hs_label.text = f'Best: {load_high_score()}'


# ── Settings Screen ───────────────────────────────────────────────────────────

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()
        with root.canvas.before:
            Color(0.04, 0.07, 0.18, 1)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda w, v: setattr(self._bg, 'pos', v),
            size=lambda w, v: setattr(self._bg, 'size', v),
        )

        layout = BoxLayout(
            orientation='vertical', padding=40, spacing=18,
            size_hint=(0.85, 0.85),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        top = BoxLayout(size_hint=(1, None), height=52, spacing=12)
        back = make_btn('Back', C_BTN_DARK,
                        font_size='18sp', size_hint=(None, 1), height=52)
        back.width = 100
        back.bind(on_press=lambda *_: setattr(
            self.manager, 'current', 'home'))
        top.add_widget(back)
        top.add_widget(Label(
            text='Settings', font_size='26sp', bold=True,
            color=(1, 1, 1, 1),
        ))
        layout.add_widget(top)

        layout.add_widget(Widget(size_hint=(1, 0.05)))

        reset_hs = make_btn('Reset High Score', C_BTN_DANGER)
        reset_hs.bind(on_press=lambda *_: save_high_score(0))
        layout.add_widget(reset_hs)

        reset_balls = make_btn('Reset Ball Count',
                               (0.45, 0.10, 0.55, 1))
        reset_balls.bind(on_press=lambda *_: save_ball_count(1))
        layout.add_widget(reset_balls)

        layout.add_widget(Label(
            text='Ball Color', font_size='18sp',
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, None), height=36,
        ))

        color_row = BoxLayout(spacing=10, size_hint=(1, None), height=52)
        for name, clr in [
            ('Orange', (1.00, 0.55, 0.10, 1)),
            ('Cyan',   (0.20, 0.85, 0.95, 1)),
            ('White',  (0.95, 0.95, 0.95, 1)),
            ('Pink',   (0.95, 0.35, 0.65, 1)),
        ]:
            b = make_btn(name, clr, font_size='15sp',
                         size_hint=(1, None), height=52)
            b.bind(on_press=lambda btn, c=clr: self._set_color(c))
            color_row.add_widget(b)
        layout.add_widget(color_row)

        root.add_widget(layout)
        self.add_widget(root)

    def _set_color(self, color):
        import config
        config.C_BALL = color


# ── Game Over Screen ──────────────────────────────────────────────────────────

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()
        with root.canvas.before:
            Color(0.04, 0.07, 0.18, 0.97)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda w, v: setattr(self._bg, 'pos', v),
            size=lambda w, v: setattr(self._bg, 'size', v),
        )

        panel = BoxLayout(
            orientation='vertical', padding=30, spacing=16,
            size_hint=(0.82, 0.65),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        with panel.canvas.before:
            Color(0.06, 0.10, 0.28, 1)
            self._panel_bg = RoundedRectangle(
                pos=panel.pos, size=panel.size, radius=[20])
        panel.bind(
            pos=lambda w, v: setattr(self._panel_bg, 'pos', v),
            size=lambda w, v: setattr(self._panel_bg, 'size', v),
        )

        panel.add_widget(Label(
            text='GAME OVER',
            font_size='36sp', bold=True,
            color=(0.95, 0.20, 0.20, 1),
        ))

        self.score_label = Label(
            text='Score: 0', font_size='26sp', color=(1, 1, 1, 1))
        self.hs_label = Label(
            text='Best: 0', font_size='20sp',
            color=(0.95, 0.85, 0.10, 1))
        panel.add_widget(self.score_label)
        panel.add_widget(self.hs_label)

        self.watch_btn = make_btn(
            'Watch Ad to Continue',
            (0.10, 0.55, 0.15, 1), height=56)
        self.watch_btn.bind(on_press=self._watch_ad)
        panel.add_widget(self.watch_btn)

        restart_btn = make_btn('Restart', (0.25, 0.25, 0.35, 1))
        restart_btn.bind(on_press=self._restart)
        panel.add_widget(restart_btn)

        menu_btn = make_btn('Main Menu', C_BTN_DARK)
        menu_btn.bind(on_press=lambda *_: setattr(
            self.manager, 'current', 'home'))
        panel.add_widget(menu_btn)

        root.add_widget(panel)
        self.add_widget(root)

    def setup(self, score: int):
        self.score_label.text = f'Score: {score}'
        self.hs_label.text    = f'Best: {load_high_score()}'
        self.watch_btn.text     = 'Watch Ad to Continue'
        self.watch_btn.disabled = False

    def _restart(self, *_):
        gs = self.manager.get_screen('game')
        gs.restart()
        self.manager.current = 'game'

    def _watch_ad(self, *_):
        self.watch_btn.text     = 'Watching ad...  5'
        self.watch_btn.disabled = True
        self._countdown = 5
        Clock.schedule_interval(self._ad_tick, 1)

    def _ad_tick(self, dt):
        self._countdown -= 1
        if self._countdown <= 0:
            Clock.unschedule(self._ad_tick)
            gs = self.manager.get_screen('game')
            gs.continue_after_ad()
            self.manager.current = 'game'
        else:
            self.watch_btn.text = f'Watching ad...  {self._countdown}'


# ── Game Screen ───────────────────────────────────────────────────────────────

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._grid       = None
        self._balls      = []
        self._cannon     = Cannon()
        self._score      = 0
        self._ball_count = 1
        self._aim_angle  = 270.0
        self._state      = 'aiming'
        self._paused     = False

        main = BoxLayout(orientation='vertical')

        # ── Top HUD ───────────────────────────────────────────────────────────
        top_hud = BoxLayout(size_hint=(1, None), height=54,
                            padding=(12, 6), spacing=6)
        with top_hud.canvas.before:
            Color(*C_HUD_BG)
            self._hud_bg = Rectangle(pos=top_hud.pos, size=top_hud.size)
        top_hud.bind(
            pos=lambda w, v: setattr(self._hud_bg, 'pos', v),
            size=lambda w, v: setattr(self._hud_bg, 'size', v),
        )

        self.balls_label = Label(
            text='Balls: 1', font_size='19sp', bold=True,
            color=(1.0, 0.75, 0.20, 1),
            halign='left', size_hint=(0.35, 1),
        )
        self.score_label = Label(
            text='Score: 0', font_size='19sp', bold=True,
            color=(1, 1, 1, 1),
            halign='center', size_hint=(0.4, 1),
        )
        self.pause_btn = make_btn(
            'II', (0.15, 0.20, 0.55, 1),
            font_size='18sp', bold=True,
            size_hint=(0.25, 1), height=54,
        )
        self.pause_btn.bind(on_press=self._toggle_pause)
        top_hud.add_widget(self.balls_label)
        top_hud.add_widget(self.score_label)
        top_hud.add_widget(self.pause_btn)
        main.add_widget(top_hud)

        # ── Game widget ───────────────────────────────────────────────────────
        self.gw = GameWidget()
        self.gw.on_angle_update  = self._on_aim_update
        self.gw.on_angle_release = self._on_aim_release
        main.add_widget(self.gw)

        # ── Bottom HUD ────────────────────────────────────────────────────────
        bot_hud = BoxLayout(size_hint=(1, None), height=46, padding=(12, 6))
        with bot_hud.canvas.before:
            Color(*C_HUD_BG)
            self._bhud = Rectangle(pos=bot_hud.pos, size=bot_hud.size)
        bot_hud.bind(
            pos=lambda w, v: setattr(self._bhud, 'pos', v),
            size=lambda w, v: setattr(self._bhud, 'size', v),
        )
        self.wave_label = Label(
            text='Wave 1', font_size='17sp',
            color=(0.7, 0.85, 1.0, 1),
            halign='left', size_hint=(0.5, 1),
        )
        self.info_label = Label(
            text='Tap anywhere to shoot',
            font_size='13sp', color=(0.6, 0.6, 0.7, 1),
            halign='right', size_hint=(0.5, 1),
        )
        bot_hud.add_widget(self.wave_label)
        bot_hud.add_widget(self.info_label)
        main.add_widget(bot_hud)

        self.add_widget(main)

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def on_pre_enter(self, *_):
        if self._grid is None:
            self._init_game()
        Clock.unschedule(self._tick)
        Clock.schedule_interval(self._tick, 1 / 60)

    def on_leave(self, *_):
        Clock.unschedule(self._tick)

    # ── Game init ─────────────────────────────────────────────────────────────

    def _init_game(self):
        self._grid       = Grid()
        self._grid.add_new_row()
        self._balls      = []
        self._score      = 0
        self._ball_count = load_ball_count()
        self._state      = 'aiming'
        self._paused     = False
        self.pause_btn.text  = 'II'
        self.info_label.text = 'Tap anywhere to shoot'
        self._refresh_hud()
        self._draw()

    def restart(self):
        """Called from GameOverScreen restart button."""
        self._grid = None
        self._balls = []
        self._init_game()
        Clock.unschedule(self._tick)
        Clock.schedule_interval(self._tick, 1 / 60)

    def continue_after_ad(self):
        """Called from GameOverScreen after watching ad."""
        self._state  = 'aiming'
        self._paused = False
        self._balls  = []
        self.info_label.text = 'Tap anywhere to shoot'
        Clock.unschedule(self._tick)
        Clock.schedule_interval(self._tick, 1 / 60)
        self._draw()

    # ── Pause ─────────────────────────────────────────────────────────────────

    def _toggle_pause(self, *_):
        self._paused = not self._paused
        self.pause_btn.text = '>' if self._paused else 'II'

    # ── Game loop ─────────────────────────────────────────────────────────────

    def _tick(self, dt):
        if self._paused:
            return

        self._grid.tick(dt)

        if self._state == 'shooting':
            cx, cy = self._cannon_pos()
            done   = self._cannon.tick(dt, cx, cy)
            self._balls.extend(self._cannon.new_balls)
            self._update_balls(dt)
            self._draw()

            if done and all(not b.alive for b in self._balls):
                self._end_round()

        elif self._state == 'aiming':
            self._draw()

    def _cannon_pos(self):
        cell   = min(self.gw.width / GRID_COLS, self.gw.height / GRID_ROWS)
        grid_w = cell * GRID_COLS
        grid_h = cell * GRID_ROWS
        return grid_w / 2.0, grid_h - cell * 0.55

    def _update_balls(self, dt):
        cell   = min(self.gw.width / GRID_COLS, self.gw.height / GRID_ROWS)
        grid_w = cell * GRID_COLS
        grid_h = cell * GRID_ROWS

        for ball in self._balls:
            if not ball.alive:
                continue

            # Use swept collision — pass blocks dict directly
            col, row = ball.move(dt, grid_w, grid_h, cell,
                                 self._grid.blocks)

            if not ball.alive:
                continue

            if col is not None:
                destroyed, is_pu = self._grid.hit_block(col, row)
                if is_pu:
                    self._ball_count += 1
                    save_ball_count(self._ball_count)
                else:
                    self._score += 1

                if self._grid.is_game_over():
                    self._trigger_game_over()
                    return

        self._refresh_hud()

    def _end_round(self):
        self._grid.add_new_row()

        if self._grid.is_game_over():
            self._trigger_game_over()
            return

        self._balls      = []
        self._state      = 'aiming'
        self.info_label.text = 'Tap anywhere to shoot'
        save_high_score(self._score)
        self._refresh_hud()
        self._draw()

    def _trigger_game_over(self):
        Clock.unschedule(self._tick)
        save_high_score(self._score)
        go = self.manager.get_screen('gameover')
        go.setup(self._score)
        self.manager.current = 'gameover'

    # ── Input ─────────────────────────────────────────────────────────────────

    def _on_aim_update(self, angle):
        if self._state == 'aiming' and not self._paused:
            self._aim_angle = angle
            self._draw()

    def _on_aim_release(self, angle):
        if self._state != 'aiming' or self._paused:
            return
        self._aim_angle      = angle
        self._state          = 'shooting'
        self.info_label.text = ''
        import config
        self._cannon.start_firing(angle, self._ball_count, config.C_BALL)

    # ── HUD ───────────────────────────────────────────────────────────────────

    def _refresh_hud(self):
        self.balls_label.text = f'Balls: {self._ball_count}'
        self.score_label.text = f'Score: {self._score}'
        self.wave_label.text  = f'Wave {self._grid.wave}'

    def _draw(self):
        cx, cy = self._cannon_pos()
        self.gw.draw(
            self._grid, self._balls,
            aiming=(self._state == 'aiming'),
            aim_angle=self._aim_angle,
            cannon_x=cx, cannon_y=cy,
        )
