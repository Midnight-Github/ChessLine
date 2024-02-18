import customtkinter as ctk
from chess.Chess import Chess

class OfflineNewGame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.side_bar = ctk.CTkFrame(self)
        self.side_bar.grid(row=0, column=1, sticky="news")

        self.quit_button = ctk.CTkButton(self.side_bar, text="Quit", command=self.quitFrame)
        self.quit_button.grid(row=0, column=0)

        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.grid(row=0, column=0, sticky="nesw")
        self.board_frame.bind("<Configure>", self.updateBoard)
        self.board_frame.grid_rowconfigure(1, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)

        self.black_ui = ctk.CTkFrame(self.board_frame)
        self.black_ui.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.black_ui.grid_columnconfigure(1, weight=1)
        self.__setUpBlackUi()

        self.white_ui = ctk.CTkFrame(self.board_frame)
        self.white_ui.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
        self.white_ui.grid_columnconfigure(1, weight=1)
        self.__setUpWhiteUi()

        self.board_canvas = ctk.CTkCanvas(self.board_frame, height=size, width=size)
        self.board_canvas.grid(row=1, column=0)

        self.chess = Chess()

    def __setUpBlackUi(self):
        self.black_name_label = ctk.CTkLabel(self.black_ui, text=self.name[1])
        self.black_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.black_timer_label = ctk.CTkLabel(self.black_ui, textvariable=self.timer[1])
        self.black_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")
    
    def __setUpWhiteUi(self):
        self.white_name_label = ctk.CTkLabel(self.white_ui, text=self.name[0])
        self.white_name_label.grid(row=0, column=0, padx=10, sticky="nesw")

        self.white_timer_label = ctk.CTkLabel(self.white_ui, textvariable=self.timer[0])
        self.white_timer_label.grid(row=0, column=2, padx=10, sticky="nesw")

    def quitFrame(self): #add confirmation box
        self.root.setActivePage("Home", "Home")
        self.root.deleteFrame("OfflineNewGame")
        self.root.showFrame("Home")
    
    def mainFrameSize(self):
        return (self.winfo_height(), abs(self.winfo_width() - self.side_bar.winfo_width()))

    def updateBoard(self, e):
        self.chess.update(*self.mainFrameSize())
        
