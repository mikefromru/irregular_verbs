from kivy.uix.screenmanager import Screen
import webbrowser
import datetime
from kivy.app import App
from tools.settings_local import whatsapp_link, telegram_link

class FaqScreen(Screen):

    def on_enter(self):
        current_year = datetime.date.today().year
        msg = f'(c) 2023-{current_year}. MFR'
        self.ids.fromtoyear.text = msg
        number_string = App.get_running_app().app_version 
        self.ids.app_version.text =  'Version ' + number_string

    def get_whatsapp(self):
        webbrowser.open(whatsapp_link)

    def get_telegram(self):
        webbrowser.open(telegram_link)

    def get_privacy_police(self):
        webbrowser.open('https://mikefromru.github.io/irregular_verbs/politica.html')

