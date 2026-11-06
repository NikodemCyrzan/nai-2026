from __future__ import annotations

import math
from typing import TYPE_CHECKING

from .physics import Physics
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2

if TYPE_CHECKING:
    from ..component_executors.physics_context import PhysicsContext


class Sensor(Component):
    """Measures the distance to the terrain and the angle of the surface it hits.
    Looks straight down (look="down") or along the velocity (look="velocity")."""

    MIN_SPEED = 0.05
    DOWN = Vector2(0.0, -1.0)

    def __init__(self, go: GameObject, offset: Vector2, max_range: float = 100.0, name: str = "",
                 look: str = "down"):
        super().__init__(go)
        assert max_range > 0.0
        assert look in ("down", "velocity")
        self._offset = offset.copy()
        self._max_range = max_range
        self._name = name
        self._look = look
        self._physics: Physics | None = None

        self._direction = self.DOWN.copy()
        self._distance: float | None = None
        self._surface_angle: float | None = None

    def on_setup(self):
        self._physics = self.game_object.get_component(Physics)
        if self._physics is None:
            raise RuntimeError("Sensor requires a Physics component on the same GameObject")

    @property
    def name(self) -> str:
        return self._name

    @property
    def offset(self) -> Vector2:
        return self._offset.copy()

    @property
    def max_range(self) -> float:
        return self._max_range

    @property
    def distance(self) -> float | None:
        """Distance to the terrain, or None if nothing is in range."""
        return self._distance

    @property
    def surface_angle(self) -> float | None:
        """Angle (rad) of the surface where the ray hit, or None."""
        return self._surface_angle

    @property
    def direction(self) -> Vector2:
        """Direction of the last measurement."""
        return self._direction.copy()

    def world_origin(self, position: Vector2, rotation: float) -> Vector2:
        return position + self._offset.rotated(rotation)

    def on_physics_update(self, ctx: PhysicsContext, delta: float):
        physics = self._physics
        velocity = physics.velocity
        if self._look == "velocity" and velocity.length >= self.MIN_SPEED:
            self._direction = velocity.normalized()
        else:
            self._direction = self.DOWN.copy()

        origin = self.world_origin(physics.position, physics.rotation)
        self._distance = ctx.terrain.raycast(origin, self._direction, self._max_range)
        if self._distance is None:
            self._surface_angle = None
        else:
            hit = origin + self._direction * self._distance
            self._surface_angle = math.atan(ctx.terrain.slope_at(hit.x))
