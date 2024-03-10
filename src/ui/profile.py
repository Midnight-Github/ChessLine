import customtkinter as ctk
from ui.MainPageStructure import MainPageStructure

class Profile(MainPageStructure):
    def __init__(self, root) -> None:
        super().__init__(root, heading="Profile")

