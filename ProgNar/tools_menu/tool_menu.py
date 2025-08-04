import tkinter as tk
from tools_menu.powlekanie_menu import CoatingMenu as PowlekanieMenu
from tools_menu.blades_menu import BladesMenu
from config.utils import load_pricing_data, add_separator
from config.ui_utils import update_button_styles
from config.utils import resource_path
from config.config import FREZY_DEFAULT_DIAMETER


class ToolMenu:
    """Bazowa klasa dla menu narzędzi (frezy, wiertła itp.)."""

    def __init__(self, parent, cart, title, json_file, types, diameter_options, default_type, default_diameter=FREZY_DEFAULT_DIAMETER, z_options=["1", "2", "3", "4", "5", "6"], default_z="4"):
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
            z_options (list): Lista opcji ilości ostrzy.
            default_z (str): Domyślna ilość ostrzy.
        """
        self.parent = parent
        self.cart = cart
        self.pricing_data = load_pricing_data(json_file)
        self.uslugi_data = load_pricing_data(resource_path("data/cennik_uslugi.json"))
        print(f"uslugi_data: {self.uslugi_data}")  # Debugowanie

        # Inicjalizacja zmiennych
        self.type_var = tk.StringVar(value=default_type)
        self.diameter_var = tk.StringVar(value=default_diameter)
        self.chwyt_var = tk.StringVar(value=default_diameter)
        self.z_var = tk.StringVar(value=default_z)
        self.quantity_var = tk.StringVar(value="1")
        self.ciecie_var = tk.BooleanVar(value=False)

        # Tworzenie okna
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("500x700")

        # Typ narzędzia
        tk.Label(self.top, text="Wybierz typ:", font=("Arial", 12)).pack(pady=5)
        self.type_buttons = {}
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=5)
        for display_name, json_name in types:
            btn = tk.Button(button_frame, text=display_name, width=10,
                            command=lambda t=json_name: self.select_type(t))
            btn.pack(side="left", padx=5)
            self.type_buttons[json_name] = btn
        update_button_styles(self.type_buttons, default_type)
        add_separator(self.top)

        # Średnica i średnica chwytu
        diameter_frame = tk.Frame(self.top)
        diameter_frame.pack(pady=5)
        tk.Label(diameter_frame, text="Średnica (mm):", font=("Arial", 12)).pack(side="left", padx=5)
        self.diameter_buttons = {}
        diameter_buttons_frame = tk.Frame(diameter_frame)
        diameter_buttons_frame.pack(pady=5)
        for display_name, value in diameter_options:
            btn = tk.Button(diameter_buttons_frame, text=display_name, width=6,
                            command=lambda v=value: self.select_diameter(v))
            btn.pack(side="left", padx=2)
            self.diameter_buttons[value] = btn
        update_button_styles(self.diameter_buttons, default_diameter)

        self.diameter_entry = tk.Entry(diameter_frame, textvariable=self.diameter_var, width=10)
        self.diameter_entry.pack(side="left", padx=5)
        tk.Label(diameter_frame, text="Średnica chwytu (mm):", font=("Arial", 12)).pack(side="left", padx=5)
        self.chwyt_entry = tk.Entry(diameter_frame, textvariable=self.chwyt_var, width=10)
        self.chwyt_entry.pack(side="left", padx=5)
        self.diameter_entry.bind("<KeyRelease>", self.on_diameter_entry_change)
        self.chwyt_entry.bind("<KeyRelease>", self.on_chwyt_entry_change)
        add_separator(self.top)

        # Ilość ostrzy
        self.blades_menu = BladesMenu(self.top, self.z_var, self.update_z_and_price, z_options, default_z)
        add_separator(self.top)

        # Ilość sztuk i cięcie
        quantity_frame = tk.Frame(self.top)
        quantity_frame.pack(pady=5)
        tk.Label(quantity_frame, text="Ilość sztuk:", font=("Arial", 12)).pack(side="left", padx=5)
        self.quantity_entry = tk.Entry(quantity_frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.pack(side="left", padx=5)
        self.quantity_entry.bind("<KeyRelease>", self.update_price)

        self.ciecie_check = tk.Checkbutton(quantity_frame, text="Cięcie", variable=self.ciecie_var, command=self.update_price)
        self.ciecie_check.pack(side="left", padx=5)
        add_separator(self.top)

        # Menu powlekania
        self.powlekanie_menu = PowlekanieMenu(self.top, self.update_price)
        add_separator(self.top)

        # Etykiety cen
        self.price_label = tk.Label(self.top, text="Cena jednostkowa: 0.00 PLN", font=("Arial", 10))
        self.price_label.pack(pady=5)
        self.powlekanie_menu.coating_price_label.pack(pady=5)
        self.total_price_label = tk.Label(self.top, text="Wartość: 0.00 PLN", font=("Arial", 12, "bold"))
        self.total_price_label.pack(pady=5)

        # Przyciski akcji
        self.add_button = tk.Button(self.top, text="Dodaj do koszyka", font=("Arial", 12), command=self.add_to_cart)
        self.add_button.pack(pady=5)
        tk.Button(self.top, text="Zamknij", font=("Arial", 12), command=self.top.destroy).pack(pady=5)

        self.update_price()

    def on_chwyt_entry_change(self, event=None):
        """Waliduje wprowadzoną wartość średnicy chwytu."""
        try:
            chwyt = float(self.chwyt_var.get())
            if chwyt <= 0:
                self.chwyt_var.set("12")
        except ValueError:
            self.chwyt_var.set("12")
        self.update_price()

    def map_diameter_to_range(self, diameter):
        """Mapuje średnicę na zakres z pliku JSON."""
        try:
            diameter = float(diameter)
            if diameter <= 0:
                return None
            selected_type = self.type_var.get()
            type_data = self.pricing_data.get(selected_type, {})
            # Obsługa różnych struktur JSON (frezy i wiertła)
            if "ilosc_ostrzy" in type_data:
                # Struktura dla frezów
                for z_key in type_data.get("ilosc_ostrzy", {}).values():
                    for item in z_key.get("cennik", []):
                        zakres = item.get("zakres_srednicy", "")
                        min_diam, max_diam = self.parse_diameter_range(zakres)
                        if min_diam is not None and max_diam is not None and min_diam <= diameter <= max_diam:
                            return zakres
            else:
                # Struktura dla wierteł
                for item in type_data.get("zakres_srednicy", []):
                    zakres = item.get("zakres_srednicy", "")
                    min_diam, max_diam = self.parse_diameter_range(zakres)
                    if min_diam is not None and max_diam is not None and min_diam <= diameter <= max_diam:
                        return zakres
            return None
        except (ValueError, TypeError):
            return None

    def parse_diameter_range(self, zakres):
        """Parsuje zakres średnicy (np. 'do 6.0' lub '6.1 - 8.0') na min i max."""
        try:
            if "do" in zakres:
                max_diam = float(zakres.replace("do ", ""))
                return 0.0, max_diam
            elif "-" in zakres:
                min_diam, max_diam = map(float, zakres.split(" - "))
                return min_diam, max_diam
            return None, None
        except (ValueError, TypeError):
            return None, None

    def select_type(self, type_name):
        """Ustawia wybrany typ i aktualizuje interfejs."""
        self.type_var.set(type_name)
        update_button_styles(self.type_buttons, type_name)
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
        update_button_styles(self.diameter_buttons, diameter)
        self.update_z_and_price()

    def on_diameter_entry_change(self, event=None):
        """Odznacza przyciski średnicy i aktualizuje cenę."""
        update_button_styles(self.diameter_buttons, None)
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

    def update_z_and_price(self):
        """Zachowuje ilość ostrzy, jeśli prawidłowa, i aktualizuje cenę."""
        current_z = self.z_var.get()
        try:
            z_value = float(current_z)
            if not z_value.is_integer():
                self.z_var.set(self.blades_menu.z_options[0])
                self.blades_menu.z_entry.delete(0, tk.END)
                self.blades_menu.z_entry.insert(0, self.blades_menu.z_options[0])
                update_button_styles(self.blades_menu.z_buttons, self.blades_menu.z_options[0])
            else:
                self.z_var.set(current_z)
                self.blades_menu.z_entry.delete(0, tk.END)
                self.blades_menu.z_entry.insert(0, current_z)
                update_button_styles(self.blades_menu.z_buttons, current_z)
        except (ValueError, TypeError):
            self.z_var.set(self.blades_menu.z_options[0])
            self.blades_menu.z_entry.delete(0, tk.END)
            self.blades_menu.z_entry.insert(0, self.blades_menu.z_options[0])
            update_button_styles(self.blades_menu.z_buttons, self.blades_menu.z_options[0])
        self.price_label.config(text="Cena jednostkowa: 0.00 PLN")
        self.powlekanie_menu.coating_price_label.config(text="Cena powłoki: 0.00 PLN")
        self.total_price_label.config(text="Wartość: 0.00 PLN")
        self.update_price()

    def get_cutting_price(self, diameter):
        """Pobiera cenę cięcia na podstawie średnicy."""
        try:
            diam_float = float(diameter)
            if diam_float <= 12.0:
                price = self.uslugi_data.get("Ciecie", {}).get("cennik", [{}])[0].get("1 - 12", 0.0)
                print(f"Średnica: {diam_float}, cena cięcia (1 - 12): {price}")
                return price
            elif 12.1 <= diam_float <= 50.0:
                price = self.uslugi_data.get("Ciecie", {}).get("cennik", [{}])[0].get("12.1 - 50", 0.0)
                print(f"Średnica: {diam_float}, cena cięcia (12.1 - 50): {price}")
                return price
            else:
                print(f"Średnica: {diam_float}, cena cięcia: 0.0 (poza zakresem)")
                return 0.0
        except (ValueError, TypeError) as e:
            print(f"Błąd w get_cutting_price: {str(e)}")
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