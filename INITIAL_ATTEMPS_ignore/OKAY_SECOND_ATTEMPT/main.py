from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager

Config.set('input', 'mouse', None)


class ScreenManagement(ScreenManager):
    pass


class Battleship(App):
    screen_manager = ObjectProperty(None)
    game = None

    def __init__(self, **kwargs):
        super(Battleship, self).__init__(**kwargs)
        self.screen_manager = Builder.load_file('scenes/kivy_screen/screenmanager.kv')

    def build(self):
        return self.screen_manager


if __name__ == "__main__":
    app_instance = Battleship()
    app_instance.run()
