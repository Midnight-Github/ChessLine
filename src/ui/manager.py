import customtkinter as ctk
from ui.menu import Menu
from ui.settings import Settings
from ui.home import Home
from ui.profile import Profile
from ui.offline.new import OfflineNewGame
from ui.offline.open import OfflineOpenGame
from ui.offline.create import OfflineCreateGame

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIDTH = 850
        HEIGHT = 450
        MONITOR_X = self.winfo_screenwidth()//2 - WIDTH//2
        MONITOR_Y = self.winfo_screenheight()//2 - HEIGHT//2
        GEOMETRY = f"{WIDTH}x{HEIGHT}+{MONITOR_X}+{MONITOR_Y}"

        self.title("ChessLine")
        self.geometry(GEOMETRY)
        # self.minsize(WIDTH, HEIGHT)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        menu_frame = Menu(self)
        menu_frame.grid(row=0, column=0, sticky="news")

        home = (OfflineNewGame, OfflineOpenGame, OfflineCreateGame)
        self.pages = (Profile, Settings, Home) + home

        self.frames = {}
        for Frame in (self.pages):
            frame = Frame(self)
            self.frames[self.__frameToStr(Frame)] = frame
            frame.grid(row=0, column=1, sticky="nsew")

        self.showFrame("Home")

    def __frameToStr(self, frame):
        return str(frame).split('.')[-1][:-2]

    def __strToFrame(self, string):
        for i in self.pages:
            if string == self.__frameToStr(i):
                return i
        raise ValueError("String does not match with any frame objects")

    def showFrame(self, frame):
        self.frames[frame].tkraise()

    def deleteFrame(self, frame):
        self.frames[frame].destroy()

    def initFrame(self, frame):
        new_frame = self.__strToFrame(frame)(self)
        self.frames[frame] = new_frame
        new_frame.grid(row=0, column=1, sticky="nsew")
        