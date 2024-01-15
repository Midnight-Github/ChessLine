import tkinter as tk
import customtkinter as ctk
from ui.settings import Settings
from ui.home import Home
# from ui.settings import Settings

# display rank

# find match -> login
# settings
# exit

class Menu(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0)

        self.menu_label = ctk.CTkLabel(
            self, 
            text="Menu", 
            font=ctk.CTkFont(size=20)
        )
        self.menu_label.grid(row=0, column=0, pady=10)

        self.buttons = {
            "home": self.makeButton(text="Home", row=1, command=lambda: root.showFrame(Home)),
            "settings": self.makeButton(text="Settings", row=2, command=lambda: root.showFrame(Settings))
        }

    def makeButton(self, text, row, command=None, width=80, pady=10, padx=10):
        button = ctk.CTkButton(
            self, 
            text=text,
            width=width,
            command=command
        )
        button.grid(row=row, column=0, pady=pady, padx=padx)
        return button