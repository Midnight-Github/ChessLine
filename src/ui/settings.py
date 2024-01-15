import tkinter as tk
import customtkinter as ctk

class Settings(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        head_frame = ctk.CTkFrame(self, fg_color="transparent")
        head_frame.grid(row=0, column=0, sticky="nesw", pady=(10, 0))

        label = ctk.CTkLabel(head_frame, text="Settings", font=ctk.CTkFont(size=20))
        label.pack()


        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)