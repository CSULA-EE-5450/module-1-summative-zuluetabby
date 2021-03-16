import pygame
import sys

import board

# Pygame initializations
pygame.init()
window = pygame.display.set_mode((800, 600))

rows = 8
cols = 8
blue = (0, 0, 255)
dblue = (55, 0, 255)
blk = (0, 0, 0)

# Create an instance of the board class
board = board.Board()


class Battleship(object):
    """
    Battleship game object
    """

    def __init__(self, num_ships: int = 4, num_players: int = 2):
        """
        Constructor for Battleship game object.

        :param num_ships: number of ships per player; default to 4
        :param num_players: number of players in game; default to 2
        """
        self._SHIPS = ("Fishboat", "Speedboat", "Kite", "Geese")
        self._LARGE_SHIP = 5
        self._MEDIUM_SHIP = 4
        self._SMALL_SHIP = 3
        self._TINY_SHIP = 2
        self._num_ships = num_ships
        self._num_players = num_players


# ======================== FUNCTIONS ==================================

# Initialize variables
player_turn = 0


def select_ship():
    pos = pygame.mouse.get_pos()
    chosen_ship = []

    if len(chosen_ship) == 1:
        # chosen_ship =  # DO SOMETHING, HIGHLIGHT IT
        return chosen_ship


def select_position():
    """
    Returns the coordinates of where the player chooses. Checks for ships overlapping.
    :return:
    """
    x, y = pygame.mouse.get_pos()
    ship = board.array[x][y]
    return x, y


def display_board():
    """
    Displays the board in a popup window.
    :return:
    """
    square = 50
    num_squares = 8
    cnt = 0

    for i in range(1, num_squares + 1):
        for j in range(1, num_squares + 1):
            if cnt % 2 == 0:
                pygame.draw.rect(window, blue, [square * j, square * i, square, square])
            else:
                pygame.draw.rect(window, dblue, [square * j, square * i, square, square])
            cnt += 1
        cnt -= 1
    pygame.draw.rect(window, blk, [square, square, num_squares * square, num_squares * square], 1)
    pygame.display.update()


# Displaying the GAME in a POPUP WINDOW
display_board()
pygame.display.update()


def run_game():
    """
    Main program for Battleship
    :return:
    """
    player = 1
    quit_game = False

    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Player 1's turn
        if player == 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and board.ready_to_start:
                    chosen_ship = select_ship()
                    if chosen_ship is not None:
                        print("Place down the ship!")
                        position = select_position()
                        if position is None:
                            board.array.append(position)

