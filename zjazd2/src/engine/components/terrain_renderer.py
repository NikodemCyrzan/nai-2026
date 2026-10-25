from ..models.component import Component
from ..models.game_object import GameObject
from ..models.terrain import Terrain


class TerrainRenderer(Component):
    def __init__(self, go: GameObject, terrain: Terrain):
        super().__init__(go)
        self._terrain = terrain

    def on_render_update(self, ctx, alpha: float, delta: float):
        pass
