
from level import generate_level

import pygame
import sys
from settings import screen, clock, FPS
from utils import load_level, create_passability_map
from objects import Tile, Player, Coin, Bomb, FlyingEnemy
from groups import tiles_group, player_group, coin_group, bomb_group, enemy_group, all_sprites
from camera import Camera
from images import *
from lives import Lives  # Предположим, что Lives реализован в отдельном файле lives.py


def main(level):
    camera = Camera()
    level_map = load_level(level)
    passability_map = create_passability_map(level_map)

    # Генерация уровня
    player, level_x, level_y = generate_level(level_map, floor, wall)

    # Инициализация системы жизней
    lives = Lives()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            player.move(0, 1, passability_map)
        if keys[pygame.K_UP]:
            player.move(0, -1, passability_map)
        if keys[pygame.K_LEFT]:
            player.move(-1, 0, passability_map)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0, passability_map)

        # Проверка сбора монет
        coins_collected = pygame.sprite.spritecollide(player, coin_group, True)
        if coins_collected:
            print("Монета собрана!")

        # Проверка столкновения с бомбой
        if pygame.sprite.spritecollideany(player, bomb_group):
            lives.decrease()
            if lives.is_game_over():
                print("Игра окончена! Вы наступили на бомбу.")
                running = False
            else:
                print(f"Осталось жизней: {lives.lives}")

        # Проверка столкновения с врагом
        if pygame.sprite.spritecollideany(player, enemy_group):
            print("Игрок погиб от врага!")
            running = False

        # Обновление всех объектов
        player.update()
        for enemy in enemy_group:
            enemy.update()
        coin_group.update()
        bomb_group.update()

        # Обновление камеры
        camera.update(player)

        # Отрисовка
        screen.fill(pygame.Color('black'))

        # Отрисовка тайлов
        for sprite in tiles_group:
            screen.blit(sprite.image, camera.apply(sprite))

        # Отрисовка бомб
        for sprite in bomb_group:
            screen.blit(sprite.image, camera.apply(sprite))

        # Отрисовка монет
        for sprite in coin_group:
            screen.blit(sprite.image, camera.apply(sprite))

        # Отрисовка врагов
        for sprite in enemy_group:
            screen.blit(sprite.image, camera.apply(sprite))

        # Отрисовка игрока
        for sprite in player_group:
            screen.blit(sprite.image, camera.apply(sprite))

        # Отрисовка жизней
        lives.draw(screen)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main('second_level.txt')
    pygame.quit()
    sys.exit()