import json
import tkinter as tk
import os
import sys

def load_pricing_data(file_path):
    """Wczytuje dane cennika z pliku JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Plik {file_path} nie znaleziony.")
        return {}
    except json.JSONDecodeError:
        print(f"Błąd dekodowania JSON w pliku {file_path}.")
        return {}

def format_price(price):
    """Formatuje cenę do dwóch miejsc po przecinku z PLN."""
    try:
        return f"{float(price):.2f} PLN"
    except (ValueError, TypeError):
        return "0.00 PLN"

def validate_positive_int(value):
    """Sprawdza, czy wartość jest dodatnią liczbą całkowitą."""
    try:
        val = int(value)
        return val if val > 0 else 1
    except (ValueError, TypeError):
        return 1

def add_separator(parent, color="#f21821", thickness=1, pady=10):
    """Dodaje wizualny separator."""
    separator = tk.Frame(parent, bg=color, height=thickness)
    separator.pack(fill="x", pady=pady)

def get_price_for_quantity(ceny_dict, quantity):
    """Znajduje cenę dla podanej ilości sztuk na podstawie zakresów w słowniku ceny."""
    ranges = []
    for key, price in ceny_dict.items():
        try:
            if "-" in key:
                lower, upper = map(float, key.split("-"))
                ranges.append((lower, upper, price))
            else:
                single = float(key)
                ranges.append((single, single, price))
        except ValueError:
            continue
    if not ranges:
        return 0.0
    ranges.sort(key=lambda x: x[0])
    for lower, upper, price in ranges:
        if lower <= quantity <= upper:
            return price
    max_upper_range = max(ranges, key=lambda x: x[1])
    if quantity > max_upper_range[1]:
        return max_upper_range[2]
    return 0.0

def validate_blades(z_value, default="2-4"):
    """Waliduje ilość ostrzy i zwraca odpowiedni klucz (np. '2-4' lub 'pozostale')."""
    try:
        z = float(z_value)
        if z.is_integer() and 2 <= z <= 4:
            return "2-4"
        if z.is_integer():
            return "pozostale"
        return default
    except (ValueError, TypeError):
        return default

def resource_path(relative_path):
    """
    Zwraca poprawną ścieżkę do zasobu:
    - w .py — względna
    - w .exe (PyInstaller) — tymczasowy katalog sys._MEIPASS
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)