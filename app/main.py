import bottle
import os

import utils
from move import Move
from coord import UP, DOWN, LEFT, RIGHT
from game import Game


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    """Start the game."""
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'sneksnek'
    }


def walls(game):
    """Return critical wall moves."""
    banned_moves = []
    head = game.me.head()
    if head.up().y < 0:
        banned_moves.append(Move(UP, 0))

    if head.down().y >= game.height:
        banned_moves.append(Move(DOWN, 0))

    if head.left().x < 0:
        banned_moves.append(Move(LEFT, 0))

    if head.right().x >= game.width:
        banned_moves.append(Move(RIGHT, 0))

    return banned_moves


def other_snakes(game):
    """Return critical moves into other snakes (including our tail)."""
    banned_moves = []
    head = game.me.head()

    neighbours = [
        {'d': head.up(), 'm': Move(UP, 0)},
        {'d': head.down(), 'm': Move(DOWN, 0)},
        {'d': head.left(), 'm': Move(LEFT, 0)},
        {'d': head.right(), 'm': Move(RIGHT, 0)}
    ]

    for n in neighbours:
        if n['d'] in game.all_but_head_coords():
            banned_moves.append(n['m'])

    return banned_moves


def food(game):
    """Return good moves towards food goodness is width * height - distance_to_food."""
    if len(game.foods) <= 0:
        return []

    moves = []

    food_distances = map(lambda c: game.me.head().distance(c), game.foods)
    for idx, d in enumerate(food_distances):
        mt = game.me.moves_to(game.foods[idx])
        for m in mt:
            moves.append(Move(m, game.width * game.height - d))

    return moves


def remove_critical(moves, banned_moves):
    """Remove all critical moves from possible move."""
    return filter(lambda d: d not in banned_moves, moves)


def choose_best_move(moves):
    """Choose the best move based on goodness."""
    moves.sort()
    moves.reverse()
    return moves[0]


@bottle.post('/move')
def move():
    """Make a move."""
    print('\n--- MAKING MOVE')

    data = bottle.request.json

    game = Game(data)

    directions = [Move(UP, 0.5), Move(DOWN, 0.5), Move(LEFT, 0.5), Move(RIGHT, 0.5)]

    # Critcal positions
    ws = walls(game)
    other = other_snakes(game)

    critcal = utils.flatten([ws, other])

    # Good positions
    food_moves = food(game)

    good = utils.flatten([food_moves, directions])

    print('\n--- critcal')
    for c in other:
        print(str(c))

    print('\n--- good')
    for c in good:
        print(str(c))

    available = remove_critical(good, critcal)
    move = choose_best_move(available)

    print('\n--- available')
    for c in available:
        print(str(c))

    print('\n--- move')
    print(move)

    return {
        'move': move.direction,
        'taunt': 'sneksnek'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
