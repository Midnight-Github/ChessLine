import customtkinter as ctk
from ui.structure import MainPage
from ui.offline.new import OfflineNewGame
from ui.offline.open import OfflineOpenGame
from ui.offline.create import OfflineCreateGame

class Home(MainPage):
    def __init__(self, root):
        super().__init__(root, heading="Home")

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

        offline_new = offline_button(text="New Offline Game", row=0, command=lambda : root.showFrame(OfflineNewGame))
        offline_open = offline_button(text="Open Offline Game", row=1, command=lambda : root.showFrame(OfflineOpenGame))
        offline_create = offline_button(text="Create Game", row=2, command=lambda : root.showFrame(OfflineCreateGame))
