#only A and D buttons, created 07.11.24
import pygame, sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Eluette')

# Set up display
screen_w = 960
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

# Ground properties
ground_width = 960
ground_height = 64
ground_color = (255, 255, 255)  # White color
ground_position = (0, 704)  # Top-left corner at (x=0, y=704)

# Player properties
player_width = 128
player_height = 128
player_x = screen_w // 2 - player_width // 2  # Center player horizontally
player_y = ground_position[1] - player_height  # Start on the ground
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_power = -12

# Load idle sprites
idle_sprites = [
    pygame.image.load('images/player/idle/Eluette_idle1.png'),
    pygame.image.load('images/player/idle/Eluette_idle2.png'),
    pygame.image.load('images/player/idle/Eluette_idle3.png'),
    pygame.image.load('images/player/idle/Eluette_idle4.png')
]
current_idle_sprite = 0
idle_animation_speed = 8  # How many frames per sprite change
idle_timer = 0

# Player state
is_facing_right = True  # Player initially faces right

# Set FPS
fps = 8
clock = pygame.time.Clock()

# Main game loop
run = True
while run:
    # Fill background
    screen.fill((0, 0, 0))  # Fill the screen with black
    
    # Draw the ground
    pygame.draw.rect(screen, ground_color, pygame.Rect(ground_position, (ground_width, ground_height)))

    # Handle gravity and player falling
    player_velocity_y += gravity  # Apply gravity to the player
    player_y += player_velocity_y  # Update player's vertical position

    # Check if player hits the ground
    if player_y >= ground_position[1] - player_height:  # Ensure player doesn't fall below the ground
        player_y = ground_position[1] - player_height  # Reset to ground level
        player_velocity_y = 0  # Stop downward velocity
    else:
        player_velocity_y += gravity  # Continue to fall if not on the ground

    # Draw the player (idle animation)
    current_sprite = idle_sprites[current_idle_sprite]
    
    # Flip sprite if player is facing left
    if not is_facing_right:
        current_sprite = pygame.transform.flip(current_sprite, True, False)
    
    screen.blit(current_sprite, (player_x, player_y))
    
    # Handle idle animation
    idle_timer += 1
    if idle_timer >= idle_animation_speed:
        current_idle_sprite = (current_idle_sprite + 1) % len(idle_sprites)
        idle_timer = 0
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            elif event.key == pygame.K_a:  # Move left
                is_facing_right = False  # Flip player to the left
                player_x -= player_speed  # Move player left
            elif event.key == pygame.K_d:  # Move right
                is_facing_right = True  # Flip player to the right
                player_x += player_speed  # Move player right

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
