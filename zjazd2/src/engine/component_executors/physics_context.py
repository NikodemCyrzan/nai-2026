from ..models.terrain import Terrain

class PhysicsContext:
    _GRAVITY = 9.81
    _TICK_RATE = 1
    _DELTA = 1.0 / _TICK_RATE

    def __init__(self, terrain: Terrain):
        self._terrain = terrain

    @property
    def terrain(self):
        return self._terrain

    @property
    def gravity(self):
        return self._GRAVITY

    @property
    def delta(self):
        return self._DELTA
