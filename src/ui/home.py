import tkinter as tk
from typing import Callable
import customtkinter as ctk
from framework.MainPage import MainPage

class Home(MainPage):
    def __init__(self, root) -> None:
        super().__init__(root, heading="Home")
        self.root = root

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        self.offlineGame()

    def offlineGame(self) -> None:
        def makeOfflineButton(text: str, row: int, command: Callable | None=None) -> None:
            b = ctk.CTkButton(self.offline_button_frame, corner_radius=20, text=text, font=ctk.CTkFont(size=15), width=200, command=command)
            b.grid(row=row, column=0, pady=(0, 10))

        def launch(frame: str) -> None:
            self.root.setActivePage("Home", frame)
            self.root.initFrame(frame)
            self.root.showFrame("Home")

        self.offline_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.offline_frame.grid(row=1, column=0, sticky="news")

        self.offline_button_frame = ctk.CTkFrame(self.offline_frame, fg_color="transparent")
        self.offline_button_frame.place(relx=0.5, rely=0.5, anchor="center")

        makeOfflineButton(text="New Game", row=0, command=lambda : launch("NewGame"))
        makeOfflineButton(text="Open Game", row=1, command=lambda : launch("OpenGame"))

    def updatePage(self) -> None:
        pass
