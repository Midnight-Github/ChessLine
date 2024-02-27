import customtkinter as ctk
from utils import CtkAddon as ctka
from ui.MainPageStructure import MainPageStructure
from reader.Toml import configurator
from CTkMessagebox import CTkMessagebox

class Setting(MainPageStructure):
    def __init__(self, root):
        super().__init__(root, heading="Settings")

        self.root = root
        self.configurator = configurator

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # board_frame = ctk.CTkFrame(self.frame)
        # board_frame.grid(row=0, column=0, sticky="nw")

        # board_label_frame = ctk.CTkFrame(board_frame)
        # board_label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        # board_label = ctk.CTkLabel(board_label_frame, text="Board", font=ctk.CTkFont(size=20))
        # board_label.pack()

        self.appearance()

        self.settings_button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.settings_button_frame.grid(row=2, column=2, sticky="nesw")

        self.reset_button = ctk.CTkButton(self.settings_button_frame, text="Reset", state="disabled", fg_color="transparent", border_width=2, command=self.reset)
        self.reset_button.grid(row=0, column=0, pady=(0, 5), sticky="nesw")
        self.reset_button.bind("<ButtonPress-1>", lambda e: self.disableButtons())

        self.save_button = ctk.CTkButton(self.settings_button_frame, text="Save", state="disabled", fg_color="transparent", border_width=2, command=self.save)
        self.save_button.grid(row=1, column=0, sticky="nesw")
        self.save_button.bind("<ButtonPress-1>", lambda e: self.disableButtons())

    def appearance(self):
        self.system_themes = ("system", "dark", "light")
        self.color_themes = ("blue", "dark-blue", "green")

        self.appearance_frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=2)
        self.appearance_frame.grid(row=0, column=0, sticky="nw")

        self.appearance_label_frame = ctk.CTkFrame(self.appearance_frame, border_width=2)
        self.appearance_label_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nesw")
        self.appearance_label_frame.grid_columnconfigure(0, weight=1)
        self.appearance_label = ctk.CTkLabel(self.appearance_label_frame, text="Appearance", font=ctk.CTkFont(size=20))
        self.appearance_label.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        self.system_theme = ctka.labeledRadioButton(self.appearance_frame, label_text="System theme", options=[i.capitalize() for i in self.system_themes], 
        row=1, column=0, padx=(5, 0), pady=(0, 5), value=self.system_themes.index(self.configurator.config["appearance"]["system_theme"]), command=self.checkChanges)

        self.color_theme = ctka.labeledRadioButton(self.appearance_frame, label_text="Color theme", options=[i.capitalize() for i in self.color_themes], 
        row=1, column=1, padx=(0, 5), pady=(0, 5), value=self.color_themes.index(self.configurator.config["appearance"]["color_theme"]), command=self.checkChanges)

    def checkChanges(self):
        changes = [ 
            self.configurator.config["appearance"]["system_theme"] != self.system_themes[self.system_theme.get()],
            self.configurator.config["appearance"]["color_theme"] != self.color_themes[self.color_theme.get()]
        ]
        
        if any(changes):
            self.enableButtons()
        else:
            self.disableButtons()
    
    def commitChanges(self):
        self.configurator.config["appearance"]["system_theme"] = self.system_themes[self.system_theme.get()]

    def executeChanges(self):
        ctk.set_appearance_mode(self.configurator.config["appearance"]["system_theme"])

    def reset(self):
        self.system_theme.set(self.system_themes.index(self.configurator.config["appearance"]["system_theme"]))
        self.resetRestartOnlyChanges()

    def checkRestartRequired(self):
        changes = [self.configurator.config["appearance"]["color_theme"] != self.color_themes[self.color_theme.get()]]
        return any(changes)

    def commitRestartOnlyChanges(self):
        self.configurator.config["appearance"]["color_theme"] = self.color_themes[self.color_theme.get()]

    def resetRestartOnlyChanges(self):
        self.color_theme.set(self.color_themes.index(self.configurator.config["appearance"]["color_theme"]))

    def enableButtons(self):
        self.save_button.configure(state="normal")
        self.reset_button.configure(state="normal")

    def disableButtons(self):
        self.save_button.configure(state="disabled")
        self.reset_button.configure(state="disabled")

    def save(self):
        if self.checkRestartRequired():
            warning_popup = CTkMessagebox(title="Unsaved changes", message="Some changes require a restart.\nClose the app?",
                            icon="info", option_1="No", option_2="Yes")
            if warning_popup.get() == "Yes":
                self.commitRestartOnlyChanges()
                configurator.push()
                self.root.destroy()
            else:
                self.resetRestartOnlyChanges()
        self.commitChanges()
        self.executeChanges()
        configurator.push()