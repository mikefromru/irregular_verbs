from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty

import webbrowser

from tools.tools import get_number

class FinishScreen(Screen):
    
    level = StringProperty()
    mistake_ = NumericProperty(0)

    def on_enter(self):
        self.ids.level_name.text = f'{self.level.capitalize()}'
        self.ids.finish.text = get_number(self.mistake_)

    def get_gneppa(self):
        webbrowser.open('https://gneppa.com')
    
    def on_leave(self):
        self.ids.level_name.text = ''
