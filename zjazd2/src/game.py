from engine.component_executors.game_loop import GameLoop
from engine.component_executors.physics_context import PhysicsContext
from engine.component_executors.render_context import RenderContext
from engine.components.camera import Camera
from engine.components.collider import Collider
from engine.components.collider_debug_renderer import ColliderDebugRenderer
from engine.components.loop_debugger import LoopDebugger, LogType
from engine.components.physics import Physics
from engine.components.sensor import Sensor
from engine.components.sensor_debug_renderer import SensorDebugRenderer
from engine.components.terrain_renderer import TerrainRenderer
from engine.components.thruster_debug_renderer import ThrusterDebugRenderer
from engine.components.thrusters import Thruster, ThrusterController
from engine.components.vector_renderer import VectorRenderer
from engine.models.game_object import GameObject
from engine.models.input import Input
from engine.models.terrain import Terrain
from engine.models.vector2 import Vector2
from engine.render_pipeline.game_widget import GameWidget
from gameplay.landing_ai import LandingAI
from gameplay.launch_controller import LaunchController


DEBUG_COLLIDERS = False
DEBUG_SENSORS = True
DEBUG_THRUST = True

ENGINE_MAX_FORCE = 25_000.0
ENGINE_OFFSET_X = 1.5
DEBUG_LOOP_LOG: set[LogType] = set()


def create_loop_debugger(log_types: set[LogType], setup=False, render=False, physics=False):
    comp = []
    go = GameObject(comp)
    comp.append(LoopDebugger(go, log_types, setup, render, physics))

    return go

def create_camera(target: GameObject | None = None):
    comp = []
    go = GameObject(comp)
    comp.append(Camera(go, pixels_per_unit=20.0, target=target))

    return go

def create_terrain(terrain: Terrain):
    comp = []
    go = GameObject(comp)
    comp.append(TerrainRenderer(go, terrain))

    return go

def create_car(debug_colliders: bool = False, debug_sensors: bool = False, debug_thrust: bool = False):
    comp = []
    go = GameObject(comp, Vector2(0.0, 100.0))
    comp.append(VectorRenderer(go, "assets/roadster.svg", width=4.7))
    l_wheel_offset = Vector2(-1.4335, -0.2937)
    r_wheel_offset = Vector2(1.5627, -0.2937)
    comp.append(VectorRenderer(go, "assets/wheel.svg", width=0.7637, offset=l_wheel_offset))
    comp.append(VectorRenderer(go, "assets/wheel.svg", width=0.7637, offset=r_wheel_offset))
    colliders = [
        Collider(go, 2.9375, 0.235, 1.0, offset=Vector2(0.0, 0.47)),
        Collider(go, 4.7, 0.705, 1.0),
        Collider(go, 0.705, 0.705, 0.2, offset=l_wheel_offset),
        Collider(go, 0.705, 0.705, 0.2, offset=r_wheel_offset),
    ]

    engine_y = l_wheel_offset.y
    comp.append(ThrusterController(go, [
        Thruster(Vector2(-ENGINE_OFFSET_X, engine_y), max_force=ENGINE_MAX_FORCE),
        Thruster(Vector2(ENGINE_OFFSET_X, engine_y), max_force=ENGINE_MAX_FORCE),
    ]))
    comp.append(LaunchController(go))
    comp.append(LandingAI(go))
    comp.append(Physics(go, colliders, 2350))

    wheel_bottom = l_wheel_offset.y - 0.3525
    comp.append(Sensor(go, Vector2(l_wheel_offset.x, wheel_bottom), name="rear", look="velocity"))
    comp.append(Sensor(go, Vector2(r_wheel_offset.x, wheel_bottom), name="front", look="velocity"))

    if debug_colliders:
        comp.append(ColliderDebugRenderer(go))
    if debug_sensors:
        comp.append(SensorDebugRenderer(go))
    if debug_thrust:
        comp.append(ThrusterDebugRenderer(go))

    return go

class Game:
    def __init__(self):
        terrain = Terrain(amplitude=35, octaves=2, lacunarity=4.5, persistence=1.5, scale=0.01, seed=42)
        input = Input()
        render_ctx = RenderContext()
        physics_ctx = PhysicsContext(terrain, input)

        car = create_car(debug_colliders=DEBUG_COLLIDERS, debug_sensors=DEBUG_SENSORS, debug_thrust=DEBUG_THRUST)

        game_objects = [
            create_camera(target=car),
            create_terrain(terrain),
            car,
        ]
        if DEBUG_LOOP_LOG:
            game_objects.append(create_loop_debugger(DEBUG_LOOP_LOG, render=True))

        self.loop = GameLoop(game_objects, render_ctx, physics_ctx)
        self.widget = GameWidget(self.loop, render_ctx, input)
        self.widget.resize(1280, 720)
        self.widget.setWindowTitle("Game")
        self.loop.setup_components()
        self.widget.show()
