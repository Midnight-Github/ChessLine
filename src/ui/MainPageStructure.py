import customtkinter as ctk

class MainPageStructure(ctk.CTkFrame):
    def __init__(self, root, heading: str) -> None:
        super().__init__(root, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.__createHeading(heading)

        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)

    def __createHeading(self, heading: str) -> None:
        head_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=2)
        head_frame.grid(row=0, column=0, sticky="nesw", pady=(10, 0), padx=10)
        head_frame.grid_columnconfigure(0, weight=1)

        head_label = ctk.CTkLabel(head_frame, height=10, text=heading, font=ctk.CTkFont(size=20))
        head_label.grid(row=0, column=0, sticky="nesw", padx=10, pady=5)
        