from .animation import AnimatedSprite
from .groups import all_sprites, player_group
from settings import TILE_WIDTH, TILE_HEIGHT
from .utils import load_image


class Player(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        # Загружаем спрайтовую таблицу для анимации
        sheet = load_image('girl_run.png')  # Добавьте изображение в папку `data`
        columns, rows = 7, 1  # Количество столбцов и строк в спрайтовой таблице

        # Инициализация AnimatedSprite
        super().__init__(sheet, columns, rows,
                         TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5,
                         all_sprites, player_group)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_moving = False  # Флаг для отслеживания движения

    def move(self, dx, dy, passability_map):
        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x < len(passability_map[0]) and 0 <= new_y < len(passability_map):
            if passability_map[new_y][new_x]:  # Если клетка проходима
                self.pos_x = new_x
                self.pos_y = new_y
                self.rect.x = TILE_WIDTH * self.pos_x + 15
                self.rect.y = TILE_HEIGHT * self.pos_y + 5
                self.is_moving = True
        else:
            self.is_moving = False

    def update(self):
        # Если игрок двигается, обновляем кадр анимации
        if self.is_moving:
            super().update()
            self.is_moving = False  # Сбрасываем, чтобы остановить анимацию