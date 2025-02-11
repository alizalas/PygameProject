import pygame

from Constants import WIDTH, HEIGHT, BUTTOM_CLICKED, pictures, user_name, floor, wall
from buttons import Button
from dialogwindow import DialogWindow
from Constants import tiles_group, coin_group, bomb_group, all_sprites, player_group, image_stay_char
from utils import load_level, create_passability_map
from camera import Camera
from level import generate_level



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
        # self.image1 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image = image

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttongroup:
                btn.get_click(event.pos)

    def draw(self, screen):
        pygame.display.set_caption("Main_window")
        screen.fill(self.color)
        self.blit_image(screen, self.image)
        self.blit_text(0, 0, f"Здравствуй, {user_name}", screen, 50, "white")
        # screen.blit(self.image1, (0, 0, WIDTH, HEIGHT))
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


class PlayWindow(Window):
    def __init__(self, name, color, level):
        super().__init__(name, color)
        self.level = level
        self.level_map = load_level(level)
        self.passability_map = create_passability_map(self.level_map)
        self.player, self.x, self.y = generate_level(self.level_map, floor, wall)
        self.camera = Camera()

    def process_event(self, event):
        if event.type == pygame.QUIT:
            print("Я здесь")
            tiles_group.empty()
            player_group.empty()
            coin_group.empty()
            bomb_group.empty()

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
            screen.blit(image, (x + width, 100))
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
    window2 = ChooseOfPlayer("Выбор персонажа", (12, 0, 150), [pygame.transform.scale(image_stay_char, (250, 400)), pictures["герой"]])
    window = 0
    
    new_window = New_window(pictures["фон для инструкции"], "Second Window", "cyan", "white")
    play_window = 1
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
                    screen = pygame.display.set_mode(size)
                    pygame.display.set_caption("MAIN")
                    window = main_window
                    if name:
                        user_name = name
                    start = True
                elif event.window_name == "Выбор персонажа":
                    window = window2
                elif event.window_name == "Инструкция":
                    window = new_window
                elif event.window_name == "Level 1":
                    play_window = PlayWindow("Level №1", "black", "first_level.txt")
                    print(play_window.player.pos_x, play_window.player.pos_y)
                    window = play_window
                elif event.window_name == "Level 2":
                    play_window = PlayWindow("Level №2", "black", "second_level.txt")
                    print(play_window.player.pos_x, play_window.player.pos_y)
                    window = play_window
                elif event.window_name == "Level 3":
                    play_window = PlayWindow("Level №3", "black", "third_level.txt")
                    print(play_window.player.pos_x, play_window.player.pos_y)
                    window = play_window
            if not start:
                dialog.process_event(event)
            
        if start and window != main_window and not game:
            game = True
            window = main_window
        if not start:
            dialog.draw()
        else:
            window.draw(screen)
        

        keys = pygame.key.get_pressed()
        if window == play_window:
            if keys[pygame.K_DOWN]:
                play_window.player.move(0, 1, play_window.passability_map)
            if keys[pygame.K_UP]:
                play_window.player.move(0, -1, play_window.passability_map)
            if keys[pygame.K_LEFT]:
                play_window.player.move(-1, 0, play_window.passability_map)
            if keys[pygame.K_RIGHT]:
                play_window.player.move(1, 0, play_window.passability_map)

        # Проверка сбора монет
            coins_collected = pygame.sprite.spritecollide(play_window.player, coin_group, True)
            if coins_collected:
                print("Монета собрана!")

            # Проверка столкновения с бомбой
            # if pygame.sprite.spritecollideany(play_window.player, bomb_group):
            #     print("Игра окончена! Вы наступили на бомбу.")
                # game = False 


        pygame.display.flip()
    pygame.quit()