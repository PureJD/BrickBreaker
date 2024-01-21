import pygame.font
import pygame.display
import pygame.time

pygame.font.init()

# define font
font = pygame.font.SysFont('Constantia', 30)

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

# define colours
bg = (234, 218, 184)
# block colours
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
# paddle colours
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
# text colour
text_col = (78, 81, 139)

# Use a contrasting color for the text
score_text_color = (255, 255, 0)  # Bright yellow
outline_color = (0, 0, 0)  # Black outline

# define game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0
