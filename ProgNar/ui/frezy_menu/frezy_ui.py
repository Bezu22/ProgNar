import tkinter as tk
import math
from tkinter import messagebox
from tools_menu.powlekanie_menu import CoatingMenu
from config.utils import add_separator, validate_positive_int, resource_path,get_grinding_price
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

        # Zmienne parametrów
        self.type_var = tk.StringVar(value=FREZY_TYPES[0][1])
        self.diameter_var = tk.StringVar(value=FREZY_DEFAULT_DIAMETER)
        self.chwyt_var = tk.StringVar(value=FREZY_DEFAULT_DIAMETER)
        self.z_var = tk.StringVar(value=FREZY_DEFAULT_Z)
        self.quantity_var = tk.StringVar(value="4")
        self.ciecie_var = tk.BooleanVar(value=False)
        self.s_var = tk.BooleanVar(value=False)
        self.s_value_var = tk.StringVar(value=self.quantity_var.get())

        # Zmienne cen !


        self.current_cutting_price_per_piece = tk.DoubleVar(value = 0.00)
        self.current_lowering_price_per_piece = tk.DoubleVar(value = 0.00)
        self.current_coating_price_per_piece = tk.DoubleVar(value = 0.00)
        self.current_grinding_price_per_piece = tk.DoubleVar(value = 0.00)
        self.current_cutting_price = tk.DoubleVar(value = 0.00)
        self.current_lowering_price = tk.DoubleVar(value = 0.00)
        self.current_coating_price = tk.DoubleVar(value = 0.00)
        self.current_grinding_price = tk.DoubleVar(value = 0.00)
        self.bonus_price_var = tk.DoubleVar(value=0.0)
        self.total_price_var = tk.DoubleVar(value=0.0)

        '''
        # Ceny liczone
        self.current_cutting_price = self.current_cutting_price_per_piece * float(self.quantity_var.get())
        self.current_lowering_price = self.current_lowering_price_per_piece * float(self.quantity_var.get())
        self.current_coating_price = self.current_coating_price_per_piece * float(self.quantity_var.get())
        self.current_grinding_price = self.current_grinding_price_per_piece * float(self.quantity_var.get())
        self.bonus_price = self.current_cutting_price + self.current_lowering_price
        self.full_price = self.bonus_price + self.current_grinding_price

        
        #Debug wejsciowy
        print(f"🔧: Typ: {self.type_var.get()}")
        print(f"Typ: {self.type_var.get()}")
        print(f"Średnica: {self.diameter_var.get()}")
        print(f"Chwyt: {self.chwyt_var.get()}")
        print(f"Ilość ostrzy (Z): {self.z_var.get()}")
        print(f"Ilość sztuk: {self.quantity_var.get()}")
        print(f"Cięcie: {'TAK' if self.ciecie_var.get() else 'NIE'}")
        '''



        # Pierwsza cena
        #self.current_grinding_price_per_piece.set(get_grinding_price(self.type_var, self.z_var, self.diameter_var,
         #                                                          self.quantity_var))

        # Sekcje UI
        self.create_type_section()
        self.create_diameter_section()
        self.create_blades_section()
        self.create_quantity_section()
        self.create_powlekanie_section()
        self.create_price_labels()
        self.create_action_buttons()

        self.update_price_labels()

    def create_type_section(self):
        tk.Label(self.top, text="Wybierz typ:", font=("Arial", 12)).pack(pady=5)
        frame = tk.Frame(self.top)
        frame.pack(pady=3)
        self.type_buttons = {}
        for display_name, json_name in FREZY_TYPES:
            btn = tk.Button(frame, text=display_name, width=10,
                            command=lambda t=json_name: self.select_type(t))
            btn.pack(side="left", padx=5)
            self.type_buttons[json_name] = btn
        update_button_styles(self.type_buttons, self.type_var.get())

        add_separator(self.top)

    def create_diameter_section(self):
        diameter_frame = tk.Frame(self.top)
        diameter_frame.pack(pady=3)
        #Etykieta
        label_frame = tk.Frame(diameter_frame)
        label_frame.pack(fill='x')
        tk.Label(label_frame, text="Średnica (mm):", font=("Arial", 12)).pack(pady=5)

        #Przyciski
        buttons_frame = tk.Frame(diameter_frame)
        buttons_frame.pack(fill='x')
        self.diameter_buttons = {}
        for display_name, json_name in FREZY_DIAMETER_OPTIONS:
            btn = tk.Button(buttons_frame, text=display_name, width=6,
                            command=lambda v=json_name: self.select_diameter(v))
            btn.pack(side="left", padx=2)
            self.diameter_buttons[json_name] = btn
        update_button_styles(self.diameter_buttons, self.diameter_var.get())

        #GRID Entry boxow
        entry_frame = tk.Frame(diameter_frame)
        entry_frame.pack(fill='x', padx=5, pady=5)
        # Robocza - lewa strona
        tk.Label(entry_frame, text="Robocza (mm):", font=("Arial", 12)).grid(row=0, column=0, sticky='w', padx=5,pady=5)
        self.diameter_entry = tk.Entry(entry_frame, textvariable=self.diameter_var, width=10)
        self.diameter_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        # Chwyt - prawa strona
        tk.Label(entry_frame, text="Chwyt (mm):", font=("Arial", 12)).grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.chwyt_entry = tk.Entry(entry_frame, textvariable=self.chwyt_var, width=10)
        self.chwyt_entry.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        self.diameter_entry.bind("<KeyRelease>", self.on_diameter_entry_change)
        self.chwyt_entry.bind("<KeyRelease>", self.on_shunk_entry_change)

        add_separator(self.top)

    def create_blades_section(self):
        # Główny kontener
        container = tk.Frame(self.top)
        container.pack(pady=3)
        # --- Etykieta ---
        label_frame = tk.Frame(container)
        label_frame.pack(fill='x')
        tk.Label(label_frame, text="Wybierz ilość ostrzy:", font=("Arial", 12)).pack(pady=5)
        # --- Przyciski ---
        buttons_frame = tk.Frame(container)
        buttons_frame.pack(pady=5)
        self.z_buttons = {}
        for z in FREZY_Z_OPTIONS:
            btn = tk.Button(buttons_frame, text=z, width=6,
                            command=lambda v=z: self.select_z(v))
            btn.pack(side="left", padx=2)
            self.z_buttons[z] = btn
        update_button_styles(self.z_buttons, self.z_var.get())

        # --- Pole tekstowe ---
        self.z_entry = tk.Entry(buttons_frame, textvariable=self.z_var, width=8,bg='#D6E8CF')
        self.z_entry.pack(padx=25 ,pady=2)

        #walidacja
        self.z_entry.bind("<KeyRelease>", self.on_z_entry_change)

        add_separator(self.top)

    def create_quantity_section(self):
        frame = tk.Frame(self.top)
        frame.pack(pady=3)
        tk.Label(frame, text="Ilość sztuk:", font=("Arial", 12)).pack(side="left", padx=5)
        self.quantity_entry = tk.Entry(frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.pack(side="left", padx=5)
        self.ciecie_check = tk.Checkbutton(frame, text="Cięcie", variable=self.ciecie_var, command=print("klik"))
        self.ciecie_check.pack(side="left", padx=5)
        add_separator(self.top)

        # Checkbox S(szyjka) i pole tekstowe
        self.s_check = tk.Checkbutton(frame, text="Szyjka", variable=self.s_var,
                                       command=self.toggle_s_entry)
        self.s_check.pack(side="left", padx=5)
        self.s_entry = tk.Entry(frame, textvariable=self.s_value_var, width=4, state='disabled')
        self.s_entry.pack(side="left", padx=5)

        self.s_entry.bind("<KeyRelease>", self.validate_s_value)
        #self.quantity_entry.bind("<KeyRelease>", self.validate_ik_value)  # Walidacja IK przy zmianie ilości sztuk

    def toggle_s_entry(self):
        """Włącza/wyłącza pole tekstowe Szyjki i ustawia domyślną wartość."""
        if self.s_var.get():
            self.s_entry.config(state='normal')
            self.s_value_var.set(self.quantity_var.get())
        else:
            self.s_entry.config(state='disabled')
            self.s_value_var.set(self.quantity_var.get())

    def validate_s_value(self, event=None):
        """Waliduje wartość w polu S."""
        s_value = self.s_value_var.get()
        quantity_raw = self.quantity_var.get()

        if not validate_positive_int(s_value):
            self.s_value_var.set(quantity_raw)
            return

        s_int = int(s_value)
        quantity = int(quantity_raw)

        if s_int > quantity or s_int < 0:
            self.s_value_var.set(str(quantity))

    def create_powlekanie_section(self):
        self.powlekanie_menu = CoatingMenu(self.top, self.update_price)
        add_separator(self.top)

    def create_price_labels(self):
        container = tk.Frame(self.top, border=2, relief='solid')
        container.pack(pady=3, fill='x')

        # Ustawienie grid w kontenerze
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # Lewe labele
        self.cutting_price_label = tk.Label(container, text=f"Cena cięcia: {self.current_cutting_price_per_piece.get():.2f} zł/ "
                                                f"{self.current_cutting_price.get():.2f} zł", font=("Arial", 10)
                                , anchor='w')
        self.cutting_price_label.grid(row=0, column=0, sticky='w', padx=5, pady=2)

        self.lowering_price_label = tk.Label(container, text=f"Cena zaniżenia: {self.current_lowering_price_per_piece.get():.2f} zł / "
                                                f"{self.current_lowering_price.get():.2f} zł", font=("Arial", 10)
                                , anchor='w')
        self.lowering_price_label.grid(row=1, column=0, sticky='w', padx=5, pady=2)

        self.coating_price_label = tk.Label(container, text=f"Cena powłoki: {self.current_coating_price_per_piece.get():.2f} zł / "
                                                f"{self.current_coating_price.get():.2f} zł", font=("Arial", 10)
                                , anchor='w')
        self.coating_price_label.grid(row=2, column=0, sticky='w', padx=5, pady=2)

        # Prawe labele
        self.grinding_price_label = tk.Label(container, text=f"Cena ostrzenia: {self.current_grinding_price.get():.2f} zł / "
                                                f"{self.current_grinding_price.get():.2f} zł", font=("Arial", 10)
                                 , anchor='e')
        self.grinding_price_label.grid(row=0, column=1, sticky='e', padx=5, pady=2)

        self.bonus_price_label = tk.Label(container, text=f"Cena usług: {self.bonus_price_var.get():.2f} zł", font=("Arial", 10)
                                 , anchor='e')
        self.bonus_price_label.grid(row=1, column=1, sticky='e', padx=5, pady=2)

        self.total_price_label = tk.Label(container, text=f"Wartość całkowita: {self.total_price_var.get():.2f} zł", font=("Arial", 10)
                                 , anchor='e')
        self.total_price_label.grid(row=2, column=1, sticky='e', padx=5, pady=2)

        '''
        self.price_label = tk.Label(self.top, text="Cena jednostkowa: 0.00 PLN", font=("Arial", 8))
        self.price_label.pack(pady=5)
        self.powlekanie_menu.coating_price_label.pack(pady=5)
        self.total_price_label = tk.Label(self.top, text="Wartość: 0.00 PLN", font=("Arial", 12, "bold"))
        self.total_price_label.pack(pady=5)
        add_separator(self.top)
        '''

    def create_action_buttons(self):
        self.add_button = tk.Button(self.top, text="Dodaj do koszyka", font=("Arial", 12), command=self.add_to_cart)
        self.add_button.pack(pady=5)
        tk.Button(self.top, text="Zamknij", font=("Arial", 12), command=self.top.destroy).pack(pady=5)
#--------------------------------------------
    def select_type(self, selected_type):
        self.type_var.set(selected_type)
        update_button_styles(self.type_buttons, selected_type)
        self.current_grinding_price_per_piece = get_grinding_price(self.type_var, self.z_var, self.diameter_var,
                                                                   self.quantity_var)
        self.update_price_labels()
        print(selected_type)

    def select_diameter(self, d_value):
        self.diameter_var.set(d_value)
        self.chwyt_var.set(d_value)
        self.current_grinding_price_per_piece = get_grinding_price(self.type_var, self.z_var, self.diameter_var,
                                                                   self.quantity_var)
        self.update_price_labels()
        update_button_styles(self.diameter_buttons, d_value)

    def on_diameter_entry_change(self, event=None):
            """Walidacja inputu srednicy."""

            diam_input = self.diameter_var.get().replace(",", ".")
            diam_default = FREZY_DEFAULT_DIAMETER
            chwyt_input = self.chwyt_var.get()
            # Obsluga pustego pola
            try:
                diam_float = float(diam_input)
                chwyt_float = float(chwyt_input)
                if diam_float == 0 or chwyt_float == 0:
                    raise ValueError
            except ValueError:
                self.diameter_var.set(diam_default)
                return


            #Korekcja chwytu
            if diam_float > chwyt_float:
                self.chwyt_var.set(int(math.ceil(diam_float / 2.0)) * 2)

            self.diameter_var.set(diam_input)
            self.current_grinding_price_per_piece = get_grinding_price(self.type_var, self.z_var, self.diameter_var,
                                                                       self.quantity_var)
            self.update_price_labels()
            update_button_styles(self.diameter_buttons, diam_input)

    def on_shunk_entry_change(self, event=None):
        shunk_input = self.chwyt_var.get().replace(",", ".")
        shunk_default = FREZY_DEFAULT_DIAMETER
        # Obsluga pustego pola
        try:
            shunk_float = float(shunk_input)
            if shunk_float == 0:
                raise ValueError
        except ValueError:
            self.chwyt_var.set(shunk_default)
            return

    def on_z_entry_change(self, event=None):
            """Walidacja inputu."""
            z_input = self.z_var.get().replace(",", ".")
            z_default = FREZY_DEFAULT_Z
            try:
                if not z_input.strip():
                    raise ValueError
            except ValueError:
                self.z_var.set(z_default)
                z_input = z_default
                return
            if not validate_positive_int(z_input):
                self.z_var.set(int(float(z_input)))
                return
            self.current_grinding_price_per_piece = get_grinding_price(self.type_var, self.z_var, self.diameter_var,
                                                                       self.quantity_var)
            self.update_price_labels()
            update_button_styles(self.z_buttons, z_input)

    def select_z(self, z_value):
        """Ustawia wybraną ilość ostrzy i aktualizuje styl przycisku."""
        self.z_var.set(z_value)
        #self.current_grinding_price_per_piece(get_grinding_price(self.type_var, self.z_var, self.diameter_var,
          #                                                         self.quantity_var))
        self.update_price_labels()
        update_button_styles(self.z_buttons, z_value)

    def update_price_labels(self):
            price = get_grinding_price(
                self.type_var,
                self.z_var,
                self.diameter_var,
                self.quantity_var
            )

            if price is not None:
                self.current_grinding_price_per_piece.set(price)
                self.grinding_price_label.config(
                    text=f"Cena ostrzenia: {price:.2f} zł / {price * float(self.quantity_var.get()):2f}"
                )
            else:
                self.current_grinding_price_per_piece.set(0.0)
                self.grinding_price_label.config(
                    text="Cena ostrzenia: brak danych"
                )




    def update_price(self):
        pass

    def add_to_cart(self):
        # Tu wrzucisz logikę dodawania do koszyka
        pass

    def fill_edit_fields(self):
        # Tu wrzucisz logikę wypełniania pól w trybie edycji
        pass
