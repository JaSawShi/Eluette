import pygame, sys
from random import randint
from os import walk
from os.path import join
from pygame.math import Vector2 as vector
from pygame.locals import *
from pytmx.util_pygame import load_pygame

s_w = 1024
s_h = 768
bg_color = (0,0,0)
fps = 60

tile_size = 64
tile_color = (255, 255, 255)

# p_w = 56
# p_h = 112
# p_c = (255,255,255)

# gravity = 0.5
# jump_strenght = -20
# p_speed = 6