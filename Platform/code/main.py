from settings import * 
from sprites import *
from support import *
from groups import All_sprites
from timer_class import Timer
from random import randint

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

        self.target_groups = pygame.sprite.Group()

        # load game
        self.load_assets()
        self.setup()

        # timers
        self.func_timer = Timer(2000, func = self.some_func)
        # self.func_timer = Timer(2000, func = self.some_func, repeat=True, autostart=True)
        self.func_timer.activate() #if autostart this line is not need
    
    def some_func(self):
        Spike((randint(300,600),randint(300,600)), (64,64), self.all_sprites)


    def load_assets(self):
        # graphics
        self.worm_frames = import_folder('images', 'enemies', 'worm')
        #surf
        self.attack_surf = pygame.Surface((64,64))


    def setup(self):
        tmx_map = load_pygame(join('data','maps','pa_map.tmx'))
        ground_layer = tmx_map.get_layer_by_name('ground')
        patrol_layer = tmx_map.get_layer_by_name('patrol')
        attack_layer = tmx_map.get_layer_by_name('attack')
        objects_layer = tmx_map.get_layer_by_name('objects')
        # for tile in ground_layer:
        #     if tile[2] == 4: 
        #         print(tile)
        self.demo_target_surf = Enemy((320,640), (128,128), self.all_sprites, self.target_groups)

        for x,y, image in ground_layer.tiles():
            Sprite((x*t_s,y*t_s),image,(self.all_sprites, self.collision_sprites)) 

        for x,y, image in patrol_layer.tiles():
            Sprite((x*t_s,y*t_s),image,(self.all_sprites)) 

        for x,y, image in attack_layer.tiles():
            Sprite((x*t_s,y*t_s),image,(self.all_sprites)) 

        for obj in objects_layer:
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y),(obj.width, obj.height), (self.all_sprites), self.collision_sprites, target=self.demo_target_surf)
            elif obj.name == 'spike':
                Spike((obj.x, obj.y),(obj.width, obj.height), self.all_sprites, self.target_groups)

    

    def run(self):
        while self.running:
            dt = self.clock.tick(fps) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.running = False 
            


            # update
            self.func_timer.update()
            # self.player.update(dt, target=self.demo_target_surf)
            self.all_sprites.update(dt,self.demo_target_surf)

            # something like respawn
            # if self.player not in self.all_sprites:
            #     self.setup()

            # draw 
            self.screen.fill(bg)
            self.all_sprites.draw(self.player.rect.topleft)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 