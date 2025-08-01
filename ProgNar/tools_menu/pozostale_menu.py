# pozostale_menu.py - Moduł menu dla pozostałych pozycji

import tkinter as tk
from tkinter import ttk, messagebox
from ProgNar.config.utils import load_pricing_data, format_price, validate_positive_int


class PozostaleMenu:
    """Klasa obsługująca menu pozostałych pozycji."""

    def __init__(self, parent, cart):
        """
        Inicjalizuje menu pozostałych pozycji.
        Args:
            parent (tk.Tk): Główne okno aplikacji.
            cart (Cart): Obiekt wspólnego koszyka.
        """
        self.parent = parent
        self.cart = cart
        # Wczytywanie danych z JSON
        self.pricing_data = load_pricing_data("../data/cennik_pozostale.json")

        # Tworzenie okna menu
        self.top = tk.Toplevel(parent)
        self.top.title("Menu pozostałe")
        self.top.geometry("400x400")

        # Etykiety i pola wyboru
        tk.Label(self.top, text="Wybierz kategorię:", font=("Arial", 12)).pack(pady=10)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.top, textvariable=self.category_var, state="readonly")
        self.category_combo.pack(pady=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.update_items)

        tk.Label(self.top, text="Wybierz produkt:", font=("Arial", 12)).pack(pady=5)
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(self.top, textvariable=self.item_var, state="readonly")
        self.item_combo.pack(pady=5)
        self.item_combo.bind("<<ComboboxSelected>>", self.update_price)

        tk.Label(self.top, text="Ilość sztuk:", font=("Arial", 12)).pack(pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(self.top, textvariable=self.quantity_var)
        self.quantity_entry.pack(pady=5)

        self.price_label = tk.Label(self.top, text="Cena: 0.00 PLN", font=("Arial", 12))
        self.price_label.pack(pady=10)

        # Przyciski
        tk.Button(self.top, text="Dodaj do koszyka", font=("Arial", 12), command=self.add_to_cart).pack(pady=5)
        tk.Button(self.top, text="Zamknij", font=("Arial", 12), command=self.top.destroy).pack(pady=5)

        # Inicjalizacja combobox z kategoriami
        self.update_categories()

    def update_categories(self):
        """Aktualizuje listę kategorii w combobox."""
        if not self.pricing_data:
            self.category_combo["values"] = ["Brak danych"]
            return

        categories = list(self.pricing_data.keys())
        self.category_combo["values"] = categories
        if categories:
            self.category_combo.set(categories[0])
            self.update_items()

    def update_items(self, event=None):
        """Aktualizuje listę produktów na podstawie wybranej kategorii."""
        selected_category = self.category_var.get()
        self.item_combo.set("")
        self.price_label.config(text="Cena: 0.00 PLN")

        if not selected_category:
            return

        items = [item["name"] for item in self.pricing_data.get(selected_category, [])]
        self.item_combo["values"] = items
        if items:
            self.item_combo.set(items[0])
            self.update_price()

    def update_price(self, event=None):
        """Aktualizuje cenę na podstawie wybranego produktu."""
        selected_category = self.category_var.get()
        selected_item = self.item_var.get()

        if not (selected_category and selected_item):
            return

        price = 0.0
        for item in self.pricing_data.get(selected_category, []):
            if item["name"] == selected_item:
                price = float(item["price"])
                break

        self.price_label.config(text=f"Cena: {format_price(price)}")

    def add_to_cart(self):
        """Dodaje wybraną pozycję do koszyka."""
        selected_category = self.category_var.get()
        selected_item = self.item_var.get()
        quantity = validate_positive_int(self.quantity_var.get())

        if not (selected_category and selected_item):
            messagebox.showerror("Błąd", "Proszę wybrać wszystkie parametry.")
            return

        price = 0.0
        for item in self.pricing_data.get(selected_category, []):
            if item["name"] == selected_item:
                price = float(item["price"])
                break

        params = {
            "Kategoria": selected_category,
            "Nazwa": selected_item
        }
        self.cart.add_item("Pozostałe", params, quantity, price)
        messagebox.showinfo("Sukces", f"Dodano {quantity} szt. {selected_item} do koszyka.")