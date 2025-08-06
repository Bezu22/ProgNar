import tkinter as tk
from tkinter import messagebox
import json
import os
from config.utils import resource_path
from config.cart_io import save_cart_to_file
from config.client_utils import get_client_data

class ClientMenu:
    """Klasa obsługująca okno zarządzania klientami."""
    def __init__(self, parent, main_app):
        """
        Inicjalizuje okno zarządzania klientami.
        Args:
            parent: Widget nadrzędny.
            main_app: Referencja do głównej aplikacji (ToolPricingApp).
        """
        self.main_app = main_app
        self.top = tk.Toplevel(parent)
        self.top.title("Zarządzanie klientami")
        self.top.geometry("600x300")
        self.top.transient(parent)
        self.top.grab_set()

        # Zmienne dla pól Entry
        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.contact_var = tk.StringVar()

        # Wczytanie danych klientów
        self.clients = self.load_clients()

        # Ustawienie danych aktywnego klienta lub tymczasowych
        client_data = get_client_data(self.main_app.client_name.get(), self.main_app)
        if client_data:
            self.name_var.set(client_data["name"])
            self.address_var.set(client_data.get("address", ""))
            self.contact_var.set(client_data.get("contact", ""))
        else:
            self.name_var.set(self.main_app.client_name.get() or "- -")
            self.address_var.set(self.main_app.temp_client_data.get("address", "") if hasattr(self.main_app, 'temp_client_data') else "")
            self.contact_var.set(self.main_app.temp_client_data.get("contact", "") if hasattr(self.main_app, 'temp_client_data') else "")

        # Lewa ramka na pola Entry i przyciski
        left_frame = tk.Frame(self.top)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Pola Entry
        tk.Label(left_frame, text="Nazwa klienta:", font=("Arial", 12)).pack(anchor="w")
        name_entry = tk.Entry(left_frame, textvariable=self.name_var, width=30)
        name_entry.pack(pady=5)
        name_entry.focus_set()

        tk.Label(left_frame, text="Adres:", font=("Arial", 12)).pack(anchor="w")
        tk.Entry(left_frame, textvariable=self.address_var, width=30).pack(pady=5)

        tk.Label(left_frame, text="Kontakt:", font=("Arial", 12)).pack(anchor="w")
        tk.Entry(left_frame, textvariable=self.contact_var, width=30).pack(pady=5)

        # Przyciski w lewej ramce
        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Dodaj", command=self.add_client, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edytuj", command=self.edit_client, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Usuń", command=self.delete_client, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Wyczyść", command=self.clear_entries, width=10).pack(side=tk.LEFT, padx=5)

        # Przycisk wyjścia
        tk.Button(left_frame, text="Wyjście", command=self.exit_client_menu, width=10).pack(pady=10)

        # Prawa ramka na Listbox
        right_frame = tk.Frame(self.top)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Listbox z klientami
        self.client_listbox = tk.Listbox(right_frame, width=30, height=10)
        self.client_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.client_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.client_listbox.yview)
        self.client_listbox.bind("<<ListboxSelect>>", self.on_client_select)

        # Aktualizacja Listbox
        self.update_client_listbox()

        # Wiązanie Enter dla dodania klienta
        name_entry.bind("<Return>", lambda e: self.add_client())

    def load_clients(self):
        """Wczytuje dane klientów z client_data.json."""
        json_path = resource_path("data/client_data.json")
        try:
            if os.path.exists(json_path):
                with open(json_path, encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Błąd wczytywania client_data.json: {e}")
            return []

    def save_clients(self):
        """Zapisuje dane klientów do client_data.json."""
        json_path = resource_path("data/client_data.json")
        try:
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.clients, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Błąd zapisu client_data.json: {e}")

    def update_client_listbox(self):
        """Aktualizuje Listbox z listą klientów."""
        self.client_listbox.delete(0, tk.END)
        for client in self.clients:
            self.client_listbox.insert(tk.END, client["name"])

    def on_client_select(self, event):
        """Wypełnia pola Entry po wybraniu klienta z Listbox i czyści temp_client_data."""
        selection = self.client_listbox.curselection()
        if selection:
            index = selection[0]
            client = self.clients[index]
            self.name_var.set(client["name"])
            self.address_var.set(client.get("address", ""))
            self.contact_var.set(client.get("contact", ""))
            # Czyść tymczasowe dane po wybraniu klienta z bazy
            if hasattr(self.main_app, 'temp_client_data'):
                self.main_app.temp_client_data.clear()

    def add_client(self):
        """Dodaje nowego klienta do listy i zapisuje do pliku."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Błąd", "Nazwa klienta nie może być pusta!", parent=self.top)
            return
        address = self.address_var.get().strip()
        contact = self.contact_var.get().strip()

        # Sprawdź, czy klient już istnieje (ignorując wielkość liter)
        for client in self.clients:
            if client["name"].lower() == name.lower():
                messagebox.showerror("Błąd", "Klient o tej nazwie już istnieje!", parent=self.top)
                return

        # Dodaj nowego klienta
        self.clients.append({"name": name, "address": address, "contact": contact})
        self.save_clients()
        self.update_client_listbox()
        self.clear_entries()
        # Czyść tymczasowe dane po dodaniu klienta
        if hasattr(self.main_app, 'temp_client_data'):
            self.main_app.temp_client_data.clear()

    def edit_client(self):
        """Edytuje wybranego klienta."""
        selection = self.client_listbox.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz klienta do edycji!", parent=self.top)
            return

        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Błąd", "Nazwa klienta nie może być pusta!", parent=self.top)
            return
        address = self.address_var.get().strip()
        contact = self.contact_var.get().strip()

        index = selection[0]
        # Sprawdź, czy nowa nazwa nie koliduje z innymi klientami
        for i, client in enumerate(self.clients):
            if client["name"].lower() == name.lower() and i != index:
                messagebox.showerror("Błąd", "Klient o tej nazwie już istnieje!", parent=self.top)
                return

        # Aktualizuj dane klienta
        self.clients[index] = {"name": name, "address": address, "contact": contact}
        self.save_clients()
        self.update_client_listbox()
        self.clear_entries()
        # Czyść tymczasowe dane po edycji klienta
        if hasattr(self.main_app, 'temp_client_data'):
            self.main_app.temp_client_data.clear()

    def delete_client(self):
        """Usuwa wybranego klienta."""
        selection = self.client_listbox.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz klienta do usunięcia!", parent=self.top)
            return

        index = selection[0]
        client_name = self.clients[index]["name"]
        if not messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć klienta {client_name}?", parent=self.top):
            return

        del self.clients[index]
        self.save_clients()
        self.update_client_listbox()
        self.clear_entries()
        # Czyść tymczasowe dane po usunięciu klienta
        if hasattr(self.main_app, 'temp_client_data'):
            self.main_app.temp_client_data.clear()

    def exit_client_menu(self):
        """Zamyka okno, aktualizuje nazwę klienta i zapisuje koszyk oraz tymczasowe dane."""
        selection = self.client_listbox.curselection()
        if selection:
            index = selection[0]
            self.main_app.client_name.set(self.clients[index]["name"])
            # Czyść tymczasowe dane po wybraniu klienta z bazy
            if hasattr(self.main_app, 'temp_client_data'):
                self.main_app.temp_client_data.clear()
        else:
            # Zapisz tymczasowe dane z pól Entry
            name = self.name_var.get().strip()
            if not name:
                self.main_app.client_name.set("- -")
                if hasattr(self.main_app, 'temp_client_data'):
                    self.main_app.temp_client_data.clear()
            else:
                self.main_app.client_name.set(name)
                if hasattr(self.main_app, 'temp_client_data'):
                    self.main_app.temp_client_data.update({
                        "name": name,
                        "address": self.address_var.get().strip(),
                        "contact": self.contact_var.get().strip()
                    })
        save_cart_to_file(self.main_app.cart, self.main_app.client_name)
        self.main_app.cart.update_cart_display(
            self.main_app.cart_tree,
            self.main_app.suma_uslug_label,
            self.main_app.suma_powlekanie_label,
            self.main_app.suma_total_label
        )
        self.top.destroy()

    def clear_entries(self):
        """Czyści pola Entry i tymczasowe dane."""
        self.name_var.set("")
        self.address_var.set("")
        self.contact_var.set("")
        if hasattr(self.main_app, 'temp_client_data'):
            self.main_app.temp_client_data.clear()