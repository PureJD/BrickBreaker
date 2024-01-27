import pygame
from variables import *
from pygame.locals import *
from paddle import *
from ball import game_ball
from levels.level1 import level1
from levels.level2 import level2
from levels.level3 import level3
from levels.level_random import level_random


pygame.init()

# Music and sound effects engine and files
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.set_num_channels(2)
intro_sound = pygame.mixer.Sound('sounds/intro_sound.wav')
pop_sound = pygame.mixer.Sound('sounds/pop.wav')



pygame.display.set_caption('Breakout')
level_wall = level_random()



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


def main_game():
    run = True
    global live_ball
    global lives
    global game_over
    global score
    global level_wall


    while run:
        clock.tick(fps)

        screen.fill(bg)

        # draw all objects
        level_wall.draw_wall()
        player_paddle.draw(screen)
        ball.draw()

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
                        ## This is where the level is changed
                        level_wall = level1()
                        ## This is where we draw the new level
                        level_wall.create_wall()
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
        #Sound effect
        pygame.mixer.Channel(1).play(pop_sound)
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
    wall_destroyed = True
    row_count = 0
     

    for row in level_wall.blocks:
        item_count = 0
        for item in row:
            if item is not None and ball.rect.colliderect(item[0]):
                score += 1

                #Plays sound effect upon collision 
                pygame.mixer.Channel(1).play(pop_sound)

                block = item[0]
                ball_rect_coords_x = ball.rect.centerx
                if ball_rect_coords_x < block.left or ball_rect_coords_x > block.right:
                    ball.collide_x()
                else:
                    ball.collide_y()

                if level_wall.blocks[row_count][item_count][1] > 1:
                    level_wall.blocks[row_count][item_count][1] -= 1
                else:
                    level_wall.blocks[row_count].pop(item_count)
                    item_count -= 1  # Adjust index since an item is removed

            if item is not None:
                wall_destroyed = False
            item_count += 1
        row_count += 1

    if wall_destroyed:
        game_over = 1


def show_intro():
    pygame.display.flip()
    pygame.mixer.Channel(0).play(intro_sound)
    pygame.mixer.Sound.stop
    pygame.time.delay(2000)  # Display intro for 2 seconds


# The main game loop has been added into a function. This is to make it easier to add sections like menus and levels and intros.
player_paddle = paddle()
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
show_intro()
level_wall.create_wall()
main_game()
 