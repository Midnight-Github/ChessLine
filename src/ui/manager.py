import customtkinter as ctk
from ui.menu import Menu
from ui.settings import Settings
from ui.home import Home
from ui.profile import Profile
from ui.offlineNewGame import OfflineNewGame
from ui.offlineOpenGame import OfflineOpenGame
from ui.offlineCreateGame import OfflineCreateGame

class Manager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.main_pages = (Profile, Settings, Home)
        self.home = (OfflineNewGame, OfflineOpenGame, OfflineCreateGame)
        self.pages = self.main_pages + self.home

        self.active_pages = {}
        for i in self.main_pages:
            i = self.__frameToStr(i)
            self.active_pages[i] = i

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

        self.frames = {}
        for Frame in (self.main_pages):
            frame = Frame(self)
            self.frames[self.__frameToStr(Frame)] = frame
            frame.grid(row=0, column=1, sticky="nsew")

        self.menu = Menu(self)
        self.menu.grid(row=0, column=0, sticky="news")

        self.showFrame("Home")

    def __frameToStr(self, frame):
        return str(frame).split('.')[-1][:-2]

    def __strToFrame(self, string):
        for i in self.pages:
            if string == self.__frameToStr(i):
                return i
        raise ValueError("String does not match with any frame objects")

    def __getMainPage(self, frame):
        if self.__strToFrame(frame) in self.main_pages:
            return frame
        if self.__strToFrame(frame) in self.home:
            return "Home"

    def setActivePage(self, main_frame, sub_frame):
        self.active_pages[main_frame] = sub_frame

    def showFrame(self, frame, forced=False):
        self.menu.focusButton(self.__getMainPage(frame))
        if forced:
            self.frames[frame].tkraise()
            return
        self.frames[self.active_pages[frame]].tkraise()

    def deleteFrame(self, frame):
        self.frames[frame].destroy()

    def initFrame(self, frame):
        new_frame = self.__strToFrame(frame)(self)
        self.frames[frame] = new_frame
        new_frame.grid(row=0, column=1, sticky="nsew")
        