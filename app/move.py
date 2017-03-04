
class Move:
    """A possible move with a direction and goodness to take the move."""

    def __init__(self, direction, goodness, taunt=''):
        self.direction = direction
        self.goodness = goodness
        self.taunt = taunt

    def __eq__(self, other):
        return self.direction == other.direction

    def __gt__(self, other):
        return self.goodness > other.goodness

    def __str__(self):
        return self.direction + " :: " + str(self.goodness) + " - " + str(self.taunt)
