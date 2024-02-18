class Piece:
    def __init__(self, name, col, moved=False, moved_again=False):
        self.name = name
        self.col = col
        self.moved = moved
        self.moved_again = moved_again