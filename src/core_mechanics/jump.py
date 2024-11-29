from settings import *
from sprites import Player

pygame.init()
screen = pygame.display.set_mode((s_w,s_h))
clock = pygame.time.Clock()

player = Player(100,100,screen)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            run = False
    
    screen.fill((0,0,0))

    player.draw()
    player.move()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()