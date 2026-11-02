import random

from .physics import Physics
from ..component_executors.physics_context import PhysicsContext
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class Thruster:
    def __init__(self, position: Vector2):
        self._position = position

    @property
    def position(self) -> Vector2:
        return self._position

class ThrusterController(Component):
    def __init__(self, go: GameObject):
        super().__init__(go)
        self._thrusters = []

    def add_thruster(self, thruster: Thruster):
        self._thrusters.append(thruster)

    def push(self, force: float, thruster_index: int | None = None):
        go = self.game_object
        physics: Physics = self.game_object.get_component(Physics)

        rot = go.rotation

        direction = Vector2(0, 1).rotated(rot)

        thrusters = self._thrusters
        if thruster_index is not None:
            if not 0 <= thruster_index < len(thrusters):
                return
            thrusters = [thrusters[thruster_index]]

        for thruster in thrusters:
            force_vector = direction * force
            if physics:
                physics.add_impulse(force_vector, thruster.position)



