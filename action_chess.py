# Imports
import pygame, sys
from pygame.locals import *
import numpy as np
import time

SCREEN_SIZE = (800, 800)
NUMBER_OF_TILES = (8,8)
PLAYER_STARTING_POSITION = np.array([0,0])

# Units
s_ = 1
ms_ = 0.001 * s_


class TimeToUpdate():
    # Takes an update period. Call function isTimeToUpdate. It returns true every time that period has passed.
    # All units are in seconds.

    last_update_time = None
    update_period = float(0)

    def __init__(self,update_period):
        self.update_period = update_period

    def isInitialized(self):
        return self.last_update_time is not None

    def isTimeToUpdate(self):
        now = time.perf_counter() # To use the same value throughout this function
        # Return true if object has never been updated
        if (not self.isInitialized() or 
                now >= self.last_update_time + self.update_period):
            self.last_update_time = now
            return True
        else:
            return False


class BoardCircle():
    color = (255,255,255)
    amount_of_square = float(1)

    def __init__(self,color,amount_of_square):
        self.color = color
        self.amount_of_square = amount_of_square

    def draw(self,screen,board,position):
        (left, top) = board.getTopLeftCornerOfSquare(position)
        (square_size_x, square_size_y) = board.getSizeOfRectangle()

        center_x = left + square_size_x/2
        center_y = top + square_size_y/2
        radius = min(square_size_x,square_size_y)/2*self.amount_of_square
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)  


class Enemy():
    position = np.array([int(0),int(0)])
    velocity = np.array([int(0),int(0)])
    update_counter = None
    draw_type = BoardCircle(color=(255,0,0),amount_of_square=0.7)

    def __init__(self,position,velocity,moving_period):
        self.position = position
        self.velocity = velocity
        self.update_counter = TimeToUpdate(moving_period)

    def update(self):
        if self.update_counter.isTimeToUpdate():
            self.position += self.velocity
            return None
        else:
            # Do not update
            return None
    
    def draw(self,screen,board):
        self.draw_type.draw(screen,board,self.position)


class Player():
    position = np.array([0,0])
    amount_of_square = 0.7
    image = None
    image_rect = None

    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False

    def __init__(self,image_file):
        self.loadImage(image_file)
    
    def __init__(self,image_file,position):
        self.loadImage(image_file)
        self.position = position

    def loadImage(self,image_file):
        self.image = pygame.image.load(image_file)
        self.image.convert()
        self.image_rect = self.image.get_rect()

    def draw(self,screen,board):
        (left, top) = board.getTopLeftCornerOfSquare(self.position)
        (square_size_x, square_size_y) = board.getSizeOfRectangle()

        square_center_x = left + square_size_x / 2
        square_center_y = top  + square_size_y / 2

        self.image_rect.center = square_center_x, square_center_y

        screen.blit(self.image,self.image_rect)

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

    def isPositionWithinBoard(self,position):
        if (position[0] < self.number_of_tiles[0] and
                position[1] < self.number_of_tiles[1]): # Board has zero indentation. Both values need to been within board
            return True
        else:
            return False
        
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


class ActionChessGame():
    screen = None
    board = None
    player = None
    enemies = []

    def __init__(self,screen_size,number_of_tiles):
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Action chess")
        self.board = Board(screen_size,number_of_tiles)
        return None

    def addPlayer(self,player):
        self.player = player

    def addEnemy(self,enemy):
        self.enemies.append(enemy)

    def update(self):
        # Update all objects
        player.update()

        for enemy in self.enemies:
            enemy.update()

        self.removeEnemiesNotOnBoard()

        print(self.enemies.__len__()) #DEBUG

    def removeEnemiesNotOnBoard(self):
        for enemy in self.enemies:
            if not self.board.isPositionWithinBoard(enemy.position):
                self.enemies.remove(enemy)
                # TODO: Garbage collect enemy?

    def draw(self):
        self.board.draw(self.screen)
        self.player.draw(self.screen,self.board)
        for enemy in self.enemies:
            enemy.draw(self.screen,self.board)


# Initialize
pygame.init()
game = ActionChessGame(SCREEN_SIZE,NUMBER_OF_TILES)

# Create player
player = Player("face.jpg",PLAYER_STARTING_POSITION)
game.addPlayer(player)

# Create enemies
enemy = Enemy(np.array([0,5]),np.array([1,0]),1000 * ms_)
game.addEnemy(enemy)

# -- Main loop --
running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()
    game.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()