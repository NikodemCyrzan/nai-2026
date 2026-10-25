import math
from .collider import Collider
from ..models.component import Component
from ..models.game_object import GameObject


class Physics(Component):
    def __init__(
        self,
        go: GameObject,
        colliders: list[Collider],
    ):
        super().__init__(go)
        self._colliders = colliders

        self.vx = 0.0
        self.vy = 0.0

    def on_physics_update(self, ctx, delta: float):
        pos = self.game_object.position

        self.vy -= ctx.gravity * delta
        pos.x += self.vx * delta
        pos.y += self.vy * delta

        deepest = 0.0
        drag_sum = 0.0
        contacts = 0

        for col in self._colliders:
            half_w = col.width / 2
            bottom = pos.y - col.height / 2

            ground = max(
                ctx.terrain.height_at(pos.x - half_w),
                ctx.terrain.height_at(pos.x),
                ctx.terrain.height_at(pos.x + half_w),
            )

            penetration = ground - bottom
            if penetration > 0.0:
                contacts += 1
                drag_sum += col.drag
                deepest = max(deepest, penetration)

        if contacts == 0:
            return

        pos.y += deepest

        tx, ty = ctx.terrain.tangent_at(pos.x)
        nx, ny = ctx.terrain.normal_at(pos.x)

        vn = self.vx * nx + self.vy * ny
        vt = self.vx * tx + self.vy * ty

        if vn < 0.0:
            vn = 0.0

        drag = drag_sum / contacts
        vt *= math.exp(-drag * delta)

        self.vx = tx * vt + nx * vn
        self.vy = ty * vt + ny * vn
