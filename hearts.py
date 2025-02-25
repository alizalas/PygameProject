import pygame
from Constants import pictures
import time

class Lives:
    def __init__(self, initial_lives=3):
        self.lives = initial_lives
        self.font = pygame.font.Font(None, 36)
        self.heart_image = pictures["heart"]
        self.dark_heart_image = pictures["broken_heart"]
        self.last_decrease_time = 0

    def decrease(self):
        current_time = time.time()  # Текущее время в секундах
        if current_time - self.last_decrease_time >= 1:  # Проверяем, прошла ли секунда
            if self.lives > 0:
                self.lives -= 1
                self.last_decrease_time = current_time  # Обновляем время последнего снятия жизни

    def draw(self, screen):
        for i in range(3):
            if i < self.lives:
                screen.blit(self.heart_image, (10 + i * 40, 10))
            else:
                screen.blit(self.dark_heart_image, (10 + i * 40, 10))

    def is_game_over(self):
        return self.lives == 0