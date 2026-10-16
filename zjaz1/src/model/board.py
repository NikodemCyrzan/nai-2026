import copy
import math

from event.bus import GameEvent
from model.player import Player


def is_intersection(index: int) -> bool:
    return index % 2 == 1


class Board:
    def __init__(self):
        self._layer_length = 8
        self._layers_count = 3
        self._nodes = [Player.Empty] * self._layer_length * self._layers_count

    @property
    def length(self) -> int:
        return self._layer_length * self._layers_count

    def get_all_nodes(self) -> list[Player]:
        return copy.deepcopy(self._nodes)

    def get_layer_number(self, index: int) -> int:
        return math.floor(index / self._layer_length)

    def set(self, index: int, value: Player):
        self._nodes[index] = value

    def get(self, index: int) -> Player:
        return self._nodes[index]

    def get_slice(self, start, end) -> list[Player]:
        return self._nodes[start: end]

    def get_neighbours(self, index: int) -> list[int]:
        layer = self.get_layer_number(index)
        local_index = index % self._layer_length
        layer_start = layer * self._layer_length

        nodes = [
            layer_start + ((local_index - 1) % self._layer_length),
            layer_start + ((local_index + 1) % self._layer_length),
        ]

        if is_intersection(index):
            match layer:
                case 0:
                    nodes.append(index + self._layer_length)
                case 1:
                    nodes.extend([
                        index - self._layer_length,
                        index + self._layer_length,
                    ])
                case 2:
                    nodes.append(index - self._layer_length)

        return nodes

    def get_mill_rows(self, index: int) -> list[list[int]]:
        length = self._layer_length
        layer_start = self.get_layer_number(index) * length
        local_index = index % length

        def at(offset: int) -> int:
            return layer_start + ((local_index + offset) % length)

        if is_intersection(index):
            return [
                [at(-1), index, at(1)],
                [local_index + layer * length for layer in range(self._layers_count)],
            ]

        return [
            [at(-2), at(-1), index],
            [index, at(1), at(2)],
        ]

    def _get_neighbours_0(self, index: int) -> list[int]:
        return [
            index + self._layer_length,
        ]

    def _get_neighbours_1(self, index: int) -> list[int]:
        return [
            index - self._layer_length,
            index + self._layer_length,
        ]

    def _get_neighbours_2(self, index: int) -> list[int]:
        return [
            index - self._layer_length,
        ]

    def _normalize_index(self, index: int) -> int:
        return self.get_layer_number(index) * self._layer_length + (index % self._layer_length)



class BoardStateChangeEvent(GameEvent):
    def __init__(self, board: Board):
        self.board = board