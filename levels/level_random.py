from pygame import *
from variables import *
import random



class level_random():
    intro_image = pygame.image.load("images/intro.jpg")
    transformed_intro_image = pygame.transform.scale(intro_image, (850, 850))
    screen.blit(transformed_intro_image, (0, 0))

    
     
    def __init__(self):
        self.width = screen_width // cols
        self.height = 30
        self.blocks = []

    def create_wall(self):
        
        
        #Plays the track for the level
        pygame.mixer.music.stop()
        pygame.time.wait(2) 
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.music.load('sounds/intro.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        


        self.blocks = []

        pattern = [
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
            [random.randint(0, 5) for _ in range(10)],
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