import tkinter as tk
import customtkinter as ctk
from ui.MainPageStructure import MainPageStructure

class Home(MainPageStructure):
    def __init__(self, root):
        super().__init__(root, heading="Home")
        self.root = root

        self.connection_status = tk.StringVar(value=f"Connection: offline")
        self.server_name = tk.StringVar(value="Server: -")

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        # hide side bar when connection is offline
        self.side_bar = ctk.CTkTabview(self.frame, fg_color="transparent", border_width=2)
        self.side_bar.add("Match")
        self.side_bar.add("Friends")
        self.side_bar.grid(row=0, column=1, rowspan=2, sticky="nesw")

        self.friends()
        self.rankedMatch()
        self.connectionBar()
        self.offlineGame()

    def friends(self):
        self.friends_frame = ctk.CTkFrame(self.side_bar.tab("Friends"), fg_color="black")
        self.friends_frame.pack(fill="both", expand=True)

    def rankedMatch(self):
        self.match_frame = ctk.CTkFrame(self.side_bar.tab("Match"), fg_color="orange")
        self.match_frame.pack(fill="both", expand=True)

    def connectionBar(self):
        self.connection_frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=2)
        self.connection_frame.grid(row=0, column=0, padx=(0, 10), pady=20, sticky="nesw")

        self.connection_frame.grid_columnconfigure(1, weight=1)

        self.connection_status_label = ctk.CTkLabel(self.connection_frame, textvariable=self.connection_status, font=ctk.CTkFont(size=17))
        self.connection_status_label.grid(row=0, column=0, padx=10, pady=5, sticky="nesw")

        self.server_name_label = ctk.CTkLabel(self.connection_frame, textvariable=self.server_name)
        self.server_name_label.grid(row=0, column=2, padx=10, pady=(8, 2), sticky="nesw")

    def offlineGame(self):
        def makeOfflineButton(text, row, command=None):
            b = ctk.CTkButton(self.offline_button_frame, corner_radius=20, text=text, font=ctk.CTkFont(size=15), width=200, command=command)
            b.grid(row=row, column=0, pady=(0, 10))

        def launch(frame):
            self.root.setActivePage("Home", frame)
            self.root.initFrame(frame)
            self.root.showFrame("Home")  

        self.offline_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.offline_frame.grid(row=1, column=0, sticky="news")

        self.offline_button_frame = ctk.CTkFrame(self.offline_frame, fg_color="transparent")
        self.offline_button_frame.place(relx=0.5, rely=0.5, anchor="center")

        makeOfflineButton(text="New Game", row=0, command=lambda : launch("OfflineNewGame"))
        makeOfflineButton(text="Open Game", row=1, command=lambda : launch("OfflineOpenGame"))
        makeOfflineButton(text="Create Game", row=2, command=lambda : launch("OfflineCreateGame"))

    def updatePage(self):
        pass
