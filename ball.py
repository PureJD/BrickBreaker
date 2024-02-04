from pygame import Rect, Vector2
from variables import *


class game_ball():
    def __init__(self, x, y, ball_size = 10):
        self.ball_rad = ball_size
        self.speed_max = Coll_variable_speed
        self.rect = Rect(x - self.ball_rad, y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed = Vector2(variable_self_speed_x, variable_self_speed_y)

    def move(self):
        # Collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.collide_x()
        # Collision with top of the screen
        if self.rect.top < 0:
            self.collide_y()

        self.rect.move_ip(self.speed)

    def draw(self):
        center = (self.rect.centerx, self.rect.centery)
        pygame.draw.circle(screen, paddle_col, center, self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, center, self.ball_rad, 3)

    def collide_y(self):
        self.speed.y *= -1

    def collide_x(self):
        self.speed.x *= -1

    def reset(self, x, y):
        self.rect.topleft = (x - self.ball_rad, y)
        self.speed = Vector2(variable_self_speed_x, variable_self_speed_y)
