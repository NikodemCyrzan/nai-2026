from typing import TYPE_CHECKING
from PySide6.QtCore import QRectF
from PySide6.QtSvg import QSvgRenderer
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2

if TYPE_CHECKING:
    from ..component_executors.render_context import RenderContext


class VectorRenderer(Component):
    _cache: dict[str, QSvgRenderer] = {}

    def __init__(
        self,
        go: GameObject,
        svg_path: str,
        width: float,
        height: float | None = None,
        offset: Vector2 | None = None,
    ):
        super().__init__(go)
        self._svg = self._load(svg_path)

        if height is None:
            view = self._svg.viewBoxF()
            height = width * view.height() / view.width()

        off = offset or Vector2()
        self._target = QRectF(off.x - width / 2, -off.y - height / 2, width, height)

        self.visible = True

    @classmethod
    def _load(cls, svg_path: str) -> QSvgRenderer:
        svg = cls._cache.get(svg_path)
        if svg is None:
            svg = QSvgRenderer(svg_path)
            if not svg.isValid():
                raise ValueError(f"Invalid or missing SVG: {svg_path}")
            cls._cache[svg_path] = svg
        return svg

    def on_render_update(self, ctx: RenderContext, alpha: float, delta: float):
        if not self.visible:
            return
        go = self.game_object
        ctx.renderer.draw_svg(self._svg, self._target, go.position, go.rotation)
