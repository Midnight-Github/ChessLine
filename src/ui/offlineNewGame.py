import customtkinter as ctk
from chess.Chess import Chess

class OfflineNewGame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.side_bar = ctk.CTkFrame(self)
        self.side_bar.grid(row=0, column=1, sticky="news")

        self.quit_button = ctk.CTkButton(self.side_bar, text="Quit", command=self.quitFrame)
        self.quit_button.grid(row=0, column=0)

        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.grid(row=0, column=0, sticky="nesw")
        self.board_frame.bind("<Configure>", self.updateBoard)

        self.chess = Chess(self.board_frame, *self.mainFrameSize())
    
    def quitFrame(self): #add confirmation box
        self.root.setActivePage("Home", "Home")
        self.root.deleteFrame("OfflineNewGame")
        self.root.showFrame("Home")
    
    def mainFrameSize(self):
        return (self.winfo_height(), abs(self.winfo_width() - self.side_bar.winfo_width()))

    def updateBoard(self, e):
        self.chess.update(*self.mainFrameSize())
        
