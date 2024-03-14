from typing import Callable
import customtkinter as ctk
import tkinter as tk
from chess.BoardState import BoardState
from math import floor
from reader.Toml import configurator
from reader.Image import Image
import time

class Chess:
    def __init__(self, board_frame, update_root: Callable, face: str='w', name: tuple[str, str]=('', ''), 
        timer: tuple[int, int]=(600, 600), animation_speed: int=1) -> None:

        self.board_frame = board_frame
        self.update_root = update_root
        self.face = face
        self.name = (name[0] + " (White)", name[1] + " (Black)")
        self.timer = (tk.StringVar(value=self.formatTime(timer[0])), tk.StringVar(value=self.formatTime(timer[1])))
        self.animation_speed = animation_speed
        
        self.configurator = configurator
        self.board_state = BoardState()
        self.board = self.board_state.getBoard()
        self.chess_image = Image(r"\..\data\chess_pieces.png")
        self.canvas_piece = dict.fromkeys(range(0, 64))

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

        self.select = False
        self.preview_pos = list()

    def updateChessPieceImage(self) -> None:
        size = self.getBoardSize()

        gen_white = self.chess_image.generate(0, 0, 333, 333, 333, 0, 6, size/3100)
        gen_black = self.chess_image.generate(0, 333, 333, 333, 333, 0, 6, size/3100)

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

    def formatTime(self, t: int) -> str:
        insert_0 = lambda t: t if len(t) == 2 else '0' + t
        mins = str(t//60)
        secs = str(t%6)
        return f"{insert_0(mins)}:{insert_0(secs)}"

    def setBlackUi(self) -> None:
        self.black_name_label = ctk.CTkLabel(self.black_ui, text=self.name[1])
        self.black_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.black_timer_label = ctk.CTkLabel(self.black_ui, textvariable=self.timer[1])
        self.black_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def setWhiteUi(self) -> None:
        self.white_name_label = ctk.CTkLabel(self.white_ui, text=self.name[0])
        self.white_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.white_timer_label = ctk.CTkLabel(self.white_ui, textvariable=self.timer[0])
        self.white_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def getBoardSize(self) -> float:
        self.update_root()
        return min(self.board_frame.winfo_height() - self.black_ui.winfo_height() - self.white_ui.winfo_height() - 60, 
            self.board_frame.winfo_width() - 20)

    def getPos(self, x: float, y: float) -> tuple[int, int]:
        box_size = (self.getBoardSize())/8
        return (floor((x + box_size)/box_size) - 1, floor((y + box_size)/box_size) - 1)

    def getIndex(self, x: int, y: int) -> int:
        return (8*y + x)

    def animate(self, initial: int, final: int) -> None:
        if initial == final:
            return
        # self.board_canvas.move(self.canvas_piece[0], 60, 0)
        # print(initial, final)
        # print(type(self.canvas_piece[0]))
        # time.sleep(5)
        # self.board_canvas.move(initial - 60, final)
        # self.board_canvas.after(50, self.animate(initial - self.animation_speed, final))
    
    def getTurn(self) -> str:
        return 'W' if self.board_state.turn else 'B'

    def boardPressEvent(self, e) -> None:
        x, y = self.getPos(e.x, e.y)
        index = self.getIndex(x, y)
        piece_drawable = False
        preview_drawable = False

        if self.select is not False:
            turn = self.getTurn()                
            try:
                self.board_state.push(self.select, index)
            except Exception:
                self.select = index if self.board[index].name not in ('E', turn) else False
            else:
                self.animate(self.select, index)
                piece_drawable = True
                self.select = False
            self.board = self.board_state.getBoard()
        else:
            self.select = index if self.board[index].name != 'E' else False

        if self.select is not False:
            self.preview_pos = self.board_state.preview(self.select)
            if self.preview_pos:
                preview_drawable = True

        self.clearCanvas('preview')
        
        fxns = list()
        if piece_drawable:
            fxns.append(self.drawPieces)

        if preview_drawable:
            fxns.append(self.drawPreview)

        if fxns:
            self.draw(*fxns)

    def draw(self, *fxns: Callable) -> None:
        box_colors = ("white", self.configurator.config["board"]["color"])
        box_size = (self.getBoardSize())/8
        board_index = 0
        for y in range(8):
            for x in range(8):
                for i in fxns:
                    i(x=x, y=y, box_colors=box_colors, box_size=box_size, board_index=board_index)
                board_index += 1

    def clearCanvas(self, tag: str="all") -> None:
        self.board_canvas.delete(tag)

    def drawBoard(self, **kwargs) -> None:
        x = kwargs['x']
        y = kwargs['y']
        box_colors = kwargs["box_colors"]
        box_size = kwargs["box_size"]

        self.board_canvas.create_rectangle( 
            x*box_size, 
            y*box_size, 
            x*box_size + box_size, 
            y*box_size + box_size,
            fill=box_colors[(x + y)%2],
            width=1,
            tags="board"
        )

        if x == 0:
            self.board_canvas.create_text(  
                x*box_size + box_size/12, 
                y*box_size + box_size/8, 
                text=str(8 - y), 
                font=ctk.CTkFont(size=abs(int(box_size//6))),
                fill=box_colors[(x + y + 1)%2],
                tags="board"
            )

        if y == 7:
            self.board_canvas.create_text( 
                x*box_size + (box_size - box_size/14), 
                y*box_size + (box_size - box_size/9), 
                text=chr(97 + x), 
                font=ctk.CTkFont(size=abs(int(box_size//6))),
                fill=box_colors[(x + y + 1)%2],
                tags="board"
            )

    def drawPieces(self, **kwargs) -> None:
        x = kwargs['x']
        y = kwargs['y']
        box_size = kwargs["box_size"]
        board_index = kwargs["board_index"]

        if self.board[board_index].col == 'N':
            self.board_canvas.delete("#" + str(board_index))
            return
        
        piece_info = self.board[board_index].col + self.board[board_index].name
        if self.canvas_piece[board_index] != piece_info:
            self.board_canvas.delete("#" + str(board_index))
            self.board_canvas.create_image(
                x*box_size + box_size/14,
                y*box_size + box_size/14,
                anchor="nw",
                image=self.chess_piece_image[piece_info],
                tags=("#" + str(board_index), "piece")
            )
            self.canvas_piece[board_index] = piece_info

    def drawPreview(self, **kwargs) -> None:
        x = kwargs['x']
        y = kwargs['y']
        box_size = kwargs["box_size"]
        board_index = kwargs["board_index"]

        if self.select is False or board_index not in self.preview_pos:
            return
            
        if self.board[board_index].col == 'N':
            r = box_size/9
            self.board_canvas.create_oval(
                x*(box_size) + box_size/2 - r,
                y*(box_size) + box_size/2 - r,
                x*(box_size) + box_size/2 + r,
                y*(box_size) + box_size/2 + r,
                fill="#363636",
                tags="preview"
            )
        elif self.board[board_index].col == 'B' if self.board_state.turn else 'W':
            r = box_size/2.2
            self.board_canvas.create_oval(
                x*(box_size) + box_size/2 - r,
                y*(box_size) + box_size/2 - r,
                x*(box_size) + box_size/2 + r,
                y*(box_size) + box_size/2 + r,
                width=4,
                outline="#363636",
                tags="preview"
            )

    def updateGame(self) -> None:
        self.canvas_piece = dict.fromkeys(range(0, 64))
        size = self.getBoardSize()
        self.board_canvas.configure(height=size, width=size)
        self.updateChessPieceImage()
        self.clearCanvas()
        self.draw(self.drawBoard, self.drawPreview, self.drawPieces)
        