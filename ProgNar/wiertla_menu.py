import tkinter as tk
from tkinter import messagebox
from tool_menu import ToolMenu
from utils import load_pricing_data, format_price, validate_positive_int

class WiertlaMenu(ToolMenu):
    """Klasa obsługująca menu wierteł, dziedzicząca po ToolMenu."""

    def __init__(self, parent, cart):
        types = [
            ("Wiertło spiralne", "Wiertlo spiralne"),
            ("Wiertło stopniowe", "Wiertlo stopniowe"),
            # Dodaj inne typy wierteł
        ]
        diameter_options = [("φ3", "3"), ("φ6", "6"), ("φ8", "8"), ("φ10", "10")]
        super().__init__(parent, cart, "Menu wierteł", "data/cennik_wiertla.json", types, diameter_options,
                         "Wiertlo spiralne", "6")

    def map_diameter_to_range(self, diameter):
        """Mapuje wpisaną średnicę na zakres z JSON dla wierteł."""
        try:
            diameter = float(diameter)
            if diameter <= 0:
                return None
            if diameter <= 5.0:
                return "do 5.0"
            elif 5.1 <= diameter <= 10.0:
                return "5.1 - 10.0"
            elif 10.1 <= diameter <= 15.0:
                return "10.1 - 15.0"
            else:
                return None
        except (ValueError, TypeError):
            return None

    def update_price(self, event=None):
        """Aktualizuje cenę na podstawie wybranych parametrów i ilości sztuk."""
        try:
            selected_type = self.type_var.get()
            diameter_input = self.diameter_var.get()
            selected_diameter = self.map_diameter_to_range(diameter_input)
            selected_z = self.z_var.get()  # Dla wierteł może być np. liczba rowków
            quantity = validate_positive_int(self.quantity_var.get())

            if not (selected_type and selected_diameter and selected_z):
                self.price_label.config(text="Cena ostrzenia: 0.00 PLN")
                self.powlekanie_menu.coating_price_label.config(text="Cena powloki: 0.00 PLN")
                return

            price = 0.0
            type_data = self.pricing_data.get(selected_type, {})
            try:
                z_value = float(selected_z)
                if not z_value.is_integer():
                    self.price_label.config(text="Cena ostrzenia: Błąd")
                    self.powlekanie_menu.coating_price_label.config(text="Cena powloki: Błąd")
                    return
                z_key = str(int(z_value))  # Przykładowo: wiertła mogą mieć ceny dla konkretnych liczb rowków
            except (ValueError, TypeError):
                z_key = "2-4" if selected_z == "2-4" else "pozostale"

            z_data = type_data.get("ilosc_rowkow", {}).get(z_key, {})  # Dostosuj klucz do JSON
            for item in z_data.get("cennik", []):
                if item["zakres_srednicy"] == selected_diameter:
                    prices = item["ceny"]
                    if quantity == 1:
                        price = prices.get("1 szt.", 0.0)
                    elif 2 <= quantity <= 4:
                        price = prices.get("2-4 szt.", 0.0)
                    elif 5 <= quantity <= 10:
                        price = prices.get("5-10 szt.", 0.0)
                    elif 11 <= quantity <= 20:
                        price = prices.get("11-20 szt.", 0.0)
                    else:
                        price = prices.get("11-20 szt.", 0.0)
                    break

            coating_price = self.powlekanie_menu.get_coating_price(diameter_input)

            self.price_label.config(text=f"Cena ostrzenia: {format_price(price)}")
            self.powlekanie_menu.coating_price_label.config(text=f"Cena powloki: {format_price(coating_price)}")
            display_z = selected_z
            coating_display = self.powlekanie_menu.coating_var.get() if coating_price > 0.0 else "BRAK"
            if coating_price > 0.0:
                print("Cena dla", selected_type, selected_diameter, display_z, quantity, "szt.:", price,
                      "Powloka:", coating_display, format_price(coating_price))
            else:
                print("Cena dla", selected_type, selected_diameter, display_z, quantity, "szt.:", price,
                      "Powloka:", coating_display)
        except Exception as e:
            self.price_label.config(text="Cena ostrzenia: Błąd")
            self.powlekanie_menu.coating_price_label.config(text="Cena powloki: Błąd")
            print("Błąd w update_price:", str(e))

    def add_to_cart(self):
        """Dodaje wybraną pozycję do koszyka."""
        try:
            selected_type = self.type_var.get()
            diameter_input = self.diameter_var.get()
            selected_diameter = self.map_diameter_to_range(diameter_input)
            selected_z = self.z_var.get()
            quantity = validate_positive_int(self.quantity_var.get())

            if not (selected_type and selected_diameter and selected_z):
                messagebox.showerror("Błąd", "Proszę wpisać prawidłową średnicę i wybrać wszystkie parametry.")
                print("Błąd: Brak parametrów w add_to_cart", selected_type, diameter_input, selected_diameter,
                      selected_z)
                return

            price = 0.0
            type_data = self.pricing_data.get(selected_type, {})
            try:
                z_value = float(selected_z)
                if not z_value.is_integer():
                    messagebox.showerror("Błąd", "Ilość rowków musi być liczbą całkowitą.")
                    print("Błąd: Ilość rowków nie jest liczbą całkowitą:", selected_z)
                    return
                z_key = str(int(z_value))
            except (ValueError, TypeError):
                z_key = "2-4" if selected_z == "2-4" else "pozostale"

            z_data = type_data.get("ilosc_rowkow", {}).get(z_key, {})
            for item in z_data.get("cennik", []):
                if item["zakres_srednicy"] == selected_diameter:
                    prices = item["ceny"]
                    if quantity == 1:
                        price = prices.get("1 szt.", 0.0)
                    elif 2 <= quantity <= 4:
                        price = prices.get("2-4 szt.", 0.0)
                    elif 5 <= quantity <= 10:
                        price = prices.get("5-10 szt.", 0.0)
                    elif 11 <= quantity <= 20:
                        price = prices.get("11-20 szt.", 0.0)
                    else:
                        price = prices.get("11-20 szt.", 0.0)
                    break

            coating_price = self.powlekanie_menu.get_coating_price(diameter_input)

            if price == 0.0 and coating_price == 0.0:
                messagebox.showerror("Błąd", "Nie znaleziono ceny dla wybranych parametrów.")
                print("Błąd: Cena = 0 w add_to_cart")
                return

            params = {
                "Typ": selected_type,
                "Srednica": diameter_input,
                "Zakres srednicy": selected_diameter,
                "Ilosc rowkow": selected_z,
                "Ilosc sztuk": quantity
            }
            coating_params = self.powlekanie_menu.get_coating_params()
            if coating_price > 0.0:
                params["Powloka"] = coating_params.get("Powloka", "BRAK")
                params["Cena powloki"] = format_price(coating_price)
            else:
                params["Powloka"] = "BRAK"

            total_price = price + coating_price
            self.cart.add_item("Wiertła", params, quantity, total_price)
            messagebox.showinfo("Sukces",
                                f"Dodano {quantity} szt. {selected_type} (srednica: {diameter_input} mm) do koszyka.")
            display_z = selected_z
            coating_display = params["Powloka"] if coating_price > 0.0 else "BRAK"
            if coating_price > 0.0:
                print("Cena dla", selected_type, selected_diameter, display_z, quantity, "szt.:", price,
                      "Powloka:", coating_display, format_price(coating_price))
            else:
                print("Cena dla", selected_type, selected_diameter, display_z, quantity, "szt.:", price,
                      "Powloka:", coating_display)
        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas dodawania do koszyka.")
            print("Błąd w add_to_cart:", str(e))