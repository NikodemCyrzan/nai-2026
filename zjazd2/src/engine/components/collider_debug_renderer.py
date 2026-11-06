from .physics import Physics
from ..models.color import Color
from ..models.component import Component
from ..models.game_object import GameObject


class ColliderDebugRenderer(Component):
    """Outlines the colliders of the object's Physics component."""

    def __init__(self, go: GameObject, color: Color = Color(200, 30, 30), stroke_width: float = 0.1):
        super().__init__(go)
        self._color = color
        self._stroke_width = stroke_width
        self._physics: Physics | None = None

    def on_setup(self):
        self._physics = self.game_object.get_component(Physics)
        if self._physics is None:
            raise RuntimeError("ColliderDebugRenderer requires a Physics component on the same GameObject")

    def on_render_update(self, ctx, alpha: float, delta: float):
        go = self.game_object
        for col in self._physics.colliders:
            ctx.renderer.draw_polygon(
                col.world_corners(go.position, go.rotation),
                stroke=self._color,
                stroke_width=self._stroke_width,
            )
