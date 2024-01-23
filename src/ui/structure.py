import customtkinter as ctk

class MainPage(ctk.CTkFrame):
    def __init__(self, root, heading):
        super().__init__(root, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.__createHeading(heading)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)

    def __createHeading(self, heading):
        head_frame = ctk.CTkFrame(self, fg_color="transparent")
        head_frame.grid(row=0, column=0, sticky="nesw", pady=(10, 0))

        ctk.CTkLabel(head_frame, text=heading, font=ctk.CTkFont(size=20)).pack()
        