# main.py - Główny moduł aplikacji z menu głównym i koszykiem

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from cart import Cart
from config.cart_io import load_cart_from_file
from tools_menu.frezy_menu import FrezyMenu
from tools_menu.wiertla_menu import WiertlaMenu
from tools_menu.pozostale_menu import PozostaleMenu
from tools_menu.uslugi_menu import UslugiMenu
from tools_menu.client_menu import ClientMenu
from config.cenniki import CennikiMenu
from config.doc_report import generate_report
from config.utils import resource_path
from tools_menu.remarks_menu import RemarksMenu
from ui.main_menu.bottom_mainmenu import BottomSection

#refaktor
from core.cart_state import CartStateManager
from ui.frezy_menu.frezy_ui import FrezyUI

class ToolPricingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ProgNar – System Regeneracji i Wyceny Narzędzi")
        self.root.geometry("1500x500")
        self.cart = Cart()
        self.client_name = tk.StringVar(value="- -")
        load_cart_from_file(self.cart, self.client_name)
        self.cart_manager = CartStateManager()

        # Lewa ramka dla menu
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

        self.right_frame = tk.Frame(self.root, width=750)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.client_label = tk.Label(self.right_frame, textvariable=self.client_name, font=("Arial", 14, "bold"), fg="black")
        self.client_label.pack(pady=5)
        self.client_label.bind("<Button-1>", self.open_client_menu)
        self.temp_client_data = {}

        tree_scroll_frame = tk.Frame(self.right_frame, borderwidth=1, relief="solid")
        tree_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("LP", "Nazwa", "Srednica", "fiChwyt", "Ilosc zebow", "Ilosc sztuk", "ciecie", "Cena/szt", "Wartosc", "Powlekanie", "L", "Cena powlekania/szt", "Wartosc powlekania", "Uwagi")
        self.cart_tree = ttk.Treeview(tree_scroll_frame, columns=columns, show="headings", height=10)
        self.cart_tree.heading("LP", text="L.P.")
        self.cart_tree.heading("Nazwa", text="Nazwa")
        self.cart_tree.heading("Srednica", text="φOD")
        self.cart_tree.heading("fiChwyt", text="φChwyt")
        self.cart_tree.heading("Ilosc zebow", text="z")
        self.cart_tree.heading("Ilosc sztuk", text="Ilość sztuk")
        self.cart_tree.heading("ciecie", text="cięcie")
        self.cart_tree.heading("Cena/szt", text="Cena/szt")
        self.cart_tree.heading("Wartosc", text="Netto")
        self.cart_tree.heading("Powlekanie", text="Powłoka")
        self.cart_tree.heading("L", text="L")
        self.cart_tree.heading("Cena powlekania/szt", text="Cena powlekania/szt")
        self.cart_tree.heading("Wartosc powlekania", text="Wartość powlekania")
        self.cart_tree.heading("Uwagi", text="Uwagi")

        self.cart_tree.column("LP", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Nazwa", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Srednica", width=60, anchor=tk.CENTER)
        self.cart_tree.column("fiChwyt", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Ilosc zebow", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Ilosc sztuk", width=80, anchor=tk.CENTER)
        self.cart_tree.column("ciecie", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Cena/szt", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Wartosc", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Powlekanie", width=100, anchor=tk.CENTER)
        self.cart_tree.column("L", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Cena powlekania/szt", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Wartosc powlekania", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Uwagi", width=120, anchor=tk.CENTER)  # Zwiększona szerokość dla większych symboli

        # Styl dla kolumny Uwagi
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), anchor="center")
        style.configure("Remarks.Treeview", font=("Arial Black", 12, "bold"), anchor="center")
        style.configure("Remarks.Treeview.Cell", relief="raised")
        self.cart_tree.bind('<Double-Button-1>', self.handle_tree_click)

        v_scrollbar = ttk.Scrollbar(tree_scroll_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(tree_scroll_frame, orient=tk.HORIZONTAL, command=self.cart_tree.xview)
        self.cart_tree.configure(xscrollcommand=h_scrollbar.set)

        self.cart_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        tree_scroll_frame.grid_rowconfigure(0, weight=1)
        tree_scroll_frame.grid_columnconfigure(0, weight=1)

        #ODPALAMY BOTTOM SECTION
        self.bottom = BottomSection(
            parent=self.right_frame,
            cart=self.cart,
            cart_tree=self.cart_tree,
            client_name=self.client_name,
            root=self.root
        )


    def handle_tree_click(self, event):
        """Obsługuje kliknięcie w tabelę koszyka."""
        region = self.cart_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.cart_tree.identify_column(event.x)
            if column == "#14":  # Kolumna Uwagi (ostatnia)
                selected = self.cart_tree.selection()
                if selected:
                    index = int(selected[0])
                    RemarksMenu(self.root, self.cart, index, self)

    def show_frezy_menu(self):
        FrezyUI(self.root, on_save=self.handle_frezy_save)

    def handle_frezy_save(self):
        self.core_manager.refresh_cart_from_file()
        self.update_cart_display()

    def show_wiertla_menu(self):
        WiertlaMenu(self.root, self.cart, main_app=self)

    def show_pozostale_menu(self):
        PozostaleMenu(self.root, self.cart, main_app=self)

    def show_uslugi_menu(self):
        UslugiMenu(self.root, self.cart, main_app=self)

    def show_cenniki_menu(self):
        CennikiMenu()

    def open_client_menu(self, event=None):
        """Otwiera okno edycji nazwy klienta."""
        ClientMenu(self.root, self)

    def generate_report(self):
        generate_report(self.client_name, self)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToolPricingApp(root)
    root.mainloop()