import math

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class Coord:
    """Represents an (x,y) coordinate on the board."""

    def __init__(self, c):
        if type(c) is dict:
            self.x = c['x']
            self.y = c['y']
        else:
            self.x = c[0]
            self.y = c[1]

    def up(self):
        """Return up Coord."""
        return Coord([self.x, self.y - 1])

    def down(self):
        """Return down Coord."""
        return Coord([self.x, self.y + 1])

    def left(self):
        """Return left Coord."""
        return Coord([self.x - 1, self.y])

    def right(self):
        """Return up Coord."""
        return Coord([self.x + 1, self.y])

    def upright(self):
        """Return up right Coord."""
        return Coord([self.x + 1, self.y - 1])

    def downright(self):
        """Return down right Coord."""
        return Coord([self.x + 1, self.y + 1])

    def upleft(self):
        """Return up left Coord."""
        return Coord([self.x - 1, self.y - 1])

    def downleft(self):
        """Return down left Coord."""
        return Coord([self.x - 1, self.y + 1])

    def neighbours(self, diagonal):
        neighbours = [self.up(), self.down(), self.right(), self.left()]
        if diagonal:
            neighbours = neighbours + [
                self.upright(),
                self.upleft(),
                self.downright(),
                self.downleft()
            ]
        return neighbours

    def is_neighbour(self, other, diagonal):
        """Return if other coord is a neighbour to self."""
        return other in self.neighbours(diagonal)

    def distance(self, other):
        """Return manhattan distance to another coordinate."""
        return float(abs(self.x - other.x) + abs(self.y - other.y))

    def sub(self, other):
        """Subtract one coordinate from self."""
        return Coord([self.x - other.x, self.y - other.y])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
