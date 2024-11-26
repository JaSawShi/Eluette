#no jump, created 07.11.24


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
player_x = 256  # Starting x position of the player
player_y = 256  # Starting y position of the player
player_speed_y = 0  # Vertical speed for gravity

# Load idle animation frames
player_idle_frames = [pygame.image.load(f'images/player/idle/Eluette_idle{i}.png').convert_alpha() for i in range(1, 5)]
current_frame = 0  # Start with the first frame
frame_duration = 4  # Number of frames to show each sprite
frame_count = 0  # Counts frames for timing animation
player_image = player_idle_frames[current_frame]  # Start with the first idle frame
player_facing_left = False  # Track if player is facing left

# Load running animation frames
run_images = [pygame.image.load(f'images/player/run/Eluette_run{i}.png').convert_alpha() for i in range(1, 9)]
run_frame_index = 0  # Start with the first frame for running
run_frame_duration = 8  # Number of frames to show each run sprite
run_frame_count = 0  # Counts frames for timing run animation
is_running = False  # Track if the player is running
player_speed_x = 5  # Horizontal movement speed


# Gravity settings
gravity = 0.5
player_on_ground = False

# Set FPS
fps = 60
clock = pygame.time.Clock()

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

    #     # Update frame count and change animation frame if necessary
    # frame_count += 1
    # if frame_count >= frame_duration:
    #     frame_count = 0
    #     current_frame = (current_frame + 1) % len(player_idle_frames)
        
    #     # Get the current frame and flip it if facing left
    #     player_image = player_idle_frames[current_frame]
    #     if player_facing_left:
    #         player_image = pygame.transform.flip(player_image, True, False)  # Flip horizontally

    # Choose animation based on movement
    if is_running:
        # Update running animation frame
        run_frame_count += 1
        if run_frame_count >= run_frame_duration:
            run_frame_count = 0
            run_frame_index = (run_frame_index + 1) % len(run_images)
            
        # Get the current running frame and flip it if facing left
        player_image = run_images[run_frame_index]
        if player_facing_left:
            player_image = pygame.transform.flip(player_image, True, False)  # Flip horizontally
    else:
        # Idle animation (same as before)
        frame_count += 1
        if frame_count >= frame_duration:
            frame_count = 0
            current_frame = (current_frame + 1) % len(player_idle_frames)
            player_image = player_idle_frames[current_frame]
            if player_facing_left:
                player_image = pygame.transform.flip(player_image, True, False)


    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_a:
                player_facing_left = True
                is_running = True
                player_x -= player_speed_x  # Move left
                player_facing_left = True  # Set facing left
                
            elif event.key == pygame.K_d:
                player_facing_left = False
                is_running = True
                player_x += player_speed_x  # Move right
                player_facing_left = False  # Set facing right
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                is_running = False  # Stop running if either key is released


    # # Event handling
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         run = False
    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_q:
    #             run = False
    #         if event.key == pygame.K_a:
    #             player_facing_left = True  # Set facing left
    #         elif event.key == pygame.K_d:
    #             player_facing_left = False  # Set facing right


    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed_x
        player_facing_left = True
        is_running = True
    elif keys[pygame.K_d]:  # Move right
        player_x += player_speed_x
        player_facing_left = False
        is_running = True
    else:
        is_running = False  # Stop animation when not pressing a movement key


    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
