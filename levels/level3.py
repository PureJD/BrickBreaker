from pygame import *
from variables import *


class level3():
    intro_image = pygame.image.load("images/intro.jpg")
    transformed_intro_image = pygame.transform.scale(intro_image, (850, 850))
    screen.blit(transformed_intro_image, (0, 0))
     
    def __init__(self):
        self.width = screen_width // cols
        self.height = 30
        self.blocks = []

    def create_wall(self):
        self.blocks = []

        pattern = [
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [5, 4, 5, 4, 5, 4, 5, 4, 5, 0],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 0]
        ]

        for row_idx, row in enumerate(pattern):
            block_row = []
            for col_idx, strength in enumerate(row):
                if strength != 0:
                    block_x = col_idx * self.width
                    block_y = row_idx * self.height
                    rect = pygame.Rect(block_x, block_y, self.width, self.height)
                    block_individual = [rect, strength]
                    block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                elif block[1] == 4:
                    block_col = block_purple
                elif block[1] == 5:
                    block_col = block_black
                else:
                    continue

                pygame.draw.rect(screen, block_col, block[0])
                # space between blocks
                pygame.draw.rect(screen, bg, block[0], 1)
