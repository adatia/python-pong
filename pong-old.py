import math
import random
import pygame

# Setup
pygame.init()
pygame.display.set_caption("PythonPong")

# Sound effects
paddle = pygame.mixer.Sound("paddle.mp3")
score = pygame.mixer.Sound("score.mp3")
wall = pygame.mixer.Sound("wall.mp3")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constants for screen dimensions
WIDTH = 700
HEIGHT = 500

# Constants for component dimensions and offsets
BALL_SIZE = 15

BALL_OFFSET_X = WIDTH/2 - BALL_SIZE/2
BALL_OFFSET_Y = HEIGHT/2 - BALL_SIZE/2

RECT_WIDTH = 5
RECT_HEIGHT = 75

RECT_OFFSET_X = RECT_WIDTH * 4
RECT_OFFSET_Y = HEIGHT/2 - RECT_HEIGHT/2

# Constant for text font
TEXT_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 60)

# Set the width and height of the screen [width, height]
size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# Speed variables (in pixels per frame)
ball_x_speed = 5
ball_y_speed = 5

left_y_speed = 0
right_y_speed = 0

# Score variables
player1_score = 0
player2_score = 0

# Game components
ball = pygame.Rect(BALL_OFFSET_X, BALL_OFFSET_Y, BALL_SIZE, BALL_SIZE)
left_rect = pygame.Rect(RECT_OFFSET_X, RECT_OFFSET_Y, RECT_WIDTH, RECT_HEIGHT)
right_rect = pygame.Rect(WIDTH - RECT_OFFSET_X - RECT_WIDTH, RECT_OFFSET_Y, RECT_WIDTH, RECT_HEIGHT)

def movement():
    """Controls movement of ball and player."""

    ball.x += ball_x_speed
    ball.y += ball_y_speed

    left_rect.y += left_y_speed
    right_rect.y += right_y_speed

def ball_collide():
    """Reverses speed when ball collides with something."""
    global ball_x_speed, ball_y_speed, player1_score, player2_score

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_y_speed *= -1
        pygame.mixer.Sound.play(wall)

    if ball.left <= 0:
        pygame.mixer.Sound.play(score)
        reset_ball()
        player2_score += 1

    if ball.right >= WIDTH:
        pygame.mixer.Sound.play(score)
        reset_ball()
        player1_score += 1

    if ball_x_speed < 0 and ball.colliderect(left_rect):
        pygame.mixer.Sound.play(paddle)

        if abs(left_rect.right - ball.left) < 10:
            ball_x_speed *= -1
        elif ball_y_speed > 0 and abs(left_rect.top - ball.bottom) < 10:
            ball_y_speed *= -1
        elif ball_y_speed < 0 and abs(left_rect.bottom - ball.top) < 10:
            ball_y_speed *= -1

    if ball_x_speed > 0 and ball.colliderect(right_rect):
        pygame.mixer.Sound.play(paddle)

        if abs(right_rect.left - ball.right) < 10:
            ball_x_speed *= -1
        elif ball_y_speed > 0 and abs(right_rect.top - ball.bottom) < 10:
            ball_y_speed *= -1
        elif ball_y_speed < 0 and abs(right_rect.bottom - ball.top) < 10:
            ball_y_speed *= -1

def reset_ball():
    """Resets ball to center of screen."""
    global ball_x_speed, ball_y_speed

    ball.center = (WIDTH / 2, HEIGHT / 2)

    if ball_x_speed > 0:
        ball_x_speed = random.uniform(-6, -4)
    else:
        ball_x_speed = random.uniform(4, 6)

    ball_y_speed = random.choice((random.uniform(-6, -4), random.uniform(4, 6)))

def rect_collide():
    """Prevents players from moving beyond screen."""
    if left_rect.top <= 0:
        left_rect.top = 0
    if left_rect.bottom >= HEIGHT:
        left_rect.bottom = HEIGHT

    if right_rect.top <= 0:
        right_rect.top = 0
    if right_rect.bottom >= HEIGHT:
        right_rect.bottom = HEIGHT

# Main game loop
while not done:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_UP:
                left_y_speed = -5

            elif event.key == pygame.K_DOWN:
                left_y_speed = 5

            elif event.key == pygame.K_w:
                right_y_speed = -5

            elif event.key == pygame.K_s:
                right_y_speed = 5

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                left_y_speed = 0

            elif event.key == pygame.K_w or event.key == pygame.K_s:
                right_y_speed = 0

    movement()
    ball_collide()
    rect_collide()

    # Updates the display
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, left_rect)
    pygame.draw.rect(screen, WHITE, right_rect)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

    player1_text = TEXT_FONT.render(f"{player1_score}", False, WHITE)
    player2_text = TEXT_FONT.render(f"{player2_score}", False, WHITE)

    if player1_score <= 9:
        screen.blit(player1_text, (280, 10))
    else:
        screen.blit(player1_text, (220, 10))

    screen.blit(player2_text, (360, 10))

    pygame.display.flip()
    clock.tick(60)

# Close everything down
pygame.quit()
