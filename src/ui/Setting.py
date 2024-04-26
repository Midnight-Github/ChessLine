import customtkinter as ctk
from utils import CtkAddon as ctka
from framework.MenuPage import MenuPage
from var.Globals import configurator
from CTkMessagebox import CTkMessagebox

class Setting(MenuPage):
    def __init__(self, root) -> None:
        super().__init__(root, heading="Settings")

        self.root = root
        self.configurator = configurator

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.appearance()
        self.board()

        self.settings_button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.settings_button_frame.grid(row=2, column=2, sticky="nesw")

        self.reset_button = ctk.CTkButton(self.settings_button_frame, text="Reset", 
            state="disabled", fg_color="transparent", border_width=2, command=self.reset
        )
        self.reset_button.grid(row=0, column=0, pady=(0, 5), sticky="nesw")
        self.reset_button.bind("<ButtonPress-1>", lambda e: self.disableButtons())

        self.save_button = ctk.CTkButton(self.settings_button_frame, text="Save", 
            state="disabled", fg_color="transparent", border_width=2, command=self.save
        )
        self.save_button.grid(row=1, column=0, sticky="nesw")
        self.save_button.bind("<ButtonPress-1>", lambda e: self.disableButtons())

    def createSettingsFrame(self, heading_text: str, row: int, column: int) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=2)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nw")

        label_frame = ctk.CTkFrame(frame, border_width=2)
        label_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nesw")
        label_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(label_frame, text=heading_text, font=ctk.CTkFont(size=20))
        label.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=5, pady=(0, 5))

        return content_frame

    def board(self) -> None:
        self.board_colors: list[str] = ["Gray", "Blue", "Green"]

        self.board_frame = self.createSettingsFrame(heading_text="Board", row=0, column=1)

        self.board_color = ctk.CTkOptionMenu(self.board_frame, values=self.board_colors, 
            width=90, command=self.checkChanges
        )
        self.board_color.grid(row=0, column=0, padx=10, pady=10)
        self.board_color.set(self.configurator.config["board"]["color"])

    def appearance(self) -> None:
        self.system_themes: tuple[str, ...] = ("system", "dark", "light")
        self.system_color_themes: tuple[str, ...] = ("blue", "dark-blue", "green")

        self.appearance_frame = self.createSettingsFrame(heading_text="Appearance", row=0, 
            column=0
        )

        self.system_theme = ctka.labeledRadioButton(self.appearance_frame, label_text="System theme", 
            options=[i.capitalize() for i in self.system_themes], row=1, column=0, padx=(5, 0), pady=(0, 5), 
            value=self.system_themes.index(self.configurator.config["appearance"]["system_theme"]), 
            command=self.checkChanges
        )

        self.color_theme = ctka.labeledRadioButton(self.appearance_frame, label_text="Color theme", 
            options=[i.capitalize() for i in self.system_color_themes], row=1, column=1, padx=(0, 5), 
            pady=(0, 5), 
            value=self.system_color_themes.index(self.configurator.config["appearance"]["color_theme"]), 
            command=self.checkChanges
        )
    
    def checkChanges(self, e=None) -> None:
        changes: list[bool] = [ 
            self.configurator.config["appearance"]["system_theme"] != self.system_themes[self.system_theme.get()],
            self.configurator.config["appearance"]["color_theme"] != self.system_color_themes[self.color_theme.get()],
            self.configurator.config["board"]["color"] != self.board_color.get()
        ]
        
        if any(changes):
            self.enableButtons()
        else:
            self.disableButtons()
    
    def commitChanges(self) -> None:
        self.configurator.config["appearance"]["system_theme"] = self.system_themes[self.system_theme.get()]
        self.configurator.config["board"]["color"] = self.board_color.get()

    def executeChanges(self) -> None:
        ctk.set_appearance_mode(self.configurator.config["appearance"]["system_theme"])

    def reset(self) -> None:
        self.system_theme.set(self.system_themes.index(self.configurator.config["appearance"]["system_theme"]))
        self.board_color.set(self.configurator.config["board"]["color"])
        self.resetRestartOnlyChanges()

    def checkRestartRequired(self) -> bool:
        changes: list[bool] = [
            self.configurator.config["appearance"]["color_theme"] != self.system_color_themes[self.color_theme.get()]
        ]
        return any(changes)

    def commitRestartOnlyChanges(self) -> None:
        self.configurator.config["appearance"]["color_theme"] = self.system_color_themes[self.color_theme.get()]

    def resetRestartOnlyChanges(self) -> None:
        self.color_theme.set(self.system_color_themes.index(self.configurator.config["appearance"]["color_theme"]))

    def enableButtons(self) -> None:
        self.save_button.configure(state="normal")
        self.reset_button.configure(state="normal")

    def disableButtons(self) -> None:
        self.save_button.configure(state="disabled")
        self.reset_button.configure(state="disabled")

    def save(self) -> None:
        if self.checkRestartRequired():
            warning_popup = CTkMessagebox(title="Unsaved changes", 
                message="Some changes require a restart.\nClose the app?", icon="info", option_1="No", 
                option_2="Yes"
            )
            if warning_popup.get() == "Yes":
                self.commitRestartOnlyChanges()
                configurator.push()
                self.root.destroy()
            else:
                self.resetRestartOnlyChanges()
        self.commitChanges()
        self.executeChanges()
        configurator.push()