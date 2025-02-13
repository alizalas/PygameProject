import pygame

# Настройки игры
FPS = 30
V = 7
TILE_WIDTH = TILE_HEIGHT = 60
WIDTH, HEIGHT = 550, 550

WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
BLACK = (0, 0, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()