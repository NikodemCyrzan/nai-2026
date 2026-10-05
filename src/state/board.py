import math
from player import Player

class Board:
    def __init__(self):
        self._layer_length = 8
        self._layers_count = 3
        self._nodes = [Player.Node] * self._layer_length * self._layers_count

    def is_intersection(index: int) -> bool:
        return index % 2 == 0

    def get_layer_number(self, index: int) -> int:
        return math.floor(index / self._layer_length)

    def set(self, index: int, value: Player):
        self._nodes[index] = value

    def get(self, index: int) -> Player:
        return self._nodes[index]

    def get_slice(self, start, end) -> list[Player]:
        return self._nodes[start: end]

    def get_neighbours(self, index: int) -> list[Player]:
        nodes = [
            self._normalize_index(index - 1),
            self._normalize_index(index + 1)
        ]

        if self.is_intersection(index):
            match self.get_layer_number(index):
                case 0:
                    nodes.extend(self._get_neighbours_0(index))
                case 1:
                    nodes.extend(self._get_neighbours_1(index))
                case 2:
                    nodes.extend(self._get_neighbours_2(index))

    def _get_neighbours_0(self, index: int) -> list[Player]:
        return [
            index + self._layer_length,
        ]

    def _get_neighbours_1(self, index: int) -> list[Player]:
        return [
            index - self._layer_length,
            index + self._layer_length,
        ]

    def _get_neighbours_2(self, index: int) -> list[Player]:
        return [
            index - self._layer_length,
        ]

    def _normalize_index(self, index: int) -> int:
        return self.get_layer_number(index) * self._layer_length + (index % self._layer_length)
