import os
import sys
import pygame
from settings import TILE_WIDTH, TILE_HEIGHT


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # Изменяем размер изображения до TILE_WIDTH x TILE_HEIGHT
    image = pygame.transform.scale(image, (TILE_WIDTH, TILE_HEIGHT))
    return image

def load_image_sheet(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def create_passability_map(level):
    passability_map = []
    for row in level:
        passability_map.append([cell != '#' for cell in row])
    return passability_map