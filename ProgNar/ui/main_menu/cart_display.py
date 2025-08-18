import tkinter as tk
from tkinter import ttk
from tools_menu.remarks_menu import RemarksMenu

class CartDisplay:
    def __init__(self, parent, root, cart, main_app):
        self.parent = parent
        self.root = root
        self.cart = cart
        self.main_app = main_app
        self.create_cart_table()

    def create_cart_table(self):
        """Tworzy tabelę koszyka z nagłówkami i stylami."""
        tree_scroll_frame = tk.Frame(self.parent, borderwidth=1, relief="solid")
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
        self.cart_tree.column("Uwagi", width=120, anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), anchor="center")
        style.configure("remarks_filled", font=("Arial Black", 12, "bold"), foreground="green")
        style.configure("remarks_empty", font=("Arial Black", 12, "bold"), foreground="red")
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
                    RemarksMenu(self.root, self.cart, index, self.main_app)

    def get_cart_tree(self):
        """Zwraca obiekt Treeview koszyka."""
        return self.cart_tree