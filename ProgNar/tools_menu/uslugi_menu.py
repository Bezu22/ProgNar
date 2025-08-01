# uslugi_menu.py - Moduł menu dla usług

import tkinter as tk
from tkinter import ttk, messagebox
from ProgNar.config.utils import load_pricing_data, format_price, validate_positive_int


class UslugiMenu:
    """Klasa obsługująca menu usług."""

    def __init__(self, parent, cart):
        """
        Inicjalizuje menu usług.
        Args:
            parent (tk.Tk): Główne okno aplikacji.
            cart (Cart): Obiekt wspólnego koszyka.
        """
        self.parent = parent
        self.cart = cart
        # Wczytywanie danych z JSON
        self.pricing_data = load_pricing_data("../data/cennik_uslugi.json")

        # Tworzenie okna menu
        self.top = tk.Toplevel(parent)
        self.top.title("Menu usług")
        self.top.geometry("400x400")

        # Etykiety i pola wyboru
        tk.Label(self.top, text="Wybierz usługę:", font=("Arial", 12)).pack(pady=10)
        self.service_var = tk.StringVar()
        self.service_combo = ttk.Combobox(self.top, textvariable=self.service_var, state="readonly")
        self.service_combo.pack(pady=5)
        self.service_combo.bind("<<ComboboxSelected>>", self.update_parameters)

        tk.Label(self.top, text="Wybierz parametr:", font=("Arial", 12)).pack(pady=5)
        self.parameter_var = tk.StringVar()
        self.parameter_combo = ttk.Combobox(self.top, textvariable=self.parameter_var, state="readonly")
        self.parameter_combo.pack(pady=5)
        self.parameter_combo.bind("<<ComboboxSelected>>", self.update_price)

        tk.Label(self.top, text="Ilość sztuk:", font=("Arial", 12)).pack(pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(self.top, textvariable=self.quantity_var)
        self.quantity_entry.pack(pady=5)

        self.price_label = tk.Label(self.top, text="Cena: 0.00 PLN", font=("Arial", 12))
        self.price_label.pack(pady=10)

        # Przyciski
        tk.Button(self.top, text="Dodaj do koszyka", font=("Arial", 12), command=self.add_to_cart).pack(pady=5)
        tk.Button(self.top, text="Zamknij", font=("Arial", 12), command=self.top.destroy).pack(pady=5)

        # Inicjalizacja combobox z usługami
        self.update_services()

    def update_services(self):
        """Aktualizuje listę usług w combobox."""
        if not self.pricing_data:
            self.service_combo["values"] = ["Brak danych"]
            return

        services = list(self.pricing_data.keys())
        self.service_combo["values"] = services
        if services:
            self.service_combo.set(services[0])
            self.update_parameters()

    def update_parameters(self, event=None):
        """Aktualizuje listę parametrów na podstawie wybranej usługi."""
        selected_service = self.service_var.get()
        self.parameter_combo.set("")
        self.price_label.config(text="Cena: 0.00 PLN")

        if not selected_service:
            return

        service_data = self.pricing_data.get(selected_service, {})
        parameter_key = "zakres_srednicy" if "zakres_srednicy" in service_data else "szerokosc"
        parameters = [item[parameter_key] for item in service_data.get(parameter_key, [])]
        self.parameter_combo["values"] = parameters
        if parameters:
            self.parameter_combo.set(parameters[0])
            self.update_price()

    def update_price(self, event=None):
        """Aktualizuje cenę na podstawie wybranych parametrów."""
        selected_service = self.service_var.get()
        selected_parameter = self.parameter_var.get()

        if not (selected_service and selected_parameter):
            return

        price = 0.0
        service_data = self.pricing_data.get(selected_service, {})
        parameter_key = "zakres_srednicy" if "zakres_srednicy" in service_data else "szerokosc"
        for item in service_data.get(parameter_key, []):
            if item[parameter_key] == selected_parameter:
                price = float(item["cena_jednostkowa"])
                break

        self.price_label.config(text=f"Cena: {format_price(price)}")

    def add_to_cart(self):
        """Dodaje wybraną pozycję do koszyka."""
        selected_service = self.service_var.get()
        selected_parameter = self.parameter_var.get()
        quantity = validate_positive_int(self.quantity_var.get())

        if not (selected_service and selected_parameter):
            messagebox.showerror("Błąd", "Proszę wybrać wszystkie parametry.")
            return

        price = 0.0
        service_data = self.pricing_data.get(selected_service, {})
        parameter_key = "zakres_srednicy" if "zakres_srednicy" in service_data else "szerokosc"
        for item in service_data.get(parameter_key, []):
            if item[parameter_key] == selected_parameter:
                price = float(item["cena_jednostkowa"])
                break

        params = {
            "Usługa": selected_service,
            "Parametr": selected_parameter
        }
        self.cart.add_item("Usługi", params, quantity, price)
        messagebox.showinfo("Sukces", f"Dodano {quantity} szt. {selected_service} do koszyka.")