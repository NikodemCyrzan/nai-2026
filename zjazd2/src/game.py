from engine.component_executors.game_loop import GameLoop
from engine.component_executors.physics_context import PhysicsContext
from engine.component_executors.render_context import RenderContext
from engine.components.loop_debugger import LoopDebugger
from engine.models.game_object import GameObject
from engine.models.terrain import Terrain


def create_debugger(setup=False, render=False, physics=False):
    comp = []
    go = GameObject(comp)
    comp.append(LoopDebugger(go, setup, render, physics))

    return go

class Game:
    def __init__(self):
        terrain = Terrain()
        render_ctx = RenderContext()
        physics_ctx = PhysicsContext(terrain)

        game_objects = [
            create_debugger(physics=True)
        ]

        loop = GameLoop(game_objects, render_ctx, physics_ctx)
        loop.setup_components()
        loop.start_loop()
