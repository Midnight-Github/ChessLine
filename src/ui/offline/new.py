import customtkinter as ctk

class OfflineNewGame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        board = ctk.CTkCanvas(self, height=700, width=700)
        board.grid(row=0, column=0)
        

        side_bar = ctk.CTkFrame(self)
        side_bar.grid(row=0, column=1, sticky="news")
