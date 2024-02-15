import customtkinter as ctk

class OfflineNewGame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.board_canvas = ctk.CTkCanvas(self)
        self.board_canvas.grid(row=0, column=0)
        self.board_canvas.bind("<Configure>", self.createBoard)
        self.board_canvas.bind("<ButtonRelease-1>", self.createBoard)

        self.side_bar = ctk.CTkFrame(self)
        self.side_bar.grid(row=0, column=1, sticky="news")

        self.quit_button = ctk.CTkButton(self.side_bar, text="Quit", command=self.quitFrame)
        self.quit_button.grid(row=0, column=0)
    
    def quitFrame(self): #add confirmation box
        self.root.setActivePage("Home", "Home")
        self.root.deleteFrame("OfflineNewGame")
        self.root.showFrame("Home")
    
    def updateSize(self):
        size = min(abs(self.winfo_width() - self.side_bar.winfo_width()), self.winfo_height())
        self.board_canvas.config(height=size, width=size)
        return size

    def createBoard(self, e):
        self.board_canvas.delete("all")
        size = self.updateSize()
        
