import customtkinter as ctk
import tkinter as tk
from chess.BoardState import BoardState
from math import floor
from reader.Toml import configurator
from reader.Image import Image
from PIL import ImageTk

class Chess:
    def __init__(self, board_frame, update_root, name=('', ''), timer=(600, 600)):
        self.board_frame = board_frame
        self.update_root = update_root
        self.name = (name[0] + " (White)", name[1] + " (Black)")
        self.timer = (tk.StringVar(value=self.formatTime(timer[0])), tk.StringVar(value=self.formatTime(timer[1])))
        self.configurator = configurator
        self.board_state = BoardState()
        self.board = self.board_state.getBoard()
        self.chess_image = Image("\\..\\data\\chess_pieces.png")

        self.board_frame.grid_rowconfigure(1, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)

        self.black_ui = ctk.CTkFrame(self.board_frame)
        self.black_ui.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.black_ui.grid_columnconfigure(1, weight=1)
        self.setBlackUi()

        self.board_canvas = ctk.CTkCanvas(self.board_frame)
        self.board_canvas.bind("<ButtonPress-1>", self.boardPressEvent)
        self.board_canvas.grid(row=1, column=0, padx=10)

        self.white_ui = ctk.CTkFrame(self.board_frame)
        self.white_ui.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
        self.white_ui.grid_columnconfigure(1, weight=1)
        self.setWhiteUi()

        self.turn = True
        self.select = False
        self.preview_pos = list()

    def updateChessPieceImage(self):
        size = self.getBoardSize()
        gen_white = self.chess_image.generate(0, 0, 333.34, 333.5, 333.34, 0, 6, size/2800)
        gen_black = self.chess_image.generate(0, 333.5, 333.34, 333.5, 333.34, 0, 6, size/2800)

        chess_piece_image = {
            "WK": next(gen_white),
            "WQ": next(gen_white),
            "WB": next(gen_white),
            "WN": next(gen_white),
            "WR": next(gen_white),
            "WP": next(gen_white),

            "BK": next(gen_black),
            "BQ": next(gen_black),
            "BB": next(gen_black),
            "BN": next(gen_black),
            "BR": next(gen_black),
            "BP": next(gen_black),
        }

        self.chess_piece_image = chess_piece_image

    def formatTime(self, t):
        insert_0 = lambda t: t if len(t) == 2 else '0' + t
        mins = str(t//60)
        secs = str(t%6)
        return f"{insert_0(mins)}:{insert_0(secs)}"

    def setBlackUi(self):
        self.black_name_label = ctk.CTkLabel(self.black_ui, text=self.name[1])
        self.black_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.black_timer_label = ctk.CTkLabel(self.black_ui, textvariable=self.timer[1])
        self.black_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def setWhiteUi(self):
        self.white_name_label = ctk.CTkLabel(self.white_ui, text=self.name[0])
        self.white_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.white_timer_label = ctk.CTkLabel(self.white_ui, textvariable=self.timer[0])
        self.white_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def getBoardSize(self):
        self.update_root()
        return min(self.board_frame.winfo_height() - self.black_ui.winfo_height() - self.white_ui.winfo_height() - 60, 
                self.board_frame.winfo_width() - 20)

    def getPos(self, x, y):
        box_size = (self.getBoardSize())/8
        return floor((x + box_size)/box_size) - 1, floor((y + box_size)/box_size) - 1

    def getIndex(self, x, y):
        return (8*y + x)

    def animate(self):
        self.drawBoard()

    def boardPressEvent(self, e):
        x, y = self.getPos(e.x, e.y)
        index = self.getIndex(x, y)
        if self.select:
            try:
                self.board_state.push(self.select, index)
                self.board = self.board_state.getBoard()
            except Exception:
                self.select = index if self.board[index].name != 'E' else False
            else:
                # self.animate()
                self.select = False
        else:
            self.select = index if self.board[index].name != 'E' else False

        if self.select:
            self.preview_pos = self.board_state.preview(self.select)
            # self.board = self.board_state.getBoard()

        self.drawBoard()

    def drawBoard(self, face="white"):
        self.board_canvas.delete("all")           

        box_colors = ("white", self.configurator.config["board"]["color"])
        box_size = (self.getBoardSize())/8
        board_index = 0
        for y in range(8):
            for x in range(8):                    
                self.board_canvas.create_rectangle( 
                    x*box_size, 
                    y*box_size, 
                    x*box_size + box_size, 
                    y*box_size + box_size,
                    fill=box_colors[(x + y)%2],
                    width=1
                )

                if board_index in self.preview_pos:
                    self.board_canvas.create_oval( # Fix it
                        x*(box_size + box_size/10),
                        y*(box_size + box_size/10),
                        y*(box_size + box_size/10),
                        x*(box_size + box_size/10)
                    )

                if self.board[board_index].col != 'N':
                    piece = self.board[board_index].col + self.board[board_index].name
                    self.board_canvas.create_image(
                        x*box_size,
                        y*box_size,
                        anchor="nw",
                        image=self.chess_piece_image[piece]
                    )

                if x == 0:
                    self.board_canvas.create_text(  
                        x*box_size + box_size/12, 
                        y*box_size + box_size/8, 
                        text=str(8 - y), 
                        font=ctk.CTkFont(size=abs(int(box_size//6))),
                        fill=box_colors[(x + y + 1)%2]
                    )

                if y == 7:
                    self.board_canvas.create_text( 
                        x*box_size + (box_size - box_size/14), 
                        y*box_size + (box_size - box_size/9), 
                        text=chr(97 + x), 
                        font=ctk.CTkFont(size=abs(int(box_size//6))),
                        fill=box_colors[(x + y + 1)%2]
                    )
                board_index += 1

    def updateGame(self):
        size = self.getBoardSize()
        self.board_canvas.configure(height=size, width=size)
        self.updateChessPieceImage()
        self.drawBoard()
        