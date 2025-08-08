import tkinter as tk
from tkinter import messagebox
from tools_menu.tool_menu import ToolMenu
from config.utils import load_pricing_data, format_price, validate_positive_int, get_price_for_quantity, add_separator, resource_path
from config.ui_utils import update_button_styles
from config.cart_io import save_cart_to_file
from config.config import WIERTLA_TYPES, WIERTLA_DIAMETER_OPTIONS, WIERTLA_DEFAULT_DIAMETER, WIERTLA_DEFAULT_Z

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
        super().__init__(parent, cart, "Menu wierteł", resource_path("data/cennik_wiertla.json"), WIERTLA_TYPES, WIERTLA_DIAMETER_OPTIONS,
                         WIERTLA_TYPES[0][1], WIERTLA_DEFAULT_DIAMETER, [], WIERTLA_DEFAULT_Z, type_button_width=20)
        self.main_app = main_app
        self.edit_index = edit_index
        self.top.attributes('-topmost', True)  # Okno zawsze na wierzchu

        # Etykiety cen
        self.price_label = tk.Label(self.top, text="Cena jednostkowa: 0.00 PLN", font=("Arial", 10))
        self.price_label.pack(pady=5)
        self.powlekanie_menu.coating_price_label.pack(pady=5)
        self.total_price_label = tk.Label(self.top, text="Wartość: 0.00 PLN", font=("Arial", 12, "bold"))
        self.total_price_label.pack(pady=5)
        add_separator(self.top)

        # Checkbox IK i pole tekstowe
        self.ik_var = tk.BooleanVar(value=False)
        self.ik_value_var = tk.StringVar(value=self.quantity_var.get())
        self.ik_check = tk.Checkbutton(self.quantity_menu, text="IK", variable=self.ik_var, command=self.toggle_ik_entry)
        self.ik_check.pack(side="left", padx=5)
        self.ik_entry = tk.Entry(self.quantity_menu, textvariable=self.ik_value_var, width=4, state='disabled')
        self.ik_entry.pack(side="left", padx=5)
        self.ik_entry.bind("<KeyRelease>", self.validate_ik_value)
        self.quantity_entry.bind("<KeyRelease>", self.validate_ik_value)  # Walidacja IK przy zmianie ilości sztuk

        # Wypełnienie pól w trybie edycji
        if self.edit_index is not None:
            edit_item = self.cart.items[self.edit_index]
            self.type_var.set(edit_item['params'].get('Typ', WIERTLA_TYPES[0][1]).replace(" (IK:", "").split(")")[0])
            diameter = edit_item['params'].get('Srednica', WIERTLA_DIAMETER_OPTIONS[0][1])
            self.diameter_var.set(diameter)
            self.diameter_entry.delete(0, tk.END)
            self.diameter_entry.insert(0, diameter)
            z_value = edit_item['params'].get('Ilosc ostrzy', WIERTLA_DEFAULT_Z)
            self.z_var.set(z_value)
            self.z_entry.delete(0, tk.END)
            self.z_entry.insert(0, z_value)
            self.quantity_var.set(str(edit_item['quantity']))
            self.chwyt_var.set(edit_item['params'].get('fiChwyt', WIERTLA_DIAMETER_OPTIONS[0][1]))
            self.ciecie_var.set(True if edit_item['params'].get('ciecie', '-') == '+' else False)
            powloka = edit_item['params'].get('Powloka', 'BRAK')
            self.powlekanie_menu.coating_var.set(powloka)
            if powloka != 'BRAK':
                self.powlekanie_menu.length_var.set(edit_item['params'].get('Długość całkowita', ''))
                self.powlekanie_menu.toggle_coating_options()
            # Obsługa IK w trybie edycji
            if "(IK:" in edit_item['params'].get('Typ', ''):
                ik_value = edit_item['params']['Typ'].split("(IK:")[1].split(")")[0]
                self.ik_var.set(True)
                self.ik_value_var.set(ik_value)
                self.ik_entry.config(state='normal')
            self.add_button.config(text="Zapisz zmiany")
            update_button_styles(self.type_buttons, self.type_var.get())
            update_button_styles(self.diameter_buttons, diameter)

        self.update_price()

    def toggle_ik_entry(self):
        """Włącza/wyłącza pole tekstowe IK i ustawia domyślną wartość."""
        if self.ik_var.get():
            self.ik_entry.config(state='normal')
            self.ik_value_var.set(self.quantity_var.get())
        else:
            self.ik_entry.config(state='disabled')
            self.ik_value_var.set(self.quantity_var.get())
        self.update_price()

    def validate_s_value(self, event=None):
        """Waliduje wartość w polu S."""
        if not self.s_var.get():
            return
        s_value = self.s_value_var.get()
        try:
            s_int = int(s_value)
            quantity = validate_positive_int(self.quantity_var.get())
            if s_int > quantity or s_int < 0:
                self.s_value_var.set(str(quantity))
        except ValueError:
            self.s_value_var.set(self.quantity_var.get())

    def map_diameter_to_range(self, diameter):
        """Mapuje średnicę na zakres z pliku cennik_wiertla.json."""
        try:
            diameter = float(diameter)
            if diameter <= 0:
                return None
            selected_type = self.type_var.get()
            z_key = WIERTLA_DEFAULT_Z  # Stała liczba ostrzy dla wierteł

            # Mapowanie typów na klucze w cennik_wiertla.json
            json_type = "Wiertlo" if selected_type in ["Wiertło", "Wiertło długie"] else "Wiertlo stopniowe"

            type_data = self.pricing_data.get(json_type, {})
            if not type_data:
                print(f"Brak danych dla typu {json_type} w pricing_data")
                return None

            z_data = type_data.get("ilosc_ostrzy", {}).get(z_key, {})
            if not z_data:
                print(f"Brak danych dla z={z_key} w typie {json_type}")
                return None

            for item in z_data.get("cennik", []):
                zakres = item.get("zakres_srednicy", "")
                min_diam, max_diam = self.parse_diameter_range(zakres)
                if min_diam is not None and max_diam is not None:
                    if min_diam == 0.0 and diameter <= max_diam + 0.0001:
                        return zakres
                    if min_diam <= diameter <= max_diam + 0.0001:
                        return zakres
            print(f"Brak zakresu dla średnicy {diameter} w typie {json_type}, z={z_key}")
            return None
        except (ValueError, TypeError) as e:
            print(f"Błąd w map_diameter_to_range: {str(e)}")
            return None

    def update_price(self, event=None):
        """Aktualizuje cenę na podstawie wybranych parametrów i ilości sztuk."""
        try:
            selected_type = self.type_var.get()
            diameter_input = self.diameter_var.get()
            selected_diameter = self.map_diameter_to_range(diameter_input)
            quantity = validate_positive_int(self.quantity_var.get())

            # Walidacja IK przy zmianie ilości sztuk
            if self.ik_var.get():
                self.validate_ik_value()

            # Walidacja diameter_input
            try:
                float(diameter_input)
            except ValueError:
                self.price_label.config(text="Cena jednostkowa: Błąd")
                self.powlekanie_menu.coating_price_label.config(text="Cena powłoki: Błąd")
                self.total_price_label.config(text="Wartość: Błąd")
                return

            if not (selected_type and selected_diameter):
                self.price_label.config(text="Cena jednostkowa: 0.00 PLN")
                self.powlekanie_menu.coating_price_label.config(text="Cena powłoki: 0.00 PLN")
                self.total_price_label.config(text="Wartość: 0.00 PLN")
                return

            sharpening_price = 0.0
            z_key = WIERTLA_DEFAULT_Z  # Stała liczba ostrzy dla wierteł
            json_type = "Wiertlo" if selected_type in ["Wiertło", "Wiertło długie"] else "Wiertlo stopniowe"
            type_data = self.pricing_data.get(json_type, {})
            z_data = type_data.get("ilosc_ostrzy", {}).get(z_key, {})
            for item in z_data.get("cennik", []):
                if item.get("zakres_srednicy") == selected_diameter:
                    prices = item.get("ceny", {})
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
            selected_z = WIERTLA_DEFAULT_Z  # Stała liczba ostrzy
            quantity = validate_positive_int(self.quantity_var.get())

            # Walidacja IK
            ik_value = 0
            if self.ik_var.get():
                try:
                    ik_value = int(self.ik_value_var.get())
                    if ik_value > quantity or ik_value < 0:
                        self.ik_value_var.set(str(quantity))
                        ik_value = quantity
                except ValueError:
                    self.ik_value_var.set(str(quantity))
                    ik_value = quantity

            if not (selected_type and selected_diameter):
                messagebox.showerror("Błąd", "Proszę wpisać prawidłową średnicę i wybrać wszystkie parametry.")
                print("Błąd: Brak parametrów w add_to_cart", selected_type, diameter_input, selected_diameter)
                return

            sharpening_price = 0.0
            z_key = WIERTLA_DEFAULT_Z
            json_type = "Wiertlo" if selected_type in ["Wiertło", "Wiertło długie"] else "Wiertlo stopniowe"
            type_data = self.pricing_data.get(json_type, {})
            z_data = type_data.get("ilosc_ostrzy", {}).get(z_key, {})
            for item in z_data.get("cennik", []):
                if item.get("zakres_srednicy") == selected_diameter:
                    prices = item.get("ceny", {})
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

            # Dodanie suffixu (IK:wartosc) do typu, jeśli IK jest zaznaczone
            display_type = selected_type
            if self.ik_var.get():
                display_type = f"{selected_type} (IK:{self.ik_value_var.get()})"

            params = {
                "Typ": display_type,
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
                self.cart.add_item("Wiertła", params, quantity, sharpening_price, cutting_price, coating_price, main_app=self.main_app)
                messagebox.showinfo("Sukces", f"Dodano {quantity} szt. {display_type} (srednica: {diameter_input} mm) do koszyka.")
            else:
                self.cart.items[self.edit_index] = {
                    'name': "Wiertła",
                    'params': params,
                    'quantity': quantity,
                    'sharpening_price': sharpening_price,
                    'cutting_price': cutting_price,
                    'coating_price': coating_price
                }
                if self.main_app:
                    save_cart_to_file(self.cart, self.main_app.client_name)  # Zapis do pliku tymczasowego po edycji
                messagebox.showinfo("Sukces", "Zaktualizowano pozycję w koszyku.")
                self.top.destroy()

            if self.main_app:
                self.main_app.cart.update_cart_display(
                    self.main_app.cart_tree,
                    self.main_app.bottom.suma_uslug_label,
                    self.main_app.bottom.suma_powlekanie_label,
                    self.main_app.bottom.suma_total_label
                )
                if self.edit_index is None:
                    self.top.focus_force()  # Przywraca fokus na okno WiertlaMenu po dodaniu

            coating_display = coating_name
            ciecie_display = "+" if self.ciecie_var.get() else "-"
            ik_display = f"(IK:{self.ik_value_var.get()})" if self.ik_var.get() else ""
            print(f"{selected_type}{ik_display} {diameter_input} {selected_z} {quantity} szt.: {sharpening_price} Cięcie: {ciecie_display} Powłoka: {coating_display}")
        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas dodawania do koszyka.")
            print(f"Błąd w add_to_cart: {str(e)}")