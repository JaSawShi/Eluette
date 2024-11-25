import pygame
from sys import exit 
from random import randint

pygame.init()
pygame.display.set_caption('myturn')

screen_w = 480
screen_h = 384
screen = pygame.display.set_mode((screen_w,screen_h))
player_surface = pygame.Surface((64,64))
player_surface.fill('white')
clock = pygame.time.Clock()
fps = 10

while True:
    screen.fill((0, 0, 0))
    screen.blit(player_surface,(screen_w//2,screen_h//2))
    pygame.draw.rect(screen,'gray', rect=(20,20,50,50))

    pygame.display.update()
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit()

                