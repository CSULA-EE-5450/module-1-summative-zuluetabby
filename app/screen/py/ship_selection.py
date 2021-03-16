from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from app.game import Ship, ShipSegments, make_random_ships

Builder.load_file('app/screen/kv/shipselectionscreen.kv')


class Buttons(Button):
    pass


class ShipSelectionScreen(Screen):
    """
    Class associated with the kivy file for the Ship Selection Screen
    """
    top_pane = ObjectProperty(None)
    ship_grid = ObjectProperty(None)
    start_button = ObjectProperty(None)
    player_input = ObjectProperty(None)

    def enable_starting(self):
        total_ships = 10
        self.start_button.disabled = (self.ship_grid.start_game != total_ships)

    def clear(self):
        self.ship_grid.clear()
        self.player_input.text = ''
        self.start_button.disabled = True


class ShipGrid(GridLayout):
    """
    Class covering the board functions.
    """
    size_button = None
    direction_button = None
    ships = []
    start_game = 0

    def __init__(self, **kwargs):
        super(ShipGrid, self).__init__(**kwargs)
        size = 10
        self.board = [[None] * size for i in range(size)]
        for i in range(size * size):
            ship_pos = GridSquares()
            self.add_widget(ship_pos)
            self.board[i // size][i % size] = ship_pos

    def clear(self):
        """
        Clears the board when the clear button is pressed.
        :return:
        """
        if len(self.ships):
            for ship in self.ships:
                self.remove(ship)
        size_button = None
        screen = App.get_running_app().screen_manager.get_screen('ship_selection')
        for button in screen.top_pane.children:
            if hasattr(button, 'ship_size'):
                self.size_button = button
                button.toggle_enable(5 - button.ship_size)
                if button.ship_size == 4:
                    size_button = button
                else:
                    self.size_button.background_color = (0.9, 0.9, 0.9, 1)
        self.ships = []
        self.start_game = 0
        self.size_button = size_button

    def ship_pos(self, ship_segment, ship_id):
        """
        Finds the position of a ship or ships.
        :param ship_segment:
        :param ship_id:
        :return:
        """
        block = self.find_square(ship_segment)
        block.background_color = (.3, .3, .3, 1)
        block.is_ship = True
        block.ship_id = ship_id

    def find_square(self, ship_segment):
        """
        Along with 'ship_pos', this will find the square block a ship is placed in.
        :param ship_segment:
        :return:
        """
        return self.board[ship_segment.row][ship_segment.col]

    def empty_pos(self, ship_segment):
        """
        Empties the block that a ship was once on.
        :param ship_segment:
        :return:
        """
        block = self.find_square(ship_segment)
        self.find_square(ship_segment).background_color = (0.5, 0.5, 0.5, 0.5)
        block.is_ship = False
        block.ship_id = None

    def surrounding_squares(self, row, col):
        """
        This function checks the surrounding squares when placing ships.
        :param row:
        :param col:
        :return:
        """
        def wrapper(x, y):
            if x < 0 or y < 0:
                return True
            try:
                check = self.board[x][y].check()
            except IndexError:
                return True
            except AttributeError:
                return True
            return check

        # Checks the squares using wrapper function
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not wrapper(row + i, col + j):
                    return False
        return True

    def create_ship(self, r, c):
        """
        Function creates a ship to be placed on the board.
        :param r:
        :param c:
        :return:
        """
        segments = []
        direction = self.direction_button.direction
        row, col = r, c

        for iterator in range(self.size_button.ship_size):
            if row > 9 or col > 9:
                return
            segments.append(ShipSegments(row, col))
            row += direction[1]
            col += direction[0]

        self.size_button.how_many -= 1
        self.start_game += 1
        ship = Ship(segments)
        for segment in segments:
            self.ship_pos(segment, ship.id)
        return ship

    def place_ship(self, ship):
        """
        This function places the ship and toggles the size buttons as well as enables the start button.
        :param ship:
        :return:
        """
        for segment in ship.segments:
            self.ship_pos(segment, ship.id)

        for button in App.get_running_app().screen_manager.get_screen('ship_selection').top_pane.children:
            if hasattr(button, 'ship_size') and ship.size == button.ship_size:
                if self.size_button:
                    self.size_button.background_color = (0.9, 0.9, 0.9, 1)
                self.size_button = button
                break
        if self.size_button.how_many:
            self.size_button.how_many -= 1
        self.toggle_button()
        self.start_game += 1
        return ship

    def remove(self, ship):
        """
        Function removes a ship if it is clicked again.
        :param ship:
        :return:
        """
        for segment in ship.segments:
            self.empty_pos(segment)

        for button in App.get_running_app().screen_manager.get_screen('ship_selection').top_pane.children:
            if hasattr(button, 'ship_size') and ship.size == button.ship_size:
                if self.size_button:
                    self.size_button.background_color = (0.9, 0.9, 0.9, 1)
                button.how_many += 1
                self.size_button = button
                break
        self.start_game -= 1
        return ship

    def toggle_button(self):
        button = self.size_button
        if button.how_many and button.disabled:
            button.toggle_enable()
        elif not button.how_many and not button.disabled:
            button.toggle_disable()

    def find_ship(self, ship_id):
        for ship in self.ships:
            if ship.id == ship_id:
                return ship
        return None


class ShipSelectionPane(GridLayout):
    pass


class RotatedImage(Image):
    angle = NumericProperty(0)
    pass


# ================================ CLASSES FOR BUTTONS IN SHIP SELECTION =================================
class GridSquares(Button):
    """
    Class defining the squares on the board, each square is a button! Grids in pygame were hard to make too.
    """
    dist = 0
    grid = None
    ship_id = None

    def __init__(self, **kwargs):
        super(GridSquares, self).__init__(**kwargs)
        size = 10
        self.is_ship = False
        self.row = GridSquares.dist // size
        self.col = GridSquares.dist % size
        GridSquares.dist = (GridSquares.dist + 1) % (size * size)

    def on_release(self):
        if not GridSquares.grid:
            GridSquares.grid = App.get_running_app().screen_manager.current_screen.ship_grid

        if self.is_ship:
            ship = self.grid.remove(self.grid.find_ship(self.ship_id))
            self.grid.ships.pop(self.grid.ships.index(ship))
        else:
            if self.grid.size_button.disabled:
                return
            else:
                ship = self.grid.create_ship(self.row, self.col)
                if ship:
                    self.grid.ships.append(ship)

        self.grid.toggle_button()
        App.get_running_app().screen_manager.current_screen.enable_starting()


class ShipOrientationButton(Buttons):
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


class ShipSizeButton(Buttons):
    ship_size = NumericProperty(0)
    how_many = NumericProperty(0)
    button_id = StringProperty('')

    def toggle_disable(self):
        self.disabled = True
        self.how_many = 0
        self.background_color = (0.9, 0.9, 0.9, 1)

    def toggle_enable(self, how_many=1):
        self.how_many = how_many
        self.background_color = (0, 229.0/250.0, 0, 1)
        self.disabled = False

    def on_release(self):
        screen = App.get_running_app().screen_manager.current_screen

        if screen.ship_grid.size_button:
            screen.ship_grid.size_button.background_color = (0.9, 0.9, 0.9, 1)
        self.background_color = (0, 229.0/250.0, 0, 1)
        screen.ship_grid.size_button = self


class RandomGridButton(Buttons):
    """
    Class assigned to the randomize ships button in the kivy file
    """

    def on_release(self):
        ships = None
        for i in range(5):
            if ships:
                break
            ships = make_random_ships()

        app = App.get_running_app()
        grid = app.screen_manager.get_screen('ship_selection').ship_grid
        grid.clear()
        for ship in ships:
            app.screen_manager.current_screen.ship_grid.ships.append(grid.place_ship(ship))
        app.screen_manager.current_screen.enable_starting()


class ClearButton(Buttons):
    def on_release(self):
        App.get_running_app().screen_manager.current_screen.ship_grid.clear()


class StartButton(Buttons):
    callback = None

    def on_release(self):
        self.callback()
