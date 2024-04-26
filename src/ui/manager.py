from typing import Callable
import customtkinter as ctk
from ui.Menu import Menu
from ui.Setting import Setting
from ui.Home import Home
from ui.Profile import Profile
from home.OfflineNewGame import OfflineNewGame
from home.OfflineOpenGame import OfflineOpenGame
from home.OfflineCreateGame import OfflineCreateGame
from ui.Guide import Guide
from var.Globals import configurator

class Manager(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.commitConfigurator()

        self.main_pages = (Profile, Setting, Home, Guide)
        self.home = (OfflineNewGame, OfflineOpenGame, OfflineCreateGame)
        self.pages = self.main_pages + self.home

        self.active_pages = {}
        for i in self.main_pages:
            i = self.frameToStr(i)
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
            self.frames[self.frameToStr(Frame)] = frame
            frame.grid(row=0, column=1, sticky="nsew")

        self.menu = Menu(self)
        self.menu.grid(row=0, column=0, sticky="news")

        self.showFrame("Home")

    def commitConfigurator(self) -> None:
        ctk.set_appearance_mode(configurator.config["appearance"]["system_theme"])
        ctk.set_default_color_theme(configurator.config["appearance"]["color_theme"])

    def frameToStr(self, frame: Callable) -> str:
        return str(frame).split('.')[-1][:-2]

    def strToFrame(self, frame: str) -> Callable:
        for i in self.pages:
            if frame == self.frameToStr(i):
                return i
        raise ValueError(frame, "does not match with any frame objects")

    def getMainPage(self, frame: str) -> str:
        frame_str = self.strToFrame(frame)
        if frame_str in self.main_pages:
            return frame
        if frame_str in self.home:
            return "Home"
        raise ValueError(frame, "does not match with any frame objects")

    def setActivePage(self, main_frame: str, sub_frame: str) -> None:
        self.active_pages[main_frame] = sub_frame

    def showFrame(self, frame: str, forced: bool=False) -> None:
        self.menu.focusButton(self.getMainPage(frame))
        if forced:
            self.frames[frame].tkraise()
            return 
        self.frames[self.active_pages[frame]].tkraise()

    def deleteFrame(self, frame: str) -> None:
        self.frames[frame].destroy()

    def initFrame(self, frame: str) -> None:
        new_frame = self.strToFrame(frame)(self)
        self.frames[frame] = new_frame
        new_frame.grid(row=0, column=1, sticky="nsew")
        