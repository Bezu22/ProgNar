import tkinter as tk
from PIL import Image, ImageTk
from config.utils import resource_path
from ui.frezy_menu.frezy_ui import FrezyUI
from tools_menu.wiertla_menu import WiertlaMenu
from tools_menu.pozostale_menu import PozostaleMenu
from tools_menu.uslugi_menu import UslugiMenu
from config.cenniki import CennikiMenu

class LeftMenu:
    def __init__(self, root, cart,client_name, main_app):
        self.root = root
        self.cart = cart
        self.client_name = client_name
        self.main_app = main_app
        self.create_left_menu()

    def create_left_menu(self):
        """Tworzy lewą ramkę z menu głównym."""
        self.left_frame = tk.Frame(self.root, width=450, bg="lightgrey")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Etykieta tytułu
        tk.Label(self.left_frame, text="ProgNar", bg="lightgrey", padx=60, font=("Arial", 18)).pack(pady=20)

        # Ramka dla przycisków Frezy i Wiertła (w jednej linii)
        button_row_frame = tk.Frame(self.left_frame, bg="lightgrey")
        button_row_frame.pack(pady=10)

        # Przygotowanie obrazów dla przycisków
        try:
            mill_img = Image.open(resource_path("img/mill.jpg")).resize((50, 50), Image.Resampling.LANCZOS)
            drill_img = Image.open(resource_path("img/drill.jpg")).resize((50, 50), Image.Resampling.LANCZOS)
            special_img = Image.open(resource_path("img/special.jpg")).resize((150, 50), Image.Resampling.LANCZOS)
            uslugi_img = Image.open(resource_path("img/uslugi.png")).resize((120, 40), Image.Resampling.LANCZOS)
            logo_img = Image.open(resource_path("img/logo.png")).resize((150, 50), Image.Resampling.LANCZOS)
            self.mill_photo = ImageTk.PhotoImage(mill_img)
            self.drill_photo = ImageTk.PhotoImage(drill_img)
            self.special_photo = ImageTk.PhotoImage(special_img)
            self.uslugi_photo = ImageTk.PhotoImage(uslugi_img)
            self.logo_photo = ImageTk.PhotoImage(logo_img)

            frezy_frame = tk.Frame(button_row_frame, bg="lightgrey")
            frezy_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(frezy_frame, text="Frezy", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(
                frezy_frame,
                image=self.mill_photo,
                command=self.show_frezy_menu,
                width=50,
                height=50
            ).pack()

            wiertla_frame = tk.Frame(button_row_frame, bg="lightgrey")
            wiertla_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(wiertla_frame, text="Wiertła", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(
                wiertla_frame,
                image=self.drill_photo,
                command=self.show_wiertla_menu,
                width=50,
                height=50
            ).pack()
        except Exception as e:
            print(f"Błąd wczytywania obrazów: {e}")
            frezy_frame = tk.Frame(button_row_frame, bg="lightgrey")
            frezy_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(frezy_frame, text="Frezy", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(frezy_frame, text="Frezy", font=("Arial", 14), command=self.show_frezy_menu).pack()

            wiertla_frame = tk.Frame(button_row_frame, bg="lightgrey")
            wiertla_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(wiertla_frame, text="Wiertła", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(wiertla_frame, text="Wiertła", font=("Arial", 14), command=self.show_wiertla_menu).pack()

            pozostale_frame = tk.Frame(button_row_frame, bg="lightgrey")
            pozostale_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(pozostale_frame, text="Pozostałe", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(pozostale_frame, text="Pozostałe", font=("Arial", 14), command=self.show_pozostale_menu, width=15).pack()

        pozostale_frame = tk.Frame(self.left_frame, bg="lightgrey")
        pozostale_frame.pack(pady=5)
        tk.Label(pozostale_frame, text="Pozostałe", bg="lightgrey", font=("Arial", 10)).pack()
        try:
            tk.Button(
                pozostale_frame,
                image=self.special_photo,
                command=self.show_pozostale_menu,
                width=150,
                height=50
            ).pack()
        except AttributeError:
            tk.Button(pozostale_frame, text="Pozostałe", font=("Arial", 14), command=self.show_pozostale_menu, width=15).pack()

        uslugi_frame = tk.Frame(self.left_frame, bg="lightgrey")
        uslugi_frame.pack(pady=5)
        tk.Label(uslugi_frame, text="Usługi", bg="lightgrey", font=("Arial", 10)).pack()
        try:
            tk.Button(
                uslugi_frame,
                image=self.uslugi_photo,
                command=self.show_uslugi_menu,
                width=150,
                height=50
            ).pack()
        except AttributeError:
            tk.Button(uslugi_frame, text="Usługi", font=("Arial", 14), command=self.show_uslugi_menu, width=15).pack()

        tk.Button(self.left_frame, text="Wyjście", font=("Arial", 14), command=self.root.quit).pack(pady=20)

        logo_frame = tk.Frame(self.left_frame, bg="lightgrey")
        logo_frame.pack(pady=5)
        try:
            tk.Button(
                logo_frame,
                image=self.logo_photo,
                command=self.show_cenniki_menu,
                relief="flat",
                borderwidth=0,
                bg="lightgrey",
                activebackground="lightgrey"
            ).pack()
        except AttributeError:
            tk.Label(logo_frame, text="Logo niedostępne", bg="lightgrey", font=("Arial", 10)).pack()

    def show_frezy_menu(self):
        """Otwiera menu frezów."""
        FrezyUI(self.root,self.cart, self.client_name,self.main_app.handle_frezy_save)

    def show_wiertla_menu(self):
        """Otwiera menu wierteł."""
        WiertlaMenu(self.root, self.cart, main_app=self.main_app)

    def show_pozostale_menu(self):
        """Otwiera menu pozostałych narzędzi."""
        PozostaleMenu(self.root, self.cart, main_app=self.main_app)

    def show_uslugi_menu(self):
        """Otwiera menu usług."""
        UslugiMenu(self.root, self.cart, main_app=self.main_app)

    def show_cenniki_menu(self):
        """Otwiera menu cenników."""
        CennikiMenu()