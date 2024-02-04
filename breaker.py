import pygame
from variables import *
from paddle import paddle
from ball import game_ball

from levels.level1 import level1
from levels.level2 import level2
from levels.level3 import level3
from levels.level4 import level4
from levels.level_random import level_random

pygame.init()

# Music and sound effects engine and files
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.set_num_channels(2)
intro_sound = pygame.mixer.Sound('sounds/intro_sound.wav')
pop_sound = pygame.mixer.Sound('sounds/pop.wav')

pygame.display.set_caption('Breakout')
level_wall = level1()


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_text_with_outline(text, font, text_col, x, y, outline_col, target_surface=None):
    if target_surface is None:
        target_surface = screen
    text_surface = font.render(text, True, text_col)
    outline_surface = font.render(text, True, outline_col)

    # Draw the outline by offsetting the position slightly
    target_surface.blit(outline_surface, (x - 1, y - 1))
    target_surface.blit(outline_surface, (x + 1, y - 1))
    target_surface.blit(outline_surface, (x - 1, y + 1))
    target_surface.blit(outline_surface, (x + 1, y + 1))

    # Draw the main text
    target_surface.blit(text_surface, (x, y))


# Create a background surface
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg)  # bg is your background color

# Create a surface for static UI elements
ui_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
ui_surface = ui_surface.convert_alpha()

# Draw static elements once
draw_text_with_outline('Score:', font, score_text_color, screen_width - 180, 10, outline_color, ui_surface)
draw_text_with_outline('Lives:', font, score_text_color, 10, 10, outline_color, ui_surface)


def main_game():
    run = True
    # global live_ball
    global lives
    global game_state
    global score
    global level_wall
    global current_level
    global max_levels

    while run:
        clock.tick(fps)

        screen.blit(background, (0, 0))
        screen.blit(ui_surface, (0, 0))

        # In your main game loop, for dynamic elements
        draw_text_with_outline(f'{score}', font, score_text_color, screen_width - 95, 10, outline_color)
        draw_text_with_outline(f'{lives}', font, score_text_color, 90, 10, outline_color)

        # draw all objects
        level_wall.draw_wall()
        player_paddle.draw(screen)
        ball.draw()

        # Move the paddle regardless of the ball's state
        player_paddle.move()
        # Move the ball if it is live
        if game_state == 'playing':
            # Handle the ball's collisions
            ball.move()
            collide_wall()
            collide_paddle()
            collide_floor()
        else:
            # if the ball is not live, keep it centered on the paddle
            ball.rect.x = player_paddle.x + (player_paddle.width // 2) - ball.ball_rad
            ball.rect.y = player_paddle.y - ball.ball_rad * 2

            # display instructions
            if game_state == 'start':
                draw_text('PRESS SPACE BAR TO START', font, score_text_color, screen_width // 4,
                          screen_height // 2 + 100)
            elif game_state == 'game_over':
                draw_text('YOU LOST!', font, score_text_color, screen_width // 4, screen_height // 2 + 50)
                draw_text('PRESS SPACE BAR TO START', font, score_text_color, 280, screen_height // 2 + 100)
            elif game_state == 'game_won':
                if current_level == max_levels:
                    draw_text('YOU WON!', font, score_text_color, screen_width // 4, screen_height // 2 + 50)
                    draw_text('PRESS SPACE BAR TO RECEIVE YOUR AWARD', font, score_text_color, 280,
                              screen_height // 2 + 100)
                else:
                    draw_text('LEVEL COMPLETE!', font, score_text_color, screen_width // 4, screen_height // 2 + 50)
                    draw_text('PRESS SPACE BAR TO START NEXT LEVEL', font, score_text_color, 140,
                              screen_height // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == 'start':
                    game_state = 'playing'
                elif event.key == pygame.K_SPACE and game_state == 'game_over':
                    reset_game()
                elif event.key == pygame.K_SPACE and game_state == 'game_won':
                    level_complete()
        pygame.display.update()
    pygame.quit()


def level_complete():
    global game_state, current_level, max_levels, level_wall
    if current_level == max_levels:
        game_state = 'game_won'
    else:
        current_level += 1
        if current_level == 2:
            level_wall = level2()
            level_wall.create_wall()
        elif current_level == 3:
            level_wall = level3()
            level_wall.create_wall()
        elif current_level == 4:
            level_wall = level4()
            level_wall.create_wall()
        elif current_level == 5:
            level_wall = level_random()
            level_wall.create_wall()
        else:
            level_wall = level1()
            level_wall.create_wall()

    game_state = 'start'


def reset_game():
    global lives, score, level_wall, game_state, current_level
    ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
    game_state = 'start'
    level_wall = level1()
    level_wall.create_wall()
    lives = 3
    score = 0
    current_level = 1


def collide_floor():
    global lives, game_state
    if ball.rect.bottom > screen_height:
        # stop the ball
        # live_ball = False
        lives -= 1
        if lives == 0:
            game_state = 'game_over'
        else:
            game_state = 'start'
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)


def collide_paddle():
    if ball.rect.colliderect(player_paddle):
        # Sound effect
        pygame.mixer.Channel(1).play(pop_sound)
        # check if colliding from the top
        if abs(ball.rect.bottom - player_paddle.rect.top) < 10 and ball.speed.y > 0:
            ball.speed.y *= -1
            ball.speed.x += player_paddle.direction
            if ball.speed.x > ball.speed_max:
                ball.speed.x = ball.speed_max
            elif ball.speed.x < 0 and ball.speed.x < -ball.speed_max:
                ball.speed.x = -ball.speed_max
        else:
            ball.speed.x *= -1


def collide_wall():
    global game_state, score
    ball_next_pos = ball.rect.copy()
    ball_next_pos.move_ip(ball.speed)

    collision_detected = False
    all_bricks_destroyed = True  # Assume all bricks are destroyed until proven otherwise
    row_count = 0
    for row in level_wall.blocks:
        item_count = 0
        for item in row:
            if item is not None:
                all_bricks_destroyed = False  # Found an intact brick
                brick_rect = item[0]
                # Check if the ball's next position collides with any brick
                if ball_next_pos.colliderect(brick_rect):
                    collision_detected = True
                    score += 1  # Adjust scoring as per your game's logic

                    # Play collision sound
                    pygame.mixer.Channel(1).play(pop_sound)

                    # Determine the side of the collision
                    if ball.rect.centery < brick_rect.top or ball.rect.centery > brick_rect.bottom:
                        ball.collide_y()
                    else:
                        ball.collide_x()

                    # Handle the brick's removal or damage here
                    if item[1] > 1:  # If the brick has more than 1 durability
                        level_wall.blocks[row_count][item_count][1] -= 1
                    else:
                        level_wall.blocks[row_count].pop(item_count)
                        item_count -= 1  # Adjust because we've removed an item

                    # Optionally, break here if you only want to handle the first collision detected
                    # break

            item_count += 1
        row_count += 1
        if collision_detected:
            break

    if all_bricks_destroyed:
        # All bricks are destroyed, advance game state
        game_state = 'game_won'  # Or any other logic to advance the level or win the game



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
