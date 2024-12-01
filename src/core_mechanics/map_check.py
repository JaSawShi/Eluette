import pygame
from support import *
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((1024,768))
tmx_map = load_pygame(join('pa_data', 'tmx', 'pa_map.tmx'))
# print(dir(tmx_map))
# for obj in tmx_map.objectgroups:
#     print(obj)
layer = tmx_map.get_layer_by_name('ground')
# print(dir(layer))
# for tile in layer.tiles():
#     print(tile)
# for x,y,surf in layer.tiles():
#     print(x)
#     print(y)
#     print(surf)
print(layer.data)

run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            run=False

    screen.fill((0,0,0))

    pygame.display.update()