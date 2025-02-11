import pygame
import os
import sys


COLOR = "black"
WIDTH = 1000
HEIGHT = 600
BUTTOM_CLICKED = pygame.USEREVENT + 1
NEW_WINDOW_EVENT = pygame.USEREVENT + 2
user_name = "NoName"


def load_image(name, colorkey=None):
    fullname = os.path.join("images", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

pictures = {"фон для инструкции": load_image("cave.png"),
            "фон для главного" : load_image("fon.png"),
            "монстр": load_image("monster.png"),
            "герой": load_image("hero.png")}