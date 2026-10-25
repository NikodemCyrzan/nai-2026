from engine.component_executors.game_loop import GameLoop
from engine.component_executors.physics_context import PhysicsContext
from engine.component_executors.render_context import RenderContext
from engine.components.camera import Camera
from engine.components.loop_debugger import LoopDebugger, LogType
from engine.models.game_object import GameObject
from engine.models.terrain import Terrain
from engine.render_pipeline.game_widget import GameWidget


def create_loop_debugger(log_types: set[LogType], setup=False, render=False, physics=False):
    comp = []
    go = GameObject(comp)
    comp.append(LoopDebugger(go, log_types, setup, render, physics))

    return go

def create_camera():
    comp = []
    go = GameObject(comp)
    comp.append(Camera(go))

    return go

class Game:
    def __init__(self):
        terrain = Terrain()
        render_ctx = RenderContext()
        physics_ctx = PhysicsContext(terrain)

        game_objects = [
            create_loop_debugger({LogType.DELTA}, render=True),
            create_camera()
        ]

        self.loop = GameLoop(game_objects, render_ctx, physics_ctx)
        self.widget = GameWidget(self.loop, render_ctx)
        self.widget.resize(1280, 720)
        self.widget.setWindowTitle("Game")
        self.loop.setup_components()
        self.widget.show()
