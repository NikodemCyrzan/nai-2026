from ..models.input import Input
from ..models.terrain import Terrain

class PhysicsContext:
    _GRAVITY = 9.81
    _TICK_RATE = 50
    _DELTA = 1.0 / _TICK_RATE

    def __init__(self, terrain: Terrain, input: Input):
        self._terrain = terrain
        self._input = input

    @property
    def terrain(self):
        return self._terrain

    @property
    def input(self) -> Input:
        return self._input

    @property
    def gravity(self):
        return self._GRAVITY

    @property
    def delta(self):
        return self._DELTA
