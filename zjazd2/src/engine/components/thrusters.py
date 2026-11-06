from .physics import Physics
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class Thruster:
    def __init__(self, position: Vector2, direction: Vector2 | None = None):
        """position: local offset from center of mass. direction: local push direction (default: up)."""
        self._position = position.copy()
        self._direction = (direction or Vector2(0.0, 1.0)).normalized()

    @property
    def position(self) -> Vector2:
        return self._position.copy()

    @property
    def direction(self) -> Vector2:
        return self._direction.copy()


class ThrusterController(Component):
    """Applies thrust through the object's Physics"""

    def __init__(self, go: GameObject, thrusters: list[Thruster] | None = None):
        super().__init__(go)
        self._thrusters = list(thrusters or [])
        self._physics: Physics | None = None

    def on_setup(self):
        self._physics = self.game_object.get_component(Physics)
        if self._physics is None:
            raise RuntimeError("ThrusterController requires a Physics component on the same GameObject")

    @property
    def thruster_count(self) -> int:
        return len(self._thrusters)

    def add_thruster(self, thruster: Thruster):
        self._thrusters.append(thruster)

    def apply_force(self, force: float, thruster_index: int | None = None) -> None:
        for thruster, direction in self._selected(thruster_index):
            self._physics.add_force(direction * force, thruster.position)

    def apply_impulse(self, impulse: float, thruster_index: int | None = None) -> None:
        for thruster, direction in self._selected(thruster_index):
            self._physics.add_impulse(direction * impulse, thruster.position)

    def _selected(self, thruster_index: int | None) -> list[tuple[Thruster, Vector2]]:
        assert self._physics is not None, "ThrusterController used before setup"

        if thruster_index is None:
            thrusters = self._thrusters
        else:
            if not 0 <= thruster_index < len(self._thrusters):
                raise IndexError(f"Thruster index {thruster_index} out of range")
            thrusters = [self._thrusters[thruster_index]]

        rotation = self._physics.rotation
        return [(t, t.direction.rotated(rotation)) for t in thrusters]
