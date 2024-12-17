import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Star Collector')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (174, 182, 191)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up font
font = pygame.font.Font(None, 36)

# Load background
background_image = pygame.image.load('chocolate_factory.jpg')  # Replace with your file
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load player character image
player_image = pygame.image.load('characterIdle.png')
player_size_ratio = 0.1  # Relative to window height
facing_right = True  # Track the direction the character is facing

# Set up balls
ball_size_ratio = 0.05  # Relative to window width
colors = [(RED, 'Red'), (GREEN, 'Green'), (BLUE, 'Blue'), (YELLOW, 'Yellow')]

# Game variables
clock = pygame.time.Clock()
speed = 5
game_duration = 60  # 1 minute
start_time = None

# Ball collection counts
color_counts = {"Red": 0, "Green": 0, "Blue": 0, "Yellow": 0}
ball_list = []

# Language selection
languages = {
    "Dutch": {"Red": "Rood", "Green": "Groen", "Blue": "Blauw", "Yellow": "Geel", "Time": "Tijd"},
    "English": {"Red": "Red", "Green": "Green", "Blue": "Blue", "Yellow": "Yellow", "Time": "Time"}
}
current_language = "Dutch"

# Function to drop balls
def drop_balls(ball_list, ball_size):
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
            ball_list.pop(idx)

# Detect collision
def detect_collision(player_pos, ball_pos, player_size, ball_size):
    p_x, p_y = player_pos
    b_x, b_y = ball_pos[:2]
    if (b_x >= p_x and b_x < (p_x + player_size)) or (p_x >= b_x and p_x < (b_x + ball_size)):
        if (b_y >= p_y and b_y < (p_y + player_size)) or (p_y >= b_y and p_y < (b_y + ball_size)):
            return True
    return False

# Draw text
def draw_text(text, color, position):
    label = font.render(text, True, color)
    screen.blit(label, position)

# Main menu for language selection
def main_menu():
    global current_language
    selecting_language = True
    while selecting_language:
        screen.fill(LIGHT_GRAY)
        draw_text("Choose Language:", BLACK, (WIDTH // 3, HEIGHT // 3))
        draw_text("1: English", BLACK, (WIDTH // 3, HEIGHT // 2))
        draw_text("2: Dutch", BLACK, (WIDTH // 3, HEIGHT // 2 + 40))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_language = "English"
                    selecting_language = False
                if event.key == pygame.K_2:
                    current_language = "Dutch"
                    selecting_language = False

# Main game loop
def main_game():
    global WIDTH, HEIGHT, screen, background_image, start_time, color_counts, facing_right
    start_time = time.time()
    game_over = False
    player_pos = [WIDTH // 2, HEIGHT - int(player_size_ratio * HEIGHT) - 10]
    ball_size = int(ball_size_ratio * WIDTH)
    player_size = int(player_size_ratio * HEIGHT)
    player_image_resized = pygame.transform.scale(player_image, (player_size, player_size))
    player_image_flipped = pygame.transform.flip(player_image_resized, True, False)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                player_size = int(player_size_ratio * HEIGHT)
                ball_size = int(ball_size_ratio * WIDTH)
                player_image_resized = pygame.transform.scale(player_image, (player_size, player_size))
                player_image_flipped = pygame.transform.flip(player_image_resized, True, False)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= speed
            facing_right = False
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += speed
            facing_right = True

        screen.blit(background_image, (0, 0))
        drop_balls(ball_list, ball_size)
        update_ball_positions(ball_list)

        for ball_pos in ball_list:
            color, color_name = ball_pos[2]
            pygame.draw.rect(screen, color, (ball_pos[0], ball_pos[1], ball_size, ball_size))
            if detect_collision(player_pos, ball_pos, player_size, ball_size):
                ball_list.remove(ball_pos)
                color_counts[color_name] += 1

        if facing_right:
            screen.blit(player_image_resized, (player_pos[0], player_pos[1]))
        else:
            screen.blit(player_image_flipped, (player_pos[0], player_pos[1]))

        # Display scores
        draw_text(f'{languages[current_language]["Red"]}: {color_counts["Red"]}', RED, (10, 10))
        draw_text(f'{languages[current_language]["Green"]}: {color_counts["Green"]}', GREEN, (10, 50))
        draw_text(f'{languages[current_language]["Blue"]}: {color_counts["Blue"]}', BLUE, (10, 90))
        draw_text(f'{languages[current_language]["Yellow"]}: {color_counts["Yellow"]}', YELLOW, (10, 130))

        # Countdown timer
        time_left = int(game_duration - (time.time() - start_time))
        draw_text(f'{languages[current_language]["Time"]}: {time_left}', WHITE, (WIDTH - 150, 10))

        if time_left <= 0:
            game_over = True

        pygame.display.update()
        clock.tick(30)

    screen.fill(LIGHT_GRAY)
    most_collected_color = max(color_counts, key=color_counts.get)
    draw_text(f'{languages[current_language][most_collected_color]} was the most collected!', WHITE, (WIDTH // 6, HEIGHT // 2))
    pygame.display.update()
    time.sleep(5)
    pygame.quit()

# Run game
main_menu()
main_game()