import customtkinter as ctk

class Menu(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0)

        self.grid_rowconfigure(3, weight=1)

        self.menu_label = ctk.CTkLabel(self, text="ChessLine", font=ctk.CTkFont(size=20))
        self.menu_label.grid(row=0, column=0, pady=10, padx=10)

        self.home_button = self.makeButton(text="Home", row=1, command=lambda: root.showFrame("Home"))
        self.settings_button = self.makeButton(text="Setting", row=2, command=lambda: root.showFrame("Setting"))
        self.profile_button = self.makeButton(text="Profile", row=4, pady=(0, 15), command=lambda: root.showFrame("Profile"))

    def makeButton(self, text, row, command=None, pady=(10, 10)):
        button = ctk.CTkButton(self, text=text, width=80, command=command)
        button.grid(row=row, column=0, pady=pady, padx=10, ipadx=10)
        return button

    def focusButton(self, button):
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