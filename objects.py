import pygame
import random
from utils import load_image, load_image_sheet
from groups import all_sprites, tiles_group, coin_group, bomb_group, player_group
from settings import TILE_WIDTH, TILE_HEIGHT
from animation import AnimatedSprite
from settings import *
from utils import load_image_sheet



class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, floor, wall):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'empty':
            self.image = load_image(random.choice(floor))
        else:
            self.image = load_image(random.choice(wall))
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('mario.png')
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_moving = False

    def move(self, dx, dy, passability_map):
        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x < len(passability_map[0]) and 0 <= new_y < len(passability_map):
            if passability_map[new_y][new_x]:
                self.pos_x = new_x
                self.pos_y = new_y
                self.rect.x = TILE_WIDTH * self.pos_x
                self.rect.y = TILE_HEIGHT * self.pos_y
                self.is_moving = True
        else:
            self.is_moving = False

    def update(self):
        if self.is_moving:
            super().update()


class Coin(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        sheet = load_image_sheet('coin64.png').convert_alpha()
        super().__init__(sheet, 4, 4, TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y, coin_group, all_sprites)




class Bomb(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        sheet = load_image_sheet('bomb8.png').convert_alpha()
        super().__init__(sheet, 8, 1, TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y, bomb_group, all_sprites)

    def update(self):
        super().update()

''''#отладка монет
pygame.init()
# Создание монеты
coin = Coin(0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление всех спрайтов
    all_sprites.update()

    # Отрисовка всех спрайтов
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()'''

'''#отладка бомб
pygame.init()

# Создание бомбы
bomb = Bomb(0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление всех спрайтов
    all_sprites.update()

    # Отрисовка всех спрайтов
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()'''