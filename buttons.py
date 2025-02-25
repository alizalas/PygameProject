import pygame
from Constants import BUTTOM_CLICKED, WIDTH, HEIGHT, RADIO_BUTTON_CLICKED
from music import playing_sound_file


class Button_Parent(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, signal, text, *group):
        super().__init__(*group)
        self.size = size
        self.text = text
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.signal = signal

    def get_click(self, mouse_pos):
        if self.check_click(mouse_pos):
            event = pygame.event.Event(self.signal, {'btn': "btn1"})
            pygame.event.post(event)

    def check_click(self, mouse_pos):
        x = self.rect.x <= mouse_pos[0] <= self.rect.x + self.size[0]
        y = self.rect.y <= mouse_pos[1] <= self.rect.y + self.size[1]
        return (x and y)


class Button(Button_Parent):
    """Класс кнопок, которые при нажатии утправляют сигнал с названием кнопки.
      Принимает в качестве аргумента координаты на окне, цвет, текст, размер и группу"""
    signal = BUTTOM_CLICKED
    def __init__(self, x, y, color, text, size, *group):
        super().__init__(x, y, color, size, Button.signal, text, *group)
        pygame.draw.rect(self.image, self.color, ((0, 0), size))
        pygame.draw.rect(self.image, "black", ((0, 0), size), width=2)
        self.blit_text(self.text)

    def blit_text(self, text):
        font = pygame.font.Font(None, 20)
        text = font.render(text, True, "white")
        text_x = self.size[0] // 2 - text.get_width() // 2
        text_y = self.size[1] // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))
        
    def get_click(self, mouse_pos):
        if self.check_click(mouse_pos):
            event = pygame.event.Event(self.signal, {'window_name': self.text})
            pygame.event.post(event)
            playing_sound_file("sounds/zvuk-najatiya-klavishi.mp3")
    

class RadioButton(Button_Parent):
    signal = RADIO_BUTTON_CLICKED
    def __init__(self, x, y, radius, color, text, clicked, *group):
        super().__init__(x, y, color, (2 * radius, 2 * radius), RadioButton.signal, text, *group)
        self.radius = radius
        self.rect.x = x - radius
        self.rect.y = y - radius
        self.clicked = clicked
        self.change()

    def get_click(self, mouse_pos):
        if self.check_click(mouse_pos):
            self.clicked = not self.clicked
            self.change()
            event = pygame.event.Event(RADIO_BUTTON_CLICKED, {'btn': self})
            pygame.event.post(event)
            playing_sound_file("sounds/zvuk-najatiya-radiobutton.mp3")
    
    def change(self):
        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, 2)
        if self.clicked:
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius - 7)

    def check_click(self, mouse_pos):
        dx = (mouse_pos[0] - self.rect.x - self.radius) ** 2
        dy = (mouse_pos[1] - self.rect.y - self.radius) ** 2
        if dx + dy <= self.radius ** 2:
            return True
    #     if pygame.sprite.spritecollide()
    #     return (x and y)






if __name__ == "__main__":
    pygame.init()
    size = WIDTH, HEIGHT
    clock = pygame.time.Clock()
    button_group = pygame.sprite.Group()
    button1 = RadioButton(100, 200, 20, (230, 27, 150), "WITCH", True, button_group)
    button2 = RadioButton(100, 100, 20, (180, 100, 150), "GIRL", False, button_group)
    button3 = RadioButton(150, 150, 20, (30, 200, 150), "KNIGHT", False, button_group)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Main")
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in button_group:
                    btn.get_click(event.pos)

            if event.type == RADIO_BUTTON_CLICKED:
                for btn in button_group:
                    btn.clicked = False
                    btn.change()
                event.btn.clicked = True
                event.btn.change()

        button_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
