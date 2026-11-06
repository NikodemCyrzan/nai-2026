from ..models.input import Input
from ..models.terrain import Terrain

class PhysicsContext:
    """Shared data for physics updates."""

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
        """Gravity in meters per second squared."""
        return self._GRAVITY

    @property
    def delta(self):
        """Length of one physics step in seconds."""
        return self._DELTA
