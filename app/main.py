import os
import random

import bottle
import utils
from .attack import attack
from .chase import chase
from .coord import DOWN, LEFT, RIGHT, UP
from .crashing import crashing_moves
from .food import food
from .game import Game
from .move import Move
from .wayout import way_out


@bottle.route('/static/<path:path>')
def static(path):
    """Static files."""
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    """Start the game."""
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (bottle.request.urlparts.scheme,
                                            bottle.request.urlparts.netloc)

    return {
        'color': '#F2A30F',
        'taunt': 'ha',
        'head_url': head_url,
        'name': 'SOHCAHTOA',
        'head_type': 'fang',
        'tail_type': 'block-bum'
    }


def unsafe_moves(game):
    """Return banned moves to neighbour positions (walls and other snakes)."""
    banned_moves = []
    head = game.me.head()

    neighbours = [{
        'd': head.up(),
        'm': Move(UP, 0, 'unsafe')
    }, {
        'd': head.down(),
        'm': Move(DOWN, 0, 'unsafe')
    }, {
        'd': head.left(),
        'm': Move(LEFT, 0, 'unsafe')
    }, {
        'd': head.right(),
        'm': Move(RIGHT, 0, 'unsafe')
    }]

    # If neighbour move is unsafe, add to banned moves
    for n in neighbours:
        if game.is_unsafe(n['d']):
            banned_moves.append(n['m'])

    return banned_moves


def remove_critical(moves, banned_moves):
    """Remove all critical moves from possible move."""
    return filter(lambda d: d not in banned_moves, moves)


def choose_best_move(moves):
    """Choose the best move based on goodness."""
    moves.sort()
    moves.reverse()
    if len(moves) <= 0:
        return None
    return moves[0]


def critical_flood(game):
    banned_moves = []

    head = game.me.head()
    neighbours = [{
        'd': head.up(),
        'm': Move(UP, 0, 'flood unsafe')
    }, {
        'd': head.down(),
        'm': Move(DOWN, 0, 'flood unsafe')
    }, {
        'd': head.left(),
        'm': Move(LEFT, 0, 'flood unsafe')
    }, {
        'd': head.right(),
        'm': Move(RIGHT, 0, 'flood unsafe')
    }]

    for n in neighbours:
        if game.is_unsafe(n['d']):
            continue

        area = utils.flood_fill(game, n['d'])
        # print(n['m'].direction + ' - ' + str(area) + ' | ' + str(game.me.length()))
        if game.me.length() > area:
            banned_moves.append(n['m'])

    return banned_moves


def get_largest_area(game):
    head = game.me.head()
    neighbours = [{
        'd': head.up(),
        'm': Move(UP, 0, 'flood unsafe')
    }, {
        'd': head.down(),
        'm': Move(DOWN, 0, 'flood unsafe')
    }, {
        'd': head.left(),
        'm': Move(LEFT, 0, 'flood unsafe')
    }, {
        'd': head.right(),
        'm': Move(RIGHT, 0, 'flood unsafe')
    }]

    max_area = -1
    max_move = neighbours[0]['m']
    for n in neighbours:
        if game.is_unsafe(n['d']):
            continue

        area = utils.flood_fill(game, n['d'])
        # print(n['m'].direction + ' - ' + str(area) + ' | ' + str(game.me.length()))
        if area > max_area:
            max_area = area
            max_move = n['m']

    return max_move


@bottle.post('/move')
def move():
    """Make a move."""
    data = bottle.request.json

    # Create game state
    game = Game(data)

    # Possible directions we can move
    directions = [
        Move(UP, 0.01, 'default'),
        Move(DOWN, 0.01, 'default'),
        Move(LEFT, 0.01, 'default'),
        Move(RIGHT, 0.01, 'default')
    ]

    # Critcal positions
    not_safe = unsafe_moves(game)
    crashing = crashing_moves(game)
    wayout = way_out(game)
    flood = critical_flood(game)
    critcal = utils.flatten([not_safe, crashing, wayout, flood])

    # print('\n--- critical')
    # for c in critcal:
    #     print(str(c))

    # print('\n--- flood')
    # for c in flood:
    # print(str(c))

    # Good positions
    food_moves = food(game)
    attack_moves = attack(game)
    chase_moves = chase(game)
    good = utils.flatten([chase_moves, food_moves, attack_moves, directions])

    # print('\n--- good')
    # for c in good:
    #     print(str(c))

    # Remove critical moves from good moves
    available = remove_critical(good, critcal)

    # Choose best move based on goodness
    move = choose_best_move(available)

    # We lost :(
    if move is None:
        # If not "good" moves, choose the least bad one
        new_crit = utils.flatten([crashing, wayout])
        better_moves = []
        for m in new_crit:
            if m not in flood and m not in not_safe:
                better_moves.append(m)
        move = choose_best_move(better_moves)
        if move is None:
            move = get_largest_area(game)

            if move is None:
                move = random.choice(directions)

    # print('\n--- move')
    # print(move)

    return {'move': move.direction, 'taunt': move.taunt}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'))
