import pygame
from settings import *
from utils import load_image_sheet

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *groups):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = pygame.transform.scale(
            self.frames[self.cur_frame], (TILE_WIDTH, TILE_HEIGHT)
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                )
        print("Кадры успешно нарезаны.")  # Подтверждение нарезки кадров

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(
            self.frames[self.cur_frame], (TILE_WIDTH, TILE_HEIGHT)
        )


# Основная программа для отладки
if __name__ == "__main__":
    pygame.init()

    # Константы (замените на реальные значения из settings)
    TILE_WIDTH = 128
    TILE_HEIGHT = 128
    SCREEN_WIDTH, SCREEN_HEIGHT = 200, 200

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AnimatedSprite Debugging")
    clock = pygame.time.Clock()

    try:
        sheet = load_image_sheet('girl.png').convert_alpha()
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        pygame.quit()
        exit()

    girl_run = AnimatedSprite(sheet, 7, 1, 50, 50)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(girl_run)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        all_sprites.update()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()