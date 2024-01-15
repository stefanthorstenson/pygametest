import pygame

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
