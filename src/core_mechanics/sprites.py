from settings import *

class Player():
    def __init__(self, pos_x, pos_y, display_surf):
        self.image = pygame.Surface((56,112))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)
        self.display_surf = display_surf
        self.speed = 5
    
    def draw(self):
        self.display_surf.blit(self.image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed