def my_snake(mid, snakes):
    return list(filter(lambda s: s.id == mid, snakes))[0]


def flatten(l):
    return [item for sublist in l for item in sublist]
