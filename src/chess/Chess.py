import customtkinter as ctk
import tkinter as tk
from chess.BoardState import BoardState

board = BoardState()

class Chess:
    def __init__(self, board_frame, name=('', ''), timer=(600, 600)):
        self.board_frame = board_frame
        self.name = (name[0] + " (White)", name[1] + " (Black)")
        self.timer = (tk.StringVar(value=self.__formatTime(timer[0])), tk.StringVar(value=self.__formatTime(timer[1])))

        self.board_frame.grid_rowconfigure(1, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)

        self.black_ui = ctk.CTkFrame(self.board_frame)
        self.black_ui.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.black_ui.grid_columnconfigure(1, weight=1)
        self.__setUpBlackUi()

        self.board_canvas = ctk.CTkCanvas(self.board_frame)
        self.board_canvas.grid(row=1, column=0, padx=10)

        self.white_ui = ctk.CTkFrame(self.board_frame)
        self.white_ui.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
        self.white_ui.grid_columnconfigure(1, weight=1)
        self.__setUpWhiteUi()

        self.turn = True
        self.preview = False

    def __formatTime(self, t):
        insert_0 = lambda t: t if len(t) == 2 else '0' + t
        mins = str(t//60)
        secs = str(t%6)
        return f"{insert_0(mins)}:{insert_0(secs)}"

    def __setUpBlackUi(self):
        self.black_name_label = ctk.CTkLabel(self.black_ui, text=self.name[1])
        self.black_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.black_timer_label = ctk.CTkLabel(self.black_ui, textvariable=self.timer[1])
        self.black_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def __setUpWhiteUi(self):
        self.white_name_label = ctk.CTkLabel(self.white_ui, text=self.name[0])
        self.white_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.white_timer_label = ctk.CTkLabel(self.white_ui, textvariable=self.timer[0])
        self.white_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def __getBoardSize(self):
        return min(self.board_frame.winfo_height() - self.black_ui.winfo_height() - self.white_ui.winfo_height() - 60, self.board_frame.winfo_width() - 20)

    def updateGame(self):
        size = self.__getBoardSize()
        self.board_canvas.configure(height=size, width=size)