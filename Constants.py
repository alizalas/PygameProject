import pygame
import os
import sys

COLOR = "black"
WIDTH = 1000
HEIGHT = 600
BUTTOM_CLICKED = pygame.USEREVENT + 1
NEW_WINDOW_EVENT = pygame.USEREVENT + 2
RADIO_BUTTON_CLICKED = pygame.USEREVENT + 3
CHOOSE_EVENT = pygame.USEREVENT + 4


FPS = 20
V = 5
TILE_WIDTH = TILE_HEIGHT = 60

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def load_image(name, change=False):
    # if name == "cave.png":
    #     print("Загрузил")
    fullname = os.path.join("images", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if change:
        image = pygame.transform.scale(image, (TILE_WIDTH, TILE_HEIGHT))
    return image

pictures = {"фон для инструкции": load_image("cave.png"),
            "фон для главного" : load_image("fon.png"),
            "монстр": load_image("monster.png"),
            "герой": load_image("hero.png"),
            "heart" : load_image('heart.png', True),
            "broken heart": load_image('broken_heart.png', True),
            "dragon" : load_image('dragon.png'),
            "witch_stay": pygame.transform.scale(load_image('witch_stay.png'), (320, 440)),
            "witch_player" : load_image('witch_stay.png', True),
            "witch": load_image('witch.png'),
            "girl_stay": pygame.transform.scale(load_image("girl_stay.png"), (319, 371)),
            "girl_player" : load_image("girl_stay.png", True),
            "girl": load_image("girl.png"),
            "knight_stay" : pygame.transform.scale(load_image("knight_stay.png"), (340, 400)),
            "knight_player" : load_image("knight_stay.png", True),
            "knight": load_image("knight.png")}


coin_image = 'coin64.png'
bomb_image = 'bomb8.png'

floor = ['floor1.png', 'floor4.png', 'floor5.png']
wall = ['wall1.png']
heart = load_image('heart.png', True)
broken_heart = load_image('broken_heart.png', True)
dragon = load_image('dragon.png')

sheet_char = load_image('witch.png')
x_sheet, y_sheet = 1, 8# Спрайт-лист для анимации движения
image_stay_char = load_image('witch_stay.png', True)  # Статичное изображение


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
far_walls = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()