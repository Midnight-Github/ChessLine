class OpponentsPiece(Exception):
    pass

class OpponentPreview(Exception):
    pass

class EmptyBox(Exception):
    pass

class CaptureOwnPiece(Exception):
    pass

class Check(Exception):
    pass

class UnNamedFile(Exception):
    pass

class InvalidPromotionInput(Exception):
    pass

class Stalemate(Exception):
    pass

class KingNotFound(Exception):
    pass

class TimeOut(Exception):
    def __init__(self, col: str) -> None:
        super().__init__(col)

class InvalidMove(Exception): 
    def __init__(self, piece: str) -> None:
        super().__init__(piece)

class Checkmate(Exception):
    def __init__(self, col: str) -> None:
        super().__init__(col)