import pygame
from support import *
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((1024,768))
tmx_map = load_pygame(join('pa_data', 'tmx', 'pa_map.tmx'))

# print(dir(tmx_map))

# for obj in tmx_map.objectgroups:
#     print(obj)

# layer = tmx_map.get_layer_by_name('ground')

# print(dir(layer))

# for tile in layer.tiles():
#     print(tile)

# for x,y,surf in layer.tiles():
#     print(x)
#     print(y)
#     print(surf)

# print(layer.data)

# object_layer = tmx_map.get_layer_by_name('objects')
# print(dir(object))

# for obj in object_layer:
#     print(obj)

# for obj in object_layer:
#     print(dir(obj))

# for obj in object_layer:
    # print(obj.x)
    # print(obj.y)
    # print(obj.width)
    # print(obj.height)
    # print(obj.name)

    # if obj.type == 'enemy':
    #     print(obj)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Object(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface(surf)
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(topleft=pos)



sprite_group = pygame.sprite.Group()

layer_ground = tmx_map.get_layer_by_name('ground')
layer_patrol = tmx_map.get_layer_by_name('patrol')
layer_attack = tmx_map.get_layer_by_name('attack')

object_layer = tmx_map.get_layer_by_name('objects')


for layer in tmx_map.layers:
    if layer.name in ('ground', 'patrol', 'attack'):
        for x,y,surf in layer.tiles():
            pos = (x * 64, y * 64)
            Tile(pos = pos, surf = surf, groups = sprite_group)

for obj in tmx_map.objects:
    pos = obj.x, obj.y
    surf = (obj.width, obj.height)
    Object(pos = pos, surf = surf, groups= sprite_group)


run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            run=False

    screen.fill((0,0,0))

    sprite_group.draw(screen)

    pygame.display.update()