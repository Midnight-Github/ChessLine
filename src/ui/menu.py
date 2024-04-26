from typing import Callable
import customtkinter as ctk

class Menu(ctk.CTkFrame):
    def __init__(self, root) -> None:
        super().__init__(root, corner_radius=0)

        self.grid_rowconfigure(2, weight=1)

        self.menu_label = ctk.CTkLabel(self, text="ChessLine", font=ctk.CTkFont(size=20))
        self.menu_label.grid(row=0, column=0, pady=10, padx=10)

        self.upper_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.upper_button_frame.grid(row=1, column=0)

        self.home_button = ctk.CTkButton(self.upper_button_frame, text="Home", width=80, command=lambda: root.showFrame("Home"))
        self.home_button.grid(row=0, column=0, pady=10, padx=10, ipadx=10)
        self.settings_button = ctk.CTkButton(self.upper_button_frame, text="Setting", width=80, command=lambda: root.showFrame("Setting"))
        self.settings_button.grid(row=1, column=0, pady=(0, 10), padx=10, ipadx=10)
        self.guide_button = ctk.CTkButton(self.upper_button_frame, text="Guide", width=80, command=lambda: root.showFrame("Guide"))
        self.guide_button.grid(row=2, column=0, pady=(0, 10), padx=10, ipadx=10)

        self.lower_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lower_button_frame.grid(row=3, column=0)

        self.profile_button = ctk.CTkButton(self.lower_button_frame, text="Profile", width=80, command=lambda: root.showFrame("Profile"))
        self.profile_button.grid(row=2, column=0, pady=10, padx=10, ipadx=10)

    def makeButton(self, text: str, row: int, command: Callable | None=None, pady: tuple[float, float]=(10, 10)) -> ctk.CTkButton:
        button = ctk.CTkButton(self, text=text, width=80, command=command)
        button.grid(row=row, column=0, pady=pady, padx=10, ipadx=10)
        return button

    def focusButton(self, button: str) -> None:
        self.home_button.configure(state='normal')
        self.settings_button.configure(state='normal')
        self.profile_button.configure(state='normal')

        match(button):
            case "Home":
                self.home_button.configure(state='disabled')
            case "Setting":
                self.settings_button.configure(state='disabled')
            case "Profile":
                self.profile_button.configure(state='disabled')        