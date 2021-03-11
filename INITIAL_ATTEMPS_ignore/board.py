import pygame
import sys

import ships_v1
from ships_v1 import *


class Board:
    """
    Battleship board, 8x8
    """

    def __init___(self):
        self.empty = [[None for x in range(8) for y in range(8)]]
        self.array = [[None for x in range(8) for y in range(8)]]

    def place_ship(self, ship, x, y):
        """
        Moves the selected ship to the selected squares.
        :param ship:
        :param x:
        :param y:
        :return:
        """
        ship.x = x
        ship.y = y
        ship.rect.x = x * 60
        ship.rect.y = y * 60

    def read_to_start(self, ship):
        """
        Checks that all ships for both players have been placed.
        :param ship:
        :return:
        """
        # if self.place_ship()
    def ship_damaged(self, ship, x, y):
        """
        Returns the coordinates of a ship that was damaged"
        :return:
        """
        pos = pygame.mouse.get_pos()
        if pos == ship:
            self.array[x][y]
        return x, y

    def print_board(self):
        """
        Prints the board in the form of an array in the terminal
        :param self:
        :return:
        """
        for i in range(8):
            arr = []
            for ship in self.array[i]:
                if ship is not None:
                    arr.append("SHIP")
                else:
                    arr.append("00")
            print(arr)

