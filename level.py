from levels import Player, Coin, Bomb, Tile, FlyingEnemy


def generate_level(level, floor, wall):
    new_player, x, y = None, None, None
    level_width = len(level[0])
    level_height = len(level)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, floor, wall)
            elif level[y][x] == '#':
                Tile('wall', x, y, floor, wall)
            elif level[y][x] == '@':
                Tile('empty', x, y, floor, wall)
                new_player = Player(x, y)
            elif level[y][x] == 'c':  # Монета
                Tile('empty', x, y, floor, wall)
                Coin(x, y)
            elif level[y][x] == 'e':
                Tile('empty', x, y, floor, wall)
                FlyingEnemy(x, y, level_width, level_height)
            elif level[y][x] == 'b':  # Бомба
                Tile('empty', x, y, floor, wall)
                Bomb(x, y)
    return new_player, x, y