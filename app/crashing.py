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

        other_neigh = s.head().neighbours(False)
        same_neighbours = utils.intersect(our_neigh, other_neigh)

        # If we have some of the same neighbours,
        #   don't move in that direction
        if len(same_neighbours) > 0:
            for n in same_neighbours:
                # Rank how bad the move is
                # if there we are sharing a neighbour that is a food, that is really bad
                # if we are just sharing a neighbour, less bad
                goodness = 0
                if n not in game.foods:
                    goodness = 0.5
                banned_moves = banned_moves + map(lambda d: Move(d, goodness), game.me.moves_to(n))

    return banned_moves
