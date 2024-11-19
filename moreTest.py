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
LIGHT_GRAY = (174, 182, 191)  # New background color
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up font
font = pygame.font.Font(None, 36)

# Load player character image
player_image = pygame.image.load('characterIdle.png')
player_size = 100
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Create a horizontally flipped version of the player image
player_image_flipped = pygame.transform.flip(player_image, True, False)

player_pos = [WIDTH // 2, HEIGHT - player_size - 10]
facing_right = True  # Track the direction the character is facing

# Set up balls
ball_size = 30
colors = [(RED, 'Red'), (GREEN, 'Green'), (BLUE, 'Blue'), (YELLOW, 'Yellow')]

# Game variables
clock = pygame.time.Clock()
speed = 5
game_duration = 60  # 1 minute
start_time = time.time()

# Ball collection counts
color_counts = {"Red": 0, "Green": 0, "Blue": 0, "Yellow": 0}
ball_list = []

# Function to drop balls
def drop_balls(ball_list):
    if len(ball_list) < 10:
        x_pos = random.randint(0, WIDTH - ball_size)
        y_pos = 0
        color = random.choice(colors)
        ball_list.append([x_pos, y_pos, color])

# Update ball positions
def update_ball_positions(ball_list):
    for idx, ball_pos in enumerate(ball_list):
        if ball_pos[1] >= 0 and ball_pos[1] < HEIGHT:
            ball_pos[1] += speed
        else:
            ball_list.pop(idx)  # Remove ball when it hits the ground without points

# Detect collision
def detect_collision(player_pos, ball_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    b_x = ball_pos[0]
    b_y = ball_pos[1]

    if (b_x >= p_x and b_x < (p_x + player_size)) or (p_x >= b_x and p_x < (b_x + ball_size)):
        if (b_y >= p_y and b_y < (p_y + player_size)) or (p_y >= b_y and p_y < (b_y + ball_size)):
            return True
    return False

# Draw text
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
        facing_right = False  # Facing left
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += speed
        facing_right = True  # Facing right

    screen.fill(LIGHT_GRAY)  # Use the new background color

    drop_balls(ball_list)
    update_ball_positions(ball_list)

    # Draw balls and handle collisions
    for ball_pos in ball_list:
        color, color_name = ball_pos[2]
        pygame.draw.rect(screen, color, (ball_pos[0], ball_pos[1], ball_size, ball_size))
        if detect_collision(player_pos, ball_pos):
            ball_list.remove(ball_pos)
            color_counts[color_name] += 1  # Increment color count

    # Draw the player character image with correct orientation
    if facing_right:
        screen.blit(player_image, (player_pos[0], player_pos[1]))
    else:
        screen.blit(player_image_flipped, (player_pos[0], player_pos[1]))

    # Display score for each color
    draw_text(f'Red: {color_counts["Red"]}', RED, (10, 10))
    draw_text(f'Green: {color_counts["Green"]}', GREEN, (10, 50))
    draw_text(f'Blue: {color_counts["Blue"]}', BLUE, (10, 90))
    draw_text(f'Yellow: {color_counts["Yellow"]}', YELLOW, (10, 130))

    # Countdown timer
    time_left = int(game_duration - (time.time() - start_time))
    draw_text(f'Time: {time_left}', WHITE, (WIDTH - 150, 10))

    if time_left <= 0:
        game_over = True

    pygame.display.update()
    clock.tick(30)

# End of game - reward based on the most collected color
screen.fill(LIGHT_GRAY)  # Keep the background consistent
most_collected_color = max(color_counts, key=color_counts.get)
draw_text(f'Congratulations! You collected the most {most_collected_color} balls!', WHITE, (WIDTH // 6, HEIGHT // 2))
pygame.display.update()

# Pause for 5 seconds to show the reward
time.sleep(5)

# Quit game
pygame.quit()
