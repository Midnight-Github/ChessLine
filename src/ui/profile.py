import customtkinter as ctk
from framework.MainPage import MainPage

class Profile(MainPage):
    def __init__(self, root) -> None:
        super().__init__(root, heading="Profile")

