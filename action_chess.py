# Imports
import pygame, sys
from pygame.locals import *
import numpy as np

SCREEN_SIZE = (800, 800)
NUMBER_OF_TILES = (8,8)
PLAYER_STARTING_POSITION = np.array([0,0])

class Player():
    position = np.array([0,0])
    color = (255,0,0)
    amount_of_square = 0.7

    # TODO: Use an image https://pygame.readthedocs.io/en/latest/3_image/image.html
    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False

    def __init__(self):
        return None
    
    def __init__(self,position):
        self.position = position

    def draw(self,screen,board):
        (left, top) = board.getTopLeftCornerOfSquare(self.position)
        (square_size_x, square_size_y) = board.getSizeOfRectangle()

        center_x = left + square_size_x/2
        center_y = top + square_size_y/2
        radius = min(square_size_x,square_size_y)/2*self.amount_of_square
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)

    def update(self):
        keys = pygame.key.get_pressed()
        # Make sure key is released before moving is triggered again
        if keys[pygame.K_w] and not self.moving_up:
            self.position[1] -= 1
            self.moving_up = True
        elif not keys[pygame.K_w]:
            self.moving_up = False

        if keys[pygame.K_s] and not self.moving_down:
            self.position[1] += 1
            self.moving_down = True
        elif not keys[pygame.K_s]:
            self.moving_down = False

        if keys[pygame.K_a] and not self.moving_left:
            self.position[0] -= 1
            self.moving_left = True
        elif not keys[pygame.K_a]:
            self.moving_left = False

        if keys[pygame.K_d] and not self.moving_right:
            self.position[0] += 1
            self.moving_right = True
        elif not keys[pygame.K_d]:
            self.moving_right = False

        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0

class Board():
    size = (0,0)
    number_of_tiles = (0,0)
    color_1 = (255,255,255)
    color_2 = (100,100,100)

    def __init__(self,size,number_of_tiles):
        self.size = size
        self.number_of_tiles = number_of_tiles

    def getSizeOfRectangle(self):
        if self.number_of_tiles[0] == 0 or self.number_of_tiles[1] == 0:
            return (None, None)
        else:
            return (self.size[0]/self.number_of_tiles[0], self.size[1]/self.number_of_tiles[1])
    
    def getTopLeftCornerOfSquare(self,square):
        rectangle_size = self.getSizeOfRectangle()
        left = square[0] * rectangle_size[0]
        top  = square[1] * rectangle_size[1]
        return (left, top)

    def isEven(self,number):
        return (number % 2) == 0
    
    def draw(self,screen):
        rectangle_size = self.getSizeOfRectangle()
        # Loop through all rectangles
        for i_x in np.arange(0,self.number_of_tiles[0]):
            for i_y in np.arange(0,self.number_of_tiles[1]):
                rectangle_left = i_x * rectangle_size[0]
                rectangle_top  = i_y * rectangle_size[1]
                if self.isEven(i_x + i_y):
                    rectangle_color = self.color_1
                else:
                    rectangle_color = self.color_2
                pygame.draw.rect(screen,rectangle_color,Rect((rectangle_left,rectangle_top),(rectangle_size[0],rectangle_size[1])))

#Initializing 
pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Action chess")

# Create board
board = Board(SCREEN_SIZE, NUMBER_OF_TILES)

# Create player
player = Player(PLAYER_STARTING_POSITION)

# -- Main loop --
running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    player.update()

    # Draw
    board.draw(screen)
    player.draw(screen,board)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()