from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from scenes.battleship_game import multiplayer_init, player_vs_mode
from scenes.battleship_game import Battleship
from scenes.player import PlayerScreen
from scenes.player_moves import Player, ThePlayer
from kivy.uix.button import Button

Builder.load_file('scenes/kivy_screen/menu.kv')
first_time = True


def clear():
    """
    Clears a session.
    """
    screen_manager = App.get_running_app().screen_manager
    if App.get_running_app().game:
        del App.get_running_app().game

    screen = screen_manager.get_screen('ship_selection')
    screen.clear()

    screen = screen_manager.get_screen('player1')
    if screen is True:
        screen_manager.remove_widget(screen)
        screen_manager.add_widget(PlayerScreen(name='player1'))

    screen = screen_manager.get_screen('player2')
    if screen is True:
        screen_manager.remove_widget(screen)
        screen_manager.add_widget(PlayerScreen(name='player2'))

    App.get_running_app().game = Battleship()
    game = App.get_running_app().game
    return game, screen_manager


def initialize_game(player1, player2, screen):
    # player1 =
    # player2 =



class MenuButtonAnimation(Animation):
    initial_pos = 0

    def on_start(self, widget):
        self.initial_pos = widget.pos[0]

    def on_complete(self, widget):
        if widget.player1 and widget.player2:
            initialize_game(widget.player1, widget.player2, widget.screen_init)
        else:
            if widget.screen_init is True:
                widget.screen_init()
            screen_manager = App.get_running_app().screen_manager
            screen_manager.current = widget.screen

        widget.pos[0] = self.initial_pos

class StyledButton(Button):
    pass


class MainMenuButton(StyledButton):
    player1 = 0
    player2 = 0
    screen_init = 0
    animation_running = 0

    def __init__(self, **kwargs):
        super(MainMenuButton, self).__init__(**kwargs)

    def on_release(self):
        if self.animation_running is False:
            self.animation_running = MenuButtonAnimation()
        self.animation_running.start(self)



class MultiplayerButton(MainMenuButton):

    def __init__(self, **kwargs):
        super(MultiplayerButton, self).__init__(**kwargs)
        self.player1 = Player
        self.player2 = ThePlayer
        self.screen_init = multiplayer_init
        self.screen = 'multiplayer'
        self.button_text = 'Start!'


class PlaywFriendButton(MainMenuButton):

    def __init__(self, **kwargs):
        super(PlaywFriendButton, self).__init__(**kwargs)
        self.player1 = Player
        self.player2 = Player
        self.screen_init = player_vs_mode
        self.screen = 'ship_selection'
        self.button_text = 'Next'


class QuitButton(MainMenuButton):

    def __init__(self, **kwargs):
        super(QuitButton, self).__init__(**kwargs)
        self.screen_init = exit



class MenuScreen(Screen):
    pass


class PlayerInput(TextInput):

    def center_text(self):
       self._get_text_width(self.text, self.tab_width)
       self.center_text()

