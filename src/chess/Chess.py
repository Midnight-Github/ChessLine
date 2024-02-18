import customtkinter as ctk
import tkinter as tk
from chess.BoardState import BoardState

board = BoardState()

class Chess:
    def __init__(self, name=('', ''), timer=(600, 600), turn=True):
        self.board_frame = board_frame
        self.name = (name[0] + "(White)", name[1] + "(Black)")
        self.timer = (tk.StringVar(value=self.__formatTime(timer[0])), tk.StringVar(value=self.__formatTime(timer[1])))

        size = self.__getBoardSize(height, width)


        self.turn = True
        self.preview = False

    def __formatTime(self, t):
        insert_0 = lambda t: t if len(t) == 2 else '0' + t
        mins = str(t//60)
        secs = str(t%6)
        return f"{insert_0(mins)}:{insert_0(secs)}"





    def __getBoardSize(self, height, width):
        return min(height - self.black_ui.winfo_height() - self.white_ui.winfo_height() - 60, width)

    def update(self, height, width):
        size = self.__getBoardSize(height, width)
        self.board_canvas.configure(height=size, width=size)