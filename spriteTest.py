import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('2D Sprite Example')

# Create a Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('characterIdle.png')
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)

    def update(self):
        # Logic to move the sprite can be added here
        pass

# Create a sprite group and add the player sprite to it
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Draw all sprites on the screen
    screen.fill((10, 20, 30))  # Clear the screen with black
    all_sprites.draw(screen)

    # Refresh the display
    pygame.display.flip()

# Quit pygame
pygame.quit()