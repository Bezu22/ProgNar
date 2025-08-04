import tkinter as tk
from tkinter import messagebox
from tools_menu.tool_menu import ToolMenu
from config.utils import load_pricing_data, format_price, validate_positive_int,get_price_for_quantity
from config.ui_utils import update_button_styles
from config.config import WIERTLA_TYPES, WIERTLA_DIAMETER_OPTIONS, WIERTLA_Z_OPTIONS, WIERTLA_DEFAULT_Z
from config.utils import resource_path

class WiertlaMenu(ToolMenu):
    """Klasa obsługująca menu wierteł, dziedzicząca po ToolMenu."""
    def __init__(self, parent, cart, main_app=None, edit_index=None):
        """
        Inicjalizuje menu wierteł.
        Args:
            parent: Widget nadrzędny.
            cart: Obiekt koszyka.
            main_app: Referencja do głównej aplikacji.
            edit_index: Indeks edytowanej pozycji w koszyku (lub None).
        """
        super().__init__(parent, cart, "Menu wierteł", resource_path("../data/cennik_wiertla.json"), WIERTLA_TYPES, WIERTLA_DIAMETER_OPTIONS,
                         WIERTLA_TYPES[0][1], WIERTLA_DIAMETER_OPTIONS[0][1], WIERTLA_Z_OPTIONS, WIERTLA_DEFAULT_Z)
        self.main_app = main_app
        self.edit_index = edit_index

        # Wypełnienie pól w trybie edycji
        if self.edit_index is not None:
            edit_item = self.cart.items[self.edit_index]
            self.type_var.set(edit_item['params'].get('Typ', WIERTLA_TYPES[0][1]))
            diameter = edit_item['params'].get('Srednica', WIERTLA_DIAMETER_OPTIONS[0][1])
            self.diameter_var.set(diameter)
            self.diameter_entry.delete(0, tk.END)
            self.diameter_entry.insert(0, diameter)
            z_value = edit_item['params'].get('Ilosc ostrzy', WIERTLA_DEFAULT_Z)
            self.z_var.set(z_value)
            self.blades_menu.z_entry.delete(0, tk.END)
            self.blades_menu.z_entry.insert(0, z_value)
            self.quantity_var.set(str(edit_item['quantity']))
            self.chwyt_var.set(edit_item['params'].get('fiChwyt', WIERTLA_DIAMETER_OPTIONS[0][1]))
            self.ciecie_var.set(True if edit_item['params'].get('ciecie', '-') == '+' else False)
            powloka = edit_item['params'].get('Powloka', 'BRAK')
            self.powlekanie_menu.coating_var.set(powloka)
            if powloka != 'BRAK':
                self.powlekanie_menu.length_var.set(edit_item['params'].get('Długość całkowita', ''))
                self.powlekanie_menu.toggle_coating_options()
            self.add_button.config(text="Zapisz zmiany")
            update_button_styles(self.type_buttons, self.type_var.get())
            update_button_styles(self.diameter_buttons, diameter)
            update_button_styles(self.blades_menu.z_buttons, z_value)

        self.update_price()

    def update_price(self, event=None):
        """Aktualizuje cenę na podstawie wybranych parametrów i ilości sztuk."""
        try:
            selected_type = self.type_var.get()
            diameter_input = self.diameter_var.get()
            selected_diameter = self.map_diameter_to_range(diameter_input)
            selected_z = self.z_var.get()
            quantity = validate_positive_int(self.quantity_var.get())

            if not (selected_type and selected_diameter and selected_z):
                self.price_label.config(text="Cena jednostkowa: 0.00 PLN")
                self.powlekanie_menu.coating_price_label.config(text="Cena powłoki: 0.00 PLN")
                self.total_price_label.config(text="Wartość: 0.00 PLN")
                print("Brak parametrów: typ, średnica lub ilość ostrzy")
                return

            sharpening_price = 0.0
            type_data = self.pricing_data.get(selected_type, {})
            for item in type_data.get("zakres_srednicy", []):
                if item["zakres_srednicy"] == selected_diameter:
                    prices = item["ceny"]
                    sharpening_price = get_price_for_quantity(prices, quantity)
                    break
            else:
                sharpening_price = 0.0

            coating_price = self.powlekanie_menu.get_coating_price(diameter_input)
            cutting_price = 0.0
            if self.ciecie_var.get():
                cutting_price = self.get_cutting_price(diameter_input)

            unit_price = sharpening_price + cutting_price
            total_price = self._calculate_total_price(sharpening_price, cutting_price, coating_price, quantity)

            self.price_label.config(text=f"Cena jednostkowa: {format_price(unit_price)}")
            self.powlekanie_menu.coating_price_label.config(text=f"Cena powłoki: {format_price(coating_price)}")
            self.total_price_label.config(text=f"Wartość: {format_price(total_price)}")
            coating_display = self.powlekanie_menu.coating_var.get() or "BRAK"
            ciecie_display = "+" if self.ciecie_var.get() else "-"
            print(f"{selected_type} {diameter_input} {selected_z} {quantity} szt.: {sharpening_price} Cięcie: {ciecie_display} Powłoka: {coating_display}")
        except Exception as e:
            self.price_label.config(text="Cena jednostkowa: Błąd")
            self.powlekanie_menu.coating_price_label.config(text="Cena powłoki: Błąd")
            self.total_price_label.config(text="Wartość: Błąd")
            print(f"Błąd w update_price: {str(e)}")

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

            sharpening_price = 0.0
            type_data = self.pricing_data.get(selected_type, {})
            for item in type_data.get("zakres_srednicy", []):
                if item["zakres_srednicy"] == selected_diameter:
                    prices = item["ceny"]
                    sharpening_price = get_price_for_quantity(prices, quantity)
                    break
            else:
                sharpening_price = 0.0

            coating_price = self.powlekanie_menu.get_coating_price(diameter_input)
            coating_name = self.powlekanie_menu.coating_var.get() or "BRAK"
            cutting_price = 0.0
            if self.ciecie_var.get():
                cutting_price = self.get_cutting_price(diameter_input)

            if sharpening_price == 0.0 and coating_price == 0.0 and cutting_price == 0.0:
                messagebox.showerror("Błąd", "Nie znaleziono ceny dla wybranych parametrów.")
                print("Błąd: Cena = 0 w add_to_cart")
                return

            params = {
                "Typ": selected_type,
                "Srednica": diameter_input,
                "Zakres srednicy": selected_diameter,
                "Ilosc ostrzy": selected_z,
                "fiChwyt": self.chwyt_var.get(),
                "ciecie": "+" if self.ciecie_var.get() else "-",
                "Ilosc sztuk": quantity,
                "Uwagi": "-",
                "Powloka": coating_name
            }
            coating_params = self.powlekanie_menu.get_coating_params()
            if coating_name != "BRAK":
                params["Długość całkowita"] = coating_params.get("Długość całkowita", "")
                if coating_price > 0.0:
                    params["Cena powloki"] = format_price(coating_price)

            if self.edit_index is None:
                self.cart.add_item("Wiertła", params, quantity, sharpening_price, cutting_price, coating_price)
                messagebox.showinfo("Sukces", f"Dodano {quantity} szt. {selected_type} (srednica: {diameter_input} mm) do koszyka.")
            else:
                self.cart.items[self.edit_index] = {
                    'name': "Wiertła",
                    'params': params,
                    'quantity': quantity,
                    'sharpening_price': sharpening_price,
                    'cutting_price': cutting_price,
                    'coating_price': coating_price
                }
                messagebox.showinfo("Sukces", "Zaktualizowano pozycję w koszyku.")
                self.top.destroy()

            if self.main_app:
                self.main_app.update_cart_display()

            coating_display = coating_name
            ciecie_display = "+" if self.ciecie_var.get() else "-"
            print(f"{selected_type} {diameter_input} {selected_z} {quantity} szt.: {sharpening_price} Cięcie: {ciecie_display} Powłoka: {coating_display}")
        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas dodawania do koszyka.")
            print(f"Błąd w add_to_cart: {str(e)}")