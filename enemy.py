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

    def update(self):
        if self.update_counter.isTimeToUpdate():
            self.position += self.velocity
        else:
            # Do not update
            pass
    
    def draw(self,screen,board):
        self.draw_type.draw(screen,board,self.position)

class BounceEnemy(Enemy):
    # An enemy that bounces off surfaces
    # It needs a board to determine where it is allowed to go
    draw_type = None
    board = None
    
    def __init__(self,position,velocity,moving_period,draw_type,board):
        super().__init__(position,velocity,moving_period,draw_type)
        self.board = board

    def update(self):
        if self.update_counter.isTimeToUpdate():
            new_position = self.position + self.velocity
            if not self.board.isPositionWithinBoard(new_position):
                # Reverse direction
                self.velocity = -self.velocity
                new_position = self.position + self.velocity
            self.position = new_position
        else:
            # Do not update
            pass
        
class HomingEnemy(Enemy):
    # An enemy that moves towards the player
    draw_type = None
    player = None

    def __init__(self,position,moving_period,draw_type,player):
        super().__init__(position,np.array([0,0]),moving_period,draw_type)
        self.player = player

    def update(self):
        if self.update_counter.isTimeToUpdate():
            vector_to_player = self.player.position - self.position
            # This will prefer moving in x direction if the distance is equal
            if np.absolute(vector_to_player[0]) >= np.absolute(vector_to_player[1]):
                # Move in x direction
                self.position += np.array([np.sign(vector_to_player[0]),0])
            else:
                # Move in y direction
                self.position += np.array([0,np.sign(vector_to_player[1])])
