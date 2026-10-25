from engine.component_executors.game_loop import GameLoop
from engine.component_executors.physics_context import PhysicsContext
from engine.component_executors.render_context import RenderContext
from engine.components.camera import Camera
from engine.components.collider import Collider
from engine.components.loop_debugger import LoopDebugger, LogType
from engine.components.physics import Physics
from engine.components.vector_renderer import VectorRenderer
from engine.models.game_object import GameObject
from engine.models.terrain import Terrain
from engine.models.vector2 import Vector2
from engine.render_pipeline.game_widget import GameWidget


def create_loop_debugger(log_types: set[LogType], setup=False, render=False, physics=False):
    comp = []
    go = GameObject(comp)
    comp.append(LoopDebugger(go, log_types, setup, render, physics))

    return go

def create_camera():
    comp = []
    go = GameObject(comp)
    comp.append(Camera(go, pixels_per_unit=6.0))

    return go

def create_car():
    comp = []
    go = GameObject(comp, Vector2(0.0, 100.0))
    comp.append(VectorRenderer(go, "assets/roadster.svg", width=40.0))
    l_wheel_offset = Vector2(-12.2, -2.5)
    r_wheel_offset = Vector2(13.3, -2.5)
    comp.append(VectorRenderer(go, "assets/wheel.svg", width=6.5, offset=l_wheel_offset))
    comp.append(VectorRenderer(go, "assets/wheel.svg", width=6.5, offset=r_wheel_offset))
    colliders = [
        Collider(go, 40.0, 20.0, 1.0)
    ]
    comp.append(Physics(go, colliders, 2350))

    return go

class Game:
    def __init__(self):
        terrain = Terrain()
        render_ctx = RenderContext()
        physics_ctx = PhysicsContext(terrain)

        game_objects = [
            create_loop_debugger({LogType.DELTA}, render=True),
            create_camera(),
            create_car()
        ]

        self.loop = GameLoop(game_objects, render_ctx, physics_ctx)
        self.widget = GameWidget(self.loop, render_ctx)
        self.widget.resize(1280, 720)
        self.widget.setWindowTitle("Game")
        self.loop.setup_components()
        self.widget.show()
