from move import Move
import utils


def crashing_moves(game):
    """Return banned moves where we could potentially crash into another snake."""
    banned_moves = []

    our_neigh = game.me.head().neighbours(False)

    # Find heads that are 8 directional neighbours to us
    for s in game.other_snakes:
        # If another snakes neighbours are neighbours to us

        # Only do this if the snake's length is >= ours
        if s.length() < game.me.length():
            continue

        print('\n--- To Snake -> ' + s.name)
        other_neigh = s.head().neighbours(False)
        same_neighbours = utils.intersect(our_neigh, other_neigh)

        print('--- other')
        print(other_neigh)
        print('--- ours')
        print(our_neigh)
        print('--- same')
        print(same_neighbours)

        # If we have some of the same neighbours,
        #   don't move in that direction
        if len(same_neighbours) > 0:
            for n in same_neighbours:
                banned_moves = banned_moves + map(lambda d: Move(d, 0), game.me.moves_to(n))

    return banned_moves
