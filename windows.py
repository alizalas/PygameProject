import pygame

from Constants import WIDTH, HEIGHT, BUTTOM_CLICKED, CHOOSE_EVENT, pictures
from dialogwindow import DialogWindow
from Constants import FPS, database_name
from mask import create_fog_mask
from class_windows import Main_Window, Rating, New_window, ChooseOfPlayer, PlayWindow, play, Result, get_time
from music import playing_sound_file
from database import SQLiteDatabase

if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    start = False
    clock = pygame.time.Clock()
    fog_mask = create_fog_mask(radius=200)
    # camera = Camera()
    button_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    dialog = DialogWindow("Введите имя")
    main_window = Main_Window(pictures["фон для главного"], "Main Window", (0, 255, 0))
    window2 = ChooseOfPlayer("Выбор персонажа", pictures["выбор"], (12, 0, 150), [pictures["witch_stay"], pictures["girl_stay"], pictures["knight_stay"]])
    window = 0
    new_window = New_window(pictures["фон для инструкции"], "Second Window", "cyan", "white")
    database = SQLiteDatabase(database_name)
    rating = Rating(pictures["рейтинг"], "Рейтинг", (0, 0, 0), (255, 255, 255), database)
    result = 0
    # play_window = 1
    player = "WITCH"
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if start:
                window.process_event(event)
            if event.type == BUTTOM_CLICKED:
                if event.window_name == "Save" and not start:
                    name = dialog.text
                    screen = pygame.display.set_mode(size)
                    pygame.display.set_caption("MAIN")
                    window = main_window
                    if name:
                        main_window.change_name(name)
                    start = True
                elif event.window_name == "Рейтинг":
                    window = rating
                    window.open_data()
                elif event.window_name == "Выбор персонажа":
                    window = window2
                elif event.window_name == "Инструкция":
                    window = new_window
                elif event.window_name == "Return to main":
                    window = main_window
                elif "Level" in event.window_name:
                    if event.window_name == "Level_1":
                        play_window = PlayWindow("Level_1", "black", "first_level.txt")
                    elif event.window_name == "Level_2":
                        play_window = PlayWindow("Level_2", "black", "second_level.txt")
                    elif event.window_name == "Level_3":
                        play_window = PlayWindow("Level_3", "black", "third_level.txt")
                    play_window.change_player(player)
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
        if start and "Level" in window.name:
            game, result = play(window, screen, fog_mask, game)
            if not game:
                play_window.clean()
                level = play_window.name
                result_window = Result("Итог", (0, 0, 0), result)
                window = result_window
                if result:
                    playing_sound_file("sounds/zvuk-pobedy.mp3")
                    database.change_table(level, {"user_name": main_window.user_name, "result": get_time(play_window)})
                else:
                    playing_sound_file("sounds/zvuk-game-over.mp3")
                game = True

        clock.tick(FPS) 
        pygame.display.flip()
    pygame.quit()