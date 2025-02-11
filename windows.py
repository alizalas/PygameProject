import pygame
from pygame.locals import SHOWN

from Constants import WIDTH, HEIGHT, BUTTOM_CLICKED, pictures, user_name
from buttons import Button
from dialogwindow import DialogWindow


class Window:
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.buttongroup = pygame.sprite.Group()

    def process_event(self, event):
        pass

    def hide(self):
        pygame.display.iconify()

    def draw(self, screen):
        pygame.display.set_caption(self.name)
        screen.fill(self.color)

    def blit_image(self, screen, image):
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image, (0, 0))

    def blit_text(self, x, y, text, screen, text_size, color_text):
        font = pygame.font.Font(None, text_size)
        if isinstance(text, list):
            text_coord = y
            for line in text:
                string_rendered = font.render(line, True, color_text)
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = x
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            text = font.render(text, True, color_text)
            screen.blit(text, (x, y))


class Main_Window(Window):
    def __init__(self, image, name, color):
        super().__init__(name, color)
        self.button = Button(100, 100, (255, 0, 255), "Инструкция", (90, 60), all_sprites)
        self.btn_r = Button(200, 100, (255, 0, 255), "Рейтинг", (90, 60), all_sprites)
        self.btn_choose = Button(300, 100, (255, 0, 255), "Выбор персонажа", (200, 60), all_sprites)
        self.btn_level1 = Button(230, 370, (0, 0, 200), "Level 1", (280, 60), all_sprites)
        self.btn_level2= Button(230, 450, (0, 0, 175), "Level 2", (280, 60), all_sprites)
        self.btn_level3 = Button(230, 530, (0, 0, 105), "Level 3", (280, 60), all_sprites)
        self.buttongroup.add(self.button, self.btn_choose, self.btn_level1, self.btn_level2, self.btn_level3, self.btn_r)
        self.image1 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image = image

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttongroup:
                btn.get_click(event.pos)

    def show(self):
        self.open()

    def draw(self, screen):
        pygame.display.set_caption("Main_window")
        screen.fill(self.color)
        self.blit_image(screen, self.image)
        self.blit_text(0, 0, f"Здравствуй, {user_name}", screen, 50, "white")
        screen.blit(self.image1, (0, 0, WIDTH, HEIGHT))
        all_sprites.draw(screen)


class New_window(Window):
    def __init__(self, image_name, name, color, color_text):
        super().__init__(name, color)
        self.image = image_name
        self.color_text = color_text

    def process_event(self, event):
        pass
    
    def draw(self, screen):
        pygame.display.set_caption(self.name)
        intro_text = ["ИНСТРУКЦИЯ",
                    "Правила игры:",
                    "-Можно ходить по коридорам, собирая монетки и избегая врагов и бомб",
                    "-Надо добраться до выхода, затратив как можно меньше времени",
                    " и собрав как можно больше монет"]
        # fon = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        screen.fill(self.color)
        self.blit_image(screen, self.image)
        self.blit_text(30, 50, intro_text, screen, 30, "white")


class ChooseOfPlayer(Window):
    def __init__(self, name, color, players):
        super().__init__(name, color)
        self.players = players

    def draw(self, screen):
        x = 50
        pygame.display.set_caption(self.name)
        screen.fill(self.color)
        for image in self.players:
            # im = load_image(image)
            width = image.get_width()
            screen.blit(image, (x + width, 200))
            x += width + 50



if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    start = False
    clock = pygame.time.Clock()
    user_name = "NoName"
    # camera = Camera()
    button_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    dialog = DialogWindow("Введите имя")
    main_window = Main_Window(pictures["фон для главного"], "Main Window", (0, 255, 0))
    window2 = ChooseOfPlayer("Выбор персонажа", (12, 0, 150), [pictures["монстр"], pictures["герой"]])
    window = 0
    
    new_window = New_window(pictures["фон для инструкции"], "Second Window", "cyan", "white")
    
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if start:
                window.process_event(event)
            if event.type == BUTTOM_CLICKED:
                if event.window_name == "Save":
                    name = dialog.text
                    screen = pygame.display.set_mode(size, SHOWN)
                    pygame.display.set_caption("MAIN")
                    window = main_window
                    if name:
                        user_name = name
                    start = True
                elif event.window_name == "Выбор персонажа":
                    window = window2
                elif event.window_name == "Инструкция":
                    window = new_window
            if not start:
                dialog.process_event(event)
            
        if start and window != main_window and not game:
            game = True
            window = main_window
        if not start:
            dialog.draw()
        else:
            window.draw(screen)
        pygame.display.flip()
    pygame.quit()