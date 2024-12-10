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
        print('attack was dealt!')
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
        self.damage_dealt = False  # damage has not been wonded

        # timers
        self.area_timer = Timer(500)
        self.cooldown_timer = Timer(2000)

    # trigger rect
    def is_player_in_range(self):
        # create trigger rect
        trigger_rect = pygame.Rect(
            self.source.rect.centerx - t_s * 2.5,  # center by horizontal
            self.source.rect.centery - t_s // 2,  # center by vertical
            t_s * 5,  # range 4 toiles
            t_s  # 1 tile height
        )

        # check player in trigger rect
        for target in self.target_group:
            if trigger_rect.colliderect(target.rect):
                return target
        return None

    # attack start
    def execute(self):
        # if area and cooldown are not active start attack
        if not self.area_active and not self.cooldown_active:
            target = self.is_player_in_range()
            if target:
                print("attack zone is active!")
                self.attacking_rect = pygame.Rect(
                    self.source.rect.centerx - self.source.rect.width // 2,
                    self.source.rect.top - t_s * 2,
                    self.source.rect.width,
                    t_s * 2
                )
                self.area_active = True  # activate zone 
                self.damage_dealt = False  # reset flag
                self.area_timer.activate()  # attack timer active

    # update state
    def update(self, dt):
        # timers update
        self.area_timer.update()
        self.cooldown_timer.update()

        # deactivate area of attaking after timers end
        if self.area_active and not self.area_timer.active:
            self.area_active = False
            self.cooldown_active = True  # turn on colldown timer
            self.cooldown_timer.activate()  # start cooldown timer
            print("Cooldown!")

        # turn off colldown timer after ending of time
        if self.cooldown_active and not self.cooldown_timer.active:
            self.cooldown_active = False

        # if area is active check is there player nearby 
        if self.area_active and not self.damage_dealt:
            for target in self.target_group:
                if self.attacking_rect.colliderect(target.rect):
                    target.take_damage(self.damage)
                    self.damage_dealt = True  # damage was takken
                    print(f"{target} is get {self.damage} damage")

class Walker(Enemy):
    def __init__(self, pos, size, groups, speed, move_area_width, target_group):
        super().__init__(pos, size, groups)
        self.health = 2  
        self.speed = speed
        self.move_area_width = move_area_width
        self.target_group = target_group


        # patrol zone
        self.move_area = pygame.Rect(
            self.rect.centerx - self.move_area_width // 2,
            self.rect.centery - t_s // 2,
            self.move_area_width,
            t_s
        )

        # state settings
        self.direction = 1  # 1 = right, -1 = left
        self.trigger_distance = t_s * 1
        self.preparing_to_attack = False
        self.attacking = False
        self.on_cooldown = False

        # timers
        self.prepare_timer = Timer(500)  # prepare to attack time (0.5sec)
        self.attack_timer = Timer(500)  # attack time (0.5sec)
        self.cooldown_timer = Timer(1000)  # cooldown (1sec)

        # for example
        # self.prepare_timer = Timer(2500)  
        # self.attack_timer = Timer(2500)  
        # self.cooldown_timer = Timer(5000)  

        # attack
        self.attack = WalkerAttack(self, self.target_group, damage=1)

    def move(self):
        # Moves only when not attacking, not on cooldown, and not preparing to attack.
        if not self.preparing_to_attack and not self.attacking and not self.on_cooldown:
            self.rect.x += self.speed * self.direction
            if self.rect.left < self.move_area.left or self.rect.right > self.move_area.right:
                self.direction *= -1

    def check_trigger_area(self):
        # check trigger zone
        trigger_rect = pygame.Rect(
            self.rect.right if self.direction == 1 else self.rect.left - self.trigger_distance,
            self.rect.top,
            self.trigger_distance,
            t_s
        )
        for target in self.target_group:
            if trigger_rect.colliderect(target.rect):
                return True
        return False

    def update(self, dt):
        # timers update
        self.prepare_timer.update()
        self.attack_timer.update()
        self.cooldown_timer.update()

        # If the player is in the trigger zone and Walker is not ready to attack, not attacking, and not on cooldown
        if self.check_trigger_area() and not self.preparing_to_attack and not self.attacking and not self.on_cooldown:
            self.preparing_to_attack = True
            self.prepare_timer.activate()
            print('in trigger zone')

        # If the preparation timer has expired
        if self.preparing_to_attack and not self.prepare_timer.active:
            self.preparing_to_attack = False
            self.attacking = True
            self.attack_timer.activate()
            print('attack zone created')

        # If the attack timer has expired
        if self.attacking and not self.attack_timer.active:
            self.attacking = False
            self.on_cooldown = True
            self.cooldown_timer.activate()
            print('cooldown start')

        # If the cooldown has ended
        if self.on_cooldown and not self.cooldown_timer.active:
            self.on_cooldown = False
            print('cooldown ends')

        # attack execution
        if self.attacking:
            self.attack.execute()

        # move
        self.move()

        # attack update
        self.attack.update(dt)


class WalkerAttack(Attack):
    def __init__(self, source, target_group, damage):
        super().__init__(source, target_group, damage, facing=None)
        self.area_active = False

        # attack range exist timer
        self.area_timer = Timer(500) 

        # for example
        # self.area_timer = Timer(2500) 

    def execute(self):
        if not self.area_active:
            # Create an attack area depending on the direction
            self.attacking_rect = pygame.Rect(
                self.source.rect.right if self.source.direction == 1 else self.source.rect.left - t_s * 2,
                self.source.rect.top,
                t_s * 2,
                t_s
            )
            self.area_active = True
            self.area_timer.activate()

            # Deal damage to the player if he is in the attack area
            for target in self.target_group:
                if self.attacking_rect.colliderect(target.rect):
                    target.take_damage(self.damage)
                    print(f"{target} получил {self.damage} урона!")

    def update(self, dt):
        self.area_timer.update()
        if self.area_active and not self.area_timer.active:
            self.area_active = False


class Runner(Walker):
    def __init__(self, pos, size, groups, player_group, collision_sprites, speed, move_area_width):
        super().__init__(pos, size, groups, speed, move_area_width, player_group)
        self.chase_delay_timer = Timer(500)  # 500 ms delay before starting chase
        self.chasing = False  # Is the Runner chasing the player
        self.returning = False  # Is the Runner returning to its start position
        self.start_position = pos  # Runner's initial position
        self.collision_sprites = collision_sprites  # Sprites to check collision
        self.base_speed = speed  # Base speed
        self.chase_speed = speed * 1.5  # Increased speed during chase (1.5x)

    def player_in_trigger_zone(self):
        """Check if the player is within the Runner's trigger zone."""
        trigger_rect = pygame.Rect(
            self.rect.centerx - t_s * 3,  # Larger horizontal detection area
            self.rect.centery - t_s // 2,  # Center vertically
            t_s * 6,  # Range of 6 tiles horizontally
            t_s  # 1 tile height
        )
        for player in self.target_group:
            if trigger_rect.colliderect(player.rect):
                return player
        return None

    def get_player(self):
        """Return the player object if in range, otherwise None."""
        return self.player_in_trigger_zone()

    def move_towards_player(self, player):
        """Move towards the player's position."""
        if player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
        elif player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed

    def move_towards_position(self, position):
        """Move towards a specific position."""
        if position[0] > self.rect.centerx:
            self.rect.x += self.speed
        elif position[0] < self.rect.centerx:
            self.rect.x -= self.speed

    def update(self, dt):
        super().update(dt)
        self.chase_delay_timer.update()

        # Check for player in trigger zone
        player = self.get_player()
        if player and not self.chasing and not self.chase_delay_timer.active:
            self.chase_delay_timer.activate()
            print("Runner is preparing to chase...")
        elif player and self.chase_delay_timer.active and not self.chase_delay_timer.active:
            self.chasing = True
            self.returning = False
            self.speed = self.chase_speed  # Increase speed during chase
            print("Runner starts chasing the player!")

        # Chase the player if in range
        if self.chasing and player:
            self.move_towards_player(player)
        elif self.chasing and not player:
            # Stop chasing and return to start position
            self.chasing = False
            self.returning = True
            self.speed = self.base_speed  # Reset speed when not chasing
            print("Runner lost the player and will return!")

        # Return to the start position
        if self.returning:
            if (self.rect.centerx, self.rect.centery) != self.start_position:
                self.move_towards_position(self.start_position)
            else:
                self.returning = False
                print("Runner returned to start position!")




class RunnerAttack(Attack):
    def __init__(self, source, target_group, damage, facing, attack_delay=500):
        super().__init__(source, target_group, damage, facing)
        self.attack_delay_timer = Timer(attack_delay)  # Задержка перед атакой (500 мс)
        self.attack_active_timer = Timer(500)  # Активная зона урона (500 мс)
        self.cooldown_timer = Timer(1000)  # Кулдаун после атаки (1 секунда)
        self.state = "idle"  # idle -> preparing -> attacking -> cooldown

    def execute(self):
        if self.state == "idle":
            self.state = "preparing"
            self.attack_delay_timer.activate()
            print("Runner is preparing to attack...")

    def update(self, dt):
        self.attack_delay_timer.update()
        self.attack_active_timer.update()
        self.cooldown_timer.update()

        if self.state == "preparing" and not self.attack_delay_timer.active:
            self.state = "attacking"
            self.attack_active_timer.activate()
            print("Runner attack area activated!")

        if self.state == "attacking":
            for target in self.target_group:
                if self.attacking_rect.colliderect(target.rect):
                    target.take_damage(self.damage)
                    print(f"Player takes {self.damage} damage!")
            if not self.attack_active_timer.active:
                self.state = "cooldown"
                self.cooldown_timer.activate()
                print("Runner is cooling down...")

        if self.state == "cooldown" and not self.cooldown_timer.active:
            self.state = "idle"
            print("Runner is ready again.")
