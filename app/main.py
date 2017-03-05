import bottle
import os
import random

import utils
from move import Move
from coord import UP, DOWN, LEFT, RIGHT
from game import Game
from crashing import crashing_moves
from wayout import way_out


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

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#09A8FA',
        'taunt': 'ha',
        'head_url': head_url,
        'name': 'notice me pls',
        'head_type': 'safe',
        'tail_type': 'freckled'
    }


def unsafe_moves(game):
    """Return banned moves to neighbour positions (walls and other snakes)."""
    banned_moves = []
    head = game.me.head()

    neighbours = [
        {'d': head.up(), 'm': Move(UP, 0, 'unsafe')},
        {'d': head.down(), 'm': Move(DOWN, 0, 'unsafe')},
        {'d': head.left(), 'm': Move(LEFT, 0, 'unsafe')},
        {'d': head.right(), 'm': Move(RIGHT, 0, 'unsafe')}
    ]

    # If neighbour move is unsafe, add to banned moves
    for n in neighbours:
        if game.is_unsafe(n['d']):
            banned_moves.append(n['m'])

    return banned_moves


def food(game):
    """Return good moves towards food goodness is determined by the weighted value function."""
    moves = []

    snake_length_ratio = utils.average_length(snakes=game.snakes)/game.me.length()

    closest_foods = []
    # Only consider food we are the closest snake too
    for f in game.foods:
        min_dist = game.width * game.height
        for s in game.other_snakes:
            if s.head().distance(f) < min_dist:
                min_dist = s.head().distance(f)

        if game.me.head().distance(f) <= min_dist:
            closest_foods.append(f)

    if len(closest_foods) <= 0:
        closest_foods = game.foods

    def weighted_value(distance, health):
        distance_weight = 1 / distance
        health_weight = 1 / (health + 0.01)
        length_compare_weight = 1 if snake_length_ratio > 1 else 0

        if health < 50:
            health_weight += 0.20 * (50 - health)

        # Return a value between 0 and 1
        return (distance_weight + health_weight + length_compare_weight)/3

    if len(closest_foods) <= 0:
        return moves

    # Get a list of distances to all foods
    food_distances = map(lambda c: game.me.head().distance(c), closest_foods)

    health = game.me.health_points

    for idx, d in enumerate(food_distances):
        # Find possible moves towards the foods
        #   i.e. if food is to the top right, possible moves are up and right
        mt = game.me.moves_to(closest_foods[idx])
        for m in mt:
            # Add possible move to possible moves with goodness from weighted values
            moves.append(Move(m, weighted_value(d, health), 'food'))

    return moves


def attack(game):
    """Return good moves towards attack goodness, determined by the weighted value function."""
    moves = []
    my_size = game.me.length()

    def weighted_value(distance, snake_index):
        other_snake = game.snakes[snake_index]

        if other_snake.length() >= my_size:
            return 0

        return 1/(distance) + (0.01 * (my_size - other_snake.length()))

    if len(game.snakes) <= 0:
        return moves

    # Get a list of distances to all snake heads
    head_coords = [snake.head() for snake in game.snakes]
    head_distances = map(lambda h: game.me.head().distance(h), head_coords)

    for idx, d in enumerate(head_distances):
        # Find possible moves towards the snake heads
        mt = game.me.moves_to(head_coords[idx])

        for m in mt:
            val = weighted_value(d, idx)

            if val:
                # Add possible move to possible moves with goodness from weighted values
                moves.append(Move(m, val, 'attack'))

    return moves


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
    neighbours = [
        {'d': head.up(), 'm': Move(UP, 0, 'flood unsafe')},
        {'d': head.down(), 'm': Move(DOWN, 0, 'flood unsafe')},
        {'d': head.left(), 'm': Move(LEFT, 0, 'flood unsafe')},
        {'d': head.right(), 'm': Move(RIGHT, 0, 'flood unsafe')}
    ]

    for n in neighbours:
        if game.is_unsafe(n['d']):
            continue

        area = utils.flood_fill(game, n['d'])
        # print(n['m'].direction + ' - ' + str(area) + ' | ' + str(game.me.length()))
        if game.me.length() > area:
            banned_moves.append(n['m'])

    return banned_moves


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
    good = utils.flatten([food_moves, attack_moves, directions])

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
        better_moves = []
        for m in critcal:
            if m not in flood:
                better_moves.append(m)
        move = choose_best_move(better_moves)

    # print('\n--- move')
    # print(move)

    return {
        'move': move.direction,
        'taunt': move.taunt
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
