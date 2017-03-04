
def flatten(l):
    """Flatten list of lists to list of items."""
    return [item for sublist in l for item in sublist]


def map_to_one(v, l, h):
    """Map a value v in range (l, h) to (0, 1)."""
    return ((v - l) / (h - l)) * (1 - 0) + 0

def average_length(snakes):
    """Get average length for a list of snakes"""
    return sum([snake.length() for snake in snakes])/len(snakes)