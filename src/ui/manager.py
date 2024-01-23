import customtkinter as ctk
from ui.menu import Menu
from ui.settings import Settings
from ui.home import Home
from ui.profile import Profile

GEOMETRY = "620x500+200+50"

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ChessLine")
        self.geometry(GEOMETRY)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        menu_frame = Menu(self)
        menu_frame.grid(row=0, column=0, sticky="news")

        self.frames = {}
        for Frame in (Profile, Settings, Home):
            frame = Frame(self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=1, sticky="nsew")

    def showFrame(self, frame):
        self.frames[frame].tkraise()