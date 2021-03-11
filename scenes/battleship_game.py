import kivy
from kivy.app import App
from kivy.uix.screenmanager import FadeTransition
import random

import atexit
import jsonpickle
from scenes.player_moves import ThePlayer
from scenes.ships_status import Ship, ShipElement
from scenes.gameover import GameOverScreen


class Battleship:
    """
    The class for Battleship Game.
    """

    def __init__(self):
        self.players = []
        self.turn = 0
        self.name = 'self'

    def make_player(self, player_type: type, name: object):
        """
        This function makes a player. Adds it to a list called players.
        :param player_type: human , computer
        :param name: name of player
        :return:
        """
        self.players.append(player_type(name))
        player = self.players[-1]
        return player

    def next_turn(self):
        """
        This determines whose turn it is.
        :param self:
        :return:
        """
        self.turn += 1
        return self.turn

    def game_over(self):
        """
        The game has ended.
        :param self:
        :return:
        """
        for player in self.players:
            if player.ships_destroyed is 10:
                screen_manager = App.get_running_app().screen_manager
                ending_screen = GameOverScreen(player.name, player.moves)
                ending_screen.change_text()
                screen_manager.switch_to(ending_screen)
                if isinstance(self.players[1], ThePlayer):
                    atexit.unregister(clear_request)
                return True
        return False


# =============================== FUNCTIONS ===============================

def clear_request():
    """
    Sends a clear request.
    :return:
    """
    players = App.get_running_app().game.players
    if len(players) >= 2 and isinstance(players[1], ThePlayer):
        players[1].multiplayer.request('clear')
    return


def make_random_ships():
    """
    Function used to make ships
    :return:
    """

    def add_ship(x, y):
        """
        This function adds a ship.
        :param x:
        :param y:
        :return:
        """
        ship_size = ship_sizes[0]
        for i in range(ship_size):
            ship_qualities.append((x, y))
            x += direction[1]
            y += direction[0]
            if not (x, y) in open_squares:
                break
            if x > 9 or y > 9:
                break
        else:
            # function to remove

            for i in range(len(ship_qualities)):
                ship_qualities[i] = ShipElement(ship_qualities[i][0], ship_qualities[i][1])

                num_ships[0] -= 1
                if not num_ships[0]:
                    num_ships.pop(0)
                    ship_sizes.pop(0)
                    placed_ships.append(Ship(ship_qualities))

    num_ships = [1, 2, 3, 4]
    ship_sizes = [1, 2, 3, 4]
    open_squares = [i for i in range(64)]
    placed_ships = []

    while num_ships > 0:
        square = open_squares[random.randrange(0, len(open_squares), 1)]
        ship_qualities = []
        row, col = square / 8

        if random.randrange(0, 2):
            direction = (0, 1)
        else:
            direction = (1, 0)
        add_ship(row, col)
    return placed_ships


def change_screen(screen):
    """
    Changes the screen of the game in the pop up window.
    :param screen:
    :param args:
    :return:
    """
    app = App.get_running_app()
    if isinstance(screen, str):
        current_screen = app.screen_manager.get_screen(screen)
        return current_screen


def connect_players(screen_manager, players):
    """
    Function to connect players to the game and assign them an index.
    :param screen_manager:
    :param players:
    :return:
    """
    player1 = screen_manager.get_screen('player1')
    player1.connect_players(players[0])
    player2 = screen_manager.get_screen('player2')
    player2.connect_players(players[1])


def player_vs_mode():
    """
    Initializes the pvp mode.
    :return:
    """
    players = App.get_running_app().game.players
    screen_manager = App.get_running_app().screen_manager
    screen_manager.get_screen('selection').start_button.text = 'Start'
    name = screen_manager.current_screen.player_input.text
    if name is True:
        players[0].name = name
        players[0].set(screen_manager.current_screen.ship_grid.ships, 0)
    else:
        players[0].name = 'stranger'
    screen_manager.get_screen('ship_selection').clear()
    screen_manager.get_screen('ship_selection').start_button.callback = singleplayer_init


def multiplayer_init():
    """
    Initializes a game with multiplayer settings.
    :return:
    """

    def setting_up_multi():
        """
        Sets things up for multiplayer.
        :return:
        """
        connect_players(screen_manager, players)

        App.get_running_app().game.turn = players[1].name_index
        screen_manager.transition = FadeTransition()
        change_screen(players[players[1].name_index].screen)

    def username():
        """
        Gets the player's username.
        :param args:
        :return:
        """
        client.request('get_player', str(players[1].name_index))
        if name is True:
            players[1].name = name
            json = jsonpickle.encode(players[0].ships)
            idx = client.request('ships', json)

    def get_ships():
        try:
            ships = client.request('get_ships', str(idx))
        except ConnectionRefusedError:
            return

        if ships != 'None':
            players[1].ships = jsonpickle.decode(ships)
            setting_up_multi()

    screen_manager = App.get_running_app().screen_manager
    name = screen_manager.current_screen.player_input.text
    players = App.get_running_app().game.players

    players[0].name = name if name else 'whom'
    players[1].name_index = int(players[1].client.request('player', str(players[0].name)))
    players[0].set(App.get_running_app().screen_manager.current_screen.ship_grid.ships, 0)

    screen_manager.transition = FadeTransition()
    screen_manager.current = 'connection'

    client = players[1].client
    idx = 0
