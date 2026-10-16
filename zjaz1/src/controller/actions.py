
class GameAction:
    pass

class GameStartAction(GameAction):
    pass

class PlayerPlacePawnAction(GameAction):
    def __init__(self, at_index: int):
        self.at_index: int = at_index

class PlayerMovePawnAction(GameAction):
    def __init__(self,from_index: int, to_index: int ):
        self.from_index: int = from_index
        self.to_index: int = to_index

class PlayerRemovePawnAction(GameAction):
    def __init__(self, at_index: int):
        self.at_index: int = at_index
