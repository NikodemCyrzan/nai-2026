import math

from engine.component_executors.physics_context import PhysicsContext
from engine.components.physics import Physics
from engine.components.sensor import Sensor
from engine.components.thrusters import ThrusterController
from engine.mathematics.fuzzy import FuzzyVariable, MamdaniSystem, Rule, trapezoid, triangle
from engine.models.component import Component


def create_braking_system() -> MamdaniSystem:
    """Distance and approach speed of one side -> thrust of the engine on that side."""
    distance = FuzzyVariable("distance", 0.0, 100.0, {
        "very_close": trapezoid(0.0, 0.0, 1.0, 3.0),
        "close": triangle(1.0, 5.0, 12.0),
        "medium": triangle(6.0, 20.0, 45.0),
        "far": trapezoid(30.0, 50.0, 100.0, 100.0),
    })
    speed = FuzzyVariable("speed", -20.0, 50.0, {
        "rising": trapezoid(-20.0, -20.0, -0.5, 0.2),
        "slow": triangle(0.0, 1.0, 2.5),
        "medium": triangle(1.5, 4.0, 8.0),
        "fast": triangle(5.0, 10.0, 18.0),
        "very_fast": trapezoid(12.0, 20.0, 50.0, 50.0),
    })
    thrust = FuzzyVariable("thrust", -0.2, 1.2, {
        "zero": triangle(-0.2, 0.0, 0.2),
        "low": triangle(0.1, 0.3, 0.45),
        "hover": triangle(0.36, 0.46, 0.56),
        "strong": triangle(0.55, 0.75, 0.95),
        "full": triangle(0.8, 1.0, 1.2),
    })

    table = {
        "very_close": ("zero", "hover", "full",   "full",   "full"),
        "close":      ("zero", "low",   "strong", "full",   "full"),
        "medium":     ("zero", "low",   "hover",  "strong", "full"),
        "far":        ("zero", "zero",  "low",    "hover",  "strong"),
    }
    speeds = ("rising", "slow", "medium", "fast", "very_fast")
    rules = [
        Rule({"distance": d, "speed": s}, out)
        for d, row in table.items()
        for s, out in zip(speeds, row)
    ]
    return MamdaniSystem([distance, speed], thrust, rules)


def create_leveling_system() -> MamdaniSystem:
    """Tilt from the wanted angle and spin -> thrust shift between rear and front engine."""
    tilt = FuzzyVariable("tilt", -1.5, 1.5, {
        "nose_down": trapezoid(-1.5, -1.5, -0.3, 0.0),
        "level": triangle(-0.15, 0.0, 0.15),
        "nose_up": trapezoid(0.0, 0.3, 1.5, 1.5),
    })
    spin = FuzzyVariable("spin", -5.0, 5.0, {
        "turning_down": trapezoid(-5.0, -5.0, -0.6, 0.0),
        "still": triangle(-0.3, 0.0, 0.3),
        "turning_up": trapezoid(0.0, 0.6, 5.0, 5.0),
    })
    shift = FuzzyVariable("shift", -1.4, 1.4, {
        "to_rear": triangle(-1.4, -1.0, -0.4),
        "to_rear_a_bit": triangle(-0.8, -0.4, 0.0),
        "none": triangle(-0.2, 0.0, 0.2),
        "to_front_a_bit": triangle(0.0, 0.4, 0.8),
        "to_front": triangle(0.4, 1.0, 1.4),
    })

    table = {
        "nose_down": ("to_front",       "to_front", "none"),
        "level":     ("to_front_a_bit", "none",     "to_rear_a_bit"),
        "nose_up":   ("none",           "to_rear",  "to_rear"),
    }
    spins = ("turning_down", "still", "turning_up")
    rules = [
        Rule({"tilt": t, "spin": s}, out)
        for t, row in table.items()
        for s, out in zip(spins, row)
    ]
    return MamdaniSystem([tilt, spin], shift, rules)


class LandingAI(Component):
    """Fuzzy-logic landing."""

    REAR, FRONT = 0, 1
    LEVELING_SHARE = 0.4
    MATCH_START = 25.0
    MATCH_FULL = 8.0
    MATCH_START_TIME = 4.0
    MATCH_FULL_TIME = 1.5
    MAX_SURFACE_ANGLE = 0.8
    LEAN_PER_SPEED = 0.03
    MAX_LEAN = 0.4

    def __init__(self, go):
        super().__init__(go)
        self._braking = create_braking_system()
        self._leveling = create_leveling_system()
        self._physics: Physics | None = None
        self._thrusters: ThrusterController | None = None
        self._sensors: dict[int, Sensor] = {}

    def on_setup(self):
        go = self.game_object
        self._physics = go.get_component(Physics)
        self._thrusters = go.get_component(ThrusterController)
        sensors = {c.name: c for c in go.components if isinstance(c, Sensor)}
        if self._physics is None or self._thrusters is None or not {"rear", "front"} <= sensors.keys():
            raise RuntimeError("LandingAI needs Physics, ThrusterController and Sensors 'rear' and 'front'")
        self._sensors = {self.REAR: sensors["rear"], self.FRONT: sensors["front"]}

    def on_physics_update(self, ctx: PhysicsContext, delta: float):
        physics = self._physics
        if physics.in_contact:
            return

        target = self._wanted_angle()
        tilt = math.remainder(physics.rotation - target, math.tau)
        shift = self._leveling.compute({"tilt": tilt, "spin": physics.angular_velocity})

        for engine, sensor in self._sensors.items():
            if sensor.distance is None:
                thrust = 0.0
            else:
                thrust = self._braking.compute({"distance": sensor.distance, "speed": self._approach_speed(sensor)})

            side = 1.0 if engine == self.FRONT else -1.0
            thrust += side * shift * self.LEVELING_SHARE

            self._thrusters.apply_force(thrust * self._thrusters.max_force(engine), engine)

    def _wanted_angle(self) -> float:
        """Target car angle. Level when far from terrain and facing terrain when close."""
        hits = [s for s in self._sensors.values() if s.distance is not None]
        if not hits:
            return 0.0

        surface = sum(s.surface_angle for s in hits) / len(hits)
        surface = min(max(surface, -self.MAX_SURFACE_ANGLE), self.MAX_SURFACE_ANGLE)

        velocity = self._physics.velocity
        along = velocity.x * math.cos(surface) + velocity.y * math.sin(surface)
        lean = min(max(along * self.LEAN_PER_SPEED, -self.MAX_LEAN), self.MAX_LEAN)

        distance = min(s.distance for s in hits)
        time_to_impact = distance / max(velocity.length, 0.1)
        closeness = max(
            (self.MATCH_START - distance) / (self.MATCH_START - self.MATCH_FULL),
            (self.MATCH_START_TIME - time_to_impact) / (self.MATCH_START_TIME - self.MATCH_FULL_TIME),
        )
        closeness = min(max(closeness, 0.0), 1.0)
        return closeness * (surface + lean)

    def _approach_speed(self, sensor: Sensor) -> float:
        """Speed of the sensor mount point toward the surface, along its normal."""
        physics = self._physics
        r = sensor.offset.rotated(physics.rotation)
        w = physics.angular_velocity
        vx = physics.velocity.x - w * r.y
        vy = physics.velocity.y + w * r.x
        angle = sensor.surface_angle
        normal_x, normal_y = -math.sin(angle), math.cos(angle)
        return -(vx * normal_x + vy * normal_y)
