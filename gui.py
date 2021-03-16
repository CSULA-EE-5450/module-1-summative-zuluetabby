import pygame
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
import app.screen

Config.set('input', 'mouse', 'mouse')


class ScreenManagement(ScreenManager):
    pass


class Battleship(App):
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Battleship, self).__init__(**kwargs)
        self.screen_manager = Builder.load_file('app/screen/kv/screenmanager.kv')

    def build(self):
        return self.screen_manager


if __name__ == "__main__":
    Battleship().run()
