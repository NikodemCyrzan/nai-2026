from engine.component_executors.physics_context import PhysicsContext
from engine.components.physics import Physics
from engine.models.component import Component


class LaunchController(Component):
    """Launches the car with a mouse drag like a slingshot."""

    SPEED_PER_PIXEL = 0.1
    MAX_LAUNCH_SPEED = 40.0

    def __init__(self, go):
        super().__init__(go)
        self._physics: Physics | None = None

    def on_setup(self):
        self._physics = self.game_object.get_component(Physics)
        if self._physics is None:
            raise RuntimeError("LaunchController requires a Physics component on the same GameObject")

    def on_physics_update(self, ctx: PhysicsContext, delta: float):
        """Launches the car opposite to each new drag."""
        for drag in ctx.input.consume_drags():
            pull = drag.delta
            distance = pull.length
            if distance == 0.0:
                continue

            speed = min(distance * self.SPEED_PER_PIXEL, self.MAX_LAUNCH_SPEED)
            direction = -pull.normalized()
            self._physics.add_impulse(direction * (self._physics.mass * speed))
