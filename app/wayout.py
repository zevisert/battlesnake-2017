from coord import UP, DOWN, LEFT, RIGHT
from move import Move


def way_out(game):
    """Return potential moves that are surrounded by 3 or more unsafe things."""
    moves = []

    head = game.me.head()
    neighbours = [
        {'d': head.up(), 'm': Move(UP, 0.6, 'unsafe')},
        {'d': head.down(), 'm': Move(DOWN, 0.6, 'unsafe')},
        {'d': head.left(), 'm': Move(LEFT, 0.6, 'unsafe')},
        {'d': head.right(), 'm': Move(RIGHT, 0.6, 'unsafe')}
    ]

    # Loop through possible moves
    for c in neighbours:
        side_sum = 0
        # Check the neighbours of potential moves
        for n in c['d'].neighbours(False):
            if game.is_unsafe(n) and not game.is_wall(n):
                side_sum += 1

        if side_sum >= 3:
            moves.append(c['m'])

    return moves
