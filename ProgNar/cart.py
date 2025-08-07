# cart.py - Moduł zarządzający wspólnym koszykiem
import tkinter as tk
from tkinter import ttk, messagebox
from tools_menu.frezy_menu import FrezyMenu
from tools_menu.wiertla_menu import WiertlaMenu
from tools_menu.pozostale_menu import PozostaleMenu
from tools_menu.uslugi_menu import UslugiMenu
from config.utils import format_price
from config.cart_io import save_cart_to_file

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, params, quantity, sharpening_price, cutting_price, coating_price, main_app=None):
        self.items.append({
            'name': name,
            'params': params,
            'quantity': quantity,
            'sharpening_price': sharpening_price,
            'cutting_price': cutting_price,
            'coating_price': coating_price
        })
        if main_app:
            save_cart_to_file(self, main_app.client_name)

    def remove_item(self, index, main_app=None):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            if main_app:
                save_cart_to_file(self, main_app.client_name)

    def clear_cart(self, main_app=None):
        self.items = []
        if main_app:
            save_cart_to_file(self, main_app.client_name)

    def update_cart_display(self, cart_tree, suma_uslug_label, suma_powlekanie_label, suma_total_label):
        cart_tree.delete(*cart_tree.get_children())

        for idx, item in enumerate(self.items):
            params = item['params']
            quantity = item['quantity']
            sharpening_price = item['sharpening_price']
            cutting_price = item.get('cutting_price', 0.0)
            coating_price = item['coating_price']

            cena_szt = format_price(sharpening_price + cutting_price)
            wartosc = format_price((sharpening_price + cutting_price) * quantity)
            cena_powlekania_szt = format_price(coating_price) if coating_price > 0 else "-"
            wartosc_powlekania = format_price(coating_price * quantity) if coating_price > 0 else "-"
            uwagi = "✓" if params.get('Uwagi', '-') != '-' else "−"
            remarks_tag = "remarks_filled" if uwagi == "✓" else "remarks_empty"

            cart_tree.insert("", tk.END, iid=str(idx), values=(
                idx + 1,
                params.get('Typ', item['name']),
                params.get('Srednica', ''),
                params.get('fiChwyt', ''),
                params.get('Ilosc ostrzy', ''),
                quantity,
                params.get('ciecie', '-'),
                cena_szt,
                wartosc,
                params.get('Powloka', 'BRAK'),
                params.get('Długość całkowita', ''),
                cena_powlekania_szt,
                wartosc_powlekania,
                uwagi
            ), tags=[remarks_tag if i == 13 else "" for i in range(14)])

        suma_uslug = sum(
            (item['sharpening_price'] + item.get('cutting_price', 0.0)) * item['quantity'] for item in self.items)
        suma_powlekanie = sum(
            item['coating_price'] * item['quantity'] for item in self.items if item['coating_price'] > 0)
        suma_total = suma_uslug + suma_powlekanie

        suma_uslug_label.config(text=f"Suma usług: {format_price(suma_uslug)} PLN")
        suma_powlekanie_label.config(text=f"Suma powlekanie: {format_price(suma_powlekanie)} PLN")
        suma_total_label.config(text=f"Suma: {format_price(suma_total)} PLN")

    def delete_selected(self, cart_tree, main_app=None):
        selected = cart_tree.selection()
        if selected:
            index = cart_tree.index(selected[0])
            self.remove_item(index, main_app)
            return True
        return False

    def edit_selected(self, cart_tree, root, main_app, edit_index=None):
        selected = cart_tree.selection()
        if selected:
            index = int(selected[0])
            item = self.items[index]
            if item['name'] == "Frezy":
                FrezyMenu(root, self, main_app=main_app, edit_index=index)
            elif item['name'] == "Wiertła":
                WiertlaMenu(root, self, main_app=main_app, edit_index=index)
            elif item['name'] == "Pozostałe":
                PozostaleMenu(root, self, main_app=main_app, edit_index=index)
            elif item['name'] == "Usługi":
                UslugiMenu(root, self, main_app=main_app, edit_index=index)
            else:
                messagebox.showwarning("Błąd", "Nieznany typ pozycji.")
            return True
        else:
            messagebox.showwarning("Błąd", "Nie wybrano żadnej pozycji.")
            return False