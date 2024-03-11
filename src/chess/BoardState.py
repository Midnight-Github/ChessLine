from chess.Errors import *
from chess.VerifyMove import VerifyMove
from chess.Piece import Piece
from copy import copy, deepcopy

class BoardState:
    def __init__(self) -> None:
        self.turn = True

        self.__board = [Piece('E', 'N')]*64
        self.__board[0] = Piece('R', 'B')
        self.__board[1] = Piece('N', 'B')
        self.__board[2] = Piece('B', 'B')
        self.__board[3] = Piece('Q', 'B')
        self.__board[4] = Piece('K', 'B')
        self.__board[5] = Piece('B', 'B')
        self.__board[6] = Piece('N', 'B')
        self.__board[7] = Piece('R', 'B')
        self.__board[63-0] = Piece('R', 'W')
        self.__board[63-1] = Piece('N', 'W')
        self.__board[63-2] = Piece('B', 'W')
        self.__board[63-3] = Piece('K', 'W')
        self.__board[63-4] = Piece('Q', 'W')
        self.__board[63-5] = Piece('B', 'W')
        self.__board[63-6] = Piece('N', 'W')
        self.__board[63-7] = Piece('R', 'W')

        for i in range(8,16):
            self.__board[i] = Piece('P', 'B')

        for i in range(48,56):
            self.__board[i] = Piece('P', 'W')

        for i in range(16,48):
            self.__board[i] = Piece('E', 'N')

        self.__move_history = ''
        self.__prev_end_pos = None
            
    def restart(self) -> None:
        self.__init__()

    def preview(self, pos: int) -> list:
        if self.__board[pos].col != ('W' if self.turn else 'B'): 
            return []

        return VerifyMove(self.__board).getPossibleMoves(pos, self.__prev_end_pos)

    def __move(self, start_pos: int, end_pos: int, move: str | None) -> None:
        if self.__board[start_pos].moved: 
            self.__board[start_pos].moved_again = True
        else: 
            self.__board[start_pos].moved = True

        self.__board[end_pos] = self.__board[start_pos]
        self.__board[start_pos] = Piece('E', 'N')

        if move != None: 
            self.__move_history += move+' '

    def commitMove(self, start_pos: int, end_pos: int, move: str | None) -> None:
        checkmove = VerifyMove(self.__board)
        col = self.__board[start_pos].col

        move_type = checkmove.validate(start_pos, end_pos, self.__prev_end_pos)          

        if move_type == "promotion":
            promo = input("Promote to: ").upper()
            if promo not in "QBNR": 
                raise InvalidPromotionInput

            self.__move(start_pos, end_pos, move)
            self.__board[end_pos].name = promo
            # self.__board[end_pos].val = 9 if promo == 'Q' else 5 if promo == 'R' else 3.3 if promo == 'B' else 3.2

        elif move_type == "enpassant":
            killpos = end_pos + (8 if col == 'W' else -8)
            self.__move(start_pos, end_pos, move)
            self.__board[killpos] = Piece('E', 'N')
            
        elif move_type == "castling":
            self.__move(start_pos, end_pos, move)
            match(end_pos):
                case 2:
                    rook_start_pos = 0
                    rook_end_pos = 3
                case 6:
                    rook_start_pos = 7
                    rook_end_pos = 5
                case 58:
                    rook_start_pos = 56
                    rook_end_pos = 59
                case 62:
                    rook_start_pos = 63
                    rook_end_pos = 61
                case _: 
                    raise Exception("Castling condition not met")

            self.__move(rook_start_pos, rook_end_pos, None)
        else:
            self.__move(start_pos, end_pos, move)

    def __getChessCoords(self, index: int) -> str:
        x = index%8
        y = index//8
        return chr(x + 97) + str(8 - y)
                
    def push(self, start_pos: int, end_pos: int) -> None:
        board_backup = deepcopy(self.__board)
        move_history_backup = copy(self.__move_history)
        col = self.__board[start_pos].col
        opp_col = 'B' if col == 'W' else 'W'

        is_same_colour =  self.__board[end_pos].col == col
        is_empty_space = col == 'N'
        is_correct_piece = (True if self.turn == (col == 'W') else False) if self.turn != None else (True)
        
        if is_empty_space: raise EmptyBox
        elif not is_correct_piece: raise OpponentsPiece
        elif is_same_colour: raise CaptureOwnPiece

        self.commitMove(start_pos, end_pos, self.__getChessCoords(start_pos) + self.__getChessCoords(end_pos))

        check_move = VerifyMove(self.__board)
        if check_move.check(self.__getKingPos(col), col): # self check
            self.__board = board_backup
            self.__move_history = move_history_backup
            raise Check

        if check_move.check(self.__getKingPos(opp_col), opp_col):
            if self.__stalemate(opp_col):
                raise Checkmate('White' if col == 'W' else 'Black')

        if self.__stalemate(opp_col):
            raise Stalemate

        self.__prev_end_pos = end_pos
        self.turn = not self.turn

    def __getKingPos(self, col: str) -> int:
        for i in range(64):
            if self.__board[i].name == 'K':
                if self.__board[i].col == (col):
                    return i
        raise KingNotFound

    def __stalemate(self, col: str) -> bool:
        king_pos = self.__getKingPos(col)
        original_board = deepcopy(self.__board)
        vm = VerifyMove(original_board)
        for i in range(64):
            move_king = False
            if self.__board[i].col != col:
                continue
            if self.__board[i].name == 'K':
                move_king = True
            for pos in vm.getPossibleMoves(i, self.__prev_end_pos):
                self.commitMove(i, pos, None)
                if not VerifyMove(self.__board).check(pos if move_king else king_pos, col):
                    self.__board = deepcopy(original_board)
                    return False
                self.__board = deepcopy(original_board)
        return True
                    
    def getMoveHistory(self) -> str:
        return self.__move_history

    def loadGame(self, move_history: str) -> None:
        self.__move_history = move_history

    def getBoard(self) -> list:
        return self.__board

    def setBoard(self, board: list) -> None:
        for i in range(64):
            self.__board[i] = Piece(*board[i])

    def getPrevEndPos(self) -> int | None:
        return self.__prev_end_pos

    def setPrevEndPos(self, prev_end_pos: int | None) -> None:
        self.__prev_end_pos = prev_end_pos
