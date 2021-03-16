import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager


class ScreenManage(ScreenManager):
    pass


class Battleship(App):
    """
    The class for the Battleship APP. Responsible for changing screens/ scenes.
    """
    screen_manager = ObjectProperty(None)
    game = None

    def __init__(self, **kwargs):
        super(Battleship, self).__init__(**kwargs)  # Inherits this class
        self.screen_manager = Builder.load_file('INSERT FILE TO SCREEN MANGER FAM')

    def build(self):
        return self.screen_manager


if __name__ == "__main__":
    app_instance = Battleship()
    app_instance.run()
