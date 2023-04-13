from kivymd.app import MDApp
from kivy.lang import Builder
from pathlib import Path
import os

def create_screen(kv_file, screen, GameScreen):
    ''' To create a new screen if it does not exist'''
    if not MDApp.get_running_app().sm.has_screen(name=screen):
        # Conver imutuble type Tuple to List
        # for changing file extension 
        name = list(os.path.splitext(kv_file))
        if name[1] == '':
            name[1] = '.kv'
        Builder.load_file(f'screens/{name[0]}/{name[0]}{name[1]}') 
        MDApp.get_running_app().sm.add_widget(GameScreen(name=screen))

def get_number(mistake):
    if mistake == 0:
        return 'Поздравляю!\nЭто лучший результат!'
    elif mistake == 1:
        return ' Хороший результат\nВы сделали одну ошибку'
    elif mistake >= 2 and mistake < 5:
        return f'Ваш результат\nВы сделали {mistake} ошибки'
    elif mistake >= 5 and mistake <= 20:
        return f'Ваш результат\nВы сделали {mistake} ошибoк'
    else:
        return f'Ваш результат\nВы сделали больше 20 ошибок'

def main():
    pass

if __name__ == '__main__':
    main()
