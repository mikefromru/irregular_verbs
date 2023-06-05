from kivymd.app import MDApp
import kivy
from kivy.lang import Builder

from kivy.animation import Animation
from kivy.utils import platform
import platform as pl

from kivy.core.text import LabelBase
from kivy.core.window import Window

from kivy.clock import Clock

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

import sys
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard

# mine Screens
from screens.levels.levels import LevelsScreen
from screens.table.table import TableScreen
from screens.finish.finish import FinishScreen
from screens.faq.faq import FaqScreen

__version__ = '1.2'

if platform != 'android':
    Window.size = (350, 750)
    Window.top = 70
    Window.right = 70


class MenuScreen(Screen):

    #from jnius import autoclass
    def share(self):
        title = 'Title'
        appgallery = 'https://appgallery.huawei.com/app/C107717287'
        google_play = 'https://play.google.com/store/apps/details?id=org.irregular_verbs.irregular_verbs'
        text = f"AppGallery:  {appgallery} \n\n Google Play: {google_play}"
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(text)))
            intent.setType('text/plain')
            chooser = Intent.createChooser(intent, String(title))
            PythonActivity.mActivity.startActivity(chooser)
        else:
            Clipboard.copy(text)

    def close_app(self):
        sys.exit()

class MainApp(MDApp):

    app_version = __version__

    def on_key(self, window, key, *args):
        if key == 27:  # the esc key
            if self.sm.current == 'menu_screen':
                return False
            else:
                self.sm.transition = FadeTransition(duration=.1)
                self.sm.current = "menu_screen"
            return True

    def build(self):
        Builder.load_file('main.kv')
        Builder.load_file('screens/table/table.kv')
        Builder.load_file('screens/levels/levels.kv')
        Builder.load_file('screens/faq/faq.kv')

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        #self.theme_cls.primary_hue = "A699"
        Window.bind(on_keyboard=self.on_key)

        self.sm = ScreenManager()
        self.sm = ScreenManager(transition=FadeTransition(duration=.1))

        # Create some screens 
        self.sm.add_widget(MenuScreen(name='menu_screen'))
        self.sm.add_widget(LevelsScreen(name='levels_screen'))
        self.sm.add_widget(TableScreen(name='table_screen'))
        self.sm.add_widget(FaqScreen(name='faq_screen'))
        return self.sm
    
if __name__ == '__main__':
    LabelBase.register(name='OpenSans',
        fn_regular='fonts/OpenSans/OpenSans-Regular.ttf',
        fn_italic='fonts/OpenSans/OpenSans-Italic.ttf',
        fn_bold='fonts/OpenSans/OpenSans-Bold.ttf',
        fn_bolditalic='fonts/OpenSans/OpenSans-BoldItalic.ttf',
    )
    MainApp().run()
