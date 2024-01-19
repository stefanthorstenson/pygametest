import pygame
import numpy as np

class DrawFigure():
    def draw(self):
        pass

class BoardCircle(DrawFigure):
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

class FigureImage(DrawFigure):
    image = None
    image_rect = None

    def __init__(self,image_file,amount_of_square,board):
        self.loadImage(image_file)
        self.scaleImage(amount_of_square,board)
        self.image_rect = self.image.get_rect() # To save getting it every time figure is drawn

    def loadImage(self,image_file):
        self.image = pygame.image.load(image_file)
        self.image.convert()

    def scaleImage(self,amount_of_square,board):
        # Calculate image size as ratio of board square size
        (square_size_x, square_size_y) = board.getSizeOfRectangle()
        ratio_x = self.image.get_width()  / square_size_x
        ratio_y = self.image.get_height() / square_size_y
        # Pick the ratio of x and y which is largest
        ratio = max(ratio_x,ratio_y)
        new_image_size = np.array([self.image.get_width(),self.image.get_height()]) / ratio * amount_of_square
        self.image = pygame.transform.scale(self.image,new_image_size)

    def draw(self,screen,board,position):
        (left, top) = board.getTopLeftCornerOfSquare(position)
        (square_size_x, square_size_y) = board.getSizeOfRectangle()

        square_center_x = left + square_size_x / 2
        square_center_y = top  + square_size_y / 2

        self.image_rect.center = square_center_x, square_center_y

        screen.blit(self.image,self.image_rect)