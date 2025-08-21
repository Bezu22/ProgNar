import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config.utils import resource_path
from ui.frezy_menu.frezy_ui import FrezyUI
from ui.wiertla_menu.wiertla_ui import WiertlaUI
#from tools_menu.wiertla_menu import WiertlaMenu
#from tools_menu.pozostale_menu import PozostaleMenu
#from tools_menu.uslugi_menu import UslugiMenu

class CartMain:
    def __init__(self):
        self.items = []
        self.filename = resource_path("data/temp_cart.json")
        self.load_from_file()

    def add_item(self, params, prices, client_name):
        """Dodaje nowy element do koszyka i zapisuje do pliku."""
        item = {
            "Nazwa": params["Nazwa"],
            "Srednica": params["Srednica"],
            "fiChwyt": params["fiChwyt"],
            "Ilosc ostrzy": params["Ilosc ostrzy"],
            "Ilosc sztuk": params["Ilosc sztuk"],
            "ciecie": params["ciecie"],
            "Uwagi": params["Uwagi"],
            "Powloka": params["Powloka"],
            "Długość całkowita": params["Długość całkowita"],
            "Cena szlifowania": prices["Cena szlifowania"],
            "Razem szlifowanie": prices["Razem szlifowanie"],
            "Cena powlekania": prices["Cena powlekania"] if params["Powloka"] != "BRAK" else "-",
            "Razem powloka": prices["Razem powloka"] if params["Powloka"] != "BRAK" else "-",
            "Cena ciecia": prices["Cena ciecia"],
            "Razem ciecie": prices["Razem ciecie"],
            "Razem uslugi": prices["Razem uslugi"],
            "Razem": prices["Razem"]
        }
        if "Stopnie" in params:
            item["Stopnie"] = params["Stopnie"]

        if "Cena zanieznia" in prices:
            item["Cena zanieznia"] = prices["Cena zanieznia"]
        if "Razem zanieznia" in prices:
            item["Razem zanieznia"] = prices["Razem zanieznia"]

        self.items.append(item)
        self.save_to_file(client_name)

    def remove_item(self, index, client_name):
        """Usuwa element z koszyka i zapisuje do pliku."""
        if 0 <= index < len(self.items):
            self.items.pop(index)
            self.save_to_file(client_name)

    def clear_cart(self, client_name):
        """Czyści koszyk i zapisuje do pliku."""
        self.items = []
        self.save_to_file(client_name)

    def save_to_file(self, client_name):
        """Zapisuje koszyk i nazwę klienta do pliku JSON."""
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            data = {
                "client_name": client_name.get() if isinstance(client_name, tk.StringVar) else client_name,
                "items": self.items
            }
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Zapisano koszyk")
            return True
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać koszyka: {str(e)}")
            return False

    def load_from_file(self, client_name=None):
        """Wczytuje koszyk i nazwę klienta z pliku JSON."""
        try:
            if not os.path.exists(self.filename):
                self.items = []
                return False
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.items = data.get("items", [])
                if client_name and "client_name" in data:
                    client_name.set(data["client_name"])
            return True
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać koszyka: {str(e)}")
            return False

    def save_to_file_with_dialog(self, client_name, parent):
        """Zapisuje koszyk z wyborem pliku."""
        original_filename = self.filename
        filename = filedialog.asksaveasfilename(
            parent=parent,
            defaultextension=".json",
            filetypes=[("Pliki JSON", "*.json"), ("Wszystkie pliki", "*.*")]
        )
        if filename:
            self.filename = filename
            success = self.save_to_file(client_name)
            self.filename = original_filename
            return success
        else:
            messagebox.showinfo("Informacja", "Zapis anulowany.", parent=parent)
            return False

    def load_from_file_with_dialog(self, client_name, parent, cart_tree):
        """Wczytuje koszyk z wyborem pliku i zapisuje do temp_cart.json."""
        original_filename = self.filename
        filename = filedialog.askopenfilename(
            parent=parent,
            filetypes=[("Pliki JSON", "*.json"), ("Wszystkie pliki", "*.*")]
        )
        if filename:
            self.filename = filename
            success = self.load_from_file(client_name)
            self.filename = original_filename
            if success:
                self.save_to_file(client_name)  # Save loaded cart to temp_cart.json
                self.update_cart_display(cart_tree)  # Refresh cart display
                return True
            return False
        else:
            messagebox.showinfo("Informacja", "Wczytywanie anulowane.", parent=parent)
            return False

    def update_cart_display(self, cart_tree):
        """Aktualizuje wyświetlanie koszyka w tabeli."""
        cart_tree.delete(*cart_tree.get_children())
        for idx, item in enumerate(self.items):
            uwagi = "✓" if item["Uwagi"] != "-" else "−"
            remarks_tag = "remarks_filled" if uwagi == "✓" else "remarks_empty"
            cart_tree.insert("", tk.END, iid=str(idx), values=(
                idx + 1,
                item.get("Nazwa", "-"),
                item.get("Srednica", "-"),
                item.get("fiChwyt", "-"),
                item.get("Ilosc ostrzy", "-"),
                item.get("Ilosc sztuk", "-"),
                item.get("ciecie", "-"),
                item.get("Cena szlifowania", "-"),
                item.get("Razem szlifowanie", "-"),
                item.get("Powloka", "-"),
                item.get("Długość całkowita", "-"),
                item.get("Cena powlekania", "-"),
                item.get("Razem powloka", "-"),
                uwagi
            ), tags=[remarks_tag if i == 13 else "" for i in range(14)])

    def delete_selected(self, cart_tree, client_name):
        """Usuwa wybrany element z koszyka."""
        selected = cart_tree.selection()
        if selected:
            index = cart_tree.index(selected[0])
            self.remove_item(index, client_name)
            self.update_cart_display(cart_tree)  # Odśwież widok po usunięciu
            return True
        else:
            messagebox.showwarning("Błąd", "Nie wybrano żadnej pozycji do usunięcia.",
                                   parent=cart_tree.winfo_toplevel())
            return False

    def edit_selected(self,cart_tree,root,cart,client_name,handle_save):
        cart_tree = cart_tree
        root = root
        cart = cart
        client_name = client_name
        handle_save = handle_save

        #FrezyUI(self.root, self.cart, self.client_name, self.main_app.handle_frezy_save)

        """Edytuje wybrany element z koszyka."""
        selected = cart_tree.selection()
        if selected:
            index = int(selected[0])
            item = self.items[index]
            if item["Nazwa"].startswith("Frezy") or item["Nazwa"].startswith("Frez"):
                FrezyUI(root,cart,client_name,handle_save,index)
                return
            if item["Nazwa"].startswith("Wiertlo") :
                WiertlaUI(root,cart,client_name,handle_save,index)
                return
            else:
                messagebox.showwarning("Błąd", "Problem.", parent=root)
            return True
        else:
            messagebox.showwarning("Błąd", "Nie wybrano żadnej pozycji do edycji.", parent=root)
            return False
