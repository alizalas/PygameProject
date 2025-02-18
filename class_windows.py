import pygame
from Constants import WIDTH, HEIGHT, all_sprites, tiles_group, player_group, coin_group, bomb_group, floor, wall, enemy_group, RADIO_BUTTON_CLICKED, CHOOSE_EVENT
from buttons import Button, RadioButton
from utils import create_passability_map, load_level
from level import generate_level
from camera import Camera
from Players import WITCH, GIRL, KNIGHT



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
        self.user_name = "NoName"
        self.button = Button(100, 100, (255, 0, 255), "Инструкция", (90, 60), all_sprites)
        self.btn_r = Button(200, 100, (255, 0, 255), "Рейтинг", (90, 60), all_sprites)
        self.btn_choose = Button(300, 100, (255, 0, 255), "Выбор персонажа", (200, 60), all_sprites)
        self.btn_level1 = Button(230, 370, (0, 0, 200), "Level 1", (280, 60), all_sprites)
        self.btn_level2= Button(230, 450, (0, 0, 175), "Level 2", (280, 60), all_sprites)
        self.btn_level3 = Button(230, 530, (0, 0, 105), "Level 3", (280, 60), all_sprites)
        self.buttongroup.add(self.button, self.btn_choose, self.btn_level1, self.btn_level2, self.btn_level3, self.btn_r)
        # self.image1 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image = image

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttongroup:
                btn.get_click(event.pos)

    def change_name(self, name):
        self.user_name = name

    def draw(self, screen):
        pygame.display.set_caption("Main_window")
        screen.fill(self.color)
        self.blit_image(screen, self.image)
        self.blit_text(0, 0, f"Здравствуй, {self.user_name}", screen, 50, "white")
        # screen.blit(self.image1, (0, 0, WIDTH, HEIGHT))
        self.buttongroup.draw(screen)


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


class PlayWindow(Window):
    def __init__(self, name, color, level):
        super().__init__(name, color)
        self.level = level
        self.level_map = load_level(level)
        self.passability_map = create_passability_map(self.level_map)
        self.player, self.x, self.y = generate_level(self.level_map, floor, wall)
        self.player_name = WITCH
        self.camera = Camera()

    def process_event(self, event):
        if event.type == pygame.QUIT:
            player_group.empty()
            coin_group.empty()
            bomb_group.empty()
            enemy_group.empty()
            tiles_group.empty()
        
        #    all_sprites.empty()
        #    player_group.empty()
    
    def change_player(self, name):
        print("Зашел")
        if name == "WITCH":
            self.player_name = WITCH
        elif name == "GIRL":
            self.player_name = GIRL
        elif name == "KNIGHT":
            self.player_name = KNIGHT
        self.player.change_image(self.player_name)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        coin_group.update()
        bomb_group.update()

        self.player.update()
        # if all(sprite.rect.x >= 0 and sprite.rect.y >= 0 for sprite in far_walls):
        self.camera.update(self.player)

        for sprite in tiles_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in bomb_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in coin_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in player_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        # else:
        #     tiles_group.draw(screen)
        #     bomb_group.draw(screen)
        #     coin_group.draw(screen)
        #     player_group.draw(screen)


class ChooseOfPlayer(Window):
    signal = CHOOSE_EVENT
    def __init__(self, name, color, players):
        super().__init__(name, color)
        self.players = players
        self.btn_group = pygame.sprite.Group()
        self.button_witch = RadioButton(150, HEIGHT - 50, 20, (230, 27, 150), "WITCH", True, self.btn_group)
        self.button_supergirl = RadioButton(470, HEIGHT - 50, 20, (180, 100, 150), "GIRL", False, self.btn_group)
        self.button_knight = RadioButton(750, HEIGHT - 50, 20, (30, 200, 150), "KNIGHT", False, self.btn_group)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btn_group:
                btn.get_click(event.pos)

        elif event.type == RADIO_BUTTON_CLICKED:
                for btn in self.btn_group:
                    btn.clicked = False
                    btn.change()
                event.btn.clicked = True
                event.btn.change()

        elif event.type == pygame.QUIT:
            for i in self.btn_group:
                if i.clicked:
                    event1 = pygame.event.Event(CHOOSE_EVENT, {'btn': i.text})
                    pygame.event.post(event1)
                    break


    def draw(self, screen):
        x = 50
        pygame.display.set_caption(self.name)
        screen.fill(self.color)
        self.btn_group.draw(screen)
        for image in self.players:
            # im = load_image(image)
            width = image.get_width() - 50
            screen.blit(image, (x, 100))
            x += width