import pygame
import sys
from settings import screen, clock, FPS
from utils import load_level, create_passability_map
from level import generate_level
from groups import tiles_group, player_group, coin_group, bomb_group
from objects import Player

# Список изображений для пола и стен
floor = ['floor1.png', 'floor4.png', 'floor5.png']
wall = ['wall1.png']

if __name__ == '__main__':
    level_map = load_level('level1.txt')
    passability_map = create_passability_map(level_map)
    player, level_x, level_y = generate_level(level_map, floor, wall)

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
            print("Игра окончена! Вы наступили на бомбу.")
            running = False

        # Отрисовка
        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        coin_group.draw(screen)
        bomb_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()