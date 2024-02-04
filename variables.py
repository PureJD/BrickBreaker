import pygame.font
import pygame.display
import pygame.time

pygame.font.init()

# define font
font = pygame.font.SysFont('Constantia', 30)

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

# define colours
bg = (38, 38, 38)

# block colours
block_red = (40, 120, 20)
block_green = (30, 130, 40)
block_blue = (20, 140, 80)
block_purple = (10, 150, 160)
block_black = (0, 160, 255)
# paddle colours
paddle_col = (125, 125, 125)
paddle_outline = (0, 0, 0)
# text colour
text_col = (78, 81, 139)

# Use a contrasting color for the text
score_text_color = (255, 255, 0)  # Bright yellow
outline_color = (0, 0, 0)  # Black outline

# define game variables
cols = 10
rows = 10
clock = pygame.time.Clock()
fps = 120
live_ball = False
#
game_state = 'start'  # 'start', 'playing', 'paused', 'game_over', 'game_won'
current_level = 1
max_levels = 4

# Game ball speed variables (update all variables evenly to increase speed and retain collisons)
Coll_variable_speed = 3
variable_self_speed_x = 4
variable_self_speed_y = -4

lives = 3
score = 0
power_up = 5

