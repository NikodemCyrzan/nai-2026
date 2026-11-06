import math

import simpful as sf

from engine.component_executors.physics_context import PhysicsContext
from engine.components.physics import Physics
from engine.components.sensor import Sensor
from engine.components.thrusters import ThrusterController
from engine.models.component import Component


RANGES = {
    "distance": (0.0, 100.0),
    "speed": (-20.0, 50.0),
    "thrust": (-0.2, 1.2),
    "tilt": (-1.5, 1.5),
    "spin": (-5.0, 5.0),
    "shift": (-1.4, 1.4),
}


def _variable(fs: sf.FuzzySystem, name: str, sets: list) -> None:
    fs.add_linguistic_variable(name, sf.LinguisticVariable(sets, concept=name, universe_of_discourse=list(RANGES[name])))


def create_braking_system() -> sf.FuzzySystem:
    """Distance and approach speed of one side -> thrust of the engine on that side."""
    fs = sf.FuzzySystem(show_banner=False, verbose=False)
    _variable(fs, "distance", [
        sf.TrapezoidFuzzySet(0.0, 0.0, 1.0, 3.0, term="very_close"),
        sf.TriangleFuzzySet(1.0, 5.0, 12.0, term="close"),
        sf.TriangleFuzzySet(6.0, 20.0, 45.0, term="medium"),
        sf.TrapezoidFuzzySet(30.0, 50.0, 100.0, 100.0, term="far"),
    ])
    _variable(fs, "speed", [
        sf.TrapezoidFuzzySet(-20.0, -20.0, -0.5, 0.2, term="rising"),
        sf.TriangleFuzzySet(0.0, 1.0, 2.5, term="slow"),
        sf.TriangleFuzzySet(1.5, 4.0, 8.0, term="medium"),
        sf.TriangleFuzzySet(5.0, 10.0, 18.0, term="fast"),
        sf.TrapezoidFuzzySet(12.0, 20.0, 50.0, 50.0, term="very_fast"),
    ])
    _variable(fs, "thrust", [
        sf.TriangleFuzzySet(-0.2, 0.0, 0.2, term="zero"),
        sf.TriangleFuzzySet(0.1, 0.3, 0.45, term="low"),
        sf.TriangleFuzzySet(0.36, 0.46, 0.56, term="hover"),
        sf.TriangleFuzzySet(0.55, 0.75, 0.95, term="strong"),
        sf.TriangleFuzzySet(0.8, 1.0, 1.2, term="full"),
    ])
    fs.add_rules([
        "IF (speed IS rising) THEN (thrust IS zero)",

        "IF (distance IS very_close) AND (speed IS slow) THEN (thrust IS hover)",
        "IF (distance IS very_close) AND (speed IS medium) THEN (thrust IS full)",
        "IF (distance IS very_close) AND (speed IS fast) THEN (thrust IS full)",
        "IF (distance IS very_close) AND (speed IS very_fast) THEN (thrust IS full)",

        "IF (distance IS close) AND (speed IS slow) THEN (thrust IS low)",
        "IF (distance IS close) AND (speed IS medium) THEN (thrust IS strong)",
        "IF (distance IS close) AND (speed IS fast) THEN (thrust IS full)",
        "IF (distance IS close) AND (speed IS very_fast) THEN (thrust IS full)",

        "IF (distance IS medium) AND (speed IS slow) THEN (thrust IS low)",
        "IF (distance IS medium) AND (speed IS medium) THEN (thrust IS hover)",
        "IF (distance IS medium) AND (speed IS fast) THEN (thrust IS strong)",
        "IF (distance IS medium) AND (speed IS very_fast) THEN (thrust IS full)",

        "IF (distance IS far) AND (speed IS slow) THEN (thrust IS zero)",
        "IF (distance IS far) AND (speed IS medium) THEN (thrust IS low)",
        "IF (distance IS far) AND (speed IS fast) THEN (thrust IS hover)",
        "IF (distance IS far) AND (speed IS very_fast) THEN (thrust IS strong)",
    ])
    return fs


def create_leveling_system() -> sf.FuzzySystem:
    """Tilt from the wanted angle and spin -> thrust shift between rear and front engine."""
    fs = sf.FuzzySystem(show_banner=False, verbose=False)
    _variable(fs, "tilt", [
        sf.TrapezoidFuzzySet(-1.5, -1.5, -0.3, 0.0, term="nose_down"),
        sf.TriangleFuzzySet(-0.15, 0.0, 0.15, term="level"),
        sf.TrapezoidFuzzySet(0.0, 0.3, 1.5, 1.5, term="nose_up"),
    ])
    _variable(fs, "spin", [
        sf.TrapezoidFuzzySet(-5.0, -5.0, -0.6, 0.0, term="turning_down"),
        sf.TriangleFuzzySet(-0.3, 0.0, 0.3, term="still"),
        sf.TrapezoidFuzzySet(0.0, 0.6, 5.0, 5.0, term="turning_up"),
    ])
    _variable(fs, "shift", [
        sf.TriangleFuzzySet(-1.4, -1.0, -0.4, term="to_rear"),
        sf.TriangleFuzzySet(-0.8, -0.4, 0.0, term="to_rear_a_bit"),
        sf.TriangleFuzzySet(-0.2, 0.0, 0.2, term="none"),
        sf.TriangleFuzzySet(0.0, 0.4, 0.8, term="to_front_a_bit"),
        sf.TriangleFuzzySet(0.4, 1.0, 1.4, term="to_front"),
    ])
    fs.add_rules([
        "IF (tilt IS nose_down) AND (spin IS turning_down) THEN (shift IS to_front)",
        "IF (tilt IS nose_down) AND (spin IS still) THEN (shift IS to_front)",
        "IF (tilt IS nose_down) AND (spin IS turning_up) THEN (shift IS none)",

        "IF (tilt IS level) AND (spin IS turning_down) THEN (shift IS to_front_a_bit)",
        "IF (tilt IS level) AND (spin IS still) THEN (shift IS none)",
        "IF (tilt IS level) AND (spin IS turning_up) THEN (shift IS to_rear_a_bit)",

        "IF (tilt IS nose_up) AND (spin IS turning_down) THEN (shift IS none)",
        "IF (tilt IS nose_up) AND (spin IS still) THEN (shift IS to_rear)",
        "IF (tilt IS nose_up) AND (spin IS turning_up) THEN (shift IS to_rear)",
    ])
    return fs


def infer(fs: sf.FuzzySystem, inputs: dict[str, float], output: str) -> float:
    """Runs Mamdani inference for crisp inputs and returns the crisp output."""
    for name, value in inputs.items():
        low, high = RANGES[name]
        fs.set_variable(name, min(max(value, low), high), verbose=False)
    return float(fs.Mamdani_inference([output], subdivisions=100, ignore_warnings=True)[output])


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
        shift = infer(self._leveling, {"tilt": tilt, "spin": physics.angular_velocity}, "shift")

        for engine, sensor in self._sensors.items():
            if sensor.distance is None:
                thrust = 0.0
            else:
                inputs = {"distance": sensor.distance, "speed": self._approach_speed(sensor)}
                thrust = infer(self._braking, inputs, "thrust")

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
