from INITIAL_ATTEMPS_ignore.OKAY_SECOND_ATTEMPT.player import *

from INITIAL_ATTEMPS_ignore.OKAY_SECOND_ATTEMPT.battleship_game import Battleship

class Square(Button):
    """
    Each square on the grid is a button.
    """
    # For drawing the board in the console
    water = '~'
    miss = '.'
    ship = 'S'
    hit = 'H'
    sunk = 'x'

    # Functions for the squares
    id = 0
    state = False

    def __init__(self, **kwargs):
        super(self, Square).__init__(**kwargs)
        size = 8
        self.row = Square.id // size  # Integer division, no remainder
        self.col = Square.id % size   # Gets the remainder
        Square.id += 1
        Square.id %= size * size
        self.background_color = (1, 1, 1, 1)

    def state_of_square(self, state):
        if state == self.miss:
            self.background_color = (0, 0, 1, 1)
        elif state == self.hit:
            self.background_color = (1, 1, 0, 0)
        self.disabled = True
        self.state = False  # Changes the state of the square from True to False

    def release_click(self):
        app = App.get_running_app()

        if Battleship.game_over():
            return

        ship = Battleship.players[]



class DrawBoard(GridLayout):
    def __init__(self, **kwargs):
        size = 8
        super(DrawBoard, self).__init(**kwargs)  # Inherets this class
        self.grid = [[None] * size for i in range(size)]
        for i in range(size * size):
            ship_square = Square()




class Board:
    board = []
    ships = 5
    size = 0

    def __init__(self, size):

        self.size = size
        for i in range(0, size):
            self.board.append([])
            for j in range(0, size):
                self.board[i].append(Square.water)

    def within_bounds(self, x, y):
        """
        Checks if the coordinates are within the boundaries of the board.
        :param x:
        :param y:
        :return:
        """
        if -1 < x < self.size:
            if -1 < y < self.size:
                return True
        else:
            return False

    def sunk_ship(self, x, y):
        direction = [1, 1, 1, 1]  # Follow the direction top, right , bottom, left
        ship = [(x, y)]  # List of coordinate tuples
        loop = 1
        search = True

        while search:
            if loop == 10:
                return False

            # Check above the block
            if direction[0] == 1 and self.within_bounds(x, y + loop):
                direction[0] = 0
                # Found a ship that was hit
                if self.board[x][y + loop] == Square.hit:
                    ship.append((x, y + loop))
                # Found a ship that wasn't hit
                elif self.board[x][y + loop] == Square.ship:
                    return False
            # Found a missed hit
            elif self.board[x][y + loop] == Square.miss or self.board[x][y + loop] == Square.water:
                direction[0] = 0

            # Check right side of block
            if direction[1] == 1 and (self.within_bounds(x + loop, y)):
                # Found a ship that was hit
                if self.board[x + loop][y] == Square.hit:
                    ship.append((x + loop, y, y))
                # Found a ship that wasn't hit
                elif self.board[x + loop][y] == Square.ship:
                    return False
                # Found a missed hit
            elif self.board[x + loop][y] == Square.miss or self.board[x + loop][y] == Square.water:
                direction[1] = 0

            # Check below the block
            if direction[2] == 1 and (self.within_bounds(x, y - loop)):
                # Found a ship that was hit
                if self.board[x][y - loop] == Square.hit:
                    ship.append((x, y - loop))
                # Found a ship that wasn't hit
                elif self.board[x][y - loop] == Square.ship:
                    return False
                # Found a missed hit
            elif self.board[x][y - loop] == Square.miss or self.board[x][y - loop] == Square.water:
                direction[2] = 0

            # Check left side of the block
            if direction[3] == 1 and (self.within_bounds(x - loop, y)):
                # Found a ship that was hit
                if self.board[x - loop][y] == Square.hit:
                    ship.append((x - loop, y))
                # Found a ship that wasn't hit
                elif self.board[x - loop][y] == Square.ship:
                    return False
                # Found a missed hit
            elif self.board[x - loop][y] == Square.miss or self.board[x - loop][y] == Square.water:
                direction[3] = 0

            # Check if all directions are equal to 0
            if direction[0] == 0 and direction[1] == 0 and direction[2] == 0 and direction[3] == 0:
                search = False
            else:
                loop += 1

            # If all parts of a ship are hit, change it the status to sunk
            for i in range(0, len(ship)):
                self.board[ship[i][0][ship[i][1]]] = Square.sunk
            return True

    def place_moves(self, x, y):
        """
        Detects a player's input and returns the respective outcome.
        :param x:
        :param y:
        :return: Returns -1 for SAME BLOCK, 0 for a MISS, 1 for GAME OVER, 2 for HIT
        """
        # Guessed and hit a ship
        if self.board[x][y] == Square.ship:
            self.board[x][y] = Square.hit
            if self.sunk_ship(x, y):
                self.ships -= 1
                if self.ships > 0:
                    return 2
                else:
                    return 1

        # Guessed and missed
        elif self.board[x][y] == Square.water:
            self.board[x][y] = Square.miss
            return 0

        # Guessed the same square twice
        else:
            return -1

