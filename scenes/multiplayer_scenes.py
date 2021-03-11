from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from scenes.multiplayer_client import Client
from kivy.uix.button import Button

Builder.load_file('scenes/kivy_screen/multiplayerscreen.kv')
Builder.load_file('scenes/kivy_screen/connection.kv')


class ConnectionScreen(Screen):
    pass


class MultiplayerScreen(Screen):
    address_field = ObjectProperty(None)
    port_field = ObjectProperty(None)
    error_message = ObjectProperty(None)


class ConnectionLabel(Label):
    pass


class StyledButton(Button):
    pass


class ConnectButton(StyledButton):
    def on_release(self):
        game = App.get_running_app().game
        screen_manager = App.get_running_app().screen_manager
        address = screen_manager.current_screen.address_field.text, int(screen_manager.current_screen.port_field.text)
        client = Client(address)
        client.request('test')
        game.players[1].make_client(address)
        screen_manager.current = 'ship_selection'
