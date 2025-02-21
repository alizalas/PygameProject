import pygame

pygame.init()


def playing_sound_file(filename):
    pygame.mixer.init()
    pygame.mixer.Sound(filename).play()