#Imports
import pygame, sys
from pygame.locals import *
import time
import numpy as np

# Information:
# First dimension, x, is right
# Second dimension, y, is down
# -----------------------> X
# |
# |
# |
# |
# |
# |
# |
# v Y
FRAME_RATE = 60.0 # FPS
TIME_PERIOD = 1/FRAME_RATE
K_SPEED = 1.0 # Used to convert keypress to velocity

class Player():
    position = np.array([0.0, 0.0])
    velocity = np.array([0.0, 0.0])
    color = "red"
    radius = 40

    def __init__(self):
        return None
    
    def __init__(self,position):
        self.position = position

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update(self,time_period):
        # Calculate velocity
        self.velocity = np.array([0.0, 0.0])
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity[1] = -K_SPEED
        if keys[pygame.K_s]:
            self.velocity[1] = K_SPEED
        if keys[pygame.K_a]:
            self.velocity[0] = -K_SPEED
        if keys[pygame.K_d]:
            self.velocity[0] = K_SPEED

        # Calculate position
        self.position += self.velocity * time_period

BACKGROUND_COLOR = (255, 255, 255)

def drawBackground(screen):
    screen.fill(BACKGROUND_COLOR)

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#Create a white screen 
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")

player_starting_position = np.array([50.0, 50.0])
player = Player(player_starting_position)

# -- Main loop --
running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    player.update(TIME_PERIOD)

    # Draw
    drawBackground(screen)
    player.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()