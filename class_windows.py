import pygame
from Constants import WIDTH, HEIGHT, tiles_group, player_group, coin_group, bomb_group, floor, wall, enemy_group
from buttons import Button, RadioButton
from sounds import playing_sound_file
from utils import create_passability_map, load_level
from level import generate_level
from camera import Camera
from hearts import Lives
from Players import WITCH, GIRL, KNIGHT
from Constants import font_coins, all_coins, pictures, FINISH_GAME, RADIO_BUTTON_CLICKED, CHOOSE_EVENT



class Window:
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.btn_group = pygame.sprite.Group()

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
        self.button = Button(100, 100, (255, 0, 255), "Инструкция", (90, 60), self.btn_group)
        self.btn_r = Button(200, 100, (255, 0, 255), "Рейтинг", (90, 60), self.btn_group)
        self.btn_choose = Button(300, 100, (255, 0, 255), "Выбор персонажа", (200, 60), self.btn_group)
        self.btn_level1 = Button(230, 370, (0, 0, 200), "Level 1", (280, 60), self.btn_group)
        self.btn_level2= Button(230, 450, (0, 0, 175), "Level 2", (280, 60), self.btn_group)
        self.btn_level3 = Button(230, 530, (0, 0, 105), "Level 3", (280, 60), self.btn_group)
        # self.buttongroup.add(self.button, self.btn_choose, self.btn_level1, self.btn_level2, self.btn_level3, self.btn_r)
        # self.image1 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image = image

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btn_group:
                btn.get_click(event.pos)

    def change_name(self, name):
        self.user_name = name

    def draw(self, screen):
        pygame.display.set_caption("Main_window")
        screen.fill(self.color)
        self.blit_image(screen, self.image)
        self.blit_text(0, 0, f"Здравствуй, {self.user_name}", screen, 50, "white")
        # screen.blit(self.image1, (0, 0, WIDTH, HEIGHT))
        self.btn_group.draw(screen)


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
        self.lives = Lives()
        self.camera = Camera()
        self.start_time = pygame.time.get_ticks()
        self.collected_coins = 0
        self.all_coins_for_level = all_coins[name]

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.clean()
            print(isinstance(int, pygame.time.get_ticks()))
        #    all_sprites.empty()
        #    player_group.empty()
    
    def clean(self):
        player_group.empty()
        coin_group.empty()
        bomb_group.empty()
        enemy_group.empty()
        tiles_group.empty()
        event1 = pygame.event.Event(FINISH_GAME, {"coins": self.collected_coins, "all_coins": self.all_coins_for_level, "time": get_time(self)})
        pygame.event.post(event1)
        # self.start_time = pygame.time.get_ticks()
    
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


class Result(Window):
    def __init__(self, name, color, result):
        super().__init__(name, color)
        self.time = 0
        self.coints = 0
        self.all_time = 0
        self.all_coins = 0
        if result:
            self.image = pygame.transform.scale(pictures["win"], (WIDTH, HEIGHT))
            self.color_btn = (100, 90, 50)
            self.sound = "sounds/zvuk-pobedy.mp3"
        else:
            self.image = pygame.transform.scale(pictures["game_over"], (WIDTH, HEIGHT))
            self.color_btn = (155, 165, 200)
            self.sound = "sounds/zvuk-game-over.mp3"

        self.btn_group = pygame.sprite.Group()
        self.btn = Button(WIDTH // 2 - 75, 500, self.color_btn, "Return to main", (150, 40), self.btn_group)
        # self.btn_group.add(self.btn)

    def draw(self, screen):
        screen.fill(self.color)
        screen.blit(self.image, (0, 0))
        self.btn_group.draw(screen)
        screen.blit(draw_time(self.time), (0, HEIGHT - 50))
        screen.blit(draw_coins(self.coins, self.all_coins), (WIDTH // 2, HEIGHT - 50))

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btn_group:
                btn.get_click(event.pos)
        if event.type == FINISH_GAME:
            self.time = event.time
            self.coins = event.coins
            self.all_coins = event.all_coins


def draw_time(current_time):
    minutes = current_time // 60
    seconds = current_time % 60

    # Форматирование времени
    time_text = f"Time: {minutes:02d}:{seconds:02d}"
    time_surface = font_coins.render(time_text, True, (255, 255, 255))
    return time_surface

def draw_coins(coins, all_coins):
    coins_text = f"Coins: {coins}/{all_coins}"
    coins_surface = font_coins.render(coins_text, True, (255, 255, 255)) 
    return coins_surface

def get_time(window):
    return (pygame.time.get_ticks() - window.start_time) // 1000
    

def play(play_window, screen, fog_mask, game):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        play_window.player.move(0, 1, play_window.passability_map)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        play_window.player.move(0, -1, play_window.passability_map)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        play_window.player.move(-1, 0, play_window.passability_map)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        play_window.player.move(1, 0, play_window.passability_map)

        # Проверка сбора монет
    play_window.coins_collected = pygame.sprite.spritecollide(play_window.player, coin_group, True)
    if play_window.coins_collected:
        play_window.collected_coins += 1
        game = not (play_window.collected_coins == play_window.all_coins_for_level)

        playing_sound_file("sounds/zvuk-sobiraniya-monetki.mp3")

        # Проверка столкновения с бомбой и врагом
    if pygame.sprite.spritecollideany(play_window.player, bomb_group) or pygame.sprite.spritecollideany(play_window.player, enemy_group):
        play_window.lives.decrease()
        if play_window.lives.is_game_over():
            print("Игра окончена! Вы наступили на бомбу.")
            game = False

        playing_sound_file("sounds/zvuk-sobiraniya-monetki.mp3")
        # else:
            # print(f"Осталось жизней: {lives.lives}")

            # Обновление всех объектов
    play_window.player.update()
    enemy_group.update()
    coin_group.update()
    bomb_group.update()

            # Обновление камеры
    play_window.camera.update(play_window.player)

            # Отрисовка
    screen.fill(pygame.Color('black'))

            # Отрисовка тайлов
    for sprite in tiles_group:
        screen.blit(sprite.image, play_window.camera.apply(sprite))

            # Отрисовка бомб
    for sprite in bomb_group:
        screen.blit(sprite.image, play_window.camera.apply(sprite))

            # Отрисовка монет
    for sprite in coin_group:
        screen.blit(sprite.image, play_window.camera.apply(sprite))

            # Отрисовка врагов
    for sprite in enemy_group:
        screen.blit(sprite.image, play_window.camera.apply(sprite))

            # Отрисовка игрока
    for sprite in player_group:
        screen.blit(sprite.image, play_window.camera.apply(sprite))

    screen.blit(fog_mask, (0, 0))
            # Отрисовка жизней
    play_window.lives.draw(screen)
    current_time = get_time(play_window)
    time_surface = draw_time(current_time)
    coins_surface = draw_coins(play_window.collected_coins, play_window.all_coins_for_level)
    
    screen.blit(time_surface, (screen.get_width() - time_surface.get_width() - 10, 10))
    screen.blit(coins_surface, (screen.get_width() - coins_surface.get_width() - 10, 50))
    return game, play_window.collected_coins == play_window.all_coins_for_level