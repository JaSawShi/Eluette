#changed animation to _one versions creted 13 nov 2024
#changed last 26 nov 2024
import pygame, sys

pygame.init()
pygame.display.set_caption('Eluette')

screen_w, screen_h = 1024, 768
screen = pygame.display.set_mode((screen_w, screen_h))

ground_y, ground_height = 704, 64
ground_color = (255, 255, 255)

# Load player frames
def load_frames(path, count):
    return [pygame.image.load(f'{path}{i}.png').convert_alpha() for i in range(1, count + 1)]

idle_images = load_frames('without knowledge/images/player/idle/Eluette_idle', 4)
run_images = load_frames('without knowledge/images/player/run/Eluette_run', 8)
jump_images = load_frames('without knowledge/images/player/jump/Eluette_jump', 2)
hit_images = load_frames('without knowledge/images/player/hit/Eluette_hit', 2)
death_images = load_frames('without knowledge/images/player/death/Eluette_disappear', 4)
attack_images = load_frames('without knowledge/images/player/attack/Eluette_attack_one', 4)
shot_images = load_frames('without knowledge/images/player/shot/Eluette_shot_one', 6)  # New shot animation

# Player properties
player_image = idle_images[0]
player_x, player_y = 100, 100
player_speed_y, player_speed_x = 0, 10
player_on_ground, jumping, facing_right, hitting, dying, attacking, shooting = False, False, True, False, False, False, False

# Gravity settings
gravity = 1.5
jump_power = -30

# Animation settings
frame_duration_idle, frame_duration_run, jump_frame_duration, hit_frame_duration = 400, 100, 700, 400
death_frame_duration = 400
attack_frame_duration = 100
shot_frame_duration = 100
frame_index_idle, frame_index_run, frame_index_jump, frame_index_hit, frame_index_death, frame_index_attack, frame_index_shot = 0, 0, 0, 0, 0, 0, 0
last_update_idle, last_update_run, last_update_jump, last_update_hit, last_update_death, last_update_attack, last_update_shot = 0, 0, 0, 0, 0, 0, 0
hit_start_time, death_start_time, attack_start_time, shot_start_time = 0, 0, 0, 0  # Track start times for animations

# Set FPS
fps = 30
clock = pygame.time.Clock()

# Functions to handle animations
def update_animation(images, index, frame_duration, last_update):
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= frame_duration:
        index = (index + 1) % len(images)
        last_update = current_time
    return images[index], index, last_update

def handle_movement():
    global player_x, facing_right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed_x
        facing_right = False
    elif keys[pygame.K_d]:  # Move right
        player_x += player_speed_x
        facing_right = True

# Main game loop
run = True
while run:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, ground_color, pygame.Rect(0, ground_y, screen_w, ground_height))

    # Apply gravity
    if not player_on_ground:
        player_speed_y += gravity
        player_y += player_speed_y

    # Ground collision check
    if player_y + player_image.get_height() >= ground_y:
        player_y = ground_y - player_image.get_height()
        player_speed_y = 0
        player_on_ground = True
        jumping = False
    else:
        player_on_ground = False

    # Handle animations
    current_time = pygame.time.get_ticks()
    if dying:
        if current_time - death_start_time >= death_frame_duration * len(death_images):
            dying = False
            frame_index_death = 0
        else:
            player_image, frame_index_death, last_update_death = update_animation(
                death_images, frame_index_death, death_frame_duration, last_update_death
            )


    elif hitting:
        if current_time - hit_start_time >= 800:
            hitting = False
        else:
            player_image, frame_index_hit, last_update_hit = update_animation(
                hit_images, frame_index_hit, hit_frame_duration // len(hit_images), last_update_hit
            )


    elif attacking:
        if current_time - attack_start_time >= attack_frame_duration * len(attack_images):
            attacking = False
            frame_index_attack = 0
        else:
            player_image, frame_index_attack, last_update_attack = update_animation(
                attack_images, frame_index_attack, attack_frame_duration, last_update_attack
            )


    elif shooting:
        if current_time - shot_start_time >= shot_frame_duration * len(shot_images):
            shooting = False
            frame_index_shot = 0
        else:
            player_image, frame_index_shot, last_update_shot = update_animation(
                shot_images, frame_index_shot, shot_frame_duration, last_update_shot
            )


    elif jumping:
        player_image, frame_index_jump, last_update_jump = update_animation(
            jump_images, frame_index_jump, jump_frame_duration, last_update_jump
        )
    elif any([pygame.key.get_pressed()[pygame.K_a], pygame.key.get_pressed()[pygame.K_d]]):
        player_image, frame_index_run, last_update_run = update_animation(
            run_images, frame_index_run, frame_duration_run, last_update_run
        )
    else:
        player_image, frame_index_idle, last_update_idle = update_animation(
            idle_images, frame_index_idle, frame_duration_idle, last_update_idle
        )

    if not facing_right:
        player_image = pygame.transform.flip(player_image, True, False)

    # Jump logic
    if not jumping and player_on_ground and pygame.key.get_pressed()[pygame.K_w]:
        jumping = True
        player_on_ground = False
        player_speed_y = jump_power

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    # Handle movement
    handle_movement()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            elif event.key == pygame.K_e:  # Start hit
                hitting = True
                frame_index_hit = 0
                last_update_hit = current_time
                hit_start_time = current_time
            elif event.key == pygame.K_r:  # Start death 
                dying = True
                frame_index_death = 0
                last_update_death = current_time
                death_start_time = current_time
            elif event.key == pygame.K_f:  # Start attack 
                attacking = True
                frame_index_attack = 0
                last_update_attack = current_time
                attack_start_time = current_time
            elif event.key == pygame.K_SPACE:  # Start shot 
                shooting = True
                frame_index_shot = 0
                last_update_shot = current_time
                shot_start_time = current_time

    # Update the display
    pygame.display.update()
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
