import tkinter as tk
from tkinter import ttk
import math ,json
from config.utils import add_separator, validate_positive_int, resource_path, get_special_grinding_price,get_cutting_price,get_coating_price
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

        self.special_name_var = tk.StringVar(value="Narzędzie specjalne")
        self.special_price_value = tk.StringVar(value = '40.0')
        self.chamfer_angle_var = tk.StringVar(value="90")
        self.chamfer_radius_var = tk.StringVar(value="1.0")
        self.is_blades_var = tk.BooleanVar(value = True)
        # Sekcje UI
        self.create_type_section()
        self.create_diameter_section()
        self.create_blades_section()
        self.create_quantity_section()
        self.create_powlekanie_section()
        self.create_price_labels()
        self.create_action_buttons()

        self.update_price_labels()

        # Jeśli edytujemy, wypełnij pola danymi z pozycji
        if edit_index is not None:
            self.load_item_data()


    def create_type_section(self):
        tk.Label(self.top, text="Wybierz typ:", font=("Arial", 12)).pack(pady=5)
        frame = tk.Frame(self.top)
        frame.pack(pady=3)
        type_buttons_frame = tk.Frame(frame)
        type_buttons_frame.pack()
        self.type_buttons = {}
        for display_name, json_name in SPEC_TYPES:
            btn = tk.Button(type_buttons_frame, text=display_name, width=10,
                            command=lambda t=json_name: self.select_type(t))
            btn.pack(side="left", padx=5)
            self.type_buttons[json_name] = btn
        update_button_styles(self.type_buttons, self.type_var.get())
        #--- special name --
        self.special_name_frame = tk.Frame(frame)
        self.special_name_entry = tk.Entry(self.special_name_frame,
                                           textvariable = self.special_name_var,
                                           font=("Arial",15),
                                           justify="center",
                                           width=40)
        self.special_name_entry.focus_set()
        self.special_name_entry.selection_range(0, 'end')
        self.special_name_entry.pack(pady=3)
        #---------
        #-----Kat dla fazownika
        self.chamfer_angle_frame = tk.Frame(frame)
        self.chamfer_angle_frame.pack(pady=2)
        chamfer_label_frame = tk.Frame(self.chamfer_angle_frame)
        chamfer_label_frame.pack(side = 'left')
        self.chamfer_angle_label = tk.Label(chamfer_label_frame,text = "Kąt : ",font=('Arial,15'))
        self.chamfer_angle_label.pack()
        chamfer_angle_label = tk.Frame(self.chamfer_angle_frame)
        chamfer_angle_label.pack(side='left')
        self.chamfer_angle_entry = tk.Entry(chamfer_angle_label,
                                            textvariable=self.chamfer_angle_var,
                                            font=("Arial,15"),
                                            justify='center',
                                            width=10)
        self.chamfer_angle_entry.focus_set()
        self.chamfer_angle_entry.selection_range(0, 'end')
        self.chamfer_angle_entry.pack(pady=3)
        #----promien fazownika
        self.chamfer_radius_frame = tk.Frame(frame)
        radius_label_frame = tk.Frame(self.chamfer_radius_frame)
        radius_label_frame.pack(side='left')
        self.chanfer_radius_label = tk.Label(radius_label_frame,text = "Promień: ",font=("Arial,15"))
        self.chanfer_radius_label.pack()
        chamfer_radius_entry_frame = tk.Frame(self.chamfer_radius_frame)
        chamfer_radius_entry_frame.pack(side ='left')
        self.chamfer_radius_entry = tk.Entry(chamfer_radius_entry_frame,
                                             textvariable=self.chamfer_radius_var,
                                             font=("Arial,15"),
                                             justify='center',
                                             width=10)
        self.chamfer_radius_entry.focus_set()
        self.chamfer_radius_entry.selection_range(0, 'end')
        self.chamfer_radius_entry.pack(pady=3)

        add_separator(self.top)

        #relief='solid',bd=2
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
        for display_name, json_name in SPEC_DIAMETER_OPTIONS:
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
        container = tk.Frame(self.top)
        container.pack(pady=1)
        self.frame_for_blades_checkbutton = tk.Frame(container)

        self.blades_checkbutton = tk.Checkbutton(self.frame_for_blades_checkbutton,variable=self.is_blades_var,command=self.turn_blades_on_and_off)
        self.blades_checkbutton.pack()


        tk.Label(container, text="Podaj ilość ostrzy:", font=("Arial", 12)).pack(padx=5,side='left')
        self.z_entry = tk.Entry(container, textvariable=self.z_var, width=8, bg='#D6E8CF')
        self.z_entry.pack(pady=1,side='left')
        self.z_entry.bind("<KeyRelease>", self.on_z_entry_change)
        add_separator(self.top)

    def create_quantity_section(self):
        frame = tk.Frame(self.top)
        frame.pack(pady=2)
        tk.Label(frame, text="Ilość sztuk:", font=("Arial", 12)).pack(side="left", padx=5)
        self.quantity_entry = tk.Entry(frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.pack(side="left", padx=5)
        self.quantity_entry.bind("<KeyRelease>", self.on_quantity_change)

        self.ciecie_check = tk.Checkbutton(frame, text="Cięcie", variable=self.ciecie_var, command=self.update_price_labels)
        self.ciecie_check.pack(side="left", padx=5)
        add_separator(self.top)
    def create_powlekanie_section(self):
        self.coating_frame = tk.Frame(self.top)
        self.coating_frame.pack(pady=3)

        # Etykieta Powłoka
        tk.Label(self.coating_frame, text="Powłoka", font=("Arial", 12)).pack(pady=5)

        # Kontener na opcje powłoki
        self.coating_options_frame = tk.Frame(self.coating_frame)
        self.coating_options_frame.pack(pady=5)

        # Combobox dla powłoki i długości
        self.coating_combo = ttk.Combobox(self.coating_options_frame, textvariable=self.coating_var, state="readonly",
                                          width=30)
        self.length_combo = ttk.Combobox(self.coating_options_frame, textvariable=self.length_var, state="readonly",
                                         width=10)
        self.coating_combo.bind("<<ComboboxSelected>>", self.on_selection_change)
        self.length_combo.bind("<<ComboboxSelected>>", self.on_selection_change)

        # DANE POWŁOK
        self.length_options = set()
        # LISTA TYPOW
        self.coating_options = ["BRAK"] + list(self.coating_data.keys())
        self.coating_combo["values"] = self.coating_options
        # LISTA DLUGOSCI
        for coating_info in self.coating_data.values():
            for diameter_range in coating_info.get("zakres_srednicy", []):
                for entry in diameter_range.get("dlugosc_calkowita", []):
                    self.length_options.add(entry["dlugosc"])

        self.length_options = sorted(self.length_options)
        self.length_combo["values"] = [str(l) for l in self.length_options] if self.length_options else ["Brak danych"]

        # Domyślne wartości
        self.coating_var.set(self.coating_options[0])  # Ustawia "BRAK"
        self.length_var.set(self.length_options[0] if self.length_options else "")  # Ustawia pierwszą długość lub pustą
        self.coating_combo.pack(side="left", padx=5)
        self.length_combo.pack(side="left", padx=5)

        # Długość zawsze dostępna
        self.length_combo.config(state="readonly")

        self.coating_var.trace("w", lambda *args: self.update_price_labels())
        add_separator(self.top)
    def create_price_labels(self):
        self.price_labels_container_frame = tk.Frame(self.top, border=2, relief='solid')
        self.price_labels_container_frame.pack(pady=3, fill='x')

        # Ustawienie grid w kontenerze
        self.price_labels_container_frame.columnconfigure(0, weight=1)
        self.price_labels_container_frame.columnconfigure(1, weight=1)

        # Lewe labele
        self.cutting_price_label = tk.Label(self.price_labels_container_frame,
                                            text=f"Cena cięcia: {self.current_cutting_price_per_piece.get():.2f} zł/ "
                                                 f"{self.current_cutting_price.get():.2f} zł", font=("Arial", 10),
                                            anchor='w')
        self.cutting_price_label.grid(row=0, column=0, sticky='w', padx=5, pady=2)

        self.free_label = tk.Label(self.price_labels_container_frame,
                                             text=f" "
                                                  , font=("Arial", 10),
                                             anchor='w')
        self.free_label.grid(row=1, column=0, sticky='w', padx=5, pady=2)


        self.coating_price_label = tk.Label(self.price_labels_container_frame,
                                            text=f"Cena powłoki: {self.current_coating_price_per_piece.get():.2f} zł / "
                                                 f"{self.current_coating_price.get():.2f} zł",
                                            font=("Arial Bold", 10), anchor='w', bg='#FCBABA', borderwidth=3,
                                            relief='ridge', padx=8, pady=4)
        self.coating_price_label.grid(row=2, column=0, sticky='w', padx=5, pady=2)

        #UKRYTY

        #--
        #Prawe labele
        self.grinding_price_label = tk.Label(self.price_labels_container_frame,
                                             text=f"Cena ostrzenia: {self.current_grinding_price.get():.2f} zł / "
                                                  f"{self.current_grinding_price.get():.2f} zł", font=("Arial", 10),
                                             anchor='e')
        self.grinding_price_label.grid(row=0, column=1, sticky='e', padx=5, pady=2)

        self.price_edit_frame = tk.Frame(self.price_labels_container_frame)
        self.cutting_price_label_small = tk.Label(
            self.price_edit_frame,
            text="Cena/szt",
            font=("Arial", 9),
            anchor='w'
        )
        self.cutting_price_label_small.pack(side='left')
        self.cutting_price_entry = tk.Entry(
            self.price_edit_frame,
            textvariable=self.special_price_value,
            font=("Arial", 10),
            justify="left",
            width=6
        )
        self.cutting_price_entry.pack(side='left',padx=15)
        self.cutting_price_entry.bind("<KeyRelease>", self.on_price_entry)




        # self.bonus_price_label = tk.Label(self.price_labels_container_frame, text=f"Cena usług: {self.bonus_price_var.get():.2f} zł",
        #                                   font=("Arial", 10), anchor='e')
        # self.bonus_price_label.grid(row=1, column=1, sticky='e', padx=5, pady=2)

        self.total_price_label = tk.Label(self.price_labels_container_frame, text=f"Wartość całkowita: {self.total_price_var.get():.2f} zł",
                                          font=("Arial Bold", 10), anchor='e', bg='#FCBABA', borderwidth=3,
                                          relief='ridge', padx=8, pady=4)
        self.total_price_label.grid(row=2, column=1, sticky='e', padx=5, pady=2)

    def create_action_buttons(self):
        self.add_button = tk.Button(self.top, text="Dodaj do koszyka", font=("Arial", 12), command=self.add_to_cart)
        self.add_button.pack(pady=5)
        tk.Button(self.top, text="Zamknij", font=("Arial", 12), command=self.top.destroy).pack(pady=5)
    #----
    def select_type(self, selected_type):
        self.type_var.set(selected_type)
        if selected_type == "Specjalne":
            self.special_name_frame.pack(pady=2)
            # Ukryj zwykły label CENOWY
            # Pokaż entry na cene
            self.price_edit_frame.grid(row=1,column=1, sticky='w', padx=39, pady=2)
            #daj opcje wylaczenia ilosci zebow
            self.frame_for_blades_checkbutton.pack(side='left')
        else:
            self.special_name_frame.pack_forget()
            # Ukryj entry
            self.price_edit_frame.grid_forget()
            #usun opcje wylaczania z
            self.frame_for_blades_checkbutton.pack_forget()
        if selected_type == "Fazownik":
            self.chamfer_angle_frame.pack(pady=2)
        else:
            self.chamfer_angle_frame.pack_forget()
        if selected_type == "Wklesly":
            self.chamfer_radius_frame.pack(pady=2)
        else:
            self.chamfer_radius_frame.pack_forget()

        self.update_price_labels()
        update_button_styles(self.type_buttons, selected_type)
    def select_diameter(self, d_value):
        self.diameter_var.set(d_value)
        self.chwyt_var.set(d_value)

        self.update_price_labels()
        update_button_styles(self.diameter_buttons, d_value)
    def on_diameter_entry_change(self, event=None):
        """Walidacja inputu srednicy."""

        diam_input = self.diameter_var.get().replace(",", ".")
        diam_default = "10"
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

        # Korekcja chwytu
        if diam_float > chwyt_float:
            self.chwyt_var.set(int(math.ceil(diam_float / 2.0)) * 2)

        self.diameter_var.set(diam_input)
        self.update_price_labels()
        update_button_styles(self.diameter_buttons, diam_input)
    def on_shunk_entry_change(self, event=None):
        shunk_input = self.chwyt_var.get().replace(",", ".")
        shunk_default = "10"
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
            z_default = "4"
            try:
                if not z_input.strip():
                    raise ValueError
            except ValueError:
                self.z_var.set(z_default)
                return
            if not validate_positive_int(z_input):
                self.z_var.set(z_default)
                return
            self.update_price_labels()
    def on_quantity_change(self,event=None):
        quantity_input = self.quantity_var.get()
        quantity_default = "1"
        try:
            if not quantity_input.strip():
                raise ValueError
        except ValueError:
            self.quantity_var.set(quantity_default)
            return
        if not validate_positive_int(quantity_input):
            self.quantity_var.set(quantity_default)
            return
        self.update_price_labels()
    def on_selection_change(self, event=None):
        """Wywołuje callback po zmianie powłoki lub długości."""
        if self.coating_var.get() == "BRAK":
            # Przy BRAK ustawiamy domyślną długość, ale combobox pozostaje aktywny
            self.length_combo["values"] = [str(l) for l in self.length_options] if self.length_options else [
                "Brak danych"]
            if self.length_options and not self.length_var.get():
                self.length_var.set(self.length_options[0])
            self.length_combo.config(state="readonly")
        else:
            self.length_combo["values"] = [str(l) for l in self.length_options] if self.length_options else [
                "Brak danych"]
            self.length_combo.config(state="readonly")
            if self.length_options and not self.length_var.get():
                self.length_var.set(self.length_options[0])

        #Aktualizacja cen tylko jeśli etykiety cenowe istnieją
        if hasattr(self, 'grinding_price_label') and self.grinding_price_label is not None:
            self.update_price_labels()

    def on_price_entry(self,event=None):
        """Walidacja inputu srednicy."""

        price_input = self.special_price_value.get().replace(",", ".")
        price_default = 12.34
        # Obsluga pustego pola
        try:
            price_float = float(price_input)
            if price_float == 0:
                raise ValueError
        except ValueError:
            self.special_price_value.set(price_default)
            return

        self.special_price_value.set(price_input)
        self.update_price_labels()

    def add_to_cart(self):
        # Zbieranie parametrów frezu
        nazwa = self.type_var.get()
        #ustaw nazwe
        if nazwa == 'Fazownik':
            nazwa += f" (k={self.chamfer_angle_var.get()})"
        elif nazwa == 'Wklesly':
            nazwa += f" (r={self.chamfer_radius_var.get()})"
        else:
            nazwa = f"*{self.special_name_var.get()}"
        #ustaw zeby
        z_var = self.z_var.get()
        if self.z_var.get() == '0':
            z_var = '-'

        params = {
            "Nazwa": nazwa,
            "Srednica": self.diameter_var.get(),
            "fiChwyt": self.chwyt_var.get(),
            "Ilosc ostrzy": z_var,
            "Ilosc sztuk": self.quantity_var.get(),
            "ciecie": "+" if self.ciecie_var.get() else "-",
            "Powloka": self.coating_var.get(),
            "Dlugosc calkowita": str(self.length_var.get()),
            "Uwagi status": self.remarks_var.get(),
            "Uwagi": self.remarks_value.get()
        }

        prices = {
            "Cena szlifowania": f"{self.current_grinding_price_per_piece.get():.2f}",
            "Razem szlifowanie": f"{self.current_grinding_price.get():.2f}",
            "Cena powlekania": f"{self.current_coating_price_per_piece.get():.2f}" if self.coating_var.get() != "BRAK" else "-",
            "Razem powloka": f"{self.current_coating_price.get():.2f}" if self.coating_var.get() != "BRAK" else "-",
            "Cena ciecia": f"{self.current_cutting_price_per_piece.get():.2f}",
            "Razem ciecie": f"{self.current_cutting_price.get():.2f}",
            "Cena zanieznia": f"{self.current_lowering_price_per_piece.get():.2f}",
            "Razem zanieznia": f"{self.current_lowering_price.get():.2f}",
            #przypisuje ciecie bo jest jedynym extrasem tu a musi zostac do temp_cart.json
            "Razem uslugi": f"{self.current_cutting_price.get():.2f}",
            "Razem": f"{self.total_price_var.get():.2f}",
            "Rabat ostrzenie": f"{self.grinding_discount_value.get()}",
            "Rabat powloka": f"{self.coating_discount_value.get()}",
            "Rabat ciecie": f"{self.cutting_discount_value.get()}",
            "Rabat zanizenie": f"{self.lowering_discount_value.get()}",

        }

        if self.edit_index is not None:
            # Aktualizuj istniejącą pozycję
            self.cart.items[self.edit_index] = params | prices
            self.cart.save_to_file(self.client_name)
        else:
            # Dodaj nową pozycję
            self.cart.add_item(params, prices, self.client_name)

        if self.on_save:
            self.on_save()  # Call the on_save callback to refresh the cart display
    def update_price_labels(self):
        print(f"Typ: {self.type_var.get()}, Ostrza: {self.z_var.get()}, Średnica: {self.diameter_var.get()}, Ilość: {self.quantity_var.get()}")
        self.grinding_price = get_special_grinding_price(
            self.type_var,
            self.z_var,
            self.diameter_var,
            self.quantity_var
        )
        print(self.grinding_price)
        if not self.grinding_price == None:
            self.current_grinding_price_per_piece.set(self.grinding_price)
            self.current_grinding_price.set(self.grinding_price * float(self.quantity_var.get()))

        else:
            self.grinding_price = self.special_price_value.get()
            self.current_grinding_price_per_piece.set(self.grinding_price)
            self.current_grinding_price.set(float(self.grinding_price) * float(self.quantity_var.get()))
        self.grinding_price_label.config(
            text=f"Cena ostrzenia: {self.current_grinding_price_per_piece.get():.2f} zł / {self.current_grinding_price.get():.2f} zł",
            font=("Arial", 10))




        if self.ciecie_var.get():
            # Checkbox zaznaczony — dodaj cenę cięcia
            self.ciecie_price = get_cutting_price(self.diameter_var)
            self.current_cutting_price_per_piece.set(self.ciecie_price)
            self.current_cutting_price.set(self.ciecie_price * int(self.quantity_var.get()))

            self.cutting_price_label.config(
                text=f"Cena cięcia: {self.ciecie_price:.2f} zł/ "
                     f"{self.current_cutting_price.get():.2f} zł", font=("Arial", 10))
        else:
            # Checkbox odznaczony — usuń cenę cięcia
            self.ciecie_price = 0.00
            self.current_cutting_price_per_piece.set(self.ciecie_price)
            self.current_cutting_price.set(self.ciecie_price)
            self.cutting_price_label.config(
                text=f"Cena cięcia: {self.ciecie_price:.2f} zł/ "
                     f"{self.ciecie_price * int(self.quantity_var.get()):.2f} zł", font=("Arial", 10))

        # POWLOKA
        if self.coating_var.get() == "BRAK":
            self.coating_price = 0.00
            self.current_coating_price_per_piece.set(self.coating_price)
            self.current_coating_price.set(self.coating_price)
        else:
            self.coating_price = get_coating_price(self.diameter_var.get(), self.coating_var.get(),
                                                   self.length_var.get(), self.coating_data)
            self.current_coating_price_per_piece.set(self.coating_price)
            self.current_coating_price.set(self.coating_price * int(self.quantity_var.get()))
        self.coating_price_label.config(
            text=f"Cena powłoki: {self.current_coating_price_per_piece.get():.2f} zł / "
                 f"{self.current_coating_price.get():.2f} zł", font=("Arial", 10))

        # # EXTRAS
        # self.extras_price = self.current_cutting_price.get()
        # self.bonus_price_var.set(self.extras_price)
        # self.bonus_price_label.config(
        #     text=f"Cena usług: {self.bonus_price_var.get():.2f} zł", font=("Arial", 10))
        # TOTAL
        self.total_price = self.current_grinding_price.get() + self.current_cutting_price.get()
        self.total_price_var.set(self.total_price)
        self.total_price_label.config(
            text=f"Wartość całkowita: {self.total_price_var.get():.2f} zł", font=("Arial", 10))

    def load_item_data(self):
        """Wypełnia pola danymi edytowanej pozycji."""
        item = self.cart.items[self.edit_index]
        #TYP
        type = item["Nazwa"]
        #TODO NIE RUSZONA FUNKCJA - DO ZROBIENIA
        if type.startswith("Fazownik"):
            self.select_type("Fazownik")
            value = float(type.split("k=")[1].split(")")[0].strip())
            self.chamfer_angle_var.set(str(value))
        elif type.startswith("Wklesly"):
            self.select_type("Wklesly")
            value = float(type.split("r=")[1].split(")")[0].strip())
            self.chamfer_radius_var.set(str(value))
        else:
            self.select_type("Specjalne")
            value = type
            self.special_name_var.set(value)

        #SREDNICE
        new_diam = item["Srednica"]
        self.diameter_var.set(new_diam)
        update_button_styles(self.diameter_buttons, new_diam)
        self.chwyt_var.set(item["fiChwyt"])
        #zeby
        new_z = item["Ilosc ostrzy"]
        if new_z=="-":
            self.z_var.set("0")
            self.is_blades_var.set(False)
            self.z_entry.config(state="disabled")
        else:
            self.z_var.set(new_z)

        self.quantity_var.set(str(item["Ilosc sztuk"]))
        self.ciecie_var.set(item["ciecie"] == "+")
        self.coating_var.set(item["Powloka"])
        self.length_var.set(item["Dlugosc calkowita"])


        self.remarks_var.set(item["Uwagi status"])
        self.remarks_value.set(item["Uwagi"])


        # Wypełnianie zmiennych cenowych
        self.current_grinding_price_per_piece.set(float(item["Cena szlifowania"]))
        self.current_grinding_price.set(float(item["Razem szlifowanie"]))
        self.current_cutting_price_per_piece.set(float(item["Cena ciecia"]))
        self.current_cutting_price.set(float(item["Razem ciecie"]))
        self.current_lowering_price_per_piece.set(float(item["Cena zanieznia"]))
        self.current_lowering_price.set(float(item["Razem zanieznia"]))
        self.bonus_price_var.set(float(item["Razem uslugi"]))
        self.total_price_var.set(float(item["Razem"]))


        try:
            self.current_coating_price_per_piece.set(float(item["Cena powlekania"]))
            self.current_coating_price.set(float(item["Razem powloka"]))
        except ValueError:
            print("brak cen dla powlekania - ustawiam na 0.0")
            self.current_coating_price_per_piece.set(0.00)
            self.current_coating_price.set(0.00)
        self.grinding_discount_value.set(int(item["Rabat ostrzenie"]))
        self.coating_discount_value.set(int(item["Rabat powloka"]))
        self.cutting_discount_value.set(int(item["Rabat ciecie"]))
        self.lowering_discount_value.set(int(item["Rabat zanizenie"]))
        print(self.grinding_discount_value.get())


        self.add_button.config(text= "Zapisz zmiany")
        self.update_price_labels()

    def load_coating_json(self ):
        with open(resource_path("data/cennik_powloki.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def turn_blades_on_and_off(self):

        if self.is_blades_var.get() is False:
            self.z_entry.config(state='disabled')  # zablokuj
            self.z_var.set("0")
        else:
            self.z_entry.config(state='normal')  # odblokuj
            self.z_var.set("4")

