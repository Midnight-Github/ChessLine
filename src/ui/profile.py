import customtkinter as ctk
from framework.MenuPage import MenuPage

class Profile(MenuPage):
    def __init__(self, root) -> None:
        super().__init__(root, heading="Profile")

