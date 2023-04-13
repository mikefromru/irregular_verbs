from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from kivy.metrics import dp
import json
from kivy.clock import Clock
from pathlib import Path
from playsound import playsound 

# uix
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import ImageLeftWidget, IconLeftWidget, IconRightWidget
from kivymd.uix.list import (
    OneLineListItem, 
    OneLineAvatarListItem,
    TwoLineIconListItem,
    TwoLineAvatarListItem,
    TwoLineAvatarIconListItem,
    OneLineAvatarIconListItem,
    ILeftBody,
    IRightBody,
)

# property
from kivy.properties import (
    NumericProperty, 
    StringProperty,
    ObjectProperty,
)

class Tab(MDFloatLayout, MDTabsBase):
    pass

class MyContainer(MDBoxLayout):

    name = StringProperty()
    text = StringProperty()
    secondary_text = StringProperty()
    past = StringProperty()
    finished = StringProperty()
    past_future = StringProperty()

    def volume(self, instance):
        TableScreen.say(instance.text)
        print(instance.text)

class TableScreen(Screen):

    page_true = True
    count = 20
    total_pages = NumericProperty()
    current_page = NumericProperty(1) 
    slice1, slice2 = 0, 20

    def __init__(self, **kwargs):
        super(TableScreen, self).__init__(**kwargs)
        self.loading = MDLabel(text='[size=16sp]Loading ...[/size]', halign='center', markup=True)
        self.add_widget(self.loading)

    def say(self):
        path_sound = Path(f'sounds/{self}' + '.ogg')
        if path_sound.exists():
            name = self + '.ogg'
            if platform != 'android':
                try:
                    playsound('sounds/' + name)
                except:
                    print('Not found')
            else:
                try:
                    sound = SoundLoader.load('sounds/' + name)
                    sound.play()
                except:
                    print('something went wrong')
        else:
            Snackbar(text='Файл недоступен').open()

    def add_widgets(self, i):
        bgr = [
            {

                'name': self.beginner_data[x][0],
                'text': self.beginner_data[x][0],
                'past': self.beginner_data[x][1],
                'finished': self.beginner_data[x][2],
                'secondary_text':x, 
            } for x in self.beginner_data]

        imd = [
            {
                'name': self.intermediate_data[x][0],
                'text': self.intermediate_data[x][0],
                'past': self.intermediate_data[x][1],
                'finished': self.intermediate_data[x][2],
                'secondary_text':x, 
            } for x in self.intermediate_data]

        acd = [
            {

                'name': self.advanced_data[x][0],
                'text': self.advanced_data[x][0],
                'past': self.advanced_data[x][1],
                'finished': self.advanced_data[x][2],
                'secondary_text':x, 
            } for x in self.advanced_data]
        
        self.ids.beginner_rv.data = bgr
        self.ids.intermediate_rv.data = imd
        self.ids.advanced_rv.data = acd
        self.remove_widget(self.loading)

    def on_enter(self, *args):
        with open('json_files/beginner.json', 'r') as f:
            self.beginner_data = json.load(f)
        with open('json_files/intermediate.json', 'r') as f:
            self.intermediate_data = json.load(f)
        with open('json_files/advanced.json', 'r') as f:
            self.advanced_data = json.load(f)

        Clock.schedule_once(self.add_widgets, .1)

    def callback(self, instance):
        self.manager.current = 'menu_screen'
