import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from chess.Chess import Chess
import tkinter as tk

class OfflineNewGame(ctk.CTkFrame):
    def __init__(self, root) -> None:
        super().__init__(root, fg_color="transparent")
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.side_bar = ctk.CTkFrame(self, corner_radius=0)
        self.side_bar.grid(row=0, column=1, sticky="news")
        self.side_bar.grid_rowconfigure(1, weight=1)

        self.quit_button = ctk.CTkButton(self.side_bar, text="Quit", command=self.quitFrame)
        self.quit_button.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nesw")

        self.refresh_button = ctk.CTkButton(self.side_bar, text="Refresh", command=self.updateBoard)
        self.refresh_button.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="nesw")

        self.setUpMoveHistory()

        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.grid(row=0, column=0, sticky="nesw")
        self.board_frame.bind("<Configure>", lambda e: self.updateBoard())

        self.chess = Chess(self.board_frame, self.root.update_idletasks, move_history=self.moves)

    def setUpMoveHistory(self):
        self.moves_frame = ctk.CTkFrame(self.side_bar)
        self.moves_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nesw")
        self.moves_frame.grid_rowconfigure(1, weight=1)
        self.moves_frame.grid_columnconfigure(0, weight=1)

        self.moves = tk.StringVar()

        self.moves_label = ctk.CTkLabel(self.moves_frame, text="Moves", font=ctk.CTkFont(size=20))
        self.moves_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nesw")

        self.moves_entry_frame = ctk.CTkScrollableFrame(self.moves_frame)
        self.moves_entry_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nesw")
        self.moves_entry_frame.grid_rowconfigure(0, weight=1)
        self.moves_entry_frame.grid_columnconfigure(0, weight=1)

        self.moves_entry_label = ctk.CTkLabel(self.moves_entry_frame, textvariable=self.moves, font=ctk.CTkFont(size=15))
        self.moves_entry_label.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
    
    def quitFrame(self) -> None:
        warning_popup = CTkMessagebox(title="Quit", message="Do you want to quit?",
                        icon="question", option_1="No", option_2="Yes")

        if warning_popup.get() == "Yes":
            self.chess.terminateGame()
            self.root.setActivePage("Home", "Home")
            self.root.deleteFrame("OfflineNewGame")
            self.root.showFrame("Home")

    def updateBoard(self) -> None:
        self.chess.updateGame()