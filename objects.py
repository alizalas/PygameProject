import pygame
import random
from utils import load_image, load_image_sheet
from groups import all_sprites, tiles_group, coin_group, bomb_group, player_group
from settings import TILE_WIDTH, TILE_HEIGHT
from animation import AnimatedSprite

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
            TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def move(self, dx, dy, passability_map):
        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x < len(passability_map[0]) and 0 <= new_y < len(passability_map):
            if passability_map[new_y][new_x]:  # Если клетка проходима
                self.pos_x = new_x
                self.pos_y = new_y
                self.rect.x = TILE_WIDTH * self.pos_x + 15
                self.rect.y = TILE_HEIGHT * self.pos_y + 5

    def move(self, dx, dy, passability_map):
        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x < len(passability_map[0]) and 0 <= new_y < len(passability_map):
            if passability_map[new_y][new_x]:
                self.pos_x = new_x
                self.pos_y = new_y
                self.rect.x = TILE_WIDTH * self.pos_x + 15
                self.rect.y = TILE_HEIGHT * self.pos_y + 5
                self.is_moving = True
        else:
            self.is_moving = False

    def update(self):

        if self.is_moving:
            super().update()


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coin_group, all_sprites)
        self.image = load_image('coin.png')
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)



class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bomb_group, all_sprites)
        self.image = load_image('bomb.png')
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)