from snake import Snake
from coord import Coord
import utils


class Game:
    def __init__(self, data):
        self.mid = data['you']
        self.width = data['width']
        self.height = data['height']
        self.turn = data['turn']
        self.foods = map(Coord, data['food'])
        self.dead_snakes = map(Snake, data['dead_snakes'])
        self.snakes = map(Snake, data['snakes'])
        self.other_snakes = filter(lambda s: s.id != self.mid, self.snakes)
        self.me = list(filter(lambda s: s.id == self.mid, self.snakes))[0]

    def all_but_head_coords(self):
        other_coords = utils.flatten(map(lambda s: s.coords, self.other_snakes))
        return other_coords + self.me.tail()
