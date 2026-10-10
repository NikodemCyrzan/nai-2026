
class GameAction:
    def __init__(self):
        pass

class PlacePawnAction(GameAction):
    def __init__(self, at_index: int):
        self.at_index: int = at_index
        super().__init__()

class MovePawnAction(GameAction):
    def __init__(self,from_index: int, to_index: int ):
        self.from_index: int = from_index
        self.to_index: int = to_index
        super().__init__()




