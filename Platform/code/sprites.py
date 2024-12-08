from settings import *
from timer_class import Timer
#t_s = tile_size

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
        
        self.facing = "right"
        self.health = 2
        self.damage = 1
        self.attack_timer = Timer(400)  
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health == 1:
            self.image.fill((127, 127, 127))  # be gray
            print("Player wounded!")
        elif self.health <= 0:
            print("respawn!")
            self.health = 2  # full health
            self.image.fill((255, 255, 255))  #  be white
            self.rect.topleft = (500, 100)  # spawn point

    def check_death_conditions(self):
        if self.rect.y >= 2560:
            self.kill()
            
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if self.direction.x > 0:
            self.facing = "right"
        elif self.direction.x < 0:
            self.facing = "left"

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = - 20
        
        # if keys[pygame.K_p] and not self.attack_timer:
        #     self.attack()
        #     self.attack_timer.activate()
            

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


    def attack(self, targets):
        if not self.attack_timer:
            attack = Attack(self, targets, self.damage, self.facing)
            attack.execute()
            self.attack_timer.activate()

    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.check_death_conditions()
        self.attack_timer.update()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)  
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect(topleft=pos)

        self.health = 1 # change in individual enemy class

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            print("enemy defeated!")
            self.kill()
        

class Spike(Enemy):
    def __init__(self, pos, size, groups, target_group):
        super().__init__(pos, size, groups)
        self.health = 1
        self.target_group = target_group  # player's single_group
        self.attack = SpikeAttack(self, self.target_group, 1, t_s * 2)  # damage 1 area 2 tiles

    def update(self, dt):
        # try to attack if in area
        self.attack.execute()
        self.attack.update(dt)

class Attack:
    def __init__(self, source, target_group, damage, facing):
        self.source = source
        self.target_group = target_group
        self.damage = damage
        self.facing = facing

        if self.facing == "right":
            self.attacking_rect = pygame.Rect(
                self.source.rect.right,
                self.source.rect.top,
                t_s, 
                self.source.rect.height
            )
        elif self.facing == "left":
            self.attacking_rect = pygame.Rect(
                self.source.rect.left - t_s, 
                self.source.rect.top,
                t_s,
                self.source.rect.height
            )
    
    def execute(self):
        for target in self.target_group:
            if self.attacking_rect.colliderect(target.rect):
                target.take_damage(self.damage)
                print(f"{target} takes {self.damage} damage!")

class SpikeAttack(Attack):
    def __init__(self, source, target_group, damage, trigger_distance):
        super().__init__(source, target_group, damage, facing=None)
        self.trigger_distance = trigger_distance
        self.area_active = False  # area of attack not active by defolt
        self.cooldown_active = False  # cooldown also

        # timers
        self.area_timer = Timer(500) 
        self.cooldown_timer = Timer(2000)  

    # check players distance
    def is_player_in_range(self):
        for target in self.target_group:
            distance_x = abs(target.rect.centerx - self.source.rect.centerx)
            distance_y = abs(target.rect.centery - self.source.rect.centery)

            if distance_x <= self.trigger_distance and distance_y <= t_s:
                return target
        return None

    # attack section
    def execute(self):
        # if area and cooldown are not active start attack
        if not self.area_active and not self.cooldown_active:
            target = self.is_player_in_range()
            if target:
                self.attacking_rect = pygame.Rect(
                    self.source.rect.centerx - self.source.rect.width // 2,
                    self.source.rect.top - t_s * 2,
                    self.source.rect.width,
                    t_s * 2
                )

                if self.attacking_rect.colliderect(target.rect):
                    target.take_damage(self.damage)
                    print(f"{target} takes {self.damage} damage!")

                self.area_active = True  # attack area active
                self.area_timer.activate()  # attack timer active

    def update(self, dt):
        # update timers
        self.area_timer.update()
        self.cooldown_timer.update()

        # turn off area of attaking after timer ends 
        if self.area_active and not self.area_timer.active:
            self.area_active = False
            self.cooldown_active = True  # turn on colldown timer
            self.cooldown_timer.activate()  # start cooldown timer

        # turn off colldown timer after ending of time
        if self.cooldown_active and not self.cooldown_timer.active:
            self.cooldown_active = False

        # if area is active check is there player nearby
        if self.area_active:
            for target in self.target_group:
                if self.attacking_rect.colliderect(target.rect):
                    # is in attacking area
                    print(f"{target} is in the attack area!")


