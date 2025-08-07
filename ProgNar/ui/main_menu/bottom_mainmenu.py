import tkinter as tk
from tkinter import messagebox
from config.cart_io import save_cart_to_file, save_cart_to_file_with_dialog, load_cart_from_file, load_cart_from_file_with_dialog, clear_temp_cart


class BottomSection:
    def __init__(self, parent, cart, cart_tree, client_name, root):
        self.cart = cart
        self.cart_tree = cart_tree
        self.client_name = client_name
        self.root = root

        self._build_ui(parent)

    def _build_ui(self, parent):
        bottom_frame = tk.Frame(parent)
        bottom_frame.pack(fill=tk.X, pady=10)

        # Lewa część
        left_button_frame = tk.Frame(bottom_frame)
        left_button_frame.pack(side=tk.LEFT, padx=10)

        self.suma_ciecie_do_12 = tk.Label(left_button_frame, text="Ciecie do D12: 0 szt. 0.00 PLN", anchor='w')
        self.suma_ciecie_do_12.pack(pady=1, fill='x')

        self.suma_ciecie_ponad_12 = tk.Label(left_button_frame, text="Ciecie ponad D12: 0 szt. 0.00 PLN", anchor='w')
        self.suma_ciecie_ponad_12.pack(pady=1, fill='x')

        self.suma_zanizenia = tk.Label(left_button_frame, text="Zanizenia: 0 szt. 0.00 PLN", anchor='w')
        self.suma_zanizenia.pack(pady=1, fill='x')

        self.suma_uslug_dodatkowych = tk.Label(left_button_frame, text="SUMA: 0.00 PLN", font="bold", anchor='w')
        self.suma_uslug_dodatkowych.pack(pady=1, fill='x')

        tk.Button(left_button_frame, text="Wyczyść koszyk", command=self.clear_cart, width=20).pack(pady=5)

        save_load_frame = tk.Frame(left_button_frame)
        save_load_frame.pack(pady=5)
        tk.Button(save_load_frame, text="Zapisz koszyk", command=self.save_cart, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(save_load_frame, text="Wczytaj koszyk", command=self.load_cart, width=10).pack(side=tk.LEFT, padx=2)

        # Prawa część
        right_button_frame = tk.Frame(bottom_frame)
        right_button_frame.pack(side=tk.RIGHT, padx=10)

        tk.Button(right_button_frame, text="Usuń wybraną pozycję", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(right_button_frame, text="Edytuj wybraną pozycję", command=self.edit_selected).pack(side=tk.LEFT, padx=5)

        self.suma_uslug_label = tk.Label(right_button_frame, text="Suma usług: 0.00 PLN")
        self.suma_uslug_label.pack(pady=5)

        self.suma_powlekanie_label = tk.Label(right_button_frame, text="Suma powlekanie: 0.00 PLN")
        self.suma_powlekanie_label.pack(pady=5)

        self.suma_total_label = tk.Label(right_button_frame, text="Suma: 0.00 PLN", font=("Arial", 12, "bold"))
        self.suma_total_label.pack(pady=5)

        tk.Button(
            right_button_frame,
            text="RAPORT",
            width=20,
            bg="red",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        self.cart.update_cart_display(self.cart_tree, self.suma_uslug_label, self.suma_powlekanie_label, self.suma_total_label)


    # 🔧 Metody obsługujące zdarzenia
    def delete_selected(self):
        if self.cart.delete_selected(self.cart_tree, main_app=self):
            self.cart.update_cart_display(
                self.cart_tree,
                self.suma_uslug_label,
                self.suma_powlekanie_label,
                self.suma_total_label
            )

    def edit_selected(self):
        if self.cart.edit_selected(self.cart_tree, self.root, self):
            self.cart.update_cart_display(
                self.cart_tree,
                self.suma_uslug_label,
                self.suma_powlekanie_label,
                self.suma_total_label
            )

    def clear_cart(self):
        if len(self.cart.items) > 0:
            if not messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić koszyk?"):
                return
        self.cart.clear_cart(main_app=self)
        clear_temp_cart()
        self.client_name.set("- -")
        self.cart.update_cart_display(
            self.cart_tree,
            self.suma_uslug_label,
            self.suma_powlekanie_label,
            self.suma_total_label
        )

    def save_cart(self):
        save_cart_to_file_with_dialog(self.cart, self.client_name, self.root)

    def load_cart(self):
        if len(self.cart.items) > 0:
            if not messagebox.askyesno("Potwierdzenie", "Wczytanie koszyka spowoduje utratę aktualnego. Kontynuować?"):
                return
        if load_cart_from_file_with_dialog(self.cart, self.client_name, self.root):
            self.cart.update_cart_display(
                self.cart_tree,
                self.suma_uslug_label,
                self.suma_powlekanie_label,
                self.suma_total_label
            )
            save_cart_to_file(self.cart, self.client_name)


