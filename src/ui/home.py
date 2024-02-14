import customtkinter as ctk
from ui.structure import MainPage

class Home(MainPage):
    def __init__(self, root):
        super().__init__(root, heading="Home")

        self.root = root

        #Main frame layout
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        friends_frame = ctk.CTkFrame(self.frame, fg_color="black")
        friends_frame.grid(row=0, column=0, rowspan=2, sticky="news")

        connection_frame = ctk.CTkFrame(self.frame, fg_color="red")
        connection_frame.grid(row=0, column=1, sticky="news")

        offline_frame = ctk.CTkFrame(self.frame)
        offline_frame.grid(row=1, column=1, sticky="news")

        match_frame = ctk.CTkFrame(self.frame, fg_color="orange")
        match_frame.grid(row=0, column=2, rowspan=2, stick="nesw")

        #Offline frame layout
        offline_frame.grid_rowconfigure((0, 1, 2), weight=1)
        offline_frame.grid_columnconfigure(0, weight=1)

        def offline_button(text, row, command=None):
            b = ctk.CTkButton(offline_frame, text=text, font=ctk.CTkFont(size=20), command=command)
            b.grid(row=row, column=0, sticky="nesw", padx=10, pady=10)
            return b

        offline_new = offline_button(text="New Game", row=0, command=lambda : self.launch("OfflineNewGame"))
        offline_open = offline_button(text="Open Game", row=1, command=lambda : self.launch("OfflineOpenGame"))
        offline_create = offline_button(text="Create Game", row=2, command=lambda : self.launch("OfflineCreateGame"))

    def launch(self, frame):
        self.root.setActivePage("Home", frame)
        self.root.initFrame(frame)
        self.root.showFrame("Home")
