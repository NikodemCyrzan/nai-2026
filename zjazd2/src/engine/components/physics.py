from __future__ import annotations

import math
from .collider import Collider
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class Physics(Component):
    def __init__(self, go: GameObject, colliders: list[Collider], mass: float = 1.0):
        super().__init__(go)
        assert mass > 0.0
        self._colliders = colliders
        self._mass = mass

        self._velocity = Vector2()
        self._acceleration = Vector2()

    @property
    def mass(self) -> float:
        return self._mass

    @property
    def velocity(self) -> Vector2:
        return Vector2(self._velocity.x, self._velocity.y)

    @velocity.setter
    def velocity(self, value: Vector2) -> None:
        self._velocity = Vector2(value.x, value.y)

    @property
    def speed(self) -> float:
        return self._velocity.length

    def add_force(self, force: Vector2) -> None:
        """Continuous force (N) for the next tick: a = F / m. Call every tick."""
        self._acceleration = self._acceleration + force / self._mass

    def add_acceleration(self, acceleration: Vector2) -> None:
        """Continuous acceleration (units/s²) for the next tick, mass-independent. Call every tick."""
        self._acceleration = self._acceleration + acceleration

    def add_impulse(self, impulse: Vector2) -> None:
        """Instant velocity change of I / m. Call once."""
        self._velocity = self._velocity + impulse / self._mass

    def add_velocity(self, dv: Vector2) -> None:
        """Instant velocity change, mass-independent. Call once."""
        self._velocity = self._velocity + dv

    def on_physics_update(self, ctx, delta: float):
        pos = self.game_object.position

        gravity = Vector2(0.0, -ctx.gravity)
        self._velocity = self._velocity + (self._acceleration + gravity) * delta
        self._acceleration = Vector2()

        pos.x += self._velocity.x * delta
        pos.y += self._velocity.y * delta

        deepest = 0.0
        drag_sum = 0.0
        contacts = 0

        for col in self._colliders:
            half_w = col.width / 2
            center_x = pos.x + col.offset.x
            bottom = pos.y + col.offset.y - col.height / 2

            ground = max(
                ctx.terrain.height_at(center_x - half_w),
                ctx.terrain.height_at(center_x),
                ctx.terrain.height_at(center_x + half_w),
            )

            penetration = ground - bottom
            if penetration > 0.0:
                contacts += 1
                drag_sum += col.drag
                deepest = max(deepest, penetration)

        if contacts == 0:
            return

        pos.y += deepest

        tangent = Vector2(*ctx.terrain.tangent_at(pos.x))
        normal = Vector2(*ctx.terrain.normal_at(pos.x))

        vn = self._velocity.dot(normal)
        vt = self._velocity.dot(tangent)

        if vn < 0.0:
            vn = 0.0

        vt *= math.exp(-(drag_sum / contacts) * delta)

        self._velocity = tangent * vt + normal * vn
