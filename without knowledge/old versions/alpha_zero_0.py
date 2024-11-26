#created 07.11.24

import pygame, sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Eluette')

# Set up display
screen_w = 960
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

# Ground properties
ground_y = 704  # Y position of the ground (top edge)
ground_color = (255, 255, 255)  # White color
ground_height = 64

# Player properties
player_image = pygame.image.load('images/player/idle/Eluette_idle1.png').convert_alpha()
# Load all idle frames
idle_images = [
    pygame.image.load(f'images/player/idle/Eluette_idle{i}.png').convert_alpha() for i in range(1, 5)]
# Load all run frames
run_images = [
    pygame.image.load(f'images/player/run/Eluette_run{i}.png').convert_alpha() for i in range(1, 9)]
run_frame_index = 0  # Start with the first frame for running
# Load all jump frames
jump_images = [
    pygame.image.load(f'images/player/jump/Eluette_jump{i}.png').convert_alpha() for i in range(1, 4)]
jump_frame_index = 0  # Start with the first frame for jumping


player_frame_index = 0  # Start with the first frame
player_image = idle_images[player_frame_index]  # Set initial image

player_x = 100  # Starting x position of the player
player_y = 100  # Starting y position of the player
player_speed_y = 0  # Vertical speed for gravity

# Gravity settings
gravity = 0.5
player_on_ground = False

# Set FPS
fps = 60
clock = pygame.time.Clock()
# Animation timer
frame_duration = 500  # Duration for each frame in milliseconds
last_update = pygame.time.get_ticks()  # Time of the last frame update

# Movement and animation settings
frame_duration_run = 125  # Duration for each run frame in milliseconds
last_run_update = pygame.time.get_ticks()
player_speed_x = 5  # Horizontal speed
moving_left = False
moving_right = False
facing_right = True  # Track which direction player is facing

# Jump settings
jumping = False
jump_power = -20  # Initial jump speed (negative for upward movement)
jump_frame_duration = 125  # Duration for each jump frame in milliseconds
last_jump_update = pygame.time.get_ticks()

# Main game loop
run = True
while run:
    # Fill background
    screen.fill((0, 0, 0))  # Fill the screen with black
    
    # Draw the ground
    pygame.draw.rect(screen, ground_color, pygame.Rect(0, ground_y, screen_w, ground_height))

    # Apply gravity
    if not player_on_ground:
        player_speed_y += gravity
        player_y += player_speed_y

    # Check for ground collision
    if player_y + player_image.get_height() >= ground_y:
        player_y = ground_y - player_image.get_height()  # Place player on the ground
        player_speed_y = 0  # Stop falling
        player_on_ground = True  # Mark player as on the ground
    else:
        player_on_ground = False

    # Update animation based on movement
    if moving_left or moving_right:
        # Run animation while moving
        current_time = pygame.time.get_ticks()
        if current_time - last_run_update >= frame_duration_run:
            run_frame_index = (run_frame_index + 1) % len(run_images)  # Loop through run frames
            last_run_update = current_time
        player_image = run_images[run_frame_index]
    else:
        # Idle animation when not moving
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= frame_duration:
            player_frame_index = (player_frame_index + 1) % len(idle_images)  # Loop through idle frames
            last_update = current_time
        player_image = idle_images[player_frame_index]

    # Flip image if moving left
    if not facing_right:
        player_image = pygame.transform.flip(player_image, True, False)

    # Jump logic
    if not jumping and player_on_ground:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Start jump on 'W' key press
            jumping = True
            player_on_ground = False
            player_speed_y = jump_power  # Apply initial jump power

    # Apply gravity during jump or fall
    if not player_on_ground:
        player_speed_y += gravity
        player_y += player_speed_y

    # Check for ground collision after jump/fall
    if player_y + player_image.get_height() >= ground_y:
        player_y = ground_y - player_image.get_height()
        player_speed_y = 0
        player_on_ground = True
        jumping = False  # Reset jump state

    # Update animation based on state
    if jumping:
        # Jump animation
        current_time = pygame.time.get_ticks()
        if current_time - last_jump_update >= jump_frame_duration:
            jump_frame_index = (jump_frame_index + 1) % len(jump_images)  # Loop through jump frames
            last_jump_update = current_time
        player_image = jump_images[jump_frame_index]
    elif moving_left or moving_right:
        # Run animation while moving
        current_time = pygame.time.get_ticks()
        if current_time - last_run_update >= frame_duration_run:
            run_frame_index = (run_frame_index + 1) % len(run_images)
            last_run_update = current_time
        player_image = run_images[run_frame_index]
    else:
        # Idle animation when not moving or jumping
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= frame_duration:
            player_frame_index = (player_frame_index + 1) % len(idle_images)
            player_image = idle_images[player_frame_index]
            last_update = current_time

    # Flip image if moving left during jump
    if not facing_right:
        player_image = pygame.transform.flip(player_image, True, False)

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    # Handle movement and direction
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_a]
    moving_right = keys[pygame.K_d]

    # Update player position based on input
    if moving_left:
        player_x -= player_speed_x
        facing_right = False
    elif moving_right:
        player_x += player_speed_x
        facing_right = True

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
