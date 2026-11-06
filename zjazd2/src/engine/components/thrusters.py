from .physics import Physics
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class Thruster:
    """A single engine on the body."""

    def __init__(self, position: Vector2, max_force: float, direction: Vector2 | None = None):
        assert max_force > 0.0
        self._position = position.copy()
        self._max_force = max_force
        self._direction = (direction or Vector2(0.0, 1.0)).normalized()

    @property
    def max_force(self) -> float:
        """Largest thrust of the engine."""
        return self._max_force

    @property
    def position(self) -> Vector2:
        """Engine position relative to the center of the body."""
        return self._position.copy()

    @property
    def direction(self) -> Vector2:
        return self._direction.copy()


class ThrusterController(Component):
    """Controls the engines of a body."""

    def __init__(self, go: GameObject, thrusters: list[Thruster] | None = None):
        super().__init__(go)
        self._thrusters = list(thrusters or [])
        self._physics: Physics | None = None
        self._forces: dict[int, float] = {}

    def on_setup(self):
        self._physics = self.game_object.get_component(Physics)
        if self._physics is None:
            raise RuntimeError("ThrusterController requires a Physics component on the same GameObject")

    @property
    def thruster_count(self) -> int:
        return len(self._thrusters)

    def add_thruster(self, thruster: Thruster):
        self._thrusters.append(thruster)

    def max_force(self, thruster_index: int) -> float:
        """Largest thrust of one engine."""
        return self._thrusters[thruster_index].max_force

    @property
    def thrusters(self) -> list[Thruster]:
        return list(self._thrusters)

    def current_force(self, thruster_index: int) -> float:
        """Thrust of one engine in the current step."""
        return self._forces.get(thruster_index, 0.0)

    def on_physics_update(self, ctx, delta: float):
        """Resets the recorded thrust for a new step."""
        self._forces = {}

    def apply_force(self, force: float, thruster_index: int | None = None) -> None:
        """Fires an engine for the next step."""
        indices = range(len(self._thrusters)) if thruster_index is None else [thruster_index]
        for i, (thruster, direction) in zip(indices, self._selected(thruster_index)):
            clamped = min(max(force, 0.0), thruster.max_force)
            self._forces[i] = self._forces.get(i, 0.0) + clamped
            self._physics.add_force(direction * clamped, thruster.position)

    def apply_impulse(self, impulse: float, thruster_index: int | None = None) -> None:
        """Gives an instant push from an engine."""
        for thruster, direction in self._selected(thruster_index):
            self._physics.add_impulse(direction * impulse, thruster.position)

    def _selected(self, thruster_index: int | None) -> list[tuple[Thruster, Vector2]]:
        """Engines to use and the direction each one pushes."""
        assert self._physics is not None, "ThrusterController used before setup"

        if thruster_index is None:
            thrusters = self._thrusters
        else:
            if not 0 <= thruster_index < len(self._thrusters):
                raise IndexError(f"Thruster index {thruster_index} out of range")
            thrusters = [self._thrusters[thruster_index]]

        rotation = self._physics.rotation
        return [(t, t.direction.rotated(rotation)) for t in thrusters]
