import tkinter as tk
from tkinter import ttk
from core.notes_main import NotesMenu

class CartDisplay:
    def __init__(self, parent, root, cart, main_app):
        self.parent = parent
        self.root = root
        self.cart = cart
        self.main_app = main_app
        self.sort_reverse = False  # domyślnie rosnąco
        self.sort_directions = {}
        self.create_cart_table()

    def create_cart_table(self):
        """Tworzy tabelę koszyka z nagłówkami i stylami."""
        tree_scroll_frame = tk.Frame(self.parent, borderwidth=1, relief="solid")
        tree_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("LP", "Nazwa", "Srednica", "fiChwyt", "Ilosc ostrzy", "Ilosc sztuk", "ciecie", "Cena szlifowania", "Razem szlifowanie", "Powloka", "Dlugosc calkowita", "Cena powlekania", "Razem powloka", "Uwagi")
        self.cart_tree = ttk.Treeview(tree_scroll_frame, columns=columns, show="headings", height=10)
        self.cart_tree.heading("LP", text="L.P.")
        self.cart_tree.heading("Nazwa", text="Nazwa", command=lambda: self.sort_by_column("Nazwa"))
        self.cart_tree.heading("Srednica", text="φOD", command=lambda: self.sort_by_column("Srednica",is_numeric=True))
        self.cart_tree.heading("fiChwyt", text="φChwyt", command=lambda: self.sort_by_column("fiChwyt",is_numeric=True))
        self.cart_tree.heading("Ilosc ostrzy", text="z", command=lambda: self.sort_by_column("Ilosc ostrzy",is_numeric=True))
        self.cart_tree.heading("Ilosc sztuk", text="Ilość sztuk", command=lambda: self.sort_by_column("Ilosc sztuk",is_numeric=True))
        self.cart_tree.heading("ciecie", text="cięcie",command=lambda: self.sort_by_column("ciecie",is_numeric=True))
        self.cart_tree.heading("Cena szlifowania", text="Cena/szt", command=lambda: self.sort_by_column("Cena szlifowania",is_numeric=True))
        self.cart_tree.heading("Razem szlifowanie", text="Netto", command=lambda: self.sort_by_column("Razem szlifowanie",is_numeric=True))
        self.cart_tree.heading("Powloka", text="Powłoka",command=lambda: self.sort_by_column("Powloka"))
        self.cart_tree.heading("Dlugosc calkowita", text="L",command=lambda: self.sort_by_column("Dlugosc calkowita",is_numeric=True))
        self.cart_tree.heading("Cena powlekania", text="Cena powlekania/szt",command=lambda: self.sort_by_column("Cena powlekania",is_numeric=True))
        self.cart_tree.heading("Razem powloka", text="Wartość powlekania",command=lambda: self.sort_by_column("Razem powloka",is_numeric=True))
        self.cart_tree.heading("Uwagi", text="Uwagi")

        self.cart_tree.column("LP", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Nazwa", width=130, anchor=tk.CENTER)
        self.cart_tree.column("Srednica", width=60, anchor=tk.CENTER)
        self.cart_tree.column("fiChwyt", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Ilosc ostrzy", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Ilosc sztuk", width=80, anchor=tk.CENTER)
        self.cart_tree.column("ciecie", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Cena szlifowania", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Razem szlifowanie", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Powloka", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Dlugosc calkowita", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Cena powlekania", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Razem powloka", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Uwagi", width=120, anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), anchor="center")
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

        # Inicjalne wypełnienie tabeli
        self.cart.update_cart_display(self.cart_tree)

    def handle_tree_click(self, event):
        """Obsługuje kliknięcie w tabelę koszyka."""
        region = self.cart_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.cart_tree.identify_column(event.x)
            if column == "#14":  # Kolumna Uwagi (ostatnia)
                selected = self.cart_tree.selection()
                if selected:
                    index = int(selected[0])
                    NotesMenu(self.root, self.cart, index, self.main_app)

    def get_cart_tree(self):
        """Zwraca obiekt Treeview koszyka."""
        return self.cart_tree

    def sort_by_column(self, column_name, is_numeric=False):
        """Sortuje dane po wskazanej kolumnie — tekstowej lub liczbowej."""
        # Odwróć kierunek sortowania dla tej kolumny
        reverse = self.sort_directions.get(column_name, False)
        self.sort_directions[column_name] = not reverse

        # Funkcja pomocnicza do konwersji
        def normalize(val):
            if val in ("-", "", None):
                return 0 if is_numeric else ""
            if val in ("+"):
                return 1 if is_numeric else ""
            if is_numeric:
                try:
                    if isinstance(val, (int, float)):
                        return val
                    return float(str(val).replace(",", "."))
                except (ValueError, TypeError):
                    return 0
            else:
                return str(val).lower()

        # Posortuj dane
        sorted_items = sorted(
            self.cart.items,
            key=lambda x: normalize(x.get(column_name)),
            reverse=reverse
        )

        # Zaktualizuj dane i odśwież tabelę
        self.cart.items = sorted_items
        self.cart.update_cart_display(self.cart_tree)

    def sort_by_name(self):
        """Sortuje dane w koszyku po nazwie i aktualizuje tabelę."""
        # Odwróć kierunek sortowania
        reverse = self.sort_directions.get("Nazwa", False)
        self.sort_directions["Nazwa"] = not reverse

        # Posortuj dane
        sorted_items = sorted(
            self.cart.items,
            key=lambda x: x.get("Nazwa", "").lower(),
            reverse=reverse  # ← tu była pomyłka
        )

        # Zaktualizuj dane w obiekcie
        self.cart.items = sorted_items

        # Odśwież tabelę
        self.cart.update_cart_display(self.cart_tree)

    def sort_by_value(self,column_name):
        """Sortuje dane po wybranej kolumnie liczbowej."""
        # Odwróć kierunek sortowania dla tej kolumny
        reverse = self.sort_directions.get(column_name, False)
        self.sort_directions[column_name] = not reverse

        # Posortuj dane
        def safe_number(val):
            try:
                if val in ("-", "", None):
                    return 0
                if val in ("+"):
                    return 1
                if isinstance(val, (int, float)):
                    return val
                return float(str(val).replace(",", "."))
            except (ValueError, TypeError):
                return 0

        sorted_items = sorted(
            self.cart.items,
            key=lambda x: safe_number(x.get(column_name, 0)),
            reverse=reverse
        )

        # Zaktualizuj dane i odśwież tabelę
        self.cart.items = sorted_items
        self.cart.update_cart_display(self.cart_tree)