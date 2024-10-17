import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Collector')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up font
font = pygame.font.Font(None, 36)

# Set up player
player_size = 50
player_color = BLUE
player_pos = [WIDTH // 2, HEIGHT - player_size - 10]

# Set up stars
star_size = 30
star_color = YELLOW
star_pos = [random.randint(0, WIDTH - star_size), 0]
star_list = [star_pos]

# Game variables
clock = pygame.time.Clock()
speed = 5
score = 0
game_duration = 120  # 2 minutes in seconds
start_time = time.time()

# Define rewards
rewards = [(GREEN, "Green Reward"), (RED, "Red Reward"), (BLUE, "Blue Reward"), (YELLOW, "Yellow Reward")]

def drop_stars(star_list):
    if len(star_list) < 10:
        x_pos = random.randint(0, WIDTH - star_size)
        y_pos = 0
        star_list.append([x_pos, y_pos])

def update_star_positions(star_list):
    for idx, star_pos in enumerate(star_list):
        if star_pos[1] >= 0 and star_pos[1] < HEIGHT:
            star_pos[1] += speed
        else:
            star_list.pop(idx)  # Remove star without adding points

def detect_collision(player_pos, star_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    s_x = star_pos[0]
    s_y = star_pos[1]

    if (s_x >= p_x and s_x < (p_x + player_size)) or (p_x >= s_x and p_x < (s_x + star_size)):
        if (s_y >= p_y and s_y < (p_y + player_size)) or (p_y >= s_y and p_y < (s_y + star_size)):
            return True
    return False

def draw_text(text, color, position):
    label = font.render(text, True, color)
    screen.blit(label, position)

# Main game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += speed

    screen.fill(BLACK)

    drop_stars(star_list)
    update_star_positions(star_list)

    for star_pos in star_list:
        pygame.draw.rect(screen, star_color, (star_pos[0], star_pos[1], star_size, star_size))
        if detect_collision(player_pos, star_pos):
            star_list.remove(star_pos)
            score += 1  # Add points only when a collision happens

    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    # Display score
    draw_text(f'Score: {score}', WHITE, (10, 10))

    # Check if game time is over
    if time.time() - start_time > game_duration:
        game_over = True

    pygame.display.update()
    clock.tick(30)

# Rewarding the player
screen.fill(BLACK)
reward = random.choice(rewards)
draw_text(f'Congratulations! You win the {reward[1]}!', reward[0], (WIDTH // 4, HEIGHT // 2))
pygame.display.update()

# Pause for 5 seconds to show the reward
time.sleep(5)

# Quit game
pygame.quit()