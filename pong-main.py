import random
import time
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

# Constants for font
TEXT_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 60)
TIME_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 30)

class Ball:
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self):
        self.speed_x = 5
        self.speed_y = 5
        self.size = 15
        self.score1 = 0
        self.score2 = 0
        self.object = pygame.Rect(
            WIDTH / 2 - self.size / 2, HEIGHT / 2 - self.size / 2, self.size, self.size)

    def move(self):
        self.object.x += self.speed_x
        self.object.y += self.speed_y

    def reset(self):
        self.object.center = (WIDTH / 2, HEIGHT / 2)

        if self.speed_x > 0:
            self.speed_x = random.uniform(-6, -4)
        else:
            self.speed_x = random.uniform(4, 6)

        self.speed_y = random.choice(
            (random.uniform(-6, -4), random.uniform(4, 6)))

    def collide(self, rect1, rect2):
        if self.object.top <= 0 or self.object.bottom >= HEIGHT:
            self.speed_y *= -1
            pygame.mixer.Sound.play(wall)

        if self.object.left <= 0:
            pygame.mixer.Sound.play(score)
            self.reset()
            self.score2 += 1

        if self.object.right >= WIDTH:
            pygame.mixer.Sound.play(score)
            self.reset()
            self.score1 += 1

        if self.speed_x < 0 and self.object.colliderect(rect1):
            pygame.mixer.Sound.play(paddle)

            if abs(rect1.right - self.object.left) < 10:
                self.speed_x *= -1
            elif self.speed_y > 0 and abs(rect1.top - self.object.bottom) < 10:
                self.speed_y *= -1
            elif self.speed_y < 0 and abs(rect1.bottom - self.object.top) < 10:
                self.speed_y *= -1

        if self.speed_x > 0 and self.object.colliderect(rect2):
            pygame.mixer.Sound.play(paddle)

            if abs(rect2.left - self.object.right) < 10:
                self.speed_x *= -1
            elif self.speed_y > 0 and abs(rect2.top - self.object.bottom) < 10:
                self.speed_y *= -1
            elif self.speed_y < 0 and abs(rect2.bottom - self.object.top) < 10:
                self.speed_y *= -1

# Set the width and height of the screen [width, height]
size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# Speed variables for paddles (in pixels per frame)
left_y_speed = 0
right_y_speed = 0

# Used to track when score changes
prev_score1 = -1
prev_score2 = -1

# Game components
ball = Ball()
left_rect = pygame.Rect(RECT_OFFSET_X, RECT_OFFSET_Y, RECT_WIDTH, RECT_HEIGHT)
right_rect = pygame.Rect(WIDTH - RECT_OFFSET_X -
                         RECT_WIDTH, RECT_OFFSET_Y, RECT_WIDTH, RECT_HEIGHT)


def movement():
    """Controls movement of ball and player."""

    ball.move()
    left_rect.y += left_y_speed
    right_rect.y += right_y_speed


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

def display_changes():
    """Makes changes to display."""
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, left_rect)
    pygame.draw.rect(screen, WHITE, right_rect)
    pygame.draw.ellipse(screen, WHITE, ball.object)
    pygame.draw.aaline(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

    player1_text = TEXT_FONT.render(f"{ball.score1}", False, WHITE)
    player2_text = TEXT_FONT.render(f"{ball.score2}", False, WHITE)

    if ball.score1 <= 9:
        screen.blit(player1_text, (280, 10))
    else:
        screen.blit(player1_text, (220, 10))

    screen.blit(player2_text, (360, 10))


# Main game loop
while not done:
    if prev_score1 != -1 and (prev_score1 != ball.score1 or prev_score2 != ball.score2):
        prev_score1 = ball.score1
        prev_score2 = ball.score2

        time1 = time.perf_counter()
        time2 = time.perf_counter()

        while time2 - time1 < 3:
            time_text = TIME_FONT.render("1", False, WHITE)

            if time2 - time1 < 2:
                time_text = TIME_FONT.render("2", False, WHITE)

            if time2 - time1 < 1:
                time_text = TIME_FONT.render("3", False, WHITE)

            display_changes()

            screen.blit(time_text, (WIDTH / 2 - 13, HEIGHT / 2 + 90))
            pygame.display.flip()

            time2 = time.perf_counter()

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

        elif prev_score1 == -1:
            prev_score1 = ball.score1
            prev_score2 = ball.score2

            time1 = time.perf_counter()
            time2 = time.perf_counter()

            while time2 - time1 < 3:
                time_text = TIME_FONT.render("1", False, WHITE)

                if time2 - time1 < 2:
                    time_text = TIME_FONT.render("2", False, WHITE)

                if time2 - time1 < 1:
                    time_text = TIME_FONT.render("3", False, WHITE)

                display_changes()

                screen.blit(time_text, (WIDTH / 2 - 13, HEIGHT / 2 + 90))
                pygame.display.flip()

                time2 = time.perf_counter()

    movement()
    ball.collide(left_rect, right_rect)
    rect_collide()

    # Updates the display
    display_changes()

    pygame.display.flip()
    clock.tick(60)

# Close everything down
pygame.quit()
