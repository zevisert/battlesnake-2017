import utils
from coord import Coord
from snake import Snake


class Game:
    """Represents the state of the game at one turn."""

    def __init__(self, data):
        """Create a game."""
        self.mid = data['you']['id']
        self.width = data['width']
        self.height = data['height']
        self.turn = data['turn']
        self.foods = map(Coord, data['food']['data'])
        # self.dead_snakes = map(Snake, data['dead_snakes'])
        self.snakes = map(Snake, data['snakes']['data'])
        self.snake_coords = utils.flatten((map(lambda s: s.coords,
                                               self.snakes)))
        self.other_snakes = filter(lambda s: s.id != self.mid, self.snakes)
        self.me = list(filter(lambda s: s.id == self.mid, self.snakes))[0]
        self.board = self.create_board_matrix()

    def is_wall(self, coord):
        """Return if coordinate is wall or not."""
        return coord.y < 0 or coord.y >= self.height or coord.x < 0 or coord.x >= self.width

    def is_against_wall(self, coord):
        """
        Return True if the coordinate is against the wall
        """
        ret = coord.y == 0 or coord.y >= self.height - 1 or coord.x == 0 or coord.x >= self.width - 1
        return ret

    def is_safe(self, coord):
        """Return if a coordinate is safe or not."""
        if self.is_wall(coord):
            return False
        if self.me.butt() == coord and not self.me.will_grow():
            return True

        return coord not in self.snake_coords

    def is_unsafe(self, coord):
        """Return if a coordinate is not safe."""
        return not self.is_safe(coord)

    def coord_type(self, c):
        return self.board[c.y + 1][c.x + 1]

    def print_matrix(self, matrix):
        """Print a matrix."""
        for i in range(len(matrix)):
            print(matrix[i])

    def create_board_matrix(self):
        """Create a matrix representation of the board."""
        matrix = [[0 for x in range(self.width + 2)]
                  for y in range(self.height + 2)]

        # Add walls on edges
        for i in range(len(matrix[0])):
            matrix[0][i] = 1
            matrix[len(matrix) - 1][i] = 1
        for i in range(len(matrix)):
            matrix[i][0] = 1
            matrix[i][len(matrix[i]) - 1] = 1

        # Add snakes bodies as a different type
        for c in self.snake_coords:
            matrix[c.y + 1][c.x + 1] = 2

        # Add snake heads as another type
        matrix[self.me.head().y + 1][self.me.head().x + 1] = 3
        for s in self.other_snakes:
            matrix[s.head().y + 1][s.head().x + 1] = 3

        # Mark our butt if we are not going to grow
        if not self.me.will_grow():
            matrix[self.me.butt().y + 1][self.me.butt().x + 1] = 0

        # self.print_matrix(matrix)

        return matrix

    def all_but_head_coords(self):
        """Return a list of all coords that are not our snakes head."""
        other_coords = utils.flatten(
            map(lambda s: s.coords, self.other_snakes))
        return other_coords + self.me.tail()
