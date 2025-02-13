from utils import load_image_sheet, load_image
from animation import AnimatedSprite

coin_image = load_image_sheet('coin64.png')
bomb_image = load_image_sheet('bomb8.png')

floor = [load_image('floor1.png'), load_image('floor4.png'), load_image('floor5.png')]
wall = [load_image('wall1.png')]
heart = load_image('heart.png')
broken_heart = load_image('broken_heart.png')

dragon = load_image_sheet('dragon.png')



class char_animation:
    def __init__(self, x_sheet, y_sheet, image_stay_char, sheet, padding):
        self.x_sheet = x_sheet
        self.y_sheet = y_sheet
        self.image_stay_char = image_stay_char
        self.sheet = sheet
        self.padding = padding


    def get_attributes(self):
        return {
            'x_sheet': self.x_sheet,
            'y_sheet': self.y_sheet,
            'image_stay_char': self.image_stay_char,
            'sheet': self.sheet,
            'padding': self.padding,
        }


sheet_char = load_image_sheet('witch.png', )
image_stay_char = load_image('witch_stay.png')
image_stay = image_stay_char

WITCH = char_animation(1, 8, image_stay_char, sheet_char, 3)


sheet_char = load_image_sheet('girl.png').convert_alpha()
image_stay_char = load_image('girl_stay.png')

GIRL = char_animation(8, 1, image_stay_char, sheet_char, 1)


sheet_char = load_image_sheet('knight.png').convert_alpha()
image_stay_char = load_image('knight_stay.png')

KNIGHT = char_animation(4, 1, image_stay_char, sheet_char, 1)