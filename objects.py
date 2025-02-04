import pygame
import random
from utils import load_image, load_image_sheet
from groups import all_sprites, tiles_group, coin_group, bomb_group, player_group
from settings import TILE_WIDTH, TILE_HEIGHT, V
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
        self.rect = self.image.get_rect()  # Получаем rect без начального смещения
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Устанавливаем начальную позицию в центре клетки
        self.rect.center = self.get_center_cell_position(pos_x, pos_y)

        self.target_position = self.rect.center  # Целевая позиция для плавного движения
        self.is_moving = False
        self.move_direction = None  # Направление движения (вектор)
        self.speed = V  # Скорость движения (можно настроить)

    def get_center_cell_position(self, pos_x, pos_y):
        """Возвращает координаты центра клетки для заданной позиции клетки."""
        return (TILE_WIDTH * pos_x + TILE_WIDTH // 2, TILE_HEIGHT * pos_y + TILE_HEIGHT // 2)

    def move(self, dx, dy, passability_map):
        """Инициирует движение в заданном направлении."""
        if self.is_moving:  # Предотвращаем новое движение, пока текущее не завершено
            return

        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x < len(passability_map[0]) and 0 <= new_y < len(passability_map):
            if passability_map[new_y][new_x]:
                self.pos_x = new_x
                self.pos_y = new_y
                self.target_position = self.get_center_cell_position(self.pos_x, self.pos_y) # Устанавливаем целевую позицию
                self.is_moving = True
                self.move_direction = pygame.math.Vector2(self.target_position) - pygame.math.Vector2(self.rect.center) # Вычисляем вектор направления
                if self.move_direction.length() > 0: # Нормализуем вектор, если длина не нулевая
                    self.move_direction = self.move_direction.normalize()
            else:
                self.is_moving = False
        else:
            self.is_moving = False

    def update(self):
        """Обновляет положение игрока для плавного движения."""
        if self.is_moving:
            if self.move_direction:
                move_vector = self.move_direction * self.speed # Умножаем направление на скорость
                self.rect.center += move_vector # Двигаем игрока

                # Проверяем, достигли ли мы целевой позиции
                distance_to_target = pygame.math.Vector2(self.target_position) - pygame.math.Vector2(self.rect.center)
                if distance_to_target.length() < self.speed: # Если расстояние меньше скорости, значит, мы почти у цели
                    self.rect.center = self.target_position # Точно устанавливаем позицию в центр клетки
                    self.is_moving = False # Останавливаем движение
                    self.move_direction = None # Сбрасываем направление



class Coin(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        sheet = load_image_sheet('coin64.png').convert_alpha()
        super().__init__(sheet, 4, 4, TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y, 4, all_sprites, coin_group)




class Bomb(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        sheet = load_image_sheet('bomb8.png').convert_alpha()
        super().__init__(sheet, 8, 1, TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y, 4, all_sprites, bomb_group)

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

pygame.quit()

#отладка персонажа
if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Пример карты проходимости (замените на вашу реальную карту)
    passability_map = [
        [True, True, True, True, True],
        [True, False, True, True, True],
        [True, True, True, False, True],
        [True, True, True, True, True],
        [True, True, True, True, True],
        [True, True, True, True, True]
    ]

    # Создаем игрока в начальной позиции (0, 0)
    player = Player(0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            player.move(0, 1, passability_map)
        if keys[pygame.K_UP]:
            player.move(0, -1, passability_map)
        if keys[pygame.K_LEFT]:
            player.move(-1, 0, passability_map)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0, passability_map)
        screen.fill(pygame.Color('black'))
        player_group.draw(screen)  # Рисуем группу спрайтов игрока
        player_group.update()      # Обновляем спрайты игрока

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()'''
