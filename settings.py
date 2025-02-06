import pygame

# Настройки игры
FPS = 60
V = 6
TILE_WIDTH = TILE_HEIGHT = 50
WIDTH, HEIGHT = 550, 550

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()