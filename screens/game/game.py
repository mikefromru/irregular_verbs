from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import NumericProperty, StringProperty
import json
from kivy.animation import Animation
import random
from kivy.utils import rgba
from kivy.clock import Clock

from kivy.core.audio import SoundLoader
from playsound import playsound 
from kivy.utils import platform
# uix
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRoundFlatButton, MDRaisedButton, MDRoundFlatIconButton, MDIconButton

# mine
from tools.tools import create_screen
from ..finish.finish import FinishScreen

class GameScreen(Screen):
    
    level = StringProperty()
    shx = .5
    red_line = NumericProperty(0)
    height_line = NumericProperty(0)
    
    dialog_table_verbs = None
    dialog = None
    number_answer = NumericProperty(1)
    mistake = NumericProperty(0)

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

    def anim_widget_opacity_1(self, buttons):
        anim = Animation(opacity=1, duration=.3)
        anim.start(buttons)

    def remove(self):
        anim = Animation(opacity=0, duration=.3)

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
            self.red_line = 0
            self.remove_widget(self.btn)
            self.remove_widget(self.say_btn)
            self.ids.button_.disabled = True

            self.key_verb = self.verbs_list[0]
            self.ids.ru_verb.text = self.key_verb.capitalize()

            self.anim_widget_opacity_1(self.ids.ru_verb)
            self.anim_widget_opacity_1(self.ids.buttons_)

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
            self.manager.transition = FadeTransition(duration=.3)
            self.manager.current = 'finish_screen'

    def callback(self, instance):
        anim = Animation(opacity=1, duration=0)
        anim_icon_button = Animation(opacity=1, duration=0.2)
        anim1 = Animation(opacity=0, duration=0.3)
        self.ids.button_.disabled = False
        var = .50
        len_split_lb = len(self.ids.verbs.text.split())
        lb = self.ids.verbs.text.strip()

        if len_split_lb < 2:
            self.ids.verbs.text = lb + ' ' + instance.strip()

            anim.start(self.ids.verbs)
            self.ids.button_.opacity = 1

            self.move_backspace() # move backspace icon

        elif len_split_lb == 2:
            print(len_split_lb, ' <<<<<')
            self.ids.verbs.text = lb + ' ' + instance.strip()

            user_anser = self.ids.verbs.text.split()
            self.right_answer = self.data[self.key_verb]
            user_words_len = len(self.ids.verbs.text)

            self.number_answer += 1

            if user_words_len > 20:
                my_font_size = '16sp'
                self.height_line = user_words_len * 10
            else:
                my_font_size = '25sp'
                self.height_line = user_words_len * 16

            if user_anser == self.right_answer: # right answer
                
                # ru_verb = self.key_verb.partition(',')[0]
                self.ids.button_.opacity = 0
                self.ids.button_.disabled = True
                self.ids.ru_verb.opacity = 0
                self.ids.buttons_.opacity = 0
                color_text = '#28C38A'

            else:
                # wrong answer
                user_text = ' '.join(user_anser)
                bot_text = ' '.join(self.right_answer)

                self.red_line = 1
                self.mistake += 1
                ru_verb = self.key_verb.partition(',')[0]
                self.ids.verbs.text = f'[color=E30B5C][size={my_font_size}]{user_text}[/size][/color]\n[size=16sp]{bot_text}[/size]'

                color_text = '#ff0000'

                self.ids.button_.opacity = 0
                self.ids.button_.disabled = True
                self.ids.ru_verb.opacity = 0
                self.ids.buttons_.opacity = 0

            self.say_btn = MDRoundFlatIconButton(
                text='Прослушать', 
                icon='volume-high',
                text_color=rgba('#DCDCDC'),
                font_style='Overline',
                theme_icon_color='Custom',
                icon_color=rgba('#DCDCDC'),
                line_color=rgba('#DCDCDC'),
                pos_hint={'center_x': .5, 'center_y': .35},
                font_name='fonts/OpenSans/OpenSans-Medium.ttf'
            )
            self.say_btn.bind(on_press=self.say)
            self.add_widget(self.say_btn)

            self.btn = MDRoundFlatButton(
                text='Дальше', 
                text_color=rgba(color_text),
                md_bg_color=rgba('#ffffff'),
                pos_hint={'center_x': .5, 'center_y': .45},
                font_name='fonts/OpenSans/OpenSans-Medium.ttf'
            )
            self.btn.bind(on_press=self.next)
            self.add_widget(self.btn)
        else:
            pass

    def say(self, instance):
        mytext = ' '.join(self.right_answer)
        name = self.right_answer[0] + '.ogg'

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
                Snackbar(text='Файл недоступен').open()

    def foo(self, *args):
        print('I am a Snackbar')

    def close_app(self, *args):
        sys.exit()

    def widgets(self, i):
        create_screen('finish.kv', 'finish_screen', FinishScreen)
        FinishScreen.level = self.level
        with open(f'json_files/{self.level}.json', 'r') as f:
            self.data = json.load(f)

            self.key_verb = ''
        
        self.number_answer = 1
        self.ids.hublet.text = f'{self.number_answer}/{len(self.data)}'
        self.ids.verbs.text = ''
        self.mistake = 0

        self.verbs_list = list(self.data.keys())
        self.verbs_list = self.verbs_list#[0:3]
        random.shuffle(self.verbs_list)
        self.key_verb = self.verbs_list[0]

        self.ids.ru_verb.text = self.key_verb.capitalize()

        # Show Russsian verb and buttons slowly
        self.anim_widget_opacity_1(self.ids.ru_verb)
        self.anim_widget_opacity_1(self.ids.buttons_) 

        list_buttons = self.get_buttons() # shuffle list for buttons

        self.ids.button1.text = list_buttons[0]
        self.ids.button2.text = list_buttons[1]
        self.ids.button3.text = list_buttons[2]
        self.ids.button4.text = list_buttons[3]
        self.ids.button5.text = list_buttons[4]
        self.ids.button6.text = list_buttons[5]
        self.verbs_list.pop(0)

    def on_enter(self):
        Clock.schedule_once(self.widgets, 0.1)

    def on_leave(self):
        try:
            self.remove_widget(self.say_btn)
        except:
            pass

        try:
            # Remove button 'Дальше'
            self.remove_widget(self.btn)
        except:
            pass

        self.red_line = 0
        self.ids.button_.disabled = True
        self.ids.ru_verb.text = ''
        self.ids.ru_verb.opacity = 0
        self.ids.verbs.text = ''
        self.ids.button_.opacity = 0
        self.ids.buttons_.opacity = 0
