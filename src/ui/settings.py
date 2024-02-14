import customtkinter as ctk
from ui.structure import MainPage
from utils.ctkAddon import scale
from engine.settings import settings

class Settings(MainPage):
    def __init__(self, root):
        super().__init__(root, heading="Settings")

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        board_frame = ctk.CTkFrame(self.frame)
        board_frame.grid(row=0, column=0, sticky="nw")

        board_label_frame = ctk.CTkFrame(board_frame)
        board_label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        board_label = ctk.CTkLabel(board_label_frame, text="Board", font=ctk.CTkFont(size=20))
        board_label.pack()

        self.board_size_slider = scale(board_frame, text="Board size",from_=500, to=1500, step=10, default=settings.config["board_size"], row=1, column=0, pady=10)
        self.board_size_slider.bind("<ButtonRelease-1>", self.__checkSliderChange)

        self.save_button = ctk.CTkButton(self.frame, text="Save", state="disabled", fg_color="transparent", border_width=2, command=self.__save)
        self.save_button.grid(row=2, column=2, sticky="es")
        self.save_button.bind("<ButtonRelease-1>", lambda e: self.save_button.configure(state="disabled"))

    def __save(self):
        settings.config["board_size"] = int(self.board_size_slider.get())
        settings.push()

    def __checkSliderChange(self, e):
        if settings.config["board_size"] != int(self.board_size_slider.get()):
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")
