from coord import Coord, UP, DOWN, LEFT, RIGHT


class Snake:
    """Represents a snake."""

    def __init__(self, s):
        self.coords = s['coords']
        self.name = s['name']
        self.id = s['id']
        self.health_points = s['health_points']
        self.coords = map(Coord, s['coords'])

    def head(self):
        """Return head of snake."""
        return self.coords[0]

    def tail(self):
        """Return all but head of snake."""
        return self.coords[1:]

    def length(self):
        """Return the length of the snake."""
        return len(self.coords)

    def moves_to(self, destination):
        """Return possible moves towards a destination."""
        head = self.head()
        diff = head.sub(destination)
        moves = []

        if diff.x < 0:
            moves.append(RIGHT)
        elif diff.x > 0:
            moves.append(LEFT)

        if diff.y > 0:
            moves.append(UP)
        elif diff.y < 0:
            moves.append(DOWN)

        return moves

    def __str__(self):
        return self.name + " :: " + self.id
