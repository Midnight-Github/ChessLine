import customtkinter as ctk
from ui.structure import MainPage

class Home(MainPage):
    def __init__(self, root):
        super().__init__(root, heading="Home")