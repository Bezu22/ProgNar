# config/cart_io.py - Funkcje do zapisu i wczytywania koszyka

import json
from tkinter import messagebox, filedialog

def save_cart_to_file(cart, client_name, filename="temp_cart.json"):
    """Zapisuje dane koszyka i nazwę klienta do pliku JSON."""
    try:
        data = {
            "client_name": client_name.get() if client_name else "- -",
            "items": cart.items
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if filename == "temp_cart.json":
            print(f"Zapisano koszyk do pliku tymczasowego: {filename}")
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać koszyka: {e}")
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

def load_cart_from_file(cart, client_name, filename="temp_cart.json"):
    """Wczytuje dane koszyka i nazwę klienta z pliku JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cart.items = data.get("items", [])
            if client_name and "client_name" in data:
                client_name.set(data["client_name"])
        return True
    except FileNotFoundError:
        return False  # Brak pliku tymczasowego nie jest błędem
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wczytać koszyka: {e}")
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

def clear_temp_cart(filename="temp_cart.json"):
    """Czyści plik tymczasowy koszyka."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({"client_name": "- -", "items": []}, f)  # Zapisuje pustą listę i domyślną nazwę klienta
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wyczyścić tymczasowego koszyka: {e}")
        return False