from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('app/screen/kv/gameoverscreen.kv')


class GameOverScreen(Screen):
    def __init__(self, name, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.player = name

    def change_text(self):
        self.text_field.text = 'Game over!'

