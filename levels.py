import pygame
import random

from utils import load_image
from animation import AnimatedSprite
from Constants import TILE_HEIGHT, TILE_WIDTH, dragon, enemy_group, sheet_char, x_sheet, y_sheet, coin_image, bomb_image, V, all_sprites, tiles_group, coin_group, bomb_group, player_group
from Players import GIRL, WITCH, KNIGHT

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, floor, wall):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'empty':
            self.image = load_image(random.choice(floor), True)
        else:
            self.image = load_image(random.choice(wall), True)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, char=KNIGHT):
        attr = char.get_attributes()
        super().__init__(player_group, all_sprites)
        self.sheet = attr['sheet']
        self.image_stay = attr['image_stay_char']
        self.animated_sprite = AnimatedSprite(self.sheet, attr['x_sheet'], attr['y_sheet'], pos_x * TILE_WIDTH,
                                              pos_y * TILE_HEIGHT)  # Анимация движения
        self.static_sprite = pygame.sprite.Sprite()  # Статичный спрайт
        self.static_sprite.image = self.image_stay
        self.static_sprite.rect = self.image_stay.get_rect()

        # Устанавливаем начальное изображение и rect
        self.image = self.static_sprite.image
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.center = self.get_center_cell_position(pos_x, pos_y)
        self.target_position = self.rect.center
        self.is_moving = False
        self.move_direction = None
        self.speed = V  # Скорость движения
        self.facing_right = True  # Направление взгляда спрайта (вправо по умолчанию)

    def get_center_cell_position(self, pos_x, pos_y):
        return (TILE_WIDTH * pos_x + TILE_WIDTH // 2, TILE_HEIGHT * pos_y + TILE_HEIGHT // 2)

    def move(self, dx, dy, passability_map):
        if self.is_moving:
            return

        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x < len(passability_map[0]) and 0 <= new_y < len(passability_map):
            if passability_map[new_y][new_x]:
                self.pos_x = new_x
                self.pos_y = new_y
                self.target_position = self.get_center_cell_position(self.pos_x, self.pos_y)
                self.is_moving = True
                self.move_direction = pygame.math.Vector2(self.target_position) - pygame.math.Vector2(self.rect.center)
                if self.move_direction.length() > 0:
                    self.move_direction = self.move_direction.normalize()

                # Определяем направление движения
                if dx < 0:
                    self.facing_right = False
                elif dx > 0:
                    self.facing_right = True
            else:
                self.is_moving = False
        else:
            self.is_moving = False

    def update(self):
        if self.is_moving:
            # Используем анимированный спрайт
            self.image = self.animated_sprite.image
            self.rect = self.animated_sprite.rect

            # Отражаем спрайт, если движемся влево
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

            # Обновляем позицию
            if self.move_direction:
                move_vector = self.move_direction * self.speed
                self.rect.center += move_vector
                self.animated_sprite.rect.center = self.rect.center  # Синхронизируем позицию

                # Проверяем, достигли ли целевой позиции
                distance_to_target = pygame.math.Vector2(self.target_position) - pygame.math.Vector2(self.rect.center)
                if distance_to_target.length() < self.speed:
                    self.rect.center = self.target_position
                    self.is_moving = False
                    self.move_direction = None
            self.animated_sprite.update()
        else:
            self.image = self.static_sprite.image
            self.rect = self.static_sprite.rect
            self.rect.center = self.get_center_cell_position(self.pos_x, self.pos_y)  # Синхронизируем позицию

            # Отражаем спрайт, если смотрим влево
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)


class Coin(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        sheet = load_image(coin_image).convert_alpha()
        super().__init__(sheet, 4, 4, TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y, 6, all_sprites, coin_group)


class Bomb(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        sheet = load_image(bomb_image).convert_alpha()
        super().__init__(sheet, 8, 1, TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y, 20, all_sprites, bomb_group)

    def update(self):
        super().update()


class FlyingEnemy(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        sheet = dragon  # Используем изображение дракона
        super().__init__(sheet, 7, 1, pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT, 4, all_sprites, enemy_group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.center = self.get_center_cell_position(pos_x, pos_y)
        self.target_position = self.rect.center
        self.is_moving = False
        self.move_direction = None
        self.speed = 15  # Скорость движения
        self.move_cooldown = 0  # Задержка перед следующим движением

    def get_center_cell_position(self, pos_x, pos_y):
        return (TILE_WIDTH * pos_x + TILE_WIDTH // 2, TILE_HEIGHT * pos_y + TILE_HEIGHT // 2)

    def choose_random_direction(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Вниз, вверх, вправо, влево
        return random.choice(directions)

    def move(self):
        if self.is_moving:
            return

        dx, dy = self.choose_random_direction()
        self.target_position = (self.rect.centerx + dx * TILE_WIDTH, self.rect.centery + dy * TILE_HEIGHT)
        self.is_moving = True
        self.move_direction = pygame.math.Vector2(self.target_position) - pygame.math.Vector2(self.rect.center)
        if self.move_direction.length() > 0:
            self.move_direction = self.move_direction.normalize()

    def update(self):
        super().update()  # Обновляем анимацию

        if self.is_moving:
            # Обновляем позицию
            if self.move_direction:
                move_vector = self.move_direction * self.speed
                self.rect.center += move_vector

                # Проверяем, достигли ли целевой позиции
                distance_to_target = pygame.math.Vector2(self.target_position) - pygame.math.Vector2(self.rect.center)
                if distance_to_target.length() < self.speed:
                    self.rect.center = self.target_position
                    self.is_moving = False
                    self.move_direction = None
        else:
            # Если враг не движется, выбираем новое направление через случайный интервал
            if self.move_cooldown <= 0:
                self.move()
                self.move_cooldown = random.randint(3, 7)  # Случайная задержка перед следующим движением
            else:
                self.move_cooldown -= 1


            