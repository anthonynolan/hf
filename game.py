import pygame
import random

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Platformer with Enemies")

# Set up the player
player_size = 50
player_x = 100
player_y = WINDOW_HEIGHT - player_size - 10
player_speed = 5
player_jump_height = 10
player_is_jumping = False

# Set up the platforms
platforms = [
    [0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50],
    [WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2, 100, 20],
    [100, WINDOW_HEIGHT - 200, 100, 20],
]

# Set up the enemies
enemies = []
for platform in platforms:
    enemy_x = random.randint(platform[0] + 20, platform[0] + platform[2] - 20)
    enemy_y = platform[1] - 40
    enemy_direction = random.choice([-1, 1])
    enemies.append([enemy_x, enemy_y, enemy_direction])

# Main game loop
game_over = False
clock = pygame.time.Clock()

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_SPACE] and not player_is_jumping:
        player_is_jumping = True
        player_jump_height = 10

    # Handle player jumping
    if player_is_jumping:
        if player_jump_height >= 0:
            player_y -= (player_jump_height**2) / 2
            player_jump_height -= 1
        else:
            player_is_jumping = False

    # Handle collisions with platforms
    on_platform = False
    for platform in platforms:
        if (
            player_y + player_size >= platform[1]
            and player_y + player_size <= platform[1] + platform[3]
        ):
            if (
                player_x + player_size >= platform[0]
                and player_x <= platform[0] + platform[2]
            ):
                player_y = platform[1] - player_size
                player_jump_height = 10
                player_is_jumping = False
                on_platform = True
    if not on_platform:
        player_y += player_speed

    # Handle enemy movement
    for enemy in enemies:
        enemy[0] += enemy[2]
        if (
            enemy[0] < platforms[0][0] + 20
            or enemy[0] > platforms[-1][0] + platforms[-1][2] - 20
        ):
            enemy[2] *= -1

    # Handle collisions with enemies
    for enemy in enemies:
        if player_y < enemy[1] + 40 and player_y + player_size > enemy[1]:
            if player_x < enemy[0] + 40 and player_x + player_size > enemy[0]:
                game_over = True

    # Clear the screen
    screen.fill(WHITE)

    # Draw the platforms
    for platform in platforms:
        pygame.draw.rect(screen, BLUE, platform)

    # Draw the player
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, BLACK, (enemy[0], enemy[1], 40, 40))

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

pygame.quit()
