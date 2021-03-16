import pygame
import sys

pygame.init()
BLUE = (0, 0, 255)
DBLUE = (50, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

gameDisplay = pygame.display.set_mode((800,600))

#Size of squares
size = 20

#board length, must be even
boardLength = 8
gameDisplay.fill(BLUE)

gameExit = False

def draw_board():
    cnt = 0
    for c in range(1, 9):
        for r in range(1, 9):
            if cnt % 2 == 0:
                pygame.draw.rect(gameDisplay, BLUE, (c * 50, r * 50, 50, 50))
            else:
                pygame.draw.rect(gameDisplay, DBLUE, (c * 50, r * 50, 50, 50))
            cnt += 1
        cnt -= 1
    pygame.draw.rect(gameDisplay, YELLOW, [50, 50, 8 * 50, 8 * 50], 1)

gameDisplay = pygame.display.set_mode((800,600))
draw_board()
pygame.display.update()

while not gameExit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


