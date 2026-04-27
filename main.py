"""
main.py - Entry point for Ball Blast.
Run: python3 main.py
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from screens import HomeScreen, SettingsScreen, GameScreen


class BallBlastApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    BallBlastApp().run()
