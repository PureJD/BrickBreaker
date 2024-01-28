from pygame import Rect
from variables import *


class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)
        self.speed_y = variable_self_speed_x
        self.speed_x = variable_self_speed_y

    def move(self):
        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.collide_x()
            

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.collide_y()

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad, 3)

    def collide_y(self):
        self.speed_y = self.speed_y * -1

    def collide_x(self):
        self.speed_x = self.speed_x * -1

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = variable_self_speed_x
        self.speed_y = variable_self_speed_y
        self.speed_max = Coll_variable_speed
