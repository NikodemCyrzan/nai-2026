from PySide6.QtCore import QPoint, Qt

from engine.component_executors.game_loop import GameLoop
from engine.component_executors.physics_context import PhysicsContext
from engine.component_executors.render_context import RenderContext
from engine.components.camera import Camera
from engine.components.collider import Collider
from engine.components.loop_debugger import LoopDebugger, LogType
from engine.components.physics import Physics
from engine.components.thrusters import Thruster, ThrusterController
from engine.components.vector_renderer import VectorRenderer
from engine.models.game_object import GameObject
from engine.models.terrain import Terrain
from engine.models.vector2 import Vector2
from engine.render_pipeline.game_widget import GameWidget
from engine.components.terrain_renderer import TerrainRenderer


def create_loop_debugger(log_types: set[LogType], setup=False, render=False, physics=False):
    comp = []
    go = GameObject(comp)
    comp.append(LoopDebugger(go, log_types, setup, render, physics))

    return go

def create_camera(terrain: Terrain, target: GameObject | None = None):
    comp = []
    go = GameObject(comp)
    comp.append(Camera(go, pixels_per_unit=5.0, target=target))
    comp.append(TerrainRenderer(go, terrain))

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
        Collider(go, 25.0, 2.0, 1.0, offset=Vector2(0.0, 4.0)),
        Collider(go, 40.0, 6.0, 1.0),
        Collider(go, 6.0, 6.0, 0.2, offset=Vector2(-12.2, -2.5)),
        Collider(go, 6, 6, 0.2, offset=Vector2(13.3, -2.5))
    ]

    thrust_controller = ThrusterController(go)
    thrust_controller.add_thruster(Thruster(l_wheel_offset))
    thrust_controller.add_thruster(Thruster(r_wheel_offset))

    comp.append(thrust_controller)
    comp.append(Physics(go, colliders, 2350))

    return go

class Game:
    DRAG_FORCE_SCALE = 20.0
    MAX_DRAG_FORCE = 5000.0
    KEY_THRUST_FORCE = 2000.0

    def __init__(self):
        self._held_keys: set[int] = set()
        terrain = Terrain(amplitude=35, octaves=1, lacunarity=4.5, persistence=1.5, scale=0.009, seed=42)
        render_ctx = RenderContext()
        physics_ctx = PhysicsContext(terrain)

        car = create_car()
        self._car = car
        camera = create_camera(terrain, target=car)

        game_objects = [
            #create_loop_debugger({LogType.DELTA}, render=True),
            camera,
            car
        ]

        self.loop = GameLoop(
            game_objects,
            render_ctx,
            physics_ctx,
            before_physics_step=self._apply_held_thrusters,
        )
        self.widget = GameWidget(
            self.loop,
            render_ctx,
            on_drag=self._on_drag,
            on_key=self._on_key,
        )
        self.widget.resize(1280, 720)
        self.widget.setWindowTitle("Game")
        self.loop.setup_components()
        self.widget.show()
        self.widget.setFocus()

    def _on_drag(self, start: QPoint, end: QPoint):
        thruster = self._car.get_component(ThrusterController)
        if thruster is None:
            return

        drag = Vector2(end.x() - start.x(), start.y() - end.y())
        distance = drag.length
        if distance == 0.0:
            return

        force = min(distance * self.DRAG_FORCE_SCALE, self.MAX_DRAG_FORCE)
        thruster.push(force)

    def _on_key(self, key: int, pressed: bool):
        if pressed:
            self._held_keys.add(key)
        else:
            self._held_keys.discard(key)

    def _apply_held_thrusters(self):
        thruster = self._car.get_component(ThrusterController)
        if thruster is None:
            return

        thruster_indices = {
            Qt.Key.Key_Left: 0,
            Qt.Key.Key_Right: 1,
        }
        for key in self._held_keys:
            thruster_index = thruster_indices.get(key)
            if thruster_index is not None:
                thruster.push(self.KEY_THRUST_FORCE, thruster_index)
