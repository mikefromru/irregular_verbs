from kivymd.app import MDApp
from kivy.app import App
import plyer
import json
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.animation import Animation

from kivy.utils import platform
from kivy.core.window import Window

from kivy.metrics import dp

from kivy.utils import escape_markup

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRoundFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import (
    NoTransition,
    SlideTransition,
    CardTransition,
    SwapTransition,
    FadeTransition,
    WipeTransition,
    FallOutTransition,
    RiseInTransition
)

import random
import sys

from kivy.core.window import Window
from kivy.utils import rgba

from tools.tools import get_number

if platform != 'android':
    Window.size = (350, 750)
    Window.top = 70
    Window.right = 70

class MenuScreen(Screen):
    
    def close_app(self):
        sys.exit()

class FinishScreen(Screen):
 
    mistake_ = NumericProperty(0)

    def __init__(self, **kwargs):
        super(FinishScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.ids.finish.text = get_number(self.mistake_)
        IndexScreen.number_answer = 1

class TableScreen(Screen):
    def my_table(self, *args):

        with open('verbs.json', 'r') as f:
            self.data = json.load(f)

        gl = GridLayout(cols=3, padding=dp(20), spacing=dp(20), size_hint=(1, None))
        gl.bind(minimum_height=gl.setter('height'))
        gl.add_widget(MDLabel(text='Infinitive', bold=True, halign='center'))
        gl.add_widget(MDLabel(text='Past Simple', bold=True, halign='center'))
        gl.add_widget(MDLabel(text='Participle II', bold=True, halign='center'))

        for x in self.data:
            key_ru = f'[size=10sp][i]{x}[/i][/size]'
            zero = '[size=18sp]{}[/size]'.format(self.data[x][0])
            first = '[size=18sp]{}[/size]'.format(self.data[x][1])
            second = '[size=18sp]{}[/size]'.format(self.data[x][2])
            gl.add_widget(MDLabel(text='\n' + zero + '\n' + key_ru, size_hint_y=None, halign='center', height=dp(40), markup=True))
            gl.add_widget(MDLabel(text=first.replace(' ', ''), size_hint_y=None, halign='center', height=dp(40), markup=True))
            gl.add_widget(MDLabel(text=second.replace(' ', ''), size_hint_y=None, halign='center', height=dp(40), markup=True))
        self.sc = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.sc.add_widget(gl)
        self.add_widget(self.sc)

        self.btn = MDRaisedButton(text='Закрыть', pos_hint={'center_x': 0.5})
        self.btn.bind(on_press=self.callback)
        self.add_widget(self.btn)

    def check_j(self, i):
        self.remove_widget(self.loading)
        self.my_table()
    
    def on_enter(self, *args):
        self.loading = MDLabel(text='Loading ...', halign='center')
        self.add_widget(self.loading)
        Clock.schedule_once(self.check_j, 0.5)

    def on_leave(self, *args):
        self.remove_widget(self.sc)
        self.remove_widget(self.btn)

    def callback(self, instance):
        self.manager.current = 'menu_screen'

class IndexScreen(Screen):

    red_line = NumericProperty(0)
    height_line = NumericProperty(0)
    
    dialog_table_verbs = None
    dialog = None
    number_answer = NumericProperty(1)
    mistake = NumericProperty(0)

    def __init__(self, **kwargs):
        super(IndexScreen, self).__init__(**kwargs)

    def get_buttons(self):
        btns = self.data.get(self.key_verb)
        btns = list(set(btns))

        s = []
        for x in self.data.values():
            for j in x:
                s.append(j)

        random.shuffle(s)

        for x in btns:
            s.remove(x)

        if len(btns) == 1: amount = 5
        if len(btns) == 2: amount = 4
        if len(btns) == 3: amount = 3

        random_ = random.sample(s, amount) + btns
        random.shuffle(random_)
        return random_
    
    def remove(self):
        anim = Animation(opacity=0, duration=0.3)

        lb = self.ids.verbs.text.split()

        try:
            lb.pop()
        except:
            pass

        if len(lb) == 0:
            anim.start(self.ids.button_)
        else:
            pass

        self.ids.verbs.text = ''.join(lb)
        self.move_backspace() # move backspace icon

    def move_backspace(self):
        self.ids.verbs.font_size = '25sp'
        len_user_words = len(self.ids.verbs.text)
        if len_user_words < 5:
            var = .69
        elif len_user_words >= 5 and len_user_words < 8:
            var = .75
        elif len_user_words >= 8 and len_user_words < 10:
            var = .8
        elif len_user_words >= 10 and len_user_words < 12:
            var = .85
        elif len_user_words >=12 and len_user_words <= 15:
            self.ids.verbs.font_size = '22sp'
            var = .9
        elif len_user_words > 20:
            self.ids.verbs.font_size = '18sp'
            var = .9
        else:
            var = .95
        self.ids.button_.pos_hint = {'center_x': var, 'center_y': 0.5}

    def next(self, *args):
        try:
            print(f'{self.mistake=}')
                
            self.red_line = 0

            self.remove_widget(self.btn)
            self.ids.button_.opacity = 0
            self.ids.button_.disabled = True
            self.ids.buttons_.opacity = 1

            self.key_verb = self.verbs_list[0]
            self.ids.ru_verb.text = self.key_verb.capitalize()

            list_buttons = self.get_buttons() # shuffle list for buttons
            self.number_answer += 0        
            self.ids.hublet.text = f'{self.number_answer}/{len(self.data)}'
            self.ids.verbs.text = ''

            self.ids.button1.text = list_buttons[0]
            self.ids.button2.text = list_buttons[1]
            self.ids.button3.text = list_buttons[2]
            self.ids.button4.text = list_buttons[3]
            self.ids.button5.text = list_buttons[4]
            self.ids.button6.text = list_buttons[5]

            self.verbs_list.pop(0)
            self.var = .5

        except IndexError as er:
            print(self.mistake)
            FinishScreen.mistake_ = self.mistake
            self.manager.current = 'finish_screen'

    def callback(self, instance):
        anim = Animation(opacity=1, duration=0.1)
        anim_icon_button = Animation(opacity=1, duration=0.2)
        anim1 = Animation(opacity=0, duration=0.3)
        #instance = 'understand'
        self.ids.button_.disabled = False
        var = .50
        len_split_lb = len(self.ids.verbs.text.split())
        lb = self.ids.verbs.text.strip()

        if len_split_lb < 2:
            self.ids.verbs.text = lb + ' ' + instance.strip()

            anim.start(self.ids.verbs)
            anim_icon_button.start(self.ids.button_)

            self.move_backspace() # move backspace icon

        elif len_split_lb == 2:
            print(len_split_lb, ' <<<<<')
            self.ids.verbs.text = lb + ' ' + instance.strip()

            user_anser = self.ids.verbs.text.split()
            right_answer = self.data[self.key_verb]
            user_words_len = len(self.ids.verbs.text)

            self.number_answer += 1

            if user_words_len > 20:
                my_font_size = '16sp'
                self.height_line = user_words_len * 10
            else:
                my_font_size = '25sp'
                self.height_line = user_words_len * 16

            if user_anser == right_answer: # right answer
 
                ru_verb = self.key_verb.partition(',')[0]
                self.ids.button_.opacity = 0
                self.ids.button_.disabled = True

                self.ids.buttons_.opacity = 0
                color_text = '#28C38A'

            else:
                # wrong answer
                self.red_line = 1
                self.mistake += 1
                user_text = ' '.join(user_anser)
                bot_text = ' '.join(right_answer)
                ru_verb = self.key_verb.partition(',')[0]
                self.ids.verbs.text = f'[color=E30B5C][size={my_font_size}]{user_text}[/size][/color]\n[size=16sp]{bot_text}[/size]'

                color_text = '#ff0000'

                self.ids.button_.opacity = 0
                self.ids.button_.disabled = True
                self.ids.buttons_.opacity = 0


            self.btn = MDRoundFlatButton(
                text='Дальше', 
                text_color=rgba(color_text),
                md_bg_color=rgba('#ffffff'),
                pos_hint={'center_x': .5, 'center_y': .4},
                font_name='fonts/roboto-mono/roboto-mono-medium.ttf'
            )
            self.btn.bind(on_press=self.next)
            self.add_widget(self.btn)

        else:
            pass

    def foo(self, *args):
        print('I am a Snackbar')

    def close_app(self, *args):
        sys.exit()

    def on_enter(self, *args):
        with open('verbs.json', 'r') as f:
            self.data = json.load(f)

            self.key_verb = ''
        
        self.number_answer = 1
        self.ids.hublet.text = f'{self.number_answer}/{len(self.data)}'
        self.ids.button_.opacity = 0
        self.ids.verbs.text = ''
        self.mistake = 0

        self.verbs_list = list(self.data.keys())
        self.verbs_list = self.verbs_list[0:6]
        random.shuffle(self.verbs_list)
        self.key_verb = self.verbs_list[0]

        self.ids.ru_verb.text = self.key_verb.capitalize()

        list_buttons = self.get_buttons() # shuffle list for buttons

        self.ids.button1.text = list_buttons[0]
        self.ids.button2.text = list_buttons[1]
        self.ids.button3.text = list_buttons[2]
        self.ids.button4.text = list_buttons[3]
        self.ids.button5.text = list_buttons[4]
        self.ids.button6.text = list_buttons[5]

        self.verbs_list.pop(0)

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):

    def build(self):
        root = Builder.load_file('index.kv')

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "A700"
        self.window_manager = WindowManager(transition=NoTransition())

        return self.window_manager
    
if __name__ == '__main__':
    MainApp().run()
