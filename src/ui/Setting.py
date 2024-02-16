import customtkinter as ctk
from ui.MainPageStructure import MainPageStructure

class Setting(MainPageStructure):
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

        self.save_button = ctk.CTkButton(self.frame, text="Save", state="disabled", fg_color="transparent", border_width=2, command=self.__save)
        self.save_button.grid(row=2, column=2, sticky="es")
        self.save_button.bind("<ButtonPress-1>", lambda e: self.save_button.configure(state="disabled"))

    def __save(self):
        pass
        # settings.push()
