import customtkinter as ctk
from framework.MainPage import MainPage

class Guide(MainPage):
    def __init__(self, root) -> None:
        super().__init__(root, heading="Guide")

        self.root = root

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nesw")

        # use self.content_frame as root