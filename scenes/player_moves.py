import jsonpickle

from kivy.app import App
from scenes.ships_status import Ship
from scenes.multiplayer_client import Client


class Player:
    def __init__(self, name):
        self.name = name
        self.ships_destroyed = 0
        self.ships = []
        self.moves = 1

    def callback(self, row=0, col=0):
        pass

    def set(self, ships, ships_destroyed):
        self.add_ships(ships)
        self.ships_destroyed = ships_destroyed

    def add_ship(self, ship):
        for i in range(self.ships):
            self.ships.append(ship)


    def find_ship(self, ship_id):
        for ship in self.ships:
            if ship.id == ship_id:
                return ship


    def pop_ship(self, ship):
        if isinstance(ship, Ship):
            idx = self.ships.index(ship)
            ship.destroy_ship()
            self.ships.pop(idx)
        elif isinstance(ship, int):
            the_ship = self.find_ship(ship)
            idx = self.ships.index(the_ship)
            the_ship.destroy_ship()
            self.ships.pop(idx)


    def add_move(self):
        self.moves += 1
        return

    def hit(self, row, col, player):
        for ship in player.ships:
            hit_ship = ship.hit(row, col)
            if hit_ship:
                if hit_ship.is_drowned():
                    for element in hit_ship.elements:
                        self.screen.ship_grid.board[element.row][element.col].surrounding_assign_state('miss')

                    player.ships.pop(player.ships.index(hit_ship))
                    self.ships_destroyed += 1
                    self.screen.change_counter(10 - self.ships_destroyed)
                return hit_ship
        else:
            return False

    def start_turn(self):
        App.get_running_app().game.game_over()


class ThePlayer(Player):
    def __init__(self, name):
        super(ThePlayer, self).__init__(name)
        self.name_index = 0
        self.wait_time = 1

    def make_client(self, address):
        self.client = Client(address)
        return self.client

    def start_turn(self):
        def get_coords(*args):
            string = self.client.request('get_coords')
            if string is True:
                row, col = jsonpickle.decode(string)
        if App.get_running_app().game.game_over():
            self.client.request('clear')
