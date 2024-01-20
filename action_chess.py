# Imports
import pygame, sys
from pygame.locals import *
import numpy as np
from helpers import * # To not having to type helpers. in front of all helper functions
from enemy import *
import figures
import random

SCREEN_SIZE = (800, 800)
NUMBER_OF_TILES = (8,8)
PLAYER_STARTING_POSITION = np.array([0,0])
COIN_SIZE = 0.6
TEXT_COLOUR_PLAYER = (25,250,29)
TEXT_COLOUR_ENEMY = (219,35,35)
TEXT_SIZE = 40
TEXT_SIZE_GAME_OVER = 100

# Units
s_ = 1
ms_ = 0.001 * s_

# Classes
class Player():
    position = np.array([0,0])
    amount_of_square = 0.7
    image = None
    image_rect = None
    board = None
    alive = True
    score = 0
    draw_figure = None

    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False

    def __init__(self,image_file,position,board):
        self.draw_figure = figures.FigureImage("velociraptor.png",0.9,board)
        self.position = position
        self.board = board

    def loadImage(self,image_file):
        self.image = pygame.image.load(image_file)
        self.image.convert()
        self.image_rect = self.image.get_rect()

    def draw(self,screen):
        self.draw_figure.draw(screen,self.board,self.position)

    def hit(self):
        # Player has been hit by enemy
        self.alive = False

    def increaseScore(self):
        self.score += 1

    def move(self,velocity):
        # Move within limits of the board
        new_position = self.position + velocity
        if self.board.isPositionWithinBoard(new_position):
            self.position = new_position

    def update(self):
        keys = pygame.key.get_pressed()
        # Make sure key is released before moving is triggered again
        if keys[pygame.K_w] and not self.moving_up:
            self.move(np.array([0,-1]))
            self.moving_up = True
        elif not keys[pygame.K_w]:
            self.moving_up = False

        if keys[pygame.K_s] and not self.moving_down:
            self.move(np.array([0,1]))
            self.moving_down = True
        elif not keys[pygame.K_s]:
            self.moving_down = False

        if keys[pygame.K_a] and not self.moving_left:
            self.move(np.array([-1,0]))
            self.moving_left = True
        elif not keys[pygame.K_a]:
            self.moving_left = False

        if keys[pygame.K_d] and not self.moving_right:
            self.move(np.array([1,0]))
            self.moving_right = True
        elif not keys[pygame.K_d]:
            self.moving_right = False


class Point():
    position = np.array([0,0])
    figure = None

    def __init__(self,position,figure):
        self.position = position
        self.figure = figure

    def draw(self,screen,board):
        self.figure.draw(screen,board,self.position)

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
                position[1] < self.number_of_tiles[1] and
                position[0] >= 0 and position[1] >= 0): # Board has zero indentation. Both values need to been within board
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
    point_figure = None
    enemies = []
    enemy_player = None
    points = []

    def __init__(self,screen_size,number_of_tiles):
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Action chess")
        self.board = Board(screen_size,number_of_tiles)
        return None

    def addPlayer(self,player):
        self.player = player

    def addEnemy(self,enemy):
        self.enemies.append(enemy)

    def setEnemyPlayer(self,enemy_player):
        self.enemy_player = enemy_player

    def setPointFigure(self,point_figure):
        self.point_figure = point_figure

    def spawnPoint(self):
        position = self.getRandomPosition()
        point = Point(position,self.point_figure)
        self.points.append(point)

    def getLastPoint(self):
        return self.points[-1]
    
    def getRandomPosition(self):
        # Gives a random position that is not on the player
        free_position_found = False
        while not free_position_found:
            x = random.randint(0,NUMBER_OF_TILES[0] - 1)
            y = random.randint(0,NUMBER_OF_TILES[1] - 1)
            position = np.array([x,y])
            if not isPositionEqual(position,self.player.position):
                free_position_found = True

        return position


    def update(self):
        # Update all objects
        if self.player.alive:
            self.player.update()

        for enemy in self.enemies:
            enemy.update()

        self.enemy_player.update()

        self.removeEnemiesNotOnBoard()

        if self.isPlayerHit():
            self.player.hit()

        point = self.PointPlayerIsOn()
        if point is not None: # Player scored
            self.player.increaseScore()
            self.points.remove(point)
            self.spawnPoint()
            self.enemy_player.setTarget(self.getLastPoint())
            self.enemy_player.setMovingPeriod(self.enemy_player.getMovingPeriod()*0.95)

        point = self.PointEnemyPlayerIsOn()
        if point is not None: # Player enemy scored
            self.enemy_player.increaseScore()
            self.points.remove(point)
            self.spawnPoint()
            self.enemy_player.setTarget(self.getLastPoint())


    def isPlayerHit(self):
        return isCollision(self.player,self.enemies)[0] # Take only the boolean. We don't care which enemy hit player

    def PointPlayerIsOn(self):
        is_collision, point = isCollision(self.player,self.points)
        return point
    
    def PointEnemyPlayerIsOn(self):
        is_collision, point = isCollision(self.enemy_player,self.points)
        return point

    def isPlayerAlive(self):
        return self.player.alive

    def removeEnemiesNotOnBoard(self):
        for enemy in self.enemies:
            if not self.board.isPositionWithinBoard(enemy.position):
                self.enemies.remove(enemy)
                # TODO: Garbage collect enemy?

    def draw(self):
        self.board.draw(self.screen)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen,self.board)
        for point in self.points:
            point.draw(self.screen,self.board)
        self.enemy_player.draw(self.screen,self.board)

        self.drawScore()

    def drawScore(self):
        score_font = pygame.font.SysFont("Verdana", TEXT_SIZE)     
        # Player score
        score_surface  = score_font.render(str(self.player.score), True, TEXT_COLOUR_PLAYER)
        self.screen.blit(score_surface, (SCREEN_SIZE[0] - self.board.getSizeOfRectangle()[0]/1.7, 2)) # Top right, almost
        # Enemy score
        score_surface  = score_font.render(str(self.enemy_player.score), True, TEXT_COLOUR_ENEMY)
        self.screen.blit(score_surface, (SCREEN_SIZE[0] - self.board.getSizeOfRectangle()[0]/1.7, 50)) # Top right, almost

    def drawGameOver(self):
        score_font = pygame.font.SysFont("Verdana", TEXT_SIZE_GAME_OVER)     
        # Player score
        score_surface  = score_font.render("GAME OVER", True, TEXT_COLOUR_ENEMY)
        self.screen.blit(score_surface, (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))


# Initialize
pygame.init()
game = ActionChessGame(SCREEN_SIZE,NUMBER_OF_TILES)

# Create player
player = Player("velociraptor.png",PLAYER_STARTING_POSITION,game.board)
game.addPlayer(player)

# Create points
point_image = figures.FigureImage("scared_face.jpg",COIN_SIZE,game.board)
game.setPointFigure(point_image)
game.spawnPoint()

# Create enemies
red_circle = figures.BoardCircle((242,51,140),0.7)
t_rex = figures.FigureImage("t-rex.png",0.9,game.board)
enemy = BounceEnemy(np.array([0,5]),np.array([1,0]),300 * ms_,red_circle,game.board)
game.addEnemy(enemy)
enemy_player = EnemyPlayer(np.array([7,7]),1000 * ms_,t_rex,game.getLastPoint())
game.setEnemyPlayer(enemy_player)


# -- Main loop --
running = True
while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # User clicked x on window
            running = False

    game.update()
    game.draw()
    if not game.isPlayerAlive():
        game.drawGameOver()

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()