# frezy_menu.py - Moduł obsługi menu frezów

import tkinter as tk
from tkinter import messagebox
from tool_menu import ToolMenu
from utils import load_pricing_data, format_price, validate_positive_int

class FrezyMenu(ToolMenu):
    """Klasa obsługująca menu frezów, dziedzicząca po ToolMenu."""
    def __init__(self, parent, cart, main_app=None, edit_index=None):
        """
        Inicjalizuje menu frezów.
        Args:
            parent: Widget nadrzędny.
            cart: Obiekt koszyka.
            main_app: Referencja do głównej aplikacji.
            edit_index: Indeks edytowanej pozycji w koszyku (lub None).
        """
        types = [
            ("Prosty", "Frez prosty"),
            ("Promieniowy", "Frez promieniowy"),
            ("Kulisty", "Frez kulisty"),
            ("Stożkowy", "Frez stozkowy")
        ]
        diameter_options = [("φ6", "6"), ("φ8", "8"), ("φ10", "10"), ("φ12", "12")]
        super().__init__(parent, cart, "Menu frezów", "data/cennik_frezy.json", types, diameter_options,
                         "Frez prosty", "12")
        self.main_app = main_app
        self.edit_index = edit_index

        ### ZMIANA ### Wypełnienie pól w trybie edycji
        if self.edit_index is not None:
            edit_item = cart.items[self.edit_index]
            self.type_var.set(edit_item['params'].get('Typ', ''))
            self.diameter_var.set(edit_item['params'].get('Srednica', ''))
            self.z_var.set(edit_item['params'].get('Ilosc ostrzy', ''))
            self.quantity_var.set(str(edit_item['quantity']))
            powloka = edit_item['params'].get('Powloka', 'BRAK')
            if powloka != 'BRAK':
                self.powlekanie_menu.coating_var.set(powloka)
                self.powlekanie_menu.length_var.set(edit_item['params'].get('Długość całkowita', ''))
                self.powlekanie_menu.toggle_coating_options()  # Pokazanie opcji powlekania
            self.add_button.config(text="Zapisz zmiany")  ### ZMIANA ### Zmiana tekstu przycisku

        self.update_price()

    def map_diameter_to_range(self, diameter):
        """Mapuje wpisaną średnicę na zakres z JSON."""
        try:
            diameter = float(diameter)
            if diameter <= 0:
                return None
            if diameter <= 6.0:
                return "do 6.0"
            elif 6.1 <= diameter <= 10.0:
                return "6.1 - 10.0"
            elif 10.1 <= diameter <= 12.0:
                return "10.1 - 12.0"
            elif 12.1 <= diameter <= 16.0:
                return "12.1 - 16.0"
            elif 16.1 <= diameter <= 20.0:
                return "16.1 - 20.0"
            elif 20.1 <= diameter <= 25.0:
                return "20.1 - 25.0"
            elif 25.1 <= diameter <= 32.0:
                return "25.1 - 32.0"
            else:
                return None
        except (ValueError, TypeError):
            return None

    def _calculate_total_price(self, price, coating_price, quantity):
        """Oblicza całkowitą wartość: (cena jednostkowa * ilość) + (cena powłoki * ilość)."""
        return (price * quantity) + (coating_price * quantity)

    def update_price(self, event=None):
        """Aktualizuje cenę na podstawie wybranych parametrów i ilości sztuk."""
        try:
            selected_type = self.type_var.get()
            diameter_input = self.diameter_var.get()
            selected_diameter = self.map_diameter_to_range(diameter_input)
            selected_z = self.z_var.get()
            quantity = validate_positive_int(self.quantity_var.get())

            if not (selected_type and selected_diameter and selected_z):
                self.price_label.config(text="Cena ostrzenia: 0.00 PLN")
                self.powlekanie_menu.coating_price_label.config(text="Cena powloki: 0.00 PLN")
                self.total_price_label.config(text="Wartość: 0.00 PLN")
                return

            price = 0.0
            type_data = self.pricing_data.get(selected_type, {})
            try:
                z_value = float(selected_z)
                if z_value.is_integer() and 2 <= z_value <= 4:
                    z_key = "2-4"
                else:
                    if not z_value.is_integer():
                        self.price_label.config(text="Cena ostrzenia: Błąd")
                        self.powlekanie_menu.coating_price_label.config(text="Cena powloki: Błąd")
                        self.total_price_label.config(text="Wartość: Błąd")
                        return
                    z_key = "pozostale"
            except (ValueError, TypeError):
                z_key = "2-4" if selected_z == "2-4" else "pozostale"

            z_data = type_data.get("ilosc_ostrzy", {}).get(z_key, {})
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
            total_price = self._calculate_total_price(price, coating_price, quantity)

            self.price_label.config(text=f"Cena ostrzenia: {format_price(price)}")
            self.powlekanie_menu.coating_price_label.config(text=f"Cena powloki: {format_price(coating_price)}")
            self.total_price_label.config(text=f"Wartość: {format_price(total_price)}")
            display_z = selected_z if selected_z != "2-4" else z_key
            coating_display = self.powlekanie_menu.coating_var.get() if coating_price > 0.0 else "BRAK"
            if coating_price > 0.0:
                print(f"{selected_type} {diameter_input} {display_z} {quantity} szt.: {price} Powloka: {coating_display} {format_price(coating_price)}")
            else:
                print(f"{selected_type} {diameter_input} {display_z} {quantity} szt.: {price} Powloka: {coating_display}")
        except Exception as e:
            self.price_label.config(text="Cena ostrzenia: Błąd")
            self.powlekanie_menu.coating_price_label.config(text="Cena powloki: Błąd")
            self.total_price_label.config(text="Wartość: Błąd")
            print("Błąd w update_price:", str(e))

    def add_to_cart(self):
        """Dodaje lub aktualizuje pozycję w koszyku."""
        try:
            selected_type = self.type_var.get()
            diameter_input = self.diameter_var.get()
            selected_diameter = self.map_diameter_to_range(diameter_input)
            selected_z = self.z_var.get()
            quantity = validate_positive_int(self.quantity_var.get())

            if not (selected_type and selected_diameter and selected_z):
                messagebox.showerror("Błąd", "Proszę wpisać prawidłową średnicę i wybrać wszystkie parametry.")
                print("Błąd: Brak parametrów w add_to_cart", selected_type, diameter_input, selected_diameter, selected_z)
                return

            price = 0.0
            type_data = self.pricing_data.get(selected_type, {})
            try:
                z_value = float(selected_z)
                if z_value.is_integer() and 2 <= z_value <= 4:
                    z_key = "2-4"
                else:
                    if not z_value.is_integer():
                        messagebox.showerror("Błąd", "Ilość ostrzy musi być liczbą całkowitą.")
                        print("Błąd: Ilość ostrzy nie jest liczbą całkowitą:", selected_z)
                        return
                    z_key = "pozostale"
            except (ValueError, TypeError):
                z_key = "2-4" if selected_z == "2-4" else "pozostale"

            z_data = type_data.get("ilosc_ostrzy", {}).get(z_key, {})
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
                "Ilosc ostrzy": selected_z,
                "Ilosc sztuk": quantity
            }
            coating_params = self.powlekanie_menu.get_coating_params()
            if coating_price > 0.0:
                params["Powloka"] = coating_params.get("Powloka", "BRAK")
                params["Długość całkowita"] = coating_params.get("Długość całkowita", "")  ### ZMIANA ### Dodano długość całkowitą
                params["Cena powloki"] = format_price(coating_price)
            else:
                params["Powloka"] = "BRAK"

            ### ZMIANA ### Aktualizacja pozycji w trybie edycji
            if self.edit_index is None:
                self.cart.add_item("Frezy", params, quantity, price, coating_price)
                messagebox.showinfo("Sukces", f"Dodano {quantity} szt. {selected_type} (srednica: {diameter_input} mm) do koszyka.")
            else:
                self.cart.items[self.edit_index] = {
                    'name': "Frezy",
                    'params': params,
                    'quantity': quantity,
                    'sharpening_price': price,
                    'coating_price': coating_price
                }
                messagebox.showinfo("Sukces", "Zaktualizowano pozycję w koszyku.")
                self.top.destroy()  ### ZMIANA ### Zamknięcie okna po edycji

            if self.main_app:
                self.main_app.update_cart_display()

            display_z = selected_z if selected_z != "2-4" else z_key
            coating_display = params["Powloka"] if coating_price > 0.0 else "BRAK"
            if coating_price > 0.0:
                print(f"{selected_type} {diameter_input} {display_z} {quantity} szt.: {price} Powloka: {coating_display} {format_price(coating_price)}")
            else:
                print(f"{selected_type} {diameter_input} {display_z} {quantity} szt.: {price} Powloka: {coating_display}")
        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas dodawania do koszyka.")
            print("Błąd w add_to_cart:", str(e))