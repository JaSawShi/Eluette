import pygame, sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Eluette')

# Set up display
screen_w, screen_h = 960//2, 768//2
screen = pygame.display.set_mode((screen_w, screen_h))

# Ground settings
ground_y, ground_height = 704//2, 64//2
ground_color = (255, 255, 255)

# Player settings
player_w, player_h = 128//2, 128//2
player_x, player_y = screen_w // 2 - player_w // 2, ground_y - player_h*4
player_color = (255, 255, 255)
player_velocity_y = 0
player_speed_x = 5
is_jumping = False

# Physics
gravity = 4
jump_power = -25

# FPS settings
fps = 10
clock = pygame.time.Clock()

# Main loop
run = True
while run:
    screen.fill((0, 0, 0))
    
    # Draw ground
    pygame.draw.rect(screen, ground_color, pygame.Rect(0, ground_y, screen_w, ground_height))
    
    # Draw player
    pygame.draw.rect(screen, player_color, pygame.Rect(player_x, player_y, player_w, player_h))
    
    # Apply gravity
    if player_y + player_h < ground_y:
        player_velocity_y += gravity
    else:
        player_y = ground_y - player_h
        player_velocity_y = 0
        is_jumping = False

    # Update player vertical position
    player_y += player_velocity_y

    # Event handling
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed_x
    if keys[pygame.K_d]:  # Move right
        player_x += player_speed_x
    if keys[pygame.K_SPACE] and not is_jumping:  # Jump
        player_velocity_y = jump_power
        is_jumping = True

    # Boundaries to keep player within the screen
    if player_x < 0:
        player_x = 0
    elif player_x + player_w > screen_w:
        player_x = screen_w - player_w

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
    
    # Update display and control FPS
    pygame.display.update()
    clock.tick(fps)

# Quit the game
pygame.quit()
sys.exit()
