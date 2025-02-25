from Constants import pictures 


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


sheet_char = pictures["witch"]
image_stay_char = pictures["witch_player"]
image_stay = image_stay_char

WITCH = char_animation(1, 8, image_stay_char, sheet_char, 3)


sheet_char = pictures["girl"]
image_stay_char = pictures["girl_player"]

GIRL = char_animation(8, 1, image_stay_char, sheet_char, 1)


sheet_char = pictures["knight"]
image_stay_char = pictures["knight_player"]

KNIGHT = char_animation(4, 1, image_stay_char, sheet_char, 1)