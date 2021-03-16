from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from app.game import Battleship, Player, OnlinePlayer, turns_setup, multiplayer_init, play_setup
from app.screen.py.player import PlayerScreen

Builder.load_file('app/screen/kv/menuscreen.kv')


class MenuScreen(Screen):
    pass


class PlayerInput(TextInput):
    pass


class Buttons(Button):
    pass


# =========================== FUNCTIONS ====================================================================
def prepare_game(player1: type, player2: type, session_init, textinput, screen, *args):
    """
    Function to setup a game of Battleship. Make players and check the screen.
    :param player1:
    :param player2:
    :param session_init:
    :param textinput:
    :param screen:
    :param args:
    :return:
    """
    game, screen_manager = clear_old_game(session_init, textinput)
    game.make_player(player1, 'Player1')
    game.make_player(player2, 'Player2')
    screen_manager.current = screen


def clear_old_game(callback, usernames):
    """
    This function clears the previous game, unless you launch it for the first time.
    :param callback:
    :param usernames:
    :return:
    """
    screen = App.get_running_app().screen_manager.get_screen('ship_selection')
    screen.start_button.callback = callback
    screen.start_button.names = usernames
    screen1 = App.get_running_app().screen_manager.get_screen('player1')
    screen2 = App.get_running_app().screen_manager.get_screen('player2')

    # Change screen between the players and clear the enemy's widgets
    if screen1 is True:
        App.get_running_app().screen_manager.add_widget(PlayerScreen(name='player1'))
        App.get_running_app().screen_manager.remove_widget(screen)
    elif screen2 is True:
        App.get_running_app().screen_manager.add_widget(PlayerScreen(name='player2'))
        App.get_running_app().screen_manager.remove_widget(screen)

    App.get_running_app().game = Battleship()
    game = App.get_running_app().game
    return game, App.get_running_app().screen_manager


# ================================ CLASSES FOR THE MENU BUTTONS ==========================================
class MenuButtonAnimation(Animation):
    """
    This is assigned to a button in the Menu KIVY file.
    """
    def on_complete(self, widget):
        if widget.player1 is True:
            if widget.player2 is True:
                prepare_game(widget.player1, widget.player2,
                             widget.screens, widget.button_text, widget.screen)
        else:
            if widget.screens:
                widget.screens()
            App.get_running_app().screen_manager.current = widget.screen


class MainMenuButton(Buttons):
    """
    Class for fancy buttons in the main menu.
    """
    player1 = None
    player2 = None
    screen = None
    screens = None
    animation_running = None

    def __init__(self, **kwargs):
        super(MainMenuButton, self).__init__(**kwargs)

    def on_release(self):
        if not self.animation_running:
            self.animation_running = MenuButtonAnimation(opacity=0, duration=0.1)
        self.animation_running.start(self)


class MenuButton(MainMenuButton):
    """
    Class for Menu button functions
    """
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.screen_init = turns_setup
        self.screen = 'ship_selection'
        self.button_text = 'Play'


class MultiplayerButton(MainMenuButton):
    """
    Class for Online Multiplayer button functions
    """
    def __init__(self, **kwargs):
        super(MultiplayerButton, self).__init__(**kwargs)
        self.player1 = Player
        self.player2 = OnlinePlayer
        self.screen_init = multiplayer_init
        self.screen = 'multiplayer'
        self.button_text = 'Play'


class PlayButton(MainMenuButton):
    """
    Class for the START/ Play button
    """
    def __init__(self, **kwargs):
        super(PlayButton, self).__init__(**kwargs)
        self.player1 = Player
        self.player2 = Player
        self.screen_init = play_setup
        self.screen = 'ship_selection'
        self.button_text = 'Place Ships!'


class AbortButton(MainMenuButton):
    """
    Class for the EXIT/ Abort button
    """
    def __init__(self, **kwargs):
        super(AbortButton, self).__init__(**kwargs)
        self.screen_init = exit
