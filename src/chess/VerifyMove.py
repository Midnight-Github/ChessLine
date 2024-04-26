from chess.Errors import *

class VerifyMove:
    def __init__(self, board: list) -> None:
        self.board = board

    def __pawn(self, pos: int, col: str) -> list:
        moves = list()
        if col == 'W':
            if 0 <= pos - 8 <= 63:
                if self.board[pos - 8].col == 'N': 
                    moves.append(pos - 8)
                
            if 0 <= pos - 8*2 <= 63 and 48 <= pos <= 55:
                if self.board[pos - 8*2].col == 'N' and self.board[pos - 8].col == 'N': 
                    moves.append(pos - 8*2)

            if 0 <= pos - (8 + 1) <= 63 and pos%8 != 0:
                if self.board[pos - (8 + 1)].col not in (col + 'N'): 
                    moves.append(pos - (8 + 1)) # right kill

            if 0 <= pos - (8 - 1) <= 63 and pos%8 != 7:
                if self.board[pos - (8 - 1)].col not in (col + 'N'): 
                    moves.append(pos - (8 - 1)) # left kill

        elif col == 'B':
            if 0 <= pos + 8 <= 63:
                if self.board[pos + 8].col == 'N': 
                    moves.append(pos + 8)
                
            if 0 <= pos + 8*2 <= 63 and 8 <= pos <= 15:
                if self.board[pos + 8*2].col == 'N' and self.board[pos + 8].col == 'N': 
                    moves.append(pos + 8*2)

            if 0 <= pos + (8 + 1) <= 63 and pos%8 != 7:
                if self.board[pos + (8 + 1)].col not in (col + 'N'): 
                    moves.append(pos + (8 + 1)) # left kill

            if 0 <= pos + (8 - 1) <= 63 and pos%8 != 0:
                if self.board[pos + (8 - 1)].col not in (col + 'N'): 
                    moves.append(pos + (8 - 1)) # right kill

        return moves
        
    def __rook(self, pos: int, col: str) -> list:
        moves = list()
        xBounds = lambda x: (0 <= x <= 63) and (pos//8 != x//8)
        yBounds = lambda x: (0 <= x <= 63) and (pos//8 == x//8)

        i = 1 #up
        while xBounds(pos - 8*i) and self.board[pos - 8*i].col != col:
            moves.append(pos - 8*i)
            if self.board[pos - 8*i].col != 'N': break
            i += 1

        i = 1 #down
        while xBounds(pos + 8*i) and self.board[pos + 8*i].col != col:
            moves.append(pos + 8*i)
            if self.board[pos + 8*i].col != 'N': break
            i += 1

        i = 1 #right
        while yBounds(pos + i) and self.board[pos + i].col != col:
            moves.append(pos + i)
            if self.board[pos + i].col != 'N': break
            i += 1
            
        i = 1 #left
        while yBounds(pos - i) and self.board[pos - i].col != col:
            moves.append(pos - i)
            if self.board[pos - i].col != 'N': break
            i += 1
            
        return moves

    def __knight(self, pos: int, col: str) -> list:
        moves = list()
        s = lambda x: abs(pos//8 - x//8) <= 2 and abs(pos%8 - x%8) <= 2

        possible_pos = [
            pos - (8*2 + 1), # extreme top left
            pos - (8*2 - 1), # extreme top right
            pos - (8 + 2),   # top left
            pos - (8 - 2),   # top right
            pos + (8 + 2),   # bottom left
            pos + (8 - 2),   # bottom right
            pos + (8*2 + 1), # extreme bottom left
            pos + (8*2 - 1)  # extreme bottom right
        ]

        for i in possible_pos:
            if (0 <= i <= 63) and self.board[i].col != col and s(i):
                moves.append(i)

        return moves

    def __bishop(self, pos: int, col: str) -> list:
        moves = list()
        bounds = lambda x: (0 <= x <= 63) and abs(pos//8 - x//8) == abs(pos%8 - x%8)

        i = 1 #top-left
        while bounds(pos - (8*i + i)) and self.board[pos - (8*i + i)].col != col:
            moves.append(pos - (8*i + i))
            if self.board[pos - (8*i + i)].col != 'N': break
            i += 1

        i = 1 #top-right
        while bounds(pos - (8*i - i)) and self.board[pos - (8*i - i)].col != col:
            moves.append(pos - (8*i - i))
            if self.board[pos - (8*i - i)].col != 'N': break
            i += 1

        i = 1 #bottom-left
        while bounds(pos + (8*i - i)) and self.board[pos + (8*i - i)].col != col:
            moves.append(pos + (8*i - i))
            if self.board[pos + (8*i - i)].col != 'N': break
            i += 1

        i = 1 #bottom-right
        while bounds(pos + (8*i + i)) and self.board[pos + (8*i + i)].col != col:
            moves.append(pos + (8*i + i))
            if self.board[pos + (8*i + i)].col != 'N': break
            i += 1

        return moves

    def __queen(self, pos: int, col: str) -> list:
        return (self.__rook(pos, col) + self.__bishop(pos, col))

    def __king(self, pos: int, col: str) -> list:
        moves = list()
        check = lambda x: (0 <= x <= 63) and (abs(pos//8 - x//8) <= 1 and abs(pos%8 - x%8) <= 1)
        possible_pos = [
            pos + (8 - 1),
            pos + (8),
            pos + (8 + 1),
            pos - 1,
            pos + 1,
            pos - (8 - 1),
            pos - (8),
            pos - (8 + 1)
        ]
        for i in possible_pos:
            if check(i) and self.board[i].col != col:
                moves.append(i)
        
        return moves

    def __promotion(self) -> bool:
        if self.end_pos not in self.__pawn(self.start_pos, self.col): 
            return False

        offset = 0 if self.board[self.start_pos].col == 'W' else 56
        return offset + 0 <= self.end_pos <= offset + 7

    def __castling(self, pos: int, col: str) -> list:
        #(rook, end_pos, start_pos/king_pos, col)
        possible_pos = [(0, 2, 4, 'B'), (7, 6, 4, 'B'), (56, 58, 60, 'W'), (63, 62, 60, 'W')]
        moves = list()
        if self.board[pos].name != 'K' or self.board[pos].moved or self.board[pos].col != col: 
            return []

        for rook_pos, end_pos, start_pos, col in possible_pos:
            if pos != start_pos:
                continue
            elif self.board[rook_pos].name != 'R' or self.board[rook_pos].col != col or self.board[rook_pos].moved:
                continue

            for i in range(start:=(min(start_pos, rook_pos)), end:=(max(start_pos, rook_pos) + 1)):
                if self.check(i, col):
                    break
                elif start < i < end - 1 and self.board[i].col != 'N':
                    break
            else:
                moves.append(end_pos)
        return moves

    def __enpassant(self, pos: int, col: str, prev_end_pos: int) -> list: # fix it
        if not(24 <= pos <= 31 or 32 <= pos <= 39):
            return []

        if col == 'W':
            possible_pos = [
                pos - 8 - 1,
                pos - 8 + 1
            ]
            for i in possible_pos:
                kill_pos = i + 8

                if self.board[kill_pos].name != 'P':
                    continue

                if self.board[kill_pos].moved_again or prev_end_pos != kill_pos:
                    continue

                return [i]

        elif col == 'B':
            possible_pos = [
                pos + 8 - 1, 
                pos + 8 + 1
            ]
            for i in possible_pos:
                kill_pos = i - 8

                if self.board[kill_pos].name != 'P':
                    continue

                if self.board[kill_pos].moved_again or prev_end_pos != kill_pos:
                    continue

                return [i]
        return []

    def check(self, pos: int, col: str) -> bool:
        for i in self.__knight(pos, ''):
            if self.board[i].name == 'N' and self.board[i].col != col:
                return True

        for i in self.__rook(pos, ''):
            if self.board[i].name in 'QR' and self.board[i].col != col:
                return True

        for i in self.__bishop(pos, ''):
            if self.board[i].name in 'QB' and self.board[i].col != col:
                return True

        for i in self.__king(pos, ''):
            if self.board[i].name in 'K' and self.board[i].col != col:
                return True

        s = lambda x: abs(pos//8 - x//8) <= 1 and abs(pos%8 - x%8) <= 1
        if col == 'B':
            if s(pos + (8 - 1)) and self.board[pos + (8 - 1)].name == 'P' and self.board[pos + (8 - 1)].col == 'W': 
                return True
            elif s(pos + (8 + 1)) and self.board[pos + (8 + 1)].name == 'P' and self.board[pos + (8 + 1)].col == 'W': 
                return True
        elif col == 'W':
            if s(pos - (8 - 1)) and self.board[pos - (8 - 1)].name == 'P' and self.board[pos - (8 - 1)].col == 'B': 
                return True
            elif s(pos - (8 + 1)) and self.board[pos - (8 + 1)].name == 'P' and self.board[pos - (8 + 1)].col == 'B': 
                return True
        
        return False

    def getKingThreats(self, pos: int, col: str) -> list:
        threat_pos = list()
        for i in self.__knight(pos, ''):
            if self.board[i].name == 'N' and self.board[i].col != col:
                threat_pos.append(i)

        for i in self.__rook(pos, ''):
            if self.board[i].name in 'QR' and self.board[i].col != col:
                threat_pos.append(i)

        for i in self.__bishop(pos, ''):
            if self.board[i].name in 'QB' and self.board[i].col != col:
                threat_pos.append(i)

        for i in self.__king(pos, ''):
            if self.board[i].name in 'K' and self.board[i].col != col:
                threat_pos.append(i)

        s = lambda x: abs(pos//8 - x//8) <= 1 and abs(pos%8 - x%8) <= 1
        if col == 'B':
            if s(pos + (8 - 1)) and self.board[pos + (8 - 1)].name == 'P' and self.board[pos + (8 - 1)].col == 'W': 
                threat_pos.append(pos + (8 - 1))
            elif s(pos + (8 + 1)) and self.board[pos + (8 + 1)].name == 'P' and self.board[pos + (8 + 1)].col == 'W': 
                threat_pos.append(pos + (8 + 1))
        elif col == 'W':
            if s(pos - (8 - 1)) and self.board[pos - (8 - 1)].name == 'P' and self.board[pos - (8 - 1)].col == 'B': 
                threat_pos.append(pos - (8 - 1))
            elif s(pos - (8 + 1)) and self.board[pos - (8 + 1)].name == 'P' and self.board[pos - (8 + 1)].col == 'B': 
                threat_pos.append(pos - (8 + 1))
        
        return threat_pos

    def __primaryValidation(self) -> bool:
        if self.name == 'P':
            if self.end_pos not in self.__pawn(self.start_pos, self.col): 
                raise InvalidMove

        elif self.name == 'R': 
            if self.end_pos not in self.__rook(self.start_pos, self.col): 
                raise InvalidMove
        
        elif self.name == 'N':
            if self.end_pos not in self.__knight(self.start_pos, self.col): 
                raise InvalidMove

        elif self.name == 'B':
            if self.end_pos not in self.__bishop(self.start_pos, self.col): 
                raise InvalidMove

        elif self.name == 'Q':
            if self.end_pos not in self.__queen(self.start_pos, self.col): 
                raise InvalidMove

        elif self.name == 'K':
            if self.end_pos not in self.__king(self.start_pos, self.col): 
                raise InvalidMove

        elif self.name == 'Z':
            if self.end_pos not in self.__king(self.start_pos, self.col) + self.__knight(self.start_pos, self.col): 
                raise InvalidMove

        else: 
            raise Exception("Invalid piece name:", self.name)

        return True
                
    def validate(self, start_pos: int, end_pos: int, prev_end_pos: int | None=None) -> bool | str:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.col = self.board[start_pos].col
        self.name = self.board[start_pos].name
        
        dx = self.end_pos%8 - self.start_pos%8

        complex_move = False
        if self.name == 'P':
            if self.__promotion(): 
                complex_move = "promotion"
            elif isinstance(prev_end_pos, int) and end_pos in self.__enpassant(start_pos, self.col, prev_end_pos): 
                complex_move = "enpassant"

        elif self.name == 'K' and abs(dx) == 2:
            if end_pos in self.__castling(start_pos, self.col): 
                complex_move = "castling"
        
        if complex_move: 
            return complex_move

        return self.__primaryValidation()
    
    def getPossibleMoves(self, pos: int, prev_end_pos: int | None=None) -> list: 
        name = self.board[pos].name
        col = self.board[pos].col

        match(name):
            case 'P':
                if isinstance(prev_end_pos, int):
                    return self.__pawn(pos, col) + self.__enpassant(pos, col, prev_end_pos)
                else:
                    return self.__pawn(pos, col)
            case 'R': 
                return self.__rook(pos, col)
            case 'N': 
                return self.__knight(pos, col)
            case 'B': 
                return self.__bishop(pos, col)
            case 'Q': 
                return self.__queen(pos, col)
            case 'K': 
                return self.__king(pos, col) + self.__castling(pos, col)
            case 'Z': 
                return self.__queen(pos, col) + self.__knight(pos, col)
            case _:
                raise ValueError("Unsupported piece found:", name)