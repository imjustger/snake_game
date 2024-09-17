import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Snake settings
SNAKE_SIZE = 10
SNAKE_SPEED = 15

# Create the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

# Font settings
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Display score
def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

# Snake creation function
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# Display game over message, now centered and with a smaller font
def message(msg, color):
    small_font_style = pygame.font.SysFont(None, 30)  # Use a smaller font size
    mesg = small_font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))  # Center the text
    screen.blit(mesg, mesg_rect)

# Button rendering function
def button(msg, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf = small_text.render(msg, True, WHITE)
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    screen.blit(text_surf, text_rect)

# Main menu function
def game_menu():
    menu = True

    while menu:
        screen.fill(BLACK)
        large_text = pygame.font.SysFont("comicsansms", 50)
        text_surf = large_text.render("Snake Game", True, WHITE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        screen.blit(text_surf, text_rect)

        button_width = 150
        button_height = 50

        # Center the Play and Exit buttons
        button_x = (SCREEN_WIDTH / 2) - (button_width / 2)
        
        # Play button at y = 200 and Exit button at y = 300
        button("Play", button_x, 200, button_width, button_height, GREEN, DARK_GREEN, gameLoop)
        button("Exit", button_x, 300, button_width, button_height, RED, BLUE, quit_game)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Define direction constants
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

# Quit game function
def quit_game():
    pygame.quit()
    quit()

# Main game loop
def gameLoop():
    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    current_direction = RIGHT  # Start the snake heading to the right
    direction_locked = False  # Prevent quick direction changes in the same frame

    snake_list = []
    snake_length = 1

    # Randomize the food's location
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            screen.fill(BLUE)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and not direction_locked:  # Allow direction change only if not locked
                # Check direction and prevent turning to the opposite direction
                if event.key == pygame.K_LEFT and current_direction != RIGHT:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                    current_direction = LEFT
                    direction_locked = True  # Lock direction change until next movement
                elif event.key == pygame.K_RIGHT and current_direction != LEFT:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                    current_direction = RIGHT
                    direction_locked = True
                elif event.key == pygame.K_UP and current_direction != DOWN:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                    current_direction = UP
                    direction_locked = True
                elif event.key == pygame.K_DOWN and current_direction != UP:
                    y1_change = SNAKE_SIZE
                    x1_change = 0
                    current_direction = DOWN
                    direction_locked = True

        # Check if the snake hits the boundary
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        pygame.draw.rect(screen, YELLOW, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if the snake collides with itself
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(SNAKE_SIZE, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        # If the snake eats the food
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / 10.0) * 10.0
            snake_length += 1

        clock.tick(SNAKE_SPEED)

        # Unlock direction change after moving the snake
        direction_locked = False  # Once snake has moved, unlock direction change

    pygame.quit()
    quit()

# Start the game with the menu
game_menu()