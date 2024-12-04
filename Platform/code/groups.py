from settings import *

class All_sprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - s_w/2)
        self.offset.y = -(target_pos[1] - s_h/2)

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)