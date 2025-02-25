import pygame
from Constants import WIDTH, HEIGHT


def create_fog_mask(radius):
    """
    Создаёт маску тумана с центром в середине экрана.
    """
    fog_mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    for x in range(WIDTH):
        for y in range(HEIGHT):
            # Расстояние от центра экрана
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if distance > radius:
                alpha = 255  # Полностью непрозрачный (чёрный)
            else:
                alpha = int(255 * (distance / radius))  # Плавное затемнение
            fog_mask.set_at((x, y), (0, 0, 0, alpha))

    return fog_mask