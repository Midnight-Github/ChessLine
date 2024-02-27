import customtkinter as ctk
import tkinter as tk
from chess.BoardState import BoardState

board = BoardState()

class Chess:
    def __init__(self, board_frame, name=('', ''), timer=(600, 600)):
        self.board_frame = board_frame
        self.name = (name[0] + " (White)", name[1] + " (Black)")
        self.timer = (tk.StringVar(value=self.formatTime(timer[0])), tk.StringVar(value=self.formatTime(timer[1])))

        self.board_frame.grid_rowconfigure(1, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)

        self.black_ui = ctk.CTkFrame(self.board_frame)
        self.black_ui.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.black_ui.grid_columnconfigure(1, weight=1)
        self.setUpBlackUi()

        self.board_canvas = ctk.CTkCanvas(self.board_frame)
        self.board_canvas.bind("<ButtonPress-1>", self.boardPressEvent)
        self.board_canvas.grid(row=1, column=0, padx=10)

        self.white_ui = ctk.CTkFrame(self.board_frame)
        self.white_ui.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
        self.white_ui.grid_columnconfigure(1, weight=1)
        self.setUpWhiteUi()

        self.turn = True
        self.preview = False

    def formatTime(self, t):
        insert_0 = lambda t: t if len(t) == 2 else '0' + t
        mins = str(t//60)
        secs = str(t%6)
        return f"{insert_0(mins)}:{insert_0(secs)}"

    def setUpBlackUi(self):
        self.black_name_label = ctk.CTkLabel(self.black_ui, text=self.name[1])
        self.black_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.black_timer_label = ctk.CTkLabel(self.black_ui, textvariable=self.timer[1])
        self.black_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def setUpWhiteUi(self):
        self.white_name_label = ctk.CTkLabel(self.white_ui, text=self.name[0])
        self.white_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.white_timer_label = ctk.CTkLabel(self.white_ui, textvariable=self.timer[0])
        self.white_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def getBoardSize(self):
        return min(self.board_frame.winfo_height() - self.black_ui.winfo_height() - self.white_ui.winfo_height() - 60, self.board_frame.winfo_width() - 20)

    def boardPressEvent(self, e):
        pass

    def drawBoard(self, size):
        box_colors = ("white", "gray25") # add settings to change color at index 1
        box_size = (size)/8
        for y in range(8):
            for x in range(8):
                self.board_canvas.create_rectangle( 
                    x*box_size, 
                    y*box_size, 
                    x*box_size + box_size, 
                    y*box_size + box_size,
                    fill=box_colors[(y+x)%2]
                )
                if x == 0:
                    self.board_canvas.create_text(  
                        x*box_size + box_size/7, 
                        y*box_size + box_size/7, 
                        text=str(8 - y), 
                        font=ctk.CTkFont(size=abs(int(box_size//5)), 
                        weight="bold")
                    )

                if y == 7:
                    self.board_canvas.create_text( 
                        x*box_size + (box_size - box_size/7), 
                        y*box_size + (box_size - box_size/7), 
                        text=chr(65 + x), 
                        font=ctk.CTkFont(size=abs(int(box_size//5)), 
                        weight="bold")
                    )
                

    def updateGame(self):
        self.board_canvas.delete("all")
        size = self.getBoardSize()
        self.board_canvas.configure(height=size, width=size)

        self.drawBoard(size)
        