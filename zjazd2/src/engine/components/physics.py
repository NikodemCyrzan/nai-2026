import math
from .collider import Collider
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class Physics(Component):
    SOLVER_ITERATIONS = 4

    def __init__(
        self,
        go: GameObject,
        colliders: list[Collider],
        mass: float = 1.0,
        inertia: float | None = None,
    ):
        super().__init__(go)
        assert mass > 0.0
        assert colliders
        self._colliders = colliders
        self._mass = mass
        self._inertia = inertia if inertia is not None else self._estimate_inertia()
        assert self._inertia > 0.0

        self._velocity = Vector2()
        self._acceleration = Vector2()
        self._angular_velocity = 0.0
        self._angular_acceleration = 0.0

    @property
    def mass(self) -> float:
        return self._mass

    @property
    def inertia(self) -> float:
        return self._inertia

    @property
    def velocity(self) -> Vector2:
        return self._velocity.copy()

    @velocity.setter
    def velocity(self, value: Vector2) -> None:
        self._velocity = value.copy()

    @property
    def speed(self) -> float:
        return self._velocity.length

    @property
    def angular_velocity(self) -> float:
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, value: float) -> None:
        self._angular_velocity = value

    def add_force(self, force: Vector2, point: Vector2 | None = None) -> None:
        """Continuous force (N) for the next tick. point: local offset from center of mass. Call every tick."""
        self._acceleration = self._acceleration + force / self._mass
        if point is not None:
            self._angular_acceleration += self._torque(force, point) / self._inertia

    def add_acceleration(self, acceleration: Vector2) -> None:
        """Continuous acceleration (units/s²) for the next tick, mass-independent. Call every tick."""
        self._acceleration = self._acceleration + acceleration

    def add_torque(self, torque: float) -> None:
        """Continuous torque (N·m) for the next tick, counter-clockwise positive. Call every tick."""
        self._angular_acceleration += torque / self._inertia

    def add_impulse(self, impulse: Vector2, point: Vector2 | None = None) -> None:
        """Instant impulse (N·s). point: local offset from center of mass. Call once."""
        self._velocity = self._velocity + impulse / self._mass
        if point is not None:
            self._angular_velocity += self._torque(impulse, point) / self._inertia

    def add_velocity(self, dv: Vector2) -> None:
        """Instant velocity change, mass-independent. Call once."""
        self._velocity = self._velocity + dv

    def add_angular_velocity(self, dw: float) -> None:
        """Instant angular velocity change (rad/s), inertia-independent. Call once."""
        self._angular_velocity += dw

    def _torque(self, force: Vector2, point: Vector2) -> float:
        c, s = math.cos(self.game_object.rotation), math.sin(self.game_object.rotation)
        rx = point.x * c - point.y * s
        ry = point.x * s + point.y * c
        return rx * force.y - ry * force.x

    def _estimate_inertia(self) -> float:
        total_area = sum(col.width * col.height for col in self._colliders)
        inertia = 0.0
        for col in self._colliders:
            m = self._mass * col.width * col.height / total_area
            box = (col.width ** 2 + col.height ** 2) / 12
            arm = col.offset.x ** 2 + col.offset.y ** 2
            inertia += m * (box + arm)
        return inertia

    def _point_velocity(self, rx: float, ry: float) -> tuple[float, float]:
        w = self._angular_velocity
        return self._velocity.x - w * ry, self._velocity.y + w * rx

    def _apply_impulse_at(self, jx: float, jy: float, rx: float, ry: float) -> None:
        self._velocity.x += jx / self._mass
        self._velocity.y += jy / self._mass
        self._angular_velocity += (rx * jy - ry * jx) / self._inertia

    def on_physics_update(self, ctx, delta: float):
        go = self.game_object
        pos = go.position

        self._velocity = self._velocity + (self._acceleration + Vector2(0.0, -ctx.gravity)) * delta
        self._angular_velocity += self._angular_acceleration * delta
        self._acceleration = Vector2()
        self._angular_acceleration = 0.0

        pos.x += self._velocity.x * delta
        pos.y += self._velocity.y * delta
        go.rotation += self._angular_velocity * delta

        contacts = self._find_contacts(ctx.terrain, delta)
        if contacts:
            self._solve_contacts(contacts)

    def _find_contacts(self, terrain, delta: float) -> list[tuple[float, float, float, float, float]]:
        go = self.game_object
        pos = go.position
        c, s = math.cos(go.rotation), math.sin(go.rotation)
        step = delta / self.SOLVER_ITERATIONS

        contacts = []
        deepest = 0.0

        for col in self._colliders:
            ox, oy = col.offset.x, col.offset.y
            cx = pos.x + ox * c - oy * s
            cy = pos.y + ox * s + oy * c

            corners = sorted(
                ((cx + lx * c - ly * s, cy + lx * s + ly * c) for lx, ly in col.corners),
                key=lambda p: p[1],
            )

            for x, y in corners[:2]:
                penetration = terrain.height_at(x) - y
                if penetration > 0.0:
                    deepest = max(deepest, penetration)
                    tangent = terrain.tangent_at(x)
                    decay = 1.0 - math.exp(-col.drag * step)
                    contacts.append((x - pos.x, y - pos.y, tangent.x, tangent.y, decay))

        pos.y += deepest
        return contacts

    def _solve_contacts(self, contacts: list[tuple[float, float, float, float, float]]) -> None:
        inv_m = 1.0 / self._mass
        inv_i = 1.0 / self._inertia

        for _ in range(self.SOLVER_ITERATIONS):
            for rx, ry, tx, ty, decay in contacts:
                nx, ny = -ty, tx

                vx, vy = self._point_velocity(rx, ry)
                vn = vx * nx + vy * ny
                if vn < 0.0:
                    rn = rx * ny - ry * nx
                    j = -vn / (inv_m + rn * rn * inv_i)
                    self._apply_impulse_at(nx * j, ny * j, rx, ry)
                    vx, vy = self._point_velocity(rx, ry)

                vt = vx * tx + vy * ty
                rt = rx * ty - ry * tx
                j = -vt * decay / (inv_m + rt * rt * inv_i)
                self._apply_impulse_at(tx * j, ty * j, rx, ry)
