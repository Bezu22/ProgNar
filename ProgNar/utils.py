# utils.py - Funkcje pomocnicze do wczytywania JSON i formatowania danych

import json
import os

def load_pricing_data(file_path):
    """
    Wczytuje dane z pliku JSON.
    Args:
        file_path (str): Ścieżka do pliku JSON (np. 'data/cennik_frezy.json').
    Returns:
        dict: Dane z pliku JSON lub pusty słownik w przypadku błędu.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Błąd: Plik {file_path} nie istnieje.")
            return {}
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Błąd: Plik {file_path} ma niepoprawny format JSON.")
        return {}
    except Exception as e:
        print(f"Błąd podczas wczytywania {file_path}: {e}")
        return {}

def format_price(price):
    """
    Formatuje cenę do dwóch miejsc po przecinku.
    Args:
        price (float): Cena do sformatowania.
    Returns:
        str: Cena w formacie 'X.XX PLN'.
    """
    return f"{price:.2f} PLN"

def validate_positive_int(value, default=1):
    """
    Waliduje, czy wartość jest dodatnią liczbą całkowitą.
    Args:
        value (str): Wartość do sprawdzenia (np. z pola tekstowego).
        default (int): Wartość domyślna, jeśli walidacja się nie powiedzie.
    Returns:
        int: Dodatnia liczba całkowita lub wartość domyślna.
    """
    try:
        num = int(value)
        return num if num > 0 else default
    except ValueError:
        return default