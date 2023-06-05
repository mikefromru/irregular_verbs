from kivy.uix.screenmanager import Screen
import webbrowser
import datetime
from kivy.app import App
from tools.settings_local import (
    whatsapp_link, 
    telegram_link,
    telegram_bot,
    privacy_police,
)

class FaqScreen(Screen):

    def on_enter(self):
        current_year = datetime.date.today().year
        msg = f'(c) 2023-{current_year}. MFR'
        self.ids.fromtoyear.text = msg
        number_string = App.get_running_app().app_version 
        self.ids.app_version.text =  'Version ' + number_string

    def get_link(self, instance):
        if instance == 'telegram_bot':
            webbrowser.open(telegram_bot)
        elif instance == 'whatsapp_link':
            webbrowser.open(whatsapp_link)
        elif instance == 'telegram_link':
            webbrowser.open(telegram_link)
        elif instance == 'privacy_police':
            webbrowser.open(privacy_police)
