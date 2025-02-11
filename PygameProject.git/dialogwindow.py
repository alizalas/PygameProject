import pygame
# import sys
from buttons import Button
from Constants import BUTTOM_CLICKED
# import os



# width, height = 600, 400
WIDTH, HEIGHT = 800, 500
button_group = pygame.sprite.Group()


class DialogWindow:
    """Диалоговое окно для ввода никнейма игрока.
      Принимает в качестве аргумента запрос, который будет расположен в левом верхнем углу"""
    def __init__(self, question):
        self.question = question
        self.size = (WIDTH, HEIGHT)
        self.text = ""
        self.active = False
        self.button = Button(self.size[0] // 2 - 50, self.size[1] - 75, "brown", "Save", (100, 50), button_group)
        self.open()

    def blit_text(self, text, coords):
        font = pygame.font.Font(None, 50)
        text = font.render(text, True, "white")
        if coords =="center":
            text_x = self.size[0] // 2 - text.get_width() // 2
            text_y = self.size[1] // 2 - text.get_height() // 2
        else:
            text_x = coords[0]
            text_y = coords[1]
        self.screen.blit(text, (text_x, text_y))
        
    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button.get_click(event.pos)
           
            self.active = True
            # else:
            #     self.active = False
            

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text = self.text + event.unicode

    def close(self):
        pygame.display.iconify()

    def change(self):
        self.screen.fill("lightgreen" if self.active else "darkgreen")
        self.blit_text(self.question, (0, 0))
        self.blit_text(self.text, "center")

    def open(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Main")

    def draw(self):
        self.change()
        button_group.draw(self.screen)
        
        
        



if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    clock = pygame.time.Clock()
    button_group = pygame.sprite.Group()
    dialog = DialogWindow("Введите имя")
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            dialog.process_event(event)
            if event.type == BUTTOM_CLICKED:
                print(dialog.text)
        dialog.draw()
        pygame.display.flip()
    pygame.quit()


