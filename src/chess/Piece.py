class Piece:
    def __init__(self, name: str, col: str, moved: bool=False, moved_again: bool=False) -> None:
        self.name = name
        self.col = col
        self.moved = moved
        self.moved_again = moved_again