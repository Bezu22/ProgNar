import json
import os
from config.utils import resource_path

def get_client_data(client_name, main_app):
    """Zwraca dane klienta z temp_client_data lub client_data.json lub None, jeśli nie istnieje."""
    if not client_name or client_name == "- -":
        return None
    # Najpierw sprawdź tymczasowe dane
    if hasattr(main_app, 'temp_client_data') and main_app.temp_client_data.get("name", "").lower() == client_name.lower():
        return main_app.temp_client_data
    # Następnie sprawdź bazę danych
    json_path = resource_path("data/client_data.json")
    try:
        if os.path.exists(json_path):
            with open(json_path, encoding='utf-8') as f:
                clients = json.load(f)
                for client in clients:
                    if client["name"].lower() == client_name.lower():
                        return client
    except Exception as e:
        print(f"Błąd wczytywania client_data.json: {e}")
    return None