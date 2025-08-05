import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from config.utils import resource_path

def save_cart_to_file(cart, client_name, filename=None):
    """Zapisuje dane koszyka i nazwę klienta do pliku JSON."""
    if filename is None:
        filename = resource_path("data/temp_cart.json")

    try:
        # Upewnij się, że folder data/ istnieje
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        data = {
            "client_name": client_name.get() if isinstance(client_name, tk.StringVar) else client_name,
            "items": cart.items
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if filename.endswith("temp_cart.json"):
            print(f"Zapisano koszyk do pliku tymczasowego: {filename}")
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać koszyka: {str(e)}")
        return False

def save_cart_to_file_with_dialog(cart, client_name, parent):
    """Zapisuje koszyk i nazwę klienta do pliku JSON z wyborem lokalizacji."""
    filename = filedialog.asksaveasfilename(
        parent=parent,
        defaultextension=".json",
        filetypes=[("Pliki JSON", "*.json"), ("Wszystkie pliki", "*.*")]
    )
    if filename:
        return save_cart_to_file(cart, client_name, filename)
    return False

def load_cart_from_file(cart, client_name, filename=None):
    """Wczytuje dane koszyka i nazwę klienta z pliku JSON."""
    if filename is None:
        filename = resource_path("data/temp_cart.json")

    try:
        if not os.path.exists(filename):
            return False
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cart.items = data.get("items", [])
            if client_name and "client_name" in data:
                client_name.set(data["client_name"])
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wczytać koszyka: {str(e)}")
        return False

def load_cart_from_file_with_dialog(cart, client_name, parent):
    """Wczytuje koszyk i nazwę klienta z pliku JSON z wyborem lokalizacji."""
    filename = filedialog.askopenfilename(
        parent=parent,
        filetypes=[("Pliki JSON", "*.json"), ("Wszystkie pliki", "*.*")]
    )
    if filename:
        return load_cart_from_file(cart, client_name, filename)
    return False

def clear_temp_cart(filename=None):
    """Usuwa plik tymczasowy koszyka."""
    if filename is None:
        filename = resource_path("data/temp_cart.json")

    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Usunięto plik tymczasowy: {filename}")
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wyczyścić tymczasowego koszyka: {str(e)}")
        return False