import pygame
from variables import *
from pygame.locals import *
from paddle import *
from ball import game_ball

# Music and sound effects engine and files
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Breakout')
intro_sound = pygame.mixer.Sound('sounds/intro_sound.wav')
main_theme_music = pygame.mixer.Sound('sounds/intro.wav')


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_text_with_outline(text, font, text_col, x, y, outline_col):
    text_surface = font.render(text, True, text_col)
    outline_surface = font.render(text, True, outline_col)

    # Draw the outline by offsetting the position slightly
    screen.blit(outline_surface, (x - 1, y - 1))
    screen.blit(outline_surface, (x + 1, y - 1))
    screen.blit(outline_surface, (x - 1, y + 1))
    screen.blit(outline_surface, (x + 1, y + 1))

    # Draw the main text
    screen.blit(text_surface, (x, y))


# brick wall class
class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 30

    def create_wall(self):
        self.blocks = []
        # define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign block strength based on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                # create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign a colour based on block strength
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)


def main_game():
    run = True
    global live_ball
    global lives
    global game_over
    global score

    while run:
        clock.tick(fps)

        screen.fill(bg)

        # Display score

        # draw all objects
        wall.draw_wall()
        player_paddle.draw(screen)
        ball.draw()

        # Music
        main_theme_music.play()
        main_theme_music.set_volume(0.1)

        draw_text_with_outline(f'Score: {score}', font, score_text_color, screen_width - 140, 10, outline_color)
        draw_text_with_outline(f'Lives: {lives}', font, score_text_color, 10, 10, outline_color)

        # Handle the ball's collisions
        collide_wall()
        collide_paddle()
        collide_floor()

        # Move the paddle regardless of the ball's state
        player_paddle.move()

        # Move the ball if it is live
        if live_ball:
            ball.move()

        if live_ball is False:

            # if the ball is not live, keep it centered on the paddle
            ball.rect.x = player_paddle.x + (player_paddle.width // 2) - ball.ball_rad
            ball.rect.y = player_paddle.y - ball.ball_rad * 2

            # display instructions
            if game_over == 0:
                draw_text('PRESS SPACE BAR TO START', font, score_text_color, 310, screen_height // 2 + 100)
            elif game_over == 1:
                draw_text('YOU WON!', font, score_text_color, 280, screen_height // 2 + 50)
                draw_text('PRESS SPACE BAR TO START', font, score_text_color, 280, screen_height // 2 + 100)
            elif game_over == -1:
                draw_text('YOU LOST!', font, score_text_color, 280, screen_height // 2 + 50)
                draw_text('PRESS SPACE BAR TO START', font, score_text_color, 280, screen_height // 2 + 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not live_ball:
                    if lives == 0:  # Only reset score and lives if the game was over
                        score = 0
                        lives = 3
                        wall.create_wall()
                    ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
                    live_ball = True

        pygame.display.update()

    pygame.quit()


def collide_floor():
    global lives, game_over, live_ball
    if ball.rect.bottom > screen_height:
        # stop the ball
        live_ball = False
        lives -= 1
        if lives == 0:
            game_over = -1
        else:
            game_over = 2


def collide_paddle():
    if ball.rect.colliderect(player_paddle):
        # check if colliding from the top
        if abs(ball.rect.bottom - player_paddle.rect.top) < 10 and ball.speed_y > 0:
            ball.speed_y *= -1
            ball.speed_x += player_paddle.direction
            if ball.speed_x > ball.speed_max:
                ball.speed_x = ball.speed_max
            elif ball.speed_x < 0 and ball.speed_x < -ball.speed_max:
                ball.speed_x = -ball.speed_max
        else:
            ball.speed_x *= -1


def collide_wall():
    global game_over, score
    # start off with the assumption that the wall has been destroyed completely
    wall_destroyed = 1
    row_count = 0
    ball_rect_coords_x = ball.rect.centerx

    for row in wall.blocks:
        item_count = 0
        for item in row:
            # check collision
            if ball.rect.colliderect(item[0]):
                # Score update
                score += 1
                block = item[0]
                if ball_rect_coords_x < block.left or ball_rect_coords_x > block.right:
                    ball.collide_x()
                else:
                    ball.collide_y()
                # reduce the block's strength by doing damage to it
                if wall.blocks[row_count][item_count][1] > 1:
                    wall.blocks[row_count][item_count][1] -= 1
                else:
                    wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

            # check if block still exists, in whcih case the wall is not destroyed
            if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                wall_destroyed = 0
            # increase item counter
            item_count += 1
        # increase row counter
        row_count += 1
    # after iterating through all the blocks, check if the wall is destroyed
    if wall_destroyed == 1:
        game_over = 1


def show_intro():
    intro_image = pygame.image.load("images/intro.jpg")
    transformed_intro_image = pygame.transform.scale(intro_image, (1000, 1000))
    screen.blit(transformed_intro_image, (0, 0))
    pygame.display.flip()
    intro_sound.play()
    pygame.time.delay(3000)  # Display intro for 3 seconds


# The main game loop has been added into a function. This is to make it easier to add sections like menus and levels and intros.
player_paddle = paddle()
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
wall = wall()
wall.create_wall()
show_intro()
main_game()
