import customtkinter as ctk
from framework.MenuPage import MenuPage

class Guide(MenuPage):
    def __init__(self, root) -> None:
        super().__init__(root, heading="Guide")