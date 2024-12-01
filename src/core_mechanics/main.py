from settings import *
from sprites import *
from support import *


def main():

    pygame.init()
    display_surf = pygame.display.set_mode((s_w, s_h))
    pygame.display.set_caption('pre-alpha')
    clock = pygame.time.Clock()

    # VARIABLES

    tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))

    # Player and platforms
    player = Player(100, 600, display_surf)
    platforms = [
        Platform(0, 704, display_surf),
        Platform(64, 704, display_surf),
        Platform(128, 704, display_surf),
        Platform(192, 704, display_surf),
        Platform(512, 640, display_surf),
        Platform(576, 384, display_surf)
    ]


    # THE LOOP

    run = True
    while run:
        display_surf.fill(bg_color)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False

        # player update
        player.move(keys, platforms)

        # draw
        player.draw()
        for platform in platforms: platform.draw()

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()