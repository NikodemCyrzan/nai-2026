
class GameAction:
    pass

class GameStartAction(GameAction):
    pass

class PlacePawnAction(GameAction):
    def __init__(self, at_index: int):
        self.at_index: int = at_index

class MovePawnAction(GameAction):
    def __init__(self,from_index: int, to_index: int ):
        self.from_index: int = from_index
        self.to_index: int = to_index




