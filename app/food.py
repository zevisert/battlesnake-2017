import params
import utils
from move import Move


def value(game, distance):
    """Return a value representing how much we want to move towards the food.

    game: Game object
    distance: manhattan distance to food
    """
    health = game.me.health()

    avg_length = utils.average_length(snakes=game.snakes)

    if health > params.FOOD_THRESH and game.me.length() >= avg_length:
        return 0
    if health < distance:
        return 100

    distance_weight = 1 / distance
    health_weight = (100 / health) * params.FOOD_HEALTH_MULTI

    return distance_weight + health_weight


def food(game):
    """Return good moves towards food, goodness is determined by the weighted value function."""
    moves = []
    closest_foods = []

    # Only consider food we are the closest snake too
    for f in game.foods:
        min_dist = game.width * game.height
        for s in game.other_snakes:
            if s.head().distance(f) < min_dist:
                min_dist = s.head().distance(f)

        if game.me.head().distance(f) <= min_dist:
            closest_foods.append(f)

    # If we are not the closest to any food, just try all
    if len(closest_foods) <= 0:
        closest_foods = game.foods

    if len(closest_foods) <= 0:
        return []

    food_distances = [game.me.head().distance(c) for c in closest_foods]

    for idx, d in enumerate(food_distances):
        # Find possible moves towards the foods
        #   i.e. if food is to the top right, possible moves are up and right
        for m in game.me.moves_to(closest_foods[idx]):
            # Add possible move to possible moves with goodness from weighted values
            val = value(game, d)
            if val > 0:
                moves.append(Move(m, val, 'food'))

    return moves
