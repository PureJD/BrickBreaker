from pygame import *
from variables import *


class level1():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 30
        self.blocks = []

    def create_wall(self):
        self.blocks = []
        # pattern for rows, e.g., [3, 5, 7, 5, 3] for a diamond shape
        pattern = [1, 1, 1, 1, 3, 5, 7, 5, 3]
        for row in range(len(pattern)):
            block_row = []
            offset = (cols - pattern[row]) // 2  # calculate offset for centered blocks
            for col in range(offset, offset + pattern[row]):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # alternating block strength
                strength = (row % 3) + 1
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
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, block[0], 2)
