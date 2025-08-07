import tkinter as tk
from tkinter import messagebox
from tools_menu.powlekanie_menu import CoatingMenu
from tools_menu.blades_menu import BladesMenu
from config.utils import add_separator, resource_path, load_pricing_data
from config.ui_utils import update_button_styles
from config.config import FREZY_TYPES, FREZY_DIAMETER_OPTIONS, FREZY_DEFAULT_DIAMETER, FREZY_Z_OPTIONS, FREZY_DEFAULT_Z

class FrezyUI:
    def __init__(self, parent, main_app=None, edit_item=None,on_save=None):
        self.parent = parent
        self.on_save = on_save
        self.main_app = main_app
        self.edit_item = edit_item

        self.top = tk.Toplevel(parent)
        self.top.title("Menu frezów")
        self.top.geometry("500x700")
        self.top.attributes('-topmost', True)

        # Zmienne
        self.type_var = tk.StringVar(value=FREZY_TYPES[0][1])
        self.diameter_var = tk.StringVar(value=FREZY_DEFAULT_DIAMETER)
        self.chwyt_var = tk.StringVar(value=FREZY_DEFAULT_DIAMETER)
        self.z_var = tk.StringVar(value=FREZY_DEFAULT_Z)
        self.quantity_var = tk.StringVar(value="1")
        self.ciecie_var = tk.BooleanVar(value=False)

        # Sekcje UI
        self.create_type_section()
        self.create_diameter_section()
        self.create_blades_section()
        self.create_quantity_section()
        self.create_powlekanie_section()
        self.create_price_labels()
        self.create_action_buttons()

        if self.edit_item:
            self.fill_edit_fields()

        self.update_price()

    def create_type_section(self):
        tk.Label(self.top, text="Wybierz typ:", font=("Arial", 12)).pack(pady=5)
        frame = tk.Frame(self.top)
        frame.pack(pady=5)
        self.type_buttons = {}
        for display_name, json_name in FREZY_TYPES:
            btn = tk.Button(frame, text=display_name, width=10,
                            command=lambda t=json_name: self.select_type(t))
            btn.pack(side="left", padx=5)
            self.type_buttons[json_name] = btn
        update_button_styles(self.type_buttons, self.type_var.get())
        add_separator(self.top)

    def create_diameter_section(self):
        frame = tk.Frame(self.top)
        frame.pack(pady=5)
        tk.Label(frame, text="Średnica (mm):", font=("Arial", 12)).pack(side="left", padx=5)
        self.diameter_entry = tk.Entry(frame, textvariable=self.diameter_var, width=10)
        self.diameter_entry.pack(side="left", padx=5)
        tk.Label(frame, text="Chwyt (mm):", font=("Arial", 12)).pack(side="left", padx=5)
        self.chwyt_entry = tk.Entry(frame, textvariable=self.chwyt_var, width=10)
        self.chwyt_entry.pack(side="left", padx=5)
        add_separator(self.top)

    def create_blades_section(self):
        self.blades_menu = BladesMenu(self.top, self.z_var, self.update_price, FREZY_Z_OPTIONS, FREZY_DEFAULT_Z)
        add_separator(self.top)

    def create_quantity_section(self):
        frame = tk.Frame(self.top)
        frame.pack(pady=5)
        tk.Label(frame, text="Ilość sztuk:", font=("Arial", 12)).pack(side="left", padx=5)
        self.quantity_entry = tk.Entry(frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.pack(side="left", padx=5)
        self.ciecie_check = tk.Checkbutton(frame, text="Cięcie", variable=self.ciecie_var, command=self.update_price)
        self.ciecie_check.pack(side="left", padx=5)
        add_separator(self.top)

    def create_powlekanie_section(self):
        self.powlekanie_menu = CoatingMenu(self.top, self.update_price)
        add_separator(self.top)

    def create_price_labels(self):
        self.price_label = tk.Label(self.top, text="Cena jednostkowa: 0.00 PLN", font=("Arial", 10))
        self.price_label.pack(pady=5)
        self.powlekanie_menu.coating_price_label.pack(pady=5)
        self.total_price_label = tk.Label(self.top, text="Wartość: 0.00 PLN", font=("Arial", 12, "bold"))
        self.total_price_label.pack(pady=5)
        add_separator(self.top)

    def create_action_buttons(self):
        self.add_button = tk.Button(self.top, text="Dodaj do koszyka", font=("Arial", 12), command=self.add_to_cart)
        self.add_button.pack(pady=5)
        tk.Button(self.top, text="Zamknij", font=("Arial", 12), command=self.top.destroy).pack(pady=5)

    def select_type(self, selected_type):
        self.type_var.set(selected_type)
        update_button_styles(self.type_buttons, selected_type)
        self.update_price()

    def update_price(self, *args):
        # Tu wrzucisz logikę obliczania ceny
        pass

    def add_to_cart(self):
        # Tu wrzucisz logikę dodawania do koszyka
        pass

    def fill_edit_fields(self):
        # Tu wrzucisz logikę wypełniania pól w trybie edycji
        pass
