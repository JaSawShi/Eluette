from settings import *
from timer_class import Timer

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=(pos))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface(size)  
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = vector()
        self.collision_sprites = collision_sprites
        self.speed = 400
        self.gravity = 50
        self.on_floor = False

        self.attack_timer = Timer(400)  
        # self.target = target 
        

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = - 20
        
        if keys[pygame.K_p] and not self.attack_timer:
            self.attack()
            self.attack_timer.activate()
            

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('hor') # horizontal

        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y 
        self.collision('ver') # vertical

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'hor':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'ver':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.FRect((0,0),(self.rect.width, 8)).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def check_death_conditions(self):
        if self.rect.y >= 2560:
            self.kill()

    def attack(self):
        self.attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 128, self.rect.height)
        print('attacking rect was created')
        # if self.attacking_rect.colliderect(self.target.rect):
        #     print('attacking rect collide with target')


    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.check_death_conditions()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)  
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect(topleft=pos)
        
        # self.target_groups = target_groups


class Spike(Enemy):
    def __init__(self, pos, size, groups):
        super().__init__(pos, size, groups)
