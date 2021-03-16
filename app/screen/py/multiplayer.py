from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from app.screen.client import Client

Builder.load_file('app/screen/kv/multiplayerscreen.kv')
Builder.load_file('app/screen/kv/connection.kv')


class ConnectionScreen(Screen):
    pass


class ConnectionLabel(Label):
    pass


class Buttons(Button):
    pass


# ==================================== CLASSES FOR MULTIPLAYER/ONLINE =========================================
# Note: WARNING!!! Using socket as done in other game examples, you've deviated from FastAPI.
# =============================================================================================================

class MultiplayerScreen(Screen):
    """
    These are assigned to IDs in the multiplayer KIVY file
    """
    port = ObjectProperty(None)
    address = ObjectProperty(None)
    error_message = ObjectProperty(None)


class ConnectButton(Buttons):
    """
    THIS WAS THE MOST IMPORTANT CLASS/ FUNCTION AND I FLOPPED. Connect to an online player.
    """
    def on_release(self):
        address = App.get_running_app().screen_manager.current_screen.address_field.text, \
                  int(App.get_running_app().screen_manager.current_screen.port_field.text)
        try:
            Client(address).request('test')
            App.get_running_app().game.players[1].add_client(address)
        except ConnectionRefusedError:
            App.get_running_app().screen_manager.current_screen.error_message.text = 'Server Connection Error!'
            return 0
        App.get_running_app().screen_manager.current_screen.error_message.text = ''
        App.get_running_app().screen_manager.current = 'ship_selection'
