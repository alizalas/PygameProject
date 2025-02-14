import pygame
from Constants import BUTTOM_CLICKED


class Button(pygame.sprite.Sprite):
    """Класс кнопок, которые при нажатии утправляют сигнал с названием кнопки.
      Принимает в качестве аргумента координаты на окне, цвет, текст, размер и группу"""
    def __init__(self, x, y, color, text, size, *group):
        super().__init__(*group)
        self.size = size
        self.text = text
        self.color = color
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, ((0, 0), size))
        pygame.draw.rect(self.image, "black", ((0, 0), size), width=2)
        self.blit_text(self.text)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blit_text(self, text):
        font = pygame.font.Font(None, 20)
        text = font.render(text, True, "white")
        text_x = self.size[0] // 2 - text.get_width() // 2
        text_y = self.size[1] // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))
        
    def get_click(self, mouse_pos):
        if self.check_click(mouse_pos):
            event = pygame.event.Event(BUTTOM_CLICKED, {'window_name': self.text})
            pygame.event.post(event)

    def check_click(self, mouse_pos):
        x = self.rect.x <= mouse_pos[0] <= self.rect.x + self.size[0]
        y = self.rect.y <= mouse_pos[1] <= self.rect.y + self.size[1]
        return (x and y)