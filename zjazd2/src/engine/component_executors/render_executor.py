from component_executor import ComponentExecutor
from ..models.game_object import GameObject


class RenderExecutor(ComponentExecutor):
    def __init__(self, game_objects: list[GameObject]):
        super().__init__(game_objects)

    def execute_components(self):
        for go in self._game_objects:
            for comp in go.components:
                comp.on_render_update()
