from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from app.game import change_screen

Builder.load_file('app/screen/kv/gamescreen.kv')


class PlayerScreen(Screen):
    """
    Class assigned to the kivy PlayerScreen file
    """
    ship_grid = ObjectProperty(None)
    ship_counter = ObjectProperty(None)
    turn_indicator = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlayerScreen, self).__init__(**kwargs)
        self.player = None

    def add_player(self, player):
        self.player = player
        self.player.screen = self

    def player_keeps_guessing(self, turn):
        if turn == 1:
            self.ship_counter.text = 'VICTORY IS NEAR'
        else:
            self.ship_counter.text = 'GUESS THE ENEMY SHIPS'

    def update_turn(self, *args):
        self.turn_indicator.text = '%s ATTACKING' % self.player.name


class Square(Button):
    dim = 0
    square_status = False

    def __init__(self, **kwargs):
        super(Square, self).__init__(**kwargs)
        size = 10
        self.row = Square.dim // size
        self.col = Square.dim % size
        Square.dim += (Square.dim + 1) % (size * size)
        self.background_color = (0.5, 0.5, 0.5, 0.5)

    def assign_state(self, state):
        """
        If player misses, it is indicated. If the player gets a hit, it is indicated.
        :param state:
        :return:
        """
        if state == 'miss':
            self.background_color = (1, 1, 0, 0)
        elif state == 'hit':
            self.background_color = (1, 0, 0, 1)
        self.disabled = True
        self.square_status = True

    def surrounding_assign_state(self, state):
        """
        Function to update the state of surrounding squares/blocks
        :param state:
        :return:
        """
        grid = App.get_running_app().screen_manager.current_screen.ship_grid.board

        def wrapper():
            if self.row + i < 0 or self.col + j < 0:
                return
            try:
                square = grid[self.row + i][self.col + j]
                if i != 0 or j != 0:
                    if not square.square_status:
                        square.assign_state(state)
            except IndexError:
                return
            except AttributeError:
                return
            return

        # Updates surrounding squares using the wrapper
        for i in range(-1, 2):
            for j in range(-1, 2):
                wrapper()
        return True

    def on_release(self):
        """
        Upon releasing the button/square, the function will tell you if it's a hit or miss.
        :return:
        """
        current_player = App.get_running_app().game.players[App.get_running_app().game.turn]
        next_player = App.get_running_app().game.players[(App.get_running_app().game.turn + 1) % 2]
        ship = current_player.hit(self.row, self.col, next_player)
        if ship:
            self.assign_state('hit')
        else:
            self.assign_state('miss')
        current_player.screen.ship_grid.toggle_disable()
        App.get_running_app().game.next_turn()
        Clock.schedule_once(partial(change_screen, next_player.screen), current_player.wait_time)
        return ship


class Board(GridLayout):
    """
    Class containing functions related to the Board/ Grid. Chess used for reference. PYGAME!!
    """

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        size = 10
        self.board = [[None] * size for i in range(size)]
        for i in range(size * size):
            ship_pos = Square()
            self.add_widget(ship_pos)
            self.board[i // size][i % size] = ship_pos

    def toggle_disable(self):
        grid = self.board
        for row in grid:
            for col in row:
                if not col.square_status:
                    col.disabled = True

    def toggle_enable(self):
        grid = self.board
        for row in grid:
            for col in row:
                if not col.square_status:
                    col.disabled = False

    def clear(self):
        size = 10
        for i in range(size):
            del self.board[i // size][i % size]
        for i in range(size):
            ship_pos = Square()
            self.add_widget(ship_pos)
            self.board[i // size][i % size] = ship_pos


