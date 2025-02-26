from settings import * 
from sprites import *
from support import *
from groups import All_sprites
from timer_class import Timer
from random import randint
import timer 

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((s_w, s_h))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = All_sprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        
        # load game
        self.load_assets()
        self.setup()

        # timers
        # self.func_timer = Timer(2000, func = self.some_func)
        # self.func_timer = Timer(2000, func = self.some_func, repeat=True, autostart=True)
        # self.func_timer.activate() #if autostart this line is not need
    
    # def some_func(self):
    #     Spike((randint(300,600),randint(300,600)), (64,64), (self.all_sprites, self.enemy_group))

    def load_assets(self):
        # graphics
        self.worm_frames = import_folder('images', 'enemies', 'worm') # just check it works 


    def setup(self):
        tmx_map = load_pygame(join('PLatform','data','maps','pa_map.tmx'))
        ground_layer = tmx_map.get_layer_by_name('ground')
        patrol_layer = tmx_map.get_layer_by_name('patrol')
        attack_layer = tmx_map.get_layer_by_name('attack')
        objects_layer = tmx_map.get_layer_by_name('objects')
        
        # for tile in ground_layer:
        #     if tile[2] == 4: 
        #         print(tile)

        # for obj in objects_layer:
        #     if obj.name == 'walker': 
        #         print(obj.x,obj.y)

        # for obj in objects_layer:
        #     if obj.name == 'runner': 
        #         print(obj.x,obj.y)

        self.enemy = Enemy((300, 600), (64, 64), (self.all_sprites, self.enemy_group))
        self.enemy2 = Enemy((500, 650), (64, 64), (self.all_sprites, self.enemy_group))

        for x,y, image in ground_layer.tiles():
            Sprite((x*t_s,y*t_s),image,(self.all_sprites, self.collision_sprites)) 

        for x,y, image in patrol_layer.tiles():
            Sprite((x*t_s,y*t_s),image,(self.all_sprites)) 

        for x,y, image in attack_layer.tiles():
            Sprite((x*t_s,y*t_s),image,(self.all_sprites)) 

        for obj in objects_layer:
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), (obj.width, obj.height), (self.all_sprites), self.collision_sprites)
                self.player_group = pygame.sprite.GroupSingle(self.player)
            elif obj.name == 'spike':
                Spike((obj.x, obj.y), (obj.width, obj.height), (self.all_sprites, self.enemy_group), self.player_group)

        class Runner0(pygame.sprite.Sprite):
            def __init__(self, pos, size, groups, player_group, collision_sprites, health=4, speed=4):
                super().__init__(groups)
                self.image = pygame.Surface(size)
                self.image.fill("red")  # Цвет для визуализации врага
                self.rect = self.image.get_rect(topleft=pos)
                self.collision_sprites = collision_sprites  # Препятствия для коллизии
                self.player_group = player_group  # Группа с игроком

                # Характеристики
                self.health = health
                self.base_speed = speed
                self.speed = speed
                self.chasing_speed = speed * 1.5
                self.start_position = pos  # Начальная позиция для возврата

                # Состояния
                self.chasing = False
                self.returning = False

                # Таймеры
                self.chase_delay_timer = Timer(500)  # Задержка преследования

            def player_in_zone(self, zone_rect):
                """Проверка: находится ли игрок в заданной зоне."""
                for player in self.player_group:
                    if zone_rect.colliderect(player.rect):
                        return player
                return None

            def move_towards(self, target_pos):
                """Движение к указанной позиции."""
                if target_pos[0] > self.rect.centerx:
                    self.rect.x += self.speed
                elif target_pos[0] < self.rect.centerx:
                    self.rect.x -= self.speed

                if target_pos[1] > self.rect.centery:
                    self.rect.y += self.speed
                elif target_pos[1] < self.rect.centery:
                    self.rect.y -= self.speed

            def update(self, dt):
                self.chase_delay_timer.update()

                # Определение зон
                player = None
                attack_zone = pygame.Rect(self.rect.centerx - 32, self.rect.centery - 32, 128, 128)
                follow_zone = pygame.Rect(self.rect.centerx - 200, self.rect.centery - 200, 400, 400)

                # Проверяем игрока в зонах
                if not self.chasing:
                    player = self.player_in_zone(follow_zone)
                    if player and not self.chase_delay_timer.active:
                        self.chase_delay_timer.activate()
                elif self.chase_delay_timer.active and not self.chase_delay_timer.active:
                    self.chasing = True
                    self.returning = False
                    print("Runner starts chasing!")

                if self.chasing:
                    self.speed = self.chasing_speed
                    if player:
                        self.move_towards(player.rect.center)
                    else:
                        # Игрок пропал из зоны, возвращаемся
                        self.chasing = False
                        self.returning = True

                # Возврат к стартовой позиции
                if self.returning:
                    self.speed = self.base_speed
                    if (self.rect.centerx, self.rect.centery) != self.start_position:
                        self.move_towards(self.start_position)
                    else:
                        self.returning = False
                        print("Runner returned to patrol zone!")

                # Обработка атаки
                if player and attack_zone.colliderect(player.rect):
                    self.attack(player)

            def attack(self, player):
                """Обработка атаки на игрока."""
                player.take_damage(1)  # Например, у игрока метод take_damage
                print("Player takes damage!")

        self.runnertest = Runner0((2800,2088),(64,152), self.all_sprites, self.player_group, self.collision_sprites)
        
        for obj in objects_layer:
            if obj.name == 'walker': 
                Walker(
                    pos=(obj.x, obj.y+16),
                    size=(obj.width, obj.height),
                    groups=(self.all_sprites, self.enemy_group),  # add to enemy_group
                    target_group = self.player_group,  # add player_group to trigger attack
                    speed=2,
                    move_area_width=t_s * 8
                )
            elif obj.name == 'runner':
                Runner(
                    (obj.x, obj.y), 
                    (obj.width, obj.height), 
                    (self.all_sprites, self.enemy_group), 
                    self.player_group, 
                    self.collision_sprites,
                    6,
                    t_s*16
                    )


    



    def run(self):
        while self.running:
            dt = self.clock.tick(fps) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False 
                    if event.key == pygame.K_p:
                            self.player.attack(self.enemy_group)
                                   


            # update
            # self.func_timer.update()
            self.all_sprites.update(dt)

            # something like respawn
            if self.player not in self.all_sprites:
                self.setup()

            # draw 
            self.screen.fill(bg)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 