from helpers import *

class Enemy():
    position = np.array([int(0),int(0)])
    velocity = np.array([int(0),int(0)])
    update_counter = None
    draw_type = None

    def __init__(self,position,velocity,moving_period,draw_type):
        self.position = position
        self.velocity = velocity
        self.update_counter = TimeToUpdate(moving_period)
        self.draw_type = draw_type

    def update(self,board):
        if self.update_counter.isTimeToUpdate():
            self.position += self.velocity
        else:
            # Do not update
            pass
    
    def draw(self,screen,board):
        self.draw_type.draw(screen,board,self.position)

class BounceEnemy(Enemy):
    draw_type = None
    # An enemy that bounces off surfaces
    def __init__(self,position,velocity,moving_period,draw_type):
        super().__init__(position,velocity,moving_period,draw_type)

    def update(self,board):
        if self.update_counter.isTimeToUpdate():
            new_position = self.position + self.velocity
            if not board.isPositionWithinBoard(new_position):
                # Reverse direction
                self.velocity = -self.velocity
                new_position = self.position + self.velocity
            self.position = new_position
        else:
            # Do not update
            pass
        