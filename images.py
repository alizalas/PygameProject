from utils import load_image_sheet, load_image

coin_image = 'coin64.png'
bomb_image = 'bomb8.png'

floor = ['floor1.png', 'floor4.png', 'floor5.png']
wall = ['wall1.png']

sheet_char = load_image_sheet('witch.png', )
x_sheet, y_sheet = 1, 8# Спрайт-лист для анимации движения
image_stay_char = load_image('witch_stay.png')  # Статичное изображение