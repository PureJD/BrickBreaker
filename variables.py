import pygame.font
import pygame.display
import pygame.time

pygame.font.init()

# define font
font = pygame.font.SysFont('Constantia', 30)

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))

# define colours
bg = (38, 38, 38)
# block colours
block_red = (178, 0, 0)
block_green = (0, 178, 0)
block_blue = (0, 11, 178)
# paddle colours
paddle_col = (80, 80, 80)
paddle_outline = (100, 100, 100)
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
game_over = None

# Game ball speed variables (update all variables evenly to increase speed and retain collisons)
Coll_variable_speed = 4
variable_self_speed_x = 5
variable_self_speed_y = -5

lives = 3
score = 0

