import random
import jsonpickle
from kivy.app import App
from kivy.uix.screenmanager import Screen
from app.screen.client import Client


def make_random_ships():
    """
    When the random button is clicked, random ships will be made on the board.
    :return:
    """
    def convert(x, y):
        size = 10
        return size * x + y

    def remove_squares():
        for length in ship_len:
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    square = convert(length[0] + i, length[1] + j)
                    if square in empty_squares:
                        index = empty_squares.index(square)
                        empty_squares.pop(index)

    def add_ship(x, y):
        ship_size = ship_sizes[0]
        for i in range(ship_size):
            ship_len.append((x, y))
            x += direction[1]
            y += direction[0]
            if not convert(x, y) in empty_squares:
                break
            if x > 9 or y > 9:
                break
        else:
            remove_squares()
            for i in range(len(ship_len)):
                ship_len[i] = ShipSegments(ship_len[i][0], ship_len[i][1])
            num_ships[0] -= 1
            if not num_ships[0]:
                num_ships.pop(0)
                ship_sizes.pop(0)
            placed_ships.append(Ship(ship_len))

    # While there are ships, keep placing!
    num_ships = [1, 2, 3, 4]
    ship_sizes = [4, 3, 2, 1]
    empty_squares = [i for i in range(100)]
    placed_ships = []

    while num_ships:
        spot = empty_squares[random.randrange(0, len(empty_squares), 1)]
        ship_len = []
        row, col = spot // 10, spot % 10

        if random.randrange(0, 2):
            direction = (0, 1)
        else:
            direction = (1, 0)
        add_ship(row, col)
    return placed_ships


def assign_players(screen_manager, players):
    """
    Function to assign players and indicate their turn.
    :param screen_manager:
    :param players:
    :return:
    """
    player1 = screen_manager.get_screen('player1')
    player2 = screen_manager.get_screen('player2')
    player1.add_player(players[0])
    player2.add_player(players[1])
    player1.turn_indicator.text = f"{players[0].name} ATTACK"
    player2.turn_indicator.text = f"{players[1].name} ATTACK"


def change_screen(screen, *args):
    """
    Function to change screen/scenes
    :param screen:
    :param args:
    :return:
    """
    app = App.get_running_app()
    if isinstance(screen, str):
        app.screen_manager.current = screen
        current_screen = app.screen_manager.get_screen(screen)
        if hasattr(current_screen, 'ship_grid'):
            current_screen.ship_grid.toggle_enable()
    elif isinstance(screen, Screen):
        app.screen_manager.current = screen.name
        current_screen = screen
        if hasattr(current_screen, 'ship_grid'):
            current_screen.ship_grid.toggle_enable()


def turns_setup():
    """
    Once the game starts, each player will take turns starting from player idx 0
    :return:
    """
    index = 1
    if App.get_running_app().screen_manager.current_screen.player_input.text is True:
        App.get_running_app().game.players[index].name = App.get_running_app().screen_manager.current_screen.player_input.text
    else:
        App.get_running_app().screen_manager.current_screen.player_input.text = 'None'

    App.get_running_app().game.players[index].set(App.get_running_app().screen_manager.current_screen.ship_grid.ships, 0)
    assign_players(App.get_running_app().screen_manager, App.get_running_app().game.players)
    App.get_running_app().game.turn = 0
    change_screen(App.get_running_app().game.players[index].screen)


def play_setup():
    """
    Sets up the game and players, if they don't input their name they are a Ghost Sailor.
    :return:
    """
    players = App.get_running_app().game.players

    screen_manager = App.get_running_app().screen_manager
    screen_manager.get_screen('ship_selection').start_button.text = 'Sail!'
    name = screen_manager.current_screen.player_input.text
    if name is True:
        players[0].name = name
    else:
        players[0].name = 'GHOST SAILOR'
    players[0].set(screen_manager.current_screen.ship_grid.ships, 0)
    screen_manager.get_screen('ship_selection').clear()
    screen_manager.get_screen('ship_selection').start_button.callback = turns_setup


def multiplayer_init():
    """
    Function for setting up online multiplayer.
    :return:
    """
    name = App.get_running_app().screen_manager.current_screen.player_input.text
    players = App.get_running_app().game.players
    if name is True:
        players[0].name = name
    else:
        players[0].name = "UNFAMILIAR GHOST SAILOR"
    players[0].set(App.get_running_app().screen_manager.current_screen.ship_grid.ships, 0)
    players[1].name_index = int(players[1].client.request('player', str(players[0].name)))
    App.get_running_app().screen_manager.current = 'connection'


class Battleship:
    """
    Main class for the Battleship Game
    """
    def __init__(self):
        self.players = []
        self.turn = 0

    def make_player(self, player_type: type, name: object):
        self.players.append(player_type(name))
        return self.players[-1]

    def next_turn(self):
        self.turn = (self.turn + 1) % 2
        return self.turn

    def has_ended(self):
        """
        Ends game if all 10 ships have sunk
        :return:
        """
        for player in self.players:
            if player.ships_destroyed == 10:
                App.get_running_app().screen_manager.switch_to('gameoverscreen')
        return False


class Ship:
    """
    Class for the ships
    """
    id = 0

    def __init__(self, ship_segments=None, sunken_ship=0):
        if ship_segments is None:
            ship_segments = list()
        self.size = len(ship_segments)
        self.segments = ship_segments
        self.drowned_elements = sunken_ship
        self.id = Ship.id
        Ship.id += 1

    def is_drowned(self):
        return self.drowned_elements == self.size

    def hit(self, row, col):
        """
        If the ship is hit, each segment hit will be drowned
        :param row:
        :param col:
        :return:
        """
        for segment in self.segments:
            if segment.row == row and segment.col == col and not segment.shot_down:
                segment.shot_down = True
                self.drowned_elements += 1
                return self
        return None

    def add_segment(self, ship_element):
        self.segments.append(ship_element)
        self.size += 1

    def destroy_ship(self):
        """
        If all parts of a ship are hit, delete the square.
        :return:
        """
        for broken in self.segments:
            del broken
        self.size = 0


class ShipSegments:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.shot_down = False


class Player:
    """
    All functions relating to a player (single) can be found here
    """
    def __init__(self, name):
        self.moves = 1
        self.ships = []
        self.name = name
        self.screen = None
        self.wait_time = 0.1
        self.ships_destroyed = 0

    def callback(self, row=0, col=0):
        pass

    def set(self, ships, ships_destroyed):
        self.add_ships(ships)
        self.ships_destroyed = ships_destroyed

    def find_ship(self, ship_id):
        for ship in self.ships:
            if ship.id == ship_id:
                return ship

    def add_ship(self, ship):
        """
        Functinon to be used for adding ships later
        :param ship:
        :return:
        """
        self.ships.append(ship)

    def add_ships(self, ships):
        """
        Function to add the ships
        :param ships:
        :return:
        """
        for ship in ships:
            self.add_ship(ship)

    def pop_ship(self, ship):
        """
        Function to pop a ship into the array
        :param ship:
        :return:
        """
        if isinstance(ship, Ship):
            index = self.ships.index(ship)
            self.ships.pop(index)
            ship.destroy_ship()
            del ship
        elif isinstance(ship, int):
            ship = self.find_ship(ship)
            index = self.ships.index(ship)
            self.ships.pop(index)
            ship.destroy_ship()
            del ship

    def update_turn(self):
        self.moves += 1
        self.screen.update_turn(self.moves)

    def hit(self, row, col, player):
        """
        Function to determine if a ship was hit.
        :param row:
        :param col:
        :param player:
        :return:
        """
        player.callback(row, col)
        for ship in player.ships:
            hit_ship = ship.hit(row, col)
            if hit_ship:
                if hit_ship.is_drowned():
                    for element in hit_ship.segments:
                        self.screen.ship_grid.board[element.row][element.col].surrounding_assign_state('miss')

                    player.ships.pop(player.ships.index(hit_ship))
                    self.ships_destroyed += 1
                    self.screen.player_keeps_guessing(10 - self.ships_destroyed)
                return hit_ship
        else:
            return False


def add_client(address):
    return Client(address)


class OnlinePlayer(Player):
    """
    Class for an online player, using JSON
    """
    def __init__(self, name):
        super(OnlinePlayer, self).__init__(name)
        self.client = None
        self.name_index = 0
        self.wait_time = 1

    def callback(self, row=0, col=0):
        json = jsonpickle.encode((row, col))
        self.client.request('coords', json)
