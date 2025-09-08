import tkinter as tk
from tkinter import ttk
import math ,json
from config.utils import add_separator, validate_positive_int, resource_path, get_grinding_price,get_cutting_price,get_coating_price
from config.ui_utils import update_button_styles
from config.config import SPEC_TYPES,SPEC_DIAMETER_OPTIONS

class PozostaleUI:
    def __init__(self, parent, cart, client_name, on_save, edit_index=None):
        self.parent = parent
        self.on_save = on_save
        self.cart = cart
        self.client_name = client_name
        self.edit_index = edit_index

        self.top = tk.Toplevel(parent)
        self.top.title("Menu specjalne")
        self.top.geometry("500x700")
        self.top.attributes('-topmost', True)
        # cennik powlok
        self.coating_data = self.load_coating_json()

        # Zmienne parametrów
        self.type_var = tk.StringVar(value = SPEC_TYPES[0][1])
        self.diameter_var = tk.StringVar(value="10")
        self.chwyt_var = tk.StringVar(value="10")
        self.z_var = tk.StringVar(value="4")
        self.quantity_var = tk.StringVar(value="4")
        self.ciecie_var = tk.BooleanVar(value=False)
        self.s_var = tk.BooleanVar(value=False)
        self.s_value_var = tk.StringVar(value=" ")
        self.coating_var = tk.StringVar(value="BRAK")
        self.length_var = tk.IntVar(value=100)
        self.remarks_var = tk.StringVar(value="-")
        self.remarks_value = tk.StringVar(value=" ")

        # Zmienne cen !
        self.current_cutting_price_per_piece = tk.DoubleVar(value=0.00)
        self.current_lowering_price_per_piece = tk.DoubleVar(value=0.00)
        self.current_coating_price_per_piece = tk.DoubleVar(value=0.00)
        self.current_grinding_price_per_piece = tk.DoubleVar(value=0.00)
        self.current_cutting_price = tk.DoubleVar(value=0.00)
        self.current_lowering_price = tk.DoubleVar(value=0.00)
        self.current_coating_price = tk.DoubleVar(value=0.00)
        self.current_grinding_price = tk.DoubleVar(value=0.00)
        self.bonus_price_var = tk.DoubleVar(value=0.0)
        self.total_price_var = tk.DoubleVar(value=0.0)

        self.grinding_discount_value = tk.IntVar(value=0)
        self.coating_discount_value = tk.IntVar(value=0)
        self.cutting_discount_value = tk.IntVar(value=0)
        self.lowering_discount_value = tk.IntVar(value=0)

        # Sekcje UI
        self.create_type_section()
        # self.create_diameter_section()
        # self.create_blades_section()
        # self.create_quantity_section()
        # self.create_powlekanie_section()
        # self.create_price_labels()
        # self.create_action_buttons()

        # self.update_price_labels()
        #
        # # Jeśli edytujemy, wypełnij pola danymi z pozycji
        # if edit_index is not None:
        #     self.load_item_data()


    def create_type_section(self):
        tk.Label(self.top, text="Wybierz typ:", font=("Arial", 12)).pack(pady=5)
        frame = tk.Frame(self.top)
        frame.pack(pady=3)
        self.type_buttons = {}
        for display_name, json_name in SPEC_TYPES:
            btn = tk.Button(frame, text=display_name, width=10,
                            command=lambda t=json_name: self.select_type(t))
            btn.pack(side="left", padx=5)
            self.type_buttons[json_name] = btn
        update_button_styles(self.type_buttons, self.type_var.get())

        add_separator(self.top)
    #----
    def select_type(self, selected_type):
        self.type_var.set(selected_type)
        print(selected_type)
        #self.update_price_labels()
        update_button_styles(self.type_buttons, selected_type)

    def load_coating_json(self ):
        with open(resource_path("data/cennik_powloki.json"), "r", encoding="utf-8") as f:
            return json.load(f)