from settings import *
from sprites import *
from support import *


def main():

    pygame.init()
    screen = pygame.display.set_mode((s_w, s_h))
    pygame.display.set_caption('pre-alpha')
    clock = pygame.time.Clock()

    # VARIABLES

    tmx_map = load_pygame(join('pa_data', 'tmx', 'pa_map.tmx'))

    lvl_w = tmx_map.width * tile_size
    lvl_h = tmx_map.height * tile_size

    class Tile(pygame.sprite.Sprite):
        def __init__(self, pos, surf, groups):
            super().__init__(groups)
            self.image = surf
            self.rect = self.image.get_rect(topleft=pos)

    class Object(pygame.sprite.Sprite):
        def __init__(self, pos, surf, groups):
            super().__init__(groups)
            self.image = pygame.Surface(surf)
            self.image.fill((255,255,255))
            self.rect = self.image.get_rect(topleft=pos)

    class Camera(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2()
            self.half_w = self.display_surface.get_size()[0] // 2
            self.half_h = self.display_surface.get_size()[1] // 2

        def center_target_camera(self, target):
            self.offset.x = target.rect.centerx - self.half_w
            self.offset.y = target.rect.centery - self.half_h

        def custom_draw(self, player):
            self.center_target_camera(player)

            for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)



    camera_group = Camera()
    sprite_group = pygame.sprite.Group()
    collision_group = pygame.sprite.Group()


    for layer in tmx_map.layers:
        if layer.name in ('ground'):
            for x,y,surf in layer.tiles():
                pos = (x * 64, y * 64)
                Tile(pos = pos, surf = surf, groups = (sprite_group, collision_group))


    for layer in tmx_map.layers:
        if layer.name in ('patrol', 'attack'):
            for x,y,surf in layer.tiles():
                pos = (x * 64, y * 64)
                Tile(pos = pos, surf = surf, groups = sprite_group)


    for obj in tmx_map.objects:
        if obj.name == 'player':
            pos = obj.x, obj.y
            surf = (obj.width, obj.height)
            # print(f"Player position: {pos}, size: {surf}")  
            # player = Player(pos=pos, surf=surf, groups=(sprite_group,camera_group), collision_sprites=collision_group)
            player = Player(pos=pos, surf=surf, groups=(camera_group, sprite_group), collision_sprites=collision_group)

        else:
            pos = obj.x, obj.y
            surf = (obj.width, obj.height)
            Object(pos = pos, surf = surf, groups= sprite_group)


    # print("Sprites in sprite_group:")
    # for sprite in sprite_group:
    #     print(sprite, sprite.rect)

    # THE LOOP

    run = True
    while run:
        screen.fill(bg_color)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False

        # player update
        camera_group.update()

        # draw
        sprite_group.draw(screen)
        camera_group.custom_draw(player)


        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()