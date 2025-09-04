import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class NotesMenu:
    """Klasa zarządzająca oknem edycji uwag dla pozycji w koszyku."""

    def __init__(self, parent, cart, item_index, main_app):
        """
        Inicjalizuje okno edycji uwag.
        Args:
            parent: Rodzic okna (np. root).
            cart: Obiekt koszyka.
            item_index: Indeks edytowanej pozycji w koszyku.
            main_app: Referencja do głównej aplikacji (ToolPricingApp).
        """
        self.parent = parent
        self.cart = cart
        self.item_index = item_index
        self.main_app = main_app

        self.item = self.cart.items[self.item_index]
        #pobierz cene szlifowania
        self.default_grinding_price = tk.DoubleVar(value = float(self.item["Cena szlifowania"]))
        #pobierz cene powloki
        try:
            coating_price = float(self.item["Cena powlekania"])
        except (ValueError, TypeError):
            coating_price = 0.0
        self.default_coating_price = tk.DoubleVar(value = coating_price)
        #pobierz cene uslug
        self.default_cutting_price = tk.DoubleVar(value = float(self.item["Cena ciecia"]))
        self.default_lowering_price = tk.DoubleVar(value= float(self.item["Cena zanieznia"]))

        self.discount_check_var = tk.BooleanVar(value=False) #Glowny check od rabatow

        self.grinding_discount_check = tk.BooleanVar(value=False)
        self.grinding_discount = tk.IntVar(value=0)
        self.coating_discount_check = tk.BooleanVar(value=False)
        self.coating_discount = tk.IntVar(value=0)
        self.cutting_discount_check = tk.BooleanVar(value=False)
        self.cutting_discount = tk.IntVar(value=0)
        self.lowering_discount_check = tk.BooleanVar(value=False)
        self.lowering_discount = tk.IntVar(value=0)

        # Tworzenie okna
        self.window = tk.Toplevel(parent)
        self.center_window(self.window, 500, 500)
        self.window.title("Edycja uwag")
        self.window.transient(parent)
        self.window.grab_set()

        # Ramka główna
        self.main_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #podglad cen
        self.prices_display()
        #uwagi
        self.uwagi_frame()
        #Rabatowanie
        self.rabaty_frame()
        #botoom
        # Przyciski zapisu i wyjscia
        self.leave_section()
        #, relief='solid', bd=2
        #pobierz wartosci
        self.set_values()

    def center_window(self, window, width=400, height=300):
        window.update_idletasks()  # Upewnia się, że rozmiary są aktualne

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_remarks_field(self):
        """Włącza/wyłącza pole tekstowe na podstawie stanu checkboxa."""
        if self.remarks_active_var.get():
            self.remarks_text.config(state='normal', bg="white",height=3)
            self.remarks_text.focus_set()
        else:
            self.remarks_text.delete("1.0", tk.END)
            self.remarks_text.config(state='disabled', bg="#d3d3d3",height=1)

    def save_remarks(self):
        """Zapisuje uwagi do pozycji w koszyku i aktualizuje widok."""
        if self.remarks_active_var.get():
            remarks = self.remarks_text.get("1.0", tk.END).strip()
            if not remarks:
                messagebox.showwarning("Błąd", "Pole uwag nie może być puste, jeśli jest aktywne.")
                return
            self.cart.items[self.item_index]['Uwagi'] = remarks
        else:
            self.cart.items[self.item_index]['Uwagi'] = '-'

        # Zapis do pliku tymczasowego
        try:
            self.cart.save_to_file(self.main_app.client_name)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać uwag: {str(e)}")

        # Aktualizacja widoku koszyka
        self.cart.update_cart_display(self.main_app.cart_tree)

        self.window.destroy()
    def prices_display(self):
        self.prices_grid = tk.Frame(self.main_frame)
        self.prices_grid.pack(pady=5,anchor = 'w')
        self.current_grinding_price_label = tk.Label(self.prices_grid,
                                       text=f"Cena szlif szt: {self.default_grinding_price.get():.2f} zł",
                                       font=("Arial", 12))
        self.current_grinding_price_label.grid(row=0, column=0, sticky='w', padx=40)
        self.current_coating_price_label = tk.Label(self.prices_grid,
                                      text=f"Cena powlekanie szt : {self.default_coating_price.get():.2f} zł",
                                      font=("Arial", 12))
        self.current_coating_price_label.grid(row=0, column=1, sticky='w')

        self.extras_grid = tk.Frame(self.main_frame)
        self.extras_grid.pack(pady=5,padx=5,anchor='w')
        self.current_cutting_price_label = tk.Label(self.extras_grid,
                                                    text=f"Cena ciecia szt: {self.default_cutting_price.get():.2f} zł",
                                                    font=("Arial", 10))
        self.current_cutting_price_label.grid(row=0,column=0,sticky='w',padx=40)
        self.current_lowering_price_label = tk.Label(self.extras_grid,
                                                    text=f"Cena szyjki szt: {self.default_lowering_price.get():.2f} zł",
                                                    font=("Arial", 10))
        self.current_lowering_price_label.grid(row=0, column=1, sticky='e',padx=60)


    def uwagi_frame(self):
        # Checkbox do aktywacji pola uwag
        current_remarks = self.cart.items[self.item_index].get('Uwagi', '-')
        self.remarks_active_var = tk.BooleanVar(value=current_remarks != '-')
        tk.Checkbutton(
            self.main_frame,
            text="Dodaj uwagi",
            variable=self.remarks_active_var,
            command=self.toggle_remarks_field,
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(anchor="nw", pady=5)

        # Pole tekstowe na uwagi (3 linie)
        self.remarks_text = tk.Text(self.main_frame, height=1, width=40, font=("Arial", 10), relief='solid', bd=2)
        self.remarks_text.pack(pady=5, fill=tk.BOTH)
        if current_remarks != '-':
            self.remarks_text.insert(tk.END, current_remarks)
            self.remarks_text.config(state='normal', bg="white", height=3)
        else:
            self.remarks_text.config(state='disabled', bg="#d3d3d3")

    def rabaty_frame(self):
        #glowny frame
        rabaty_mainframe = tk.Frame(self.main_frame,relief='solid', bd=2)
        rabaty_mainframe.pack(pady = 5,fill = 'x')
        #checkbox
        leftframe = tk.Frame(rabaty_mainframe, relief='solid', bd=2)
        leftframe.pack(pady=1, anchor='nw')

        tk.Checkbutton(
            leftframe,
            text="Dodaj rabat",
            variable=self.discount_check_var,
            command=self.toggle_discount_check,
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(pady=1,anchor="nw")

        #discount options
        self.discount_options_frame = tk.Frame(leftframe)

        #checkboxy
        self.combogrid = tk.Frame(self.discount_options_frame,border=2, relief='solid')
        self.combogrid.pack()


        #rabat szlif
        tk.Checkbutton(self.combogrid, text="Rabat ostrzenie %", variable=self.grinding_discount_check,
                                                 command=self.toggle_discount_entry).grid(
            row=0, column=0, sticky='w', padx=2, pady=2)
        self.grinding_disc_entry = tk.Entry(self.combogrid, textvariable=self.grinding_discount, width=4, state='disabled')
        self.grinding_disc_entry.grid(row=0, column=1, sticky='w', padx=2, pady=2)
        #rabat powloka
        tk.Checkbutton(self.combogrid, text="Rabat powłoka %", variable=self.coating_discount_check,
                                                  command=self.toggle_discount_entry).grid(
            row=1, column=0, sticky='w', padx=2, pady=2)
        self.coating_discount_entry = tk.Entry(self.combogrid, textvariable=self.coating_discount, width=4, state='disabled')
        self.coating_discount_entry.grid(row=1, column=1, sticky='w', padx=2, pady=2)
        # rabat ciecie
        tk.Checkbutton(self.combogrid, text="Rabat ciecie %", variable=self.cutting_discount_check,
                                               command=self.toggle_discount_entry).grid(
            row=2, column=0, sticky='w', padx=2, pady=2)
        self.cutting_discount_entry = tk.Entry(self.combogrid, textvariable=self.cutting_discount, width=4, state='disabled')
        self.cutting_discount_entry.grid(row=2, column=1, sticky='w', padx=2, pady=2)
        # rabat zanizenie
        tk.Checkbutton(self.combogrid, text="Rabat zanizenie %", variable=self.lowering_discount_check,
                       command=self.toggle_discount_entry).grid(
            row=3, column=0, sticky='w', padx=2, pady=2)
        self.lowering_discount_entry = tk.Entry(self.combogrid, textvariable=self.lowering_discount, width=4,
                                               state='disabled')
        self.lowering_discount_entry.grid(row=3, column=1, sticky='w', padx=2, pady=2)


    def leave_section(self):
        self.quit_buttons_frame = tk.Frame(self.main_frame)
        self.quit_buttons_frame.pack(pady=5)
        tk.Button(
            self.quit_buttons_frame,
            text="Zapisz",
            command=self.save_remarks,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10, side='left')

        # Przycisk anulowania
        tk.Button(
            self.quit_buttons_frame,
            text="Anuluj",
            command=self.window.destroy,
            font=("Arial", 12),
            bg="#f44336",
            fg="white"
        ).pack(pady=15, padx=20, side='left')

    def toggle_discount_entry(self):
        #szlif
        if self.grinding_discount_check.get():
            self.grinding_disc_entry.config(state = 'normal')
            self.grinding_disc_entry.focus_set()
            self.grinding_disc_entry.selection_range(0, 'end')
        else:
            self.grinding_disc_entry.config(state = 'disabled')
            self.grinding_discount.set(0)
        #powloka
        if self.coating_discount_check.get():
            self.coating_discount_entry.config(state = 'normal')
            self.coating_discount_entry.focus_set()
            self.coating_discount_entry.selection_range(0, 'end')
        else:
            self.coating_discount_entry.config(state = 'disabled')
            self.coating_discount.set(0)
        #ciecie
        if self.cutting_discount_check.get():
            self.cutting_discount_entry.config(state = 'normal')
            self.cutting_discount_entry.focus_set()
            self.cutting_discount_entry.selection_range(0, 'end')
        else:
            self.cutting_discount_entry.config(state = 'disabled')
            self.cutting_discount.set(0)
        #zanizenie
        if self.lowering_discount_check.get():
            self.lowering_discount_entry.config(state = 'normal')
            self.lowering_discount_entry.focus_set()
            self.lowering_discount_entry.selection_range(0, 'end')
        else:
            self.lowering_discount_entry.config(state = 'disabled')
            self.lowering_discount.set(0)



    def toggle_discount_check(self):
        if self.discount_check_var.get():
            self.discount_options_frame.pack(anchor = "nw", padx = 5)
        else:
            self.grinding_discount_check.set(False)
            self.grinding_discount.set(0)
            self.coating_discount_check.set(False)
            self.coating_discount.set(0)
            self.cutting_discount_check.set(False)
            self.cutting_discount.set(0)
            self.lowering_discount_check.set(False)
            self.lowering_discount.set(0)

            self.discount_options_frame.pack_forget()

    def set_values(self):
        #Ceny
        self.current_grinding_price_per_piece = tk.DoubleVar(value=self.default_grinding_price.get())
        self.current_coating_price_per_piece = tk.DoubleVar(value=self.default_coating_price.get())
        self.current_cutting_price_per_piece = tk.DoubleVar(value=self.default_cutting_price.get())
        self.current_lowering_price_per_piece = tk.DoubleVar(value=self.default_lowering_price.get())

        # POBIERZ STAN RABATU Z KOSZYKA
        self.acc_grinding_discount = self.item["Rabat ostrzenie"]
        self.acc_coating_discount = self.item["Rabat powloka"]
        self.acc_cutting_discount = self.item["Rabat ciecie"]
        self.acc_lowering_discount = self.item["Rabat zanizenie"]

        if self.acc_grinding_discount != "0" or self.acc_coating_discount != "0" or self.acc_cutting_discount != "0" or self.acc_lowering_discount != "0":
            self.grinding_discount.set(int(self.acc_grinding_discount))
            self.coating_discount.set(int(self.acc_coating_discount))
            self.cutting_discount.set(int(self.acc_cutting_discount))
            self.lowering_discount.set(int(self.acc_lowering_discount))
            # Wlacza okno rabatowe
            self.discount_check_var.set(True)
            self.toggle_discount_check()

            if self.acc_grinding_discount != "0":
                self.grinding_discount_check.set(True)
            if self.acc_coating_discount != "0":
                self.coating_discount_check.set(True)
            if self.acc_cutting_discount != "0":
                self.cutting_discount_check.set(True)
            if self.acc_lowering_discount != "0":
                self.lowering_discount_check.set(True)

            self.toggle_discount_entry()


    def refresh(self):
        #jesli cena jest zmieniona zmien kolor tekstu
        '''
        self.current_grinding_price_label
        self.current_coating_price_label
        self.current_cutting_price_label
        self.current_lowering_price_label'''



        pass

    def empty(self):
        pass
