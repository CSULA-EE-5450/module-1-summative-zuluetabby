from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

Builder.load_file('scenes/kivy_Screen/gameover.kv')


class GameOverScreen(Screen):
    def __init__(self, name, moves, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.player = name
        self.moves = moves

    def change_text(self):
        self.text_field.text = 'Game Over!'


class Button(Button):
    pass


class EndButton(Button):
    def on_release(self):
        screen_manager = App.get_running_app().screen_manager
        screen_manager.current = 'main'
