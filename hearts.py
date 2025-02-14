import pygame
import sys
import os
from Constants import TILE_HEIGHT, TILE_WIDTH, WIDTH, HEIGHT

# def load_image(name, change=False):
#     fullname = os.path.join("images", name)
#     if not os.path.isfile(fullname):
#         print(f"Файл с изображением '{fullname}' не найден")
#         sys.exit()
#     image = pygame.image.load(fullname)
#     if change:
#         image = pygame.transform.scale(image, (TILE_WIDTH, TILE_HEIGHT))
#     return image


# heart1 = load_image("heart.png")
# heart2 = load_image("heart_2_3.png")
# heart3 = load_image("heart_1_3.png")
# heart4 = load_image("heart_0_3.png")


# heart1 =  pygame.transform.scale(heart1, (50, 50))
# heart2 = pygame.transform.scale(heart2, (50, 50))
# heart3 = pygame.transform.scale(heart3, (50, 50))
# heart4 = pygame.transform.scale(heart4, (50, 50))

# class Heart:
#     lifes_of_hero = 6
#     def __init__(self, lifes):
#         self.lifes = int(lifes * 3)

#     def draw(self, screen):
#         l = self.lifes
#         for i in range(Heart.lifes_of_hero):
#             if l - 3 >= 0:
#                 screen.blit(heart1, (i * 60, 0))
#             elif l == 1:
#                 screen.blit(heart3, (i * 60, 0))
#             elif l == 2:
#                 screen.blit(heart2, (i * 60, 0))
#             else:
#                 screen.blit(heart4, (i * 60, 0))
#             l -= 3


# if __name__ == '__main__':
#     pygame.init()
#     size = WIDTH, HEIGHT
#     screen = pygame.display.set_mode(size)
#     screen.fill((255, 255, 255))
#     pygame.display.set_caption("MAIN")
#     hearts = Heart(4 - 2/3)
#     hearts.draw(screen)
#     game = True
#     while game:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 game = False
        
#         pygame.display.flip()
#     pygame.quit()



from Constants import heart, broken_heart
import time

class Lives:
    def __init__(self, initial_lives=3):
        self.lives = initial_lives
        self.font = pygame.font.Font(None, 36)
        self.heart_image = heart
        self.dark_heart_image = broken_heart
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