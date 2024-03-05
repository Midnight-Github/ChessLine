import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from chess.Chess import Chess

class OfflineNewGame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.side_bar = ctk.CTkTabview(self)
        self.side_bar.add("Game")
        self.side_bar.add("History")
        self.side_bar.grid(row=0, column=1, padx=(0, 10), pady=(0, 10), sticky="news")
        self.side_bar.tab("Game").grid_columnconfigure(0, weight=1)

        self.quit_button = ctk.CTkButton(self.side_bar.tab("Game"), text="Quit", command=self.quitFrame)
        self.quit_button.grid(row=0, column=0, padx=(10, 0), sticky="nesw")

        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.grid(row=0, column=0, sticky="nesw")
        self.board_frame.bind("<Configure>", lambda e: self.updateBoard())

        self.chess = Chess(self.board_frame, self.root.update_idletasks)
    
    def quitFrame(self):
        warning_popup = CTkMessagebox(title="Quit", message="Do you want to quit?",
                        icon="question", option_1="No", option_2="Yes")

        if warning_popup.get() == "Yes":
            self.root.setActivePage("Home", "Home")
            self.root.deleteFrame("OfflineNewGame")
            self.root.showFrame("Home")

    def updateBoard(self):
        self.chess.updateGame()