import tkinter as tk
from tools_menu.client_menu import ClientMenu

class TopMenu:
    def __init__(self, parent, client_name, main_app):
        self.parent = parent
        self.client_name = client_name
        self.main_app = main_app
        self.create_top_menu()

    def create_top_menu(self):
        """Tworzy górną sekcję z etykietą klienta."""
        self.client_label = tk.Label(self.parent, textvariable=self.client_name, font=("Arial", 14, "bold"), fg="black")
        self.client_label.pack(pady=5)
        self.client_label.bind("<Button-1>", self.open_client_menu)

    def open_client_menu(self, event=None):
        """Otwiera okno edycji nazwy klienta."""
        ClientMenu(self.main_app.root, self.main_app)