# powlekanie_menu.py - Moduł obsługi powłok

import tkinter as tk
from tkinter import ttk
from config.utils import load_pricing_data


class CoatingMenu:
    """Klasa obsługująca wybór powłoki i długości całkowitej."""
    def __init__(self, parent, update_callback):
        """
        Inicjalizuje menu powłok.
        Args:
            parent: Widget nadrzędny (np. Toplevel lub Frame).
            update_callback: Funkcja do wywołania po zmianie powłoki/długości.
        """
        self.parent = parent
        self.update_callback = update_callback
        self.coating_data = load_pricing_data("data/cennik_powloki.json")
        self.coating_options = ["BRAK"] + list(self.coating_data.keys())
        self.length_options = []
        for coating in self.coating_data.values():
            for diameter_range in coating.get("zakres_srednicy", []):
                for length_item in diameter_range.get("dlugosc_calkowita", []):
                    length = str(length_item["dlugosc"])
                    if length not in self.length_options:
                        self.length_options.append(length)
        self.length_options.sort(key=lambda x: int(x))

        # Przycisk Powłoka
        self.coating_button = tk.Button(parent, text="Powłoka", font=("Arial", 12),
                                       command=self.toggle_coating_options)
        self.coating_button.pack(pady=5)

        # Kontener na opcje powłoki
        self.coating_frame = tk.Frame(self.parent)
        self.coating_price_frame = tk.Frame(self.parent)
        self.coating_var = tk.StringVar(value="BRAK")
        self.length_var = tk.StringVar(value="")
        self.coating_price_label = tk.Label(self.coating_price_frame, text="Cena powłoki: 0.00 PLN", font=("Arial", 10))

        # Combobox dla powłoki i długości
        self.coating_combo = ttk.Combobox(self.coating_frame, textvariable=self.coating_var, state="readonly", width=20)
        self.length_combo = ttk.Combobox(self.coating_frame, textvariable=self.length_var, state="readonly", width=10)
        self.coating_combo.bind("<<ComboboxSelected>>", self.on_selection_change)
        self.length_combo.bind("<<ComboboxSelected>>", self.on_selection_change)

    def toggle_coating_options(self):
        """Pokazuje/ukrywa opcje powłoki."""
        if self.coating_frame.winfo_ismapped():
            self.coating_frame.pack_forget()
            self.coating_price_frame.pack_forget()
            self.coating_button.config(bg="SystemButtonFace", relief="raised")
            self.coating_var.set("BRAK")
            self.length_var.set("")
            self.coating_price_label.config(text="Cena powłoki: 0.00 PLN")
            self.length_combo["values"] = []
        else:
            self.coating_frame.pack(after=self.coating_button, pady=5)
            self.coating_price_frame.pack(after=self.coating_frame, pady=5)
            self.coating_button.config(bg="lightgreen", relief="sunken")
            self.coating_combo["values"] = self.coating_options
            self.length_combo["values"] = self.length_options if self.length_options else ["Brak danych"]
            self.coating_var.set(self.coating_options[1] if len(self.coating_options) > 1 else "BRAK")
            self.length_var.set(self.length_options[0] if self.length_options else "")
            self.coating_combo.pack(side="left", padx=5)
            self.length_combo.pack(side="left", padx=5)
            self.coating_price_label.pack()
            if self.coating_var.get() == "BRAK":
                self.length_combo.config(state="disabled")
            else:
                self.length_combo.config(state="readonly")
        self.update_callback()

    def on_selection_change(self, event=None):
        """Wywołuje callback po zmianie powłoki lub długości."""
        if self.coating_var.get() == "BRAK":
            self.length_var.set("")
            self.length_combo["values"] = []
            self.length_combo.config(state="disabled")
        else:
            self.length_combo["values"] = self.length_options if self.length_options else ["Brak danych"]
            self.length_combo.config(state="readonly")
            if self.length_options and not self.length_var.get():
                self.length_var.set(self.length_options[0])
        self.update_callback()

    def get_coating_price(self, diameter):
        """Zwraca cenę powłoki na podstawie średnicy i wybranej powłoki/długości."""
        try:
            diameter = float(diameter)
            coating = self.coating_var.get()
            length = self.length_var.get()
            if coating == "BRAK" or not (length and diameter > 0):
                return 0.0
            coating_data = self.coating_data.get(coating, {})
            for range_item in coating_data.get("zakres_srednicy", []):
                if diameter <= range_item["srednica_max"]:
                    for length_item in range_item.get("dlugosc_calkowita", []):
                        if str(length_item["dlugosc"]) == length:
                            return length_item["cena_jednostkowa"]
                    break
            return 0.0
        except (ValueError, TypeError):
            return 0.0

    def get_coating_params(self):
        """Zwraca wybrane parametry powłoki."""
        coating = self.coating_var.get()
        length = self.length_var.get()
        if coating and coating != "BRAK" and length:
            return {"Powloka": coating, "Długość całkowita": length}
        return {"Powloka": "BRAK", "Długość całkowita": ""}