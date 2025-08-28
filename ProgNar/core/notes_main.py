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
        #POBIERZ STAN RABATU Z KOSZYKA
        self.discount_status = "-"  # Do pobrania z cart

        if self.discount_status != "-":
            pass
        else:
            self.discount_check_var = tk.BooleanVar(value = False)
            self.discount_value = tk.StringVar(value='0')

        self.discount_options = ["Szlifowanie", "Powłoka"]
        self.discount_value = tk.StringVar(value = '0')

        #---

        self.discount_option_var = tk.StringVar(value="BRAK")

        # Tworzenie okna
        self.window = tk.Toplevel(parent)
        self.center_window(self.window, 400, 300)
        self.window.title("Edycja uwag")
        #self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()

        # Ramka główna
        self.main_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

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
        self.remarks_text = tk.Text(self.main_frame, height=1, width=40, font=("Arial", 10),relief='solid', bd=2)
        self.remarks_text.pack(pady=5, fill=tk.BOTH)
        if current_remarks != '-':
            self.remarks_text.insert(tk.END, current_remarks)
            self.remarks_text.config(state='normal', bg="white",height=3)
        else:
            self.remarks_text.config(state='disabled', bg="#d3d3d3")
        #Rabatowanie
        self.rabaty_frame()


        #, relief='solid', bd=2
        # Przyciski zapisu i wyjscia
        self.quit_buttons_frame = tk.Frame(self.main_frame)
        self.quit_buttons_frame.pack(pady=5)
        tk.Button(
            self.quit_buttons_frame,
            text="Zapisz",
            command=self.save_remarks,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10,side='left')

        # Przycisk anulowania
        tk.Button(
            self.quit_buttons_frame,
            text="Anuluj",
            command=self.window.destroy,
            font=("Arial", 12),
            bg="#f44336",
            fg="white"
        ).pack(pady=15,padx=20,side='left')

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

    def rabaty_frame(self):
        #glowny frame
        self.rabaty_mainframe = tk.Frame(self.main_frame,relief='solid', bd=2)
        self.rabaty_mainframe.pack(pady = 5,anchor = 'w')
        #checkbox

        tk.Checkbutton(
            self.rabaty_mainframe,
            text="Dodaj rabat",
            variable=self.discount_check_var,
            command=self.toggle_discount_check,
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(pady=1,anchor="nw")

        #discount options
        self.discount_options_frame = tk.Frame(self.rabaty_mainframe)
        #comboboxy

        self.left_discount_frame = tk.Frame(self.discount_options_frame,relief='solid', bd=2)
        self.left_discount_frame.pack()
        self.discount_options = ["Szlifowanie" , "Powłoka"]
        self.discount_options_combo = ttk.Combobox(self.left_discount_frame, state="readonly",
                                         width=10)
        self.discount_options_combo["values"] = self.discount_options
        self.discount_options_combo.current(0)
        self.discount_options_combo.pack(pady=2,side = 'left')
        #self.discount_option_combo.bind("<<ComboboxSelected>>", self.empty)

        self.discount_value_entry = tk.Entry(self.left_discount_frame,textvariable=self.discount_value,width=8)
        self.discount_value_entry.pack(pady=2,padx=10,side = 'left')

        #kwota
        self.cena_frame = tk.Frame(self.main_frame)
        self.cena_frame.pack(pady = 5,anchor = 'w')


    def toggle_discount_check(self):
        if self.discount_check_var.get() == True:
            self.discount_options_frame.pack(pady=2)

        else:
            self.discount_status = "-"
            self.discount_value = "0"
            self.discount_options_frame.pack_forget()

    def empty(self):
        pass
