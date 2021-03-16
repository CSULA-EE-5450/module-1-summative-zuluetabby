import pygame


class Ships(pygame.sprite.Sprite):
    """
    Stores the position of the ship on the board.
    """

    def __init__(self, player, size, orientation, coords):
        super().__init__()
        self.player = player
        self.size = size

        if orientation == 'horizontal' or orientation == 'vertical':
            self.orientation = orientation
        else:
            raise ValueError("Must be horizontal or vertical")

        self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = x * 60, y * 60

        self.highlighted = False

    def highlight(self):
        """
        Highlights the boxes that a user clicks on
        :return:
        """
        pygame.draw.rect(self.image, (138, 45, 226), (0, 0, 60, 60), 5)
        self.highlighted = not self.highlighted

    def unhighlight(self):
        """
        Unhighlights a sprite
        :return:
        """
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.highlighted = not self.highlighted


# ======================== FUNCTIONS ==================================

def rotate_ship(player, x, y, board):
    """
    Rotates the chosen ship before positioning it on the board.
    :param player:
    :param x:
    :param y:
    :param board:
    :return:
    """
    # if orientation == 'vertical' or orientation == 'horizontal'
    #    self.orientation = orientation


def attack_ship(player, x, y, board):
    """
    Checks if am enemy ship was attacked.
    :param player:
    :param x:
    :param y:
    :param board:
    :return:
    """
    ship = board.array[x][y]
    if ship is None:
        return False
    else:
        if ship.player != player:
            return True
        else:
            return False


def ship_sink() -> bool:
    """
    If all parts of a ship are damaged, it sinks.
    :return:
    """
    # if ship_damaged()
