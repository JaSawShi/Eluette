from settings import *

class Real_Object():
    def __init__(self, pos_x, pos_y, w, h, color, display_surf):
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)
        self.display_surf = display_surf

    def draw(self):
        self.display_surf.blit(self.image, self.rect)

class Player(Real_Object):
    def __init__(self, pos_x, pos_y, w, h, color, display_surf, speed):
        super().__init__(pos_x, pos_y, w, h, color, display_surf)
        self.speed = speed
        self.on_ground

    def draw(self):
        self.display_surf.blit(self.image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            self.rect.y -= 2