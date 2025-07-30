import tkinter as tk
from tkinter import messagebox
from powlekanie_menu import CoatingMenu as PowlekanieMenu
from utils import load_pricing_data, format_price, validate_positive_int

class ToolMenu:
    """Bazowa klasa dla menu narzędzi (frezy, wiertła itp.)."""

    def __init__(self, parent, cart, title, json_file, types, diameter_options, default_type, default_diameter):
        """
        Inicjalizuje menu narzędzia.
        Args:
            parent (tk.Tk): Główne okno aplikacji.
            cart (Cart): Obiekt koszyka.
            title (str): Tytuł okna.
            json_file (str): Ścieżka do pliku JSON z cennikiem.
            types (list): Lista krotek (display_name, json_name) dla typów.
            diameter_options (list): Lista krotek (display_name, value) dla średnic.
            default_type (str): Domyślny typ narzędzia.
            default_diameter (str): Domyślna średnica.
        """
        self.parent = parent
        self.cart = cart
        self.pricing_data = load_pricing_data(json_file)
        self.uslugi_data = load_pricing_data('data/cennik_uslugi.json')

        # Inicjalizacja zmiennych
        self.type_var = tk.StringVar(value=default_type)
        self.diameter_var = tk.StringVar(value=default_diameter)
        self.chwyt_var = tk.StringVar(value=default_diameter)
        self.z_var = tk.StringVar(value="4")
        self.quantity_var = tk.StringVar(value="1")
        self.ciecie_var = tk.BooleanVar(value=False)

        # Tworzenie okna
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("500x700")

        # Typ narzędzia
        tk.Label(self.top, text="Wybierz typ:", font=("Arial", 12)).pack(pady=10)
        self.type_buttons = {}
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=5)
        for display_name, json_name in types:
            btn = tk.Button(button_frame, text=display_name, width=10,
                            command=lambda t=json_name: self.select_type(t))
            btn.pack(side="left", padx=5)
            self.type_buttons[json_name] = btn

        # Średnica i średnica chwytu w jednej linii
        diameter_frame = tk.Frame(self.top)
        diameter_frame.pack(pady=5)
        tk.Label(diameter_frame, text="Średnica (mm):", font=("Arial", 12)).pack(side="left", padx=5)
        self.diameter_buttons = {}
        diameter_buttons_frame = tk.Frame(diameter_frame)
        diameter_buttons_frame.pack(side="left", pady=5)
        for display_name, value in diameter_options:
            btn = tk.Button(diameter_buttons_frame, text=display_name, width=6,
                            command=lambda v=value: self.select_diameter(v))
            btn.pack(side="left", padx=5)
            self.diameter_buttons[value] = btn

        self.diameter_entry = tk.Entry(diameter_frame, textvariable=self.diameter_var, width=10)
        self.diameter_entry.pack(side="left", padx=5)
        self.diameter_entry.bind("<KeyRelease>", self.on_diameter_entry_change)

        tk.Label(diameter_frame, text="φ Chwytu:", font=("Arial", 12)).pack(side="left", padx=5)
        self.chwyt_entry = tk.Entry(diameter_frame, textvariable=self.chwyt_var, width=10)
        self.chwyt_entry.pack(side="left", padx=5)

        # Ilość ostrzy
        tk.Label(self.top, text="Wybierz ilość ostrzy:", font=("Arial", 12)).pack(pady=5)
        self.z_frame = tk.Frame(self.top)
        self.z_frame.pack(pady=5)
        self.z_buttons = {}
        z_options = ["1", "2", "3", "4", "5", "6"]
        for z in z_options:
            btn = tk.Button(self.z_frame, text=z, width=6,
                            command=lambda v=z: self.select_z(v))
            btn.pack(side="left", padx=5)
            self.z_buttons[z] = btn
            btn.config(bg="lightgreen" if z == "4" else "SystemButtonFace",
                       relief="sunken" if z == "4" else "raised")

        self.z_entry = tk.Entry(self.top, textvariable=self.z_var, width=10)
        self.z_entry.pack(pady=5)
        self.z_entry.bind("<KeyRelease>", self.on_z_entry_change)

        # Ilość sztuk i cięcie w jednej linii
        quantity_frame = tk.Frame(self.top)
        quantity_frame.pack(pady=5)
        tk.Label(quantity_frame, text="Ilość sztuk:", font=("Arial", 12)).pack(side="left", padx=5)
        self.quantity_entry = tk.Entry(quantity_frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.pack(side="left", padx=5)
        self.quantity_entry.bind("<KeyRelease>", self.update_price)

        self.ciecie_check = tk.Checkbutton(quantity_frame, text="Cięcie", variable=self.ciecie_var, command=self.update_price)
        self.ciecie_check.pack(side="left", padx=5)

        # Menu powlekania
        self.powlekanie_menu = PowlekanieMenu(self.top, self.update_price)

        # Etykieta ceny jednostkowej (uwzględnia cięcie)
        self.price_label = tk.Label(self.top, text="Cena jednostkowa: 0.00 PLN", font=("Arial", 10))
        self.price_label.pack(pady=10)

        # Etykieta ceny powlekania
        self.powlekanie_menu.coating_price_label.pack(pady=10)

        # Etykieta wartości całkowitej
        self.total_price_label = tk.Label(self.top, text="Wartość: 0.00 PLN", font=("Arial", 12, "bold"))
        self.total_price_label.pack(pady=10)

        # Przyciski akcji
        self.add_button = tk.Button(self.top, text="Dodaj do koszyka", font=("Arial", 12), command=self.add_to_cart)
        self.add_button.pack(pady=5)
        tk.Button(self.top, text="Zamknij", font=("Arial", 12), command=self.top.destroy).pack(pady=5)

        # Inicjalizacja stylu przycisków
        for json_name, btn in self.type_buttons.items():
            btn.config(bg="lightgreen" if json_name == default_type else "SystemButtonFace",
                       relief="sunken" if json_name == default_type else "raised")
        for value, btn in self.diameter_buttons.items():
            btn.config(bg="lightgreen" if value == default_diameter else "SystemButtonFace",
                       relief="sunken" if value == default_diameter else "raised")
        self.update_price()

    def select_type(self, type_name):
        """Ustawia wybrany typ i aktualizuje interfejs."""
        self.type_var.set(type_name)
        for json_name, btn in self.type_buttons.items():
            btn.config(bg="lightgreen" if json_name == type_name else "SystemButtonFace",
                       relief="sunken" if json_name == type_name else "raised")
        self.update_price()

    def select_diameter(self, diameter):
        """Ustawia wybraną średnicę i aktualizuje styl przycisków."""
        self.diameter_var.set(diameter)
        self.diameter_entry.delete(0, tk.END)
        self.diameter_entry.insert(0, diameter)
        try:
            diam_float = float(diameter)
            if diam_float.is_integer():
                self.chwyt_var.set(str(int(diam_float)))
            else:
                self.chwyt_var.set("12")
        except ValueError:
            self.chwyt_var.set("12")
        for value, btn in self.diameter_buttons.items():
            btn.config(bg="lightgreen" if value == diameter else "SystemButtonFace",
                       relief="sunken" if value == diameter else "raised")
        self.update_z_and_price()

    def on_diameter_entry_change(self, event=None):
        """Odznacza przyciski średnicy i aktualizuje cenę."""
        for btn in self.diameter_buttons.values():
            btn.config(bg="SystemButtonFace", relief="raised")
        diameter = self.diameter_var.get()
        try:
            diam_float = float(diameter)
            if diam_float.is_integer():
                self.chwyt_var.set(str(int(diam_float)))
            else:
                self.chwyt_var.set("12")
        except ValueError:
            self.chwyt_var.set("12")
        self.update_z_and_price()

    def select_z(self, z_value):
        """Ustawia wybraną ilość ostrzy i aktualizuje styl przycisku."""
        self.z_var.set(z_value)
        self.z_entry.delete(0, tk.END)
        self.z_entry.insert(0, z_value)
        for value, btn in self.z_buttons.items():
            btn.config(bg="lightgreen" if value == z_value else "SystemButtonFace",
                       relief="sunken" if value == z_value else "raised")
        self.update_price()

    def on_z_entry_change(self, event=None):
        """Odznacza przyciski ostrzy przy wpisywaniu w pole tekstowe."""
        for btn in self.z_buttons.values():
            btn.config(bg="SystemButtonFace", relief="raised")
        self.update_price()

    def update_z_and_price(self):
        """Zachowuje ilość ostrzy, jeśli prawidłowa, i aktualizuje cenę."""
        current_z = self.z_var.get()
        try:
            z_value = float(current_z)
            if not z_value.is_integer():
                self.z_var.set("4")
                self.z_entry.delete(0, tk.END)
                self.z_entry.insert(0, "4")
                for value, btn in self.z_buttons.items():
                    btn.config(bg="lightgreen" if value == "4" else "SystemButtonFace",
                               relief="sunken" if value == "4" else "raised")
            else:
                self.z_var.set(current_z)
                self.z_entry.delete(0, tk.END)
                self.z_entry.insert(0, current_z)
                for value, btn in self.z_buttons.items():
                    btn.config(bg="lightgreen" if value == current_z else "SystemButtonFace",
                               relief="sunken" if value == current_z else "raised")
        except (ValueError, TypeError):
            self.z_var.set("4")
            self.z_entry.delete(0, tk.END)
            self.z_entry.insert(0, "4")
            for value, btn in self.z_buttons.items():
                btn.config(bg="lightgreen" if value == "4" else "SystemButtonFace",
                           relief="sunken" if value == "4" else "raised")
        self.price_label.config(text="Cena jednostkowa: 0.00 PLN")
        self.powlekanie_menu.coating_price_label.config(text="Cena powłoki: 0.00 PLN")
        self.total_price_label.config(text="Wartość: 0.00 PLN")
        self.update_price()

    def get_cutting_price(self, diameter):
        """Pobiera cenę cięcia na podstawie średnicy."""
        try:
            diam_float = float(diameter)
            if diam_float <= 12.0:
                return self.uslugi_data.get("Ciecie", {}).get("cennik", [{}])[0].get("1 - 12", 0.0)
            elif 12.1 <= diam_float <= 50.0:
                return self.uslugi_data.get("Ciecie", {}).get("cennik", [{}])[0].get("12.1 - 50", 0.0)
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0

    def _calculate_total_price(self, sharpening_price, cutting_price, coating_price, quantity):
        """Oblicza całkowitą wartość: (cena ostrzenia + cięcia + powłoki) * ilość."""
        return (sharpening_price + cutting_price + coating_price) * quantity

    def update_price(self, event=None):
        """Abstrakcyjna metoda do aktualizacji ceny - do nadpisu w podklasach."""
        raise NotImplementedError("Metoda update_price musi być zaimplementowana w podklasie.")

    def add_to_cart(self):
        """Abstrakcyjna metoda do dodawania do koszyka - do nadpisu w podklasach."""
        raise NotImplementedError("Metoda add_to_cart musi być zaimplementowana w podklasie.")

    def map_diameter_to_range(self, diameter):
        """Abstrakcyjna metoda do mapowania średnicy - do nadpisu w podklasach."""
        raise NotImplementedError("Metoda map_diameter_to_range musi być zaimplementowana w podklasie.")