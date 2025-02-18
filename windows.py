import pygame

from Constants import WIDTH, HEIGHT, BUTTOM_CLICKED, CHOOSE_EVENT, pictures
from dialogwindow import DialogWindow
from Constants import tiles_group, coin_group, bomb_group, all_sprites, player_group, enemy_group, FPS
from hearts import Lives

from class_windows import Main_Window, New_window, ChooseOfPlayer, PlayWindow



if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    start = False
    
    clock = pygame.time.Clock()
    lives = Lives()
    # camera = Camera()
    button_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    dialog = DialogWindow("Введите имя")
    main_window = Main_Window(pictures["фон для главного"], "Main Window", (0, 255, 0))
    window2 = ChooseOfPlayer("Выбор персонажа", (12, 0, 150), [pictures["witch_stay"], pictures["girl_stay"], pictures["knight_stay"]])
    window = 0
    
    new_window = New_window(pictures["фон для инструкции"], "Second Window", "cyan", "white")
    play_window = 1
    player = "WITCH"
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
                        main_window.change_name(name)
                    start = True
                elif event.window_name == "Выбор персонажа":
                    window = window2
                elif event.window_name == "Инструкция":
                    window = new_window
                elif event.window_name == "Level 1":
                    play_window = PlayWindow("Level №1", "black", "first_level.txt")
                    play_window.change_player(player)
                    # print(play_window.player.pos_x, play_window.player.pos_y)
                    window = play_window
                elif event.window_name == "Level 2":
                    play_window = PlayWindow("Level №2", "black", "second_level.txt")
                    play_window.change_player(player)
                    # print(play_window.player.pos_x, play_window.player.pos_y)
                    window = play_window
                elif event.window_name == "Level 3":
                    play_window = PlayWindow("Level №3", "black", "third_level.txt")
                    play_window.change_player(player)
                    # print(play_window.player.pos_x, play_window.player.pos_y)
                    window = play_window
            if event.type == CHOOSE_EVENT:
                player = event.btn
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
            if pygame.sprite.spritecollideany(play_window.player, bomb_group):
                lives.decrease()
                if lives.is_game_over():
                    print("Игра окончена! Вы наступили на бомбу.")
                    game = False
                else:
                    print(f"Осталось жизней: {lives.lives}")

            # Проверка столкновения с врагом
            if pygame.sprite.spritecollideany(play_window.player, enemy_group):
                print("Игрок погиб от врага!")
                game = False

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

            # Отрисовка жизней
            lives.draw(screen)

        # Обновление экрана
        clock.tick(FPS)

            # Проверка столкновения с бомбой
            # if pygame.sprite.spritecollideany(play_window.player, bomb_group):
            #     print("Игра окончена! Вы наступили на бомбу.")
                # game = False 


        pygame.display.flip()
    pygame.quit()