import pygame
from pygame.math import Vector2 as vector

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
PLAYER_WIDTH, PLAYER_HEIGHT = 56, 112
PLAYER_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Rectangle:
    def __init__(self, pos_x, pos_y, w, h, color, display_surf):
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.display_surf = display_surf

    def draw(self):
        self.display_surf.blit(self.image, self.rect)

class Player(Rectangle):
    def __init__(self, pos_x, pos_y, display_surf):
        super().__init__(pos_x, pos_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR, display_surf)
        self.position = vector(pos_x, pos_y)
        self.velocity = vector(0, 0)
        self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity.y += GRAVITY

    def jump(self):
        if self.on_ground:
            self.velocity.y = JUMP_STRENGTH
            self.on_ground = False

    def update(self, platforms):
        self.apply_gravity()

        # Обновление позиции игрока
        self.position += self.velocity
        self.rect.topleft = self.position

        # Проверка коллизии с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity.y >= 0:
                self.on_ground = True
                self.velocity.y = 0
                self.position.y = platform.rect.top - PLAYER_HEIGHT
                break

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

class Platform(Rectangle):
    pass

# Список платформ
platforms = [
    Platform(200, 600, 400, 64, (255, 255, 255), screen),
    Platform(700, 400, 200, 64, (255, 255, 255), screen)
]

# Создание игрока
player = Player(300, 500, screen)

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка ввода
    player.handle_input()

    # Обновление игрока
    player.update(platforms)

    # Отрисовка
    screen.fill(BG_COLOR)
    player.draw()
    for platform in platforms:
        platform.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
