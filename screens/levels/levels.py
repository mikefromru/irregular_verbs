from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from screens.game.game import GameScreen
from tools.tools import create_screen
from kivy.clock import Clock

class LevelsScreen(Screen):

    def foo(self, i):
        create_screen('game.kv', 'game_screen', GameScreen)

    def on_enter(self):
        # Create Game screen if it does not exist
        Clock.schedule_once(self.foo, .1)
