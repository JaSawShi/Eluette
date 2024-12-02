from settings import *

# class Rectangle():
#     def __init__(self, pos_x, pos_y, w, h, color, display_surf):
#         self.image = pygame.Surface((w,h))
#         self.image.fill(color)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (pos_x,pos_y)
#         self.display_surf = display_surf

#     def draw(self):
#         self.display_surf.blit(self.image, self.rect)


# class Platform(Rectangle):
#     def __init__(self, pos_x, pos_y, display_surf):
#         super().__init__(pos_x, pos_y, tile_size, tile_size, tile_color, display_surf)


# class Player(Rectangle):
#     def __init__(self, pos_x, pos_y, display_surf):
#         super().__init__(pos_x, pos_y, p_w, p_h, p_c, display_surf)
#         self.direction = vector(0, 0)
#         self.on_floor = False

#     def move(self, keys, platforms):
#         self.direction.x = 0
#         if keys[K_a]: self.direction.x = -p_speed
#         if keys[K_d]: self.direction.x = p_speed

#         self.direction.y += gravity
#         if keys[K_SPACE] and self.on_floor:
#             self.direction.y = jump_strenght
#             self.on_floor = False

#         self.rect.x += self.direction.x
#         self.handle_collision(platforms, 'horizontal')
#         self.rect.y += self.direction.y
#         self.handle_collision(platforms, 'vertical')

#     def handle_collision(self, platforms, direction):
#         for platform in platforms:
#             if self.rect.colliderect(platform.rect):
#                 if direction == 'horizontal':
#                     if self.direction.x > 0:  # right
#                         self.rect.right = platform.rect.left
#                     if self.direction.x < 0:  # left
#                         self.rect.left = platform.rect.right
#                 if direction == 'vertical':
#                     if self.direction.y > 0:  # fall
#                         self.rect.bottom = platform.rect.top
#                         self.direction.y = 0
#                         self.on_floor = True
#                     if self.direction.y < 0:  # jump
#                         self.rect.top = platform.rect.bottom
#                         self.direction.y = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, collision_sprites):
        super().__init__(groups)
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.pos = pos
        self.image = pygame.Surface(surf)
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 5
        self.gravity = 0.6
        self.on_floor = False


    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -20

    def move(self):
        # horizontal
        self.rect.x += self.direction.x * self.speed 
        self.collision('horizontal')
        
        # vertical 
        self.direction.y += self.gravity 
        self.rect.y += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        self.on_floor = True if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) >= 0 else False

    def update(self):
        self.check_floor()
        self.input()
        self.move()

