def setup_blinker(game):
    game.state[(5, 6)] = 1
    game.state[(6, 6)] = 1
    game.state[(7, 6)] = 1
    game.state[(8, 6)] = 1
    game.state[(9, 6)] = 1


def setup_ship(game):
    game.state[(15, 16)] = 1
    game.state[(18, 16)] = 1
    game.state[(14, 17)] = 1
    game.state[(14, 18)] = 1
    game.state[(18, 18)] = 1
    game.state[(14, 19)] = 1
    game.state[(15, 19)] = 1
    game.state[(16, 19)] = 1
    game.state[(17, 19)] = 1


def setup_random(game):
    from random import randrange
    for y in range(game.h):
        for x in range(game.w):
            r = randrange(0, 9)
            if r < 2:
                game.state[(x, y)] = 1
