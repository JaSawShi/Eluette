from settings import *

class Rectangle():
    def __init__(self, pos_x, pos_y, w, h, color, display_surf):
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)
        self.display_surf = display_surf

    def draw(self):
        self.display_surf.blit(self.image, self.rect)


class Platform(Rectangle):
    def __init__(self, pos_x, pos_y, display_surf):
        super().__init__(pos_x, pos_y, tile_size, tile_size, tile_color, display_surf)


class Player(Rectangle):
    def __init__(self, pos_x, pos_y, display_surf):
        super().__init__(pos_x, pos_y, p_w, p_h, p_c, display_surf)
        self.direction = vector(0, 0)
        self.on_ground = False

    def move(self, keys, platforms):
        self.direction.x = 0
        if keys[K_a]: self.direction.x = -p_speed
        if keys[K_d]: self.direction.x = p_speed

        self.direction.y += gravity
        if keys[K_SPACE] and self.on_ground:
            self.direction.y = jump_strenght
            self.on_ground = False

        self.rect.x += self.direction.x
        self.handle_collision(platforms, 'horizontal')
        self.rect.y += self.direction.y
        self.handle_collision(platforms, 'vertical')

    def handle_collision(self, platforms, direction):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # right
                        self.rect.right = platform.rect.left
                    if self.direction.x < 0:  # left
                        self.rect.left = platform.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:  # fall
                        self.rect.bottom = platform.rect.top
                        self.direction.y = 0
                        self.on_ground = True
                    if self.direction.y < 0:  # jump
                        self.rect.top = platform.rect.bottom
                        self.direction.y = 0


