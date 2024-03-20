class Check(Exception):
    pass

class Stalemate(Exception):
    pass

class KingNotFound(Exception):
    pass

class InvalidMove(Exception): 
    pass

class Checkmate(Exception):
    def __init__(self, col: str) -> None:
        super().__init__(col)