import customtkinter as ctk
from ui.settings import Configuration

class OfflineNewGame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")
        self.root = root

        board_size = Configuration().game_config["board_size"]

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        board = ctk.CTkCanvas(self, height=board_size, width=board_size)
        board.grid(row=0, column=0)

        side_bar = ctk.CTkFrame(self)
        side_bar.grid(row=0, column=1, sticky="news")

        quit_button = ctk.CTkButton(side_bar, text="Quit", command=self.quitFrame)
        quit_button.grid(row=0, column=0)
    
    def quitFrame(self): #add confirmation box
        self.root.deleteFrame("OfflineNewGame")
        # self.root.initFrame("OfflineNewGame")
        self.root.showFrame("Home")
