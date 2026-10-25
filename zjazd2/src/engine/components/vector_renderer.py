from ..models.component import Component
from ..models.game_object import GameObject


class VectorRenderer(Component):
    def __init__(self, go: GameObject):
        super().__init__(go)
