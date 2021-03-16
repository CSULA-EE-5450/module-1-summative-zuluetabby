from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from INITIAL_ATTEMPS_ignore.OKAY_SECOND_ATTEMPT.battleship_game import Ship, ShipElement

Builder.load_file('scenes/kivy_screen/selections.kv')


class Selection(Screen):
    start_button = ObjectProperty()
    player_input = ObjectProperty()
    ship_grid = ObjectProperty()

    def start_button_enable(self):
        self.start_button.disabled = (self.ship_grid.start_game != 8)

    def clear(self):
        self.ship_grid.clear()
        self.start_button.disabled = True


class LimitShips(GridLayout):
    limit = 1

    def set_limit(self, limit):
        self.limit = limit

        for i in range(4):
            self.children[i].opacity = 0
        for i in range(self.limit):
            self.children[i].opacity = 1


class ShipPos(Button):
    grid = 0
    ship_id = 0

    def __init__(self, **kwargs):
        super(ShipPos, self).__init__(**kwargs)

        self.next_cell = None
        self.prev_cell = None
        self.is_ship = False
        self.row = ShipPos / 8
        self.col = ShipPos / 8



    def on_release(self):
        if ShipPos.grid is False:
            ShipPos.grid = App.get_running_app().screen_manager.current_screen.ship_grid

        if self.is_ship is True:
            ship = self.grid.remove(self.grid.find_ship(self.ship_id))
            self.grid.ships.append(ship)
        else:
            ship = self.grid.create_ship(self.row, self.col)
            if ship is True:
                self.grid.ships.append(ship)
        App.get_running_app().screen_manager.current_screen.start_button_enable()
        limit = App.get_running_app().screen_manager.current_screen.limit_indicator
        limit.set_limit(self.grid.size_button.num_ships)

class RotateIcon(Image):
    angle = NumericProperty(0)

class Board(GridLayout):
    size_button = 0
    start_game = 0
    ships = []

    def __init__(self):
        super(Board, self).__init__()
        for i in range(64):
            ship_cell = ShipPos()
            self.add_widget(ship_cell)
    def clear(self):
        if len(self.ships):
            for ship in self.ships:
                self.remove(ship)

        size_button = None
        screen = App.get_running_app().screen_manager.get_screen('ship_selection')

        self.ships = []
        self.start_game = 0
        self.size_button = size_button

    def get_cell(self, coords):
        return self.grid[coords.row][coords.col]


    def check_nearby_squares(self, row, col):
        for i in range(-1, 2):
            for j in range(-1, 2):
        # if i or j == overlap
        return True

    def place_ship(self, ship):
        for element in ship.elements:
            self.sign_cell(element, ship.id)

        for button in App.get_running_app().screen_manager.get_screen('ship_selection').top_pane.children:
            if hasattr(button, 'ship_size') and ship.size == button.ship_size:
                if self.size_button:
                    self.size_button.background_color = (0, 0, 0, 1)
                self.size_button = button
                break

        if self.size_button.num_ships:
            self.size_button.num_ships -= 1
        self.toggle_button()
        self.start_game += 1
        return ship

    def create_ship(self, row, col):
        ship_parts = []
        #direction = self.orientation
        if not self.check_nearby_squares(row, col):
            ship_parts.append(ShipElement(row, col))
            row += direction[1]
            col += direction[0]

            self.size_button.num_ships -= 1
            ship = Ship(ship_parts)
        for j in ship_parts:
            self.sign_cell(ship_parts, ship.id)
        return ship

    def remove(self, ship):
        for element in ship.elements:
            if len(ship.elements) >= 2:
                direction = (abs(ship.elements[0].col - ship.elements[1].col),
                             abs(ship.elements[0].row - ship.elements[1].row))
            else:
                direction = (1, 0)

        self.direction_button.change_direction(direction)

        for button in App.get_running_app().screen_manager.get_screen('ship_selection').top_pane.children:
            if hasattr(button, 'ship_size') and ship.size == button.ship_size:
                if self.size_button:
                    self.size_button.background_color = (0, 0, 0, 1)
                button.num_ships += 1
                self.size_button = button
                break

        self.start_game -= 1
        return ship

    def find_ship(self, ship_id):
        for ship in self.ships:
            if ship.id == ship_id:
                return ship
        return None


class ShipSelectionPane(GridLayout):
    pass


class StyledButton(Button):
    pass


class ShipOrientationButton(StyledButton):
    direction = (1, 0)
    image = ObjectProperty(None)

    def change_direction(self, vector):
        if vector == (1, 0):
            self.direction = vector
            self.image.angle = 0
        elif vector == (0, 1):
            self.direction = vector
            self.image.angle = 90

    def on_release(self):
        self.change_direction((self.direction[1], self.direction[0]))


class ShipSizeButton(StyledButton):
    ship_size = 0
    num_ships = 0

    def on_release(self):
        screen = App.get_running_app().screen_manager.current_screen

        screen.limit_indicator.set_limit(self.num_ships)
        if screen.ship_grid.size_button:
            screen.ship_grid.size_button.background_color = (0.5, 0.5, 0.5, 1)
        screen.ship_grid.size_button = self


class StartButton(StyledButton):
    def on_release(self):
        self.callback()


class ClearButton(StyledButton):
    def on_release(self):
        App.get_running_app().screen_manager.current_screen.ship_grid.clear()
