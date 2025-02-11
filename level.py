from levels import Player, Coin, Bomb, Tile
from Constants import far_walls



def generate_level(level, floor, wall):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, floor, wall)
            elif level[y][x] == '#':
                tile = Tile('wall', x, y, floor, wall)
                if x == 0 or y == 0:
                    far_walls.add(tile)
            elif level[y][x] == '@':
                Tile('empty', x, y, floor, wall)
                new_player = Player(x, y)
            elif level[y][x] == 'c':  # Монета
                Tile('empty', x, y, floor, wall)
                Coin(x, y)
            elif level[y][x] == 'b':  # Бомба
                Tile('empty', x, y, floor, wall)
                Bomb(x, y)
    return new_player, x, y