import params
import utils
from move import Move


def value(game, distance, snake):
    """Return a value representing how much we want to move towards the other snake.

    game: Game object
    distance: Euclidean distance to snake
    snake: The enemy snake object we can attack
    """
    my_size = game.me.length()

    if (snake.length() >= my_size) or (distance >
                                       params.ATTACK_DISTANCE_THRESH):
        return 0

    length_diff = my_size - snake.length()
    return (1 / distance) + (params.ATTACK_LENGTH_MULTI * length_diff)


def attack(game):
    """Return good moves towards attack, goodness determined by the weighted value function."""
    moves = []

    # There are no other snakes
    if len(game.snakes) <= 0:
        return moves

    # Get a list of distances to all snake heads
    head_coords = [snake.head() for snake in game.snakes]
    head_distances = map(lambda h: game.me.head().distance(h), head_coords)

    for idx, d in enumerate(head_distances):
        # Find possible moves towards the snake heads
        mt = game.me.moves_to(head_coords[idx])

        for m in mt:
            val = value(game, d, game.snakes[idx])
            if val > 0:
                # Add possible move to possible moves with goodness from weighted values
                moves.append(Move(m, val, 'attack'))

    return moves
