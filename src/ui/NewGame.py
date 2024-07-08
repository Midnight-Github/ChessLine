import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from chess.Chess import Chess
import tkinter as tk

class NewGame(ctk.CTkFrame):
    def __init__(self, root) -> None:
        super().__init__(root, fg_color="transparent")
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.side_bar = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.side_bar.grid(row=0, column=1, sticky="news")
        self.side_bar.grid_rowconfigure(1, weight=1)

        self.board_frame = ctk.CTkFrame(self, corner_radius=0)
        self.board_frame.grid(row=0, column=0, sticky="nesw")
        self.board_frame.bind("<Configure>", lambda e: self.chess.updateGame())

        self.setUpMoveHistory()

        self.chess = Chess(self.board_frame, self.root.update_idletasks, move_history=self.moves)

        self.quit_button = ctk.CTkButton(self.side_bar, text="Quit", width=30, command=self.quitFrame)
        self.quit_button.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nesw")

        self.refresh_button = ctk.CTkButton(self.side_bar, text="Refresh", width=30, command=self.chess.updateGame)
        self.refresh_button.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="nesw")

        self.pause_button = ctk.CTkButton(self.side_bar, text="Pause", width=30, command=self.togglePause)
        self.pause_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="nesw")

    def setUpMoveHistory(self):
        self.moves_frame = ctk.CTkFrame(self.side_bar)
        self.moves_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nesw")
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
            self.root.deleteFrame("NewGame")
            self.root.showFrame("Home")

    def togglePause(self) -> None:
        if self.chess.paused:
            self.chess.unpause()
            self.pause_button.configure(text="Pause")
        else:
            self.chess.pause()
            self.pause_button.configure(text="Unpause")