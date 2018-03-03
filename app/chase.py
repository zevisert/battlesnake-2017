import utils
from move import Move


def value(game, distance):
    """Return a value representing how much we want to move towards our butt."""
    if distance == 0:
        return 1
    return 1 / (distance + 10)


def chase(game):
    """Returns good moves towards tail, goodness determined by how far away it is."""
    moves = []

    distance = game.me.head().distance(game.me.butt())
    val = value(game, distance)
    if val <= 0:
        return []

    for m in game.me.moves_to(game.me.butt()):
        moves.append(Move(m, val, 'chase'))

    return moves
