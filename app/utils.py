import Queue

from coord import Coord


def flatten(l):
    """Flatten list of lists to list of items."""
    return [item for sublist in l for item in sublist]


def map_to_one(v, l, h):
    """Map a value v in range (l, h) to (0, 1)."""
    return ((v - l) / (h - l)) * (1 - 0) + 0

def clamp(point, min, max):
    return min if point < min else max if point > max else point

def intersect(a, b):
    """Return the intersection of two lists."""
    return list(set(a) & set(b))


def average_length(snakes):
    """Get average length for a list of snakes"""
    return sum([snake.length() for snake in snakes])/len(snakes)


def flood_fill(game, coord):
    '''
    Flood fill an area to check if it's large enough to enter
    :param game: A game object
    :param coord: A coordinate to try
    :return: Number of empty cells immediately reachable if this move is chosen
    '''
    class Cell(Coord):
        def __init__(self, c, type):
            Coord.__init__(self, c)
            self.wall = type
            self.visited = False

        def __str__(self):
            return "{}".format("+" if self.wall == 1 and self.visited else "X" if self.wall == 1 else "." if self.visited else " ")

        def __repr__(self):
            return self.__str__()

    def markup(board):
        return [[Cell([x,y], cell) for x, cell in enumerate(row)] for y, row in enumerate(board)]

    board = markup(game.board)

    # 3. Set Q to the empty queue.
    Q = Queue.Queue()

    # 4. Add node to Q.
    start = board[coord.y + 1][coord.x + 1]
    start.visited = True
    start.type = 1
    Q.put(start)

    # 5. For each element N of Q:
    space = 0
    while not Q.empty():

        # 6. Set west and east equal to the current spot.
        spot = Q.get()
        west = spot
        east = spot

        next_west = board[west.y][west.left().x]
        next_east = board[east.y][east.right().x]

        # 7. Move west to the left until
        #  - the cell to the left of west no longer open.
        while next_west.wall != 1 and next_west.visited == False:
            west = next_west
            next_west = board[next_west.y][next_west.x - 1]

        # 8. Move east to the right until
        #  - the cell to the right of east no longer open.
        while next_east.wall != 1 and next_east.visited == False:
            east = next_east
            next_east = board[next_east.y][next_east.x + 1]


        # 9. For each cell between west and east:
        for x in range(west.x, east.x + 1):

            # 10. Set the this cell visited
            point = board[spot.y][x]
            point.visited = True

            # Keep track of total found space
            space += 1

            if space > 2*game.me.length():
                return space

            # 11. If the cell to the north of this is unvisited, add that cell to Q.
            y = clamp(point.up().y, 0, game.height)
            if not board[y][x].visited and board[y][x].wall != 1:
                Q.put(board[y][x])

            # 12. If the cell to the south of this is unvisited, add that cell to Q.
            y = clamp(point.down().y, 0, game.height)
            if not board[y][x].visited and board[y][x].wall != 1:
                Q.put(board[y][x])

            # 13. Continue looping until Q is exhausted or there's enough space

    return space









