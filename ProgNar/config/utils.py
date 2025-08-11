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
        return True if val > 0 else False
    except (ValueError, TypeError):
        return False

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

def get_grinding_price(tool_type_var, num_blades_var, diameter_var, quantity_var):
    #konwersja ze StripVar
    tool_type = tool_type_var.get().strip()
    try:
        num_blades = int(num_blades_var.get().strip())
        diameter = float(diameter_var.get().replace(",", ".").strip())
        quantity = int(quantity_var.get().strip())
    except ValueError:
        print("Błąd konwersji danych wejściowych")
        return None

    print("Na wejsciu")
    print(f"Zeby: {num_blades}")
    print(f"Srednica: {diameter}")
    print(f"ilosc: {quantity}")


    cennik_frezy_path = "data/cennik_frezy.json"
    with open(cennik_frezy_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        #1. Typ
        tool_data = data.get(tool_type)
        if not tool_data:
            print("Brak Tool Type")
            return None
        #Ilosc ostrzy
        blade_category = "2-4" if 2 <= num_blades <= 4 else "pozostale"
        blade_data = tool_data["ilosc_ostrzy"].get(blade_category)
        if not blade_data:
            print("Brak ilsoci ostrzy")
            return None
        #zakres srednicy
        for entry in blade_data["cennik"]:
            zakres = entry["zakres_srednicy"]
            if zakres.startswith("do"):
                max_diameter = float(zakres.split(" ")[1])
                if diameter <= max_diameter:
                    price_table = entry["ceny"]
                    break
            else:
                min_d, max_d = map(float, zakres.split(" - "))
                if min_d <= diameter <= max_d:
                    price_table = entry["ceny"]
                    break
        else:
            return None  # średnica poza zakresem
        #Ilosc sztuk
        if quantity == 1:
            qty_key = "1"
        elif 2 <= quantity <= 4:
            qty_key = "2-4"
        elif 5 <= quantity <= 10:
            qty_key = "5-10"
        elif 11 <= quantity <= 20:
            qty_key = "11-20"
        else:
            qty_key = "11-20"  # lub inna logika dla większych ilości

        #debug
        print(f"Typ: {tool_type}, Ostrza: {num_blades}, Średnica: {diameter}, Ilość: {quantity}, Cena: {price_table.get(qty_key)}")
        #pobierz cene
        print(f"Typ zwracanej wartości: {type(price_table.get(qty_key))}")
        return price_table.get(qty_key)