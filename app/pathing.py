from heapq import heappop, heappush
from sys import maxint

# from game import EMPTY, HEAD, WALL
EMPTY = 0
WALL = 1
HEAD = 1

limit = 10


class Node():
    def __init__(self, h, g, coord):
        # 0 = empty, 1 = wall, 2 = snake
        self.coord = coord
        self.parent = None
        self.ope = True
        self.valid = True
        self.H = h
        self.G = g
        self.F = h + g


def heuristic(game, c):
    t = game.coord_type(c)
    return 1


def cost(c1, c2):
    return c1.distance(c2)


def find_path(game, start, end):
    """Finds a path from start to end."""
    nums = iter(xrange(maxint))
    start_h = heuristic(game, start)
    start = Node(start_h, 1, start)

    # Track all nodes seen so far
    nodes = {start.coord: start}

    # Heap of nodes
    heap = [start]

    # Best path so far
    best = start

    # print('finding path from {} to {}'.format(start.coord, end))

    # F, H, NUM, G, POS, OPEN, VALID, PARENT = xrange(8)
    while len(heap) > 0:
        # pop next node from heap
        current = heappop(heap)
        current.ope = False

        # Have we reached the goal?
        if current.coord == end:
            best = current
            break

        for nc in current.coord.neighbours(False):
            if game.coord_type(nc) != EMPTY:
                continue

            n_g = current.G + cost(current.coord, nc)
            neighbour = nodes.get(nc)
            if neighbour is None:
                if len(nodes) >= limit:
                    continue

                # We have found a new node
                n_h = heuristic(game, nc)
                n = Node(n_h, n_g, nc)
                n.parent = current
                nodes[nc] = n
                heappush(heap, n)

                if n.H <= best.H:
                    best = n

            elif n_g < neighbour.G:
                # We have found a better path to neighbor
                if neighbour.ope:
                    neighbour.valid = False
                    neighbour.F = n_g + neighbour.H
                    neighbour.G = n_g
                    neighbour.valid = True
                    neighbour.parent = current
                    heappush(heap, neighbour)
                else:
                    # Reopen the neighbor
                    neighbour.F = n_g + neighbour.H
                    neighbour.G = n_g
                    neighbour.parent = current
                    neighbour.ope = True
                    heappush(heap, neighbour)

        while len(heap) > 0 and not heap[0].valid:
            heappop(heap)

    path = []
    current = best
    while current.parent is not None:
        path.append(current.coord)
        current = nodes[current.parent.coord]
    path.reverse()
    return path
