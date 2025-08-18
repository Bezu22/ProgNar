import tkinter as tk
from tkinter import messagebox

class BottomSection:
    def __init__(self, parent, cart, cart_tree, client_name, root,main_app):
        self.cart = cart
        self.cart_tree = cart_tree
        self.client_name = client_name
        self.root = root
        self.main_app = main_app
        self._build_ui(parent)

    def _build_ui(self, parent):
        bottom_frame = tk.Frame(parent)
        bottom_frame.pack(fill=tk.X, pady=10)

        # Lewa część
        left_button_frame = tk.Frame(bottom_frame)
        left_button_frame.pack(side=tk.LEFT, padx=10)

        self.suma_ciecie_do_12 = tk.Label(left_button_frame, text="Cięcie do D12: 0 szt. 0.00 PLN", anchor='w')
        self.suma_ciecie_do_12.pack(pady=1, fill='x')

        self.suma_ciecie_ponad_12 = tk.Label(left_button_frame, text="Cięcie ponad D12: 0 szt. 0.00 PLN", anchor='w')
        self.suma_ciecie_ponad_12.pack(pady=1, fill='x')

        self.suma_zanizenia = tk.Label(left_button_frame, text="Zaniżenia: 0 szt. 0.00 PLN", anchor='w')
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
            font=("Arial", 12, "bold"),
            command=self.generate_pdf
        ).pack(pady=10)

        self.cart.update_cart_display(self.cart_tree)
        self.update_price_labels()

    def update_price_labels(self):
        """Aktualizuje etykiety cen na podstawie zawartości koszyka."""
        ciecie_do_12_count = 0
        ciecie_do_12_total = 0.0
        ciecie_ponad_12_count = 0
        ciecie_ponad_12_total = 0.0
        zanizenia_count = 0
        zanizenia_total = 0.0
        uslugi_total = 0.0
        powlekanie_total = 0.0
        total = 0.0

        for item in self.cart.items:
            try:
                # Cięcie
                if item["ciecie"] == "+" and float(item["Srednica"]) <= 12:
                    ciecie_do_12_count += int(item["Ilosc sztuk"])
                    ciecie_do_12_total += float(item["Razem ciecie"])
                elif item["ciecie"] == "+" and float(item["Srednica"]) > 12:
                    ciecie_ponad_12_count += int(item["Ilosc sztuk"])
                    ciecie_ponad_12_total += float(item["Razem ciecie"])
                # Zaniżenia
                if float(item["Cena zanieznia"]) > 0:
                    zanizenia_count += int(item["Ilosc sztuk"])
                    zanizenia_total += float(item["Razem zanieznia"])
                # Usługi
                uslugi_total += float(item["Razem uslugi"])
                # Powlekanie
                if item["Powloka"] != "BRAK":
                    powlekanie_total += float(item["Razem powlekania"])
                # Całkowita suma
                total += float(item["Razem"])
            except (ValueError, KeyError):
                continue

        self.suma_ciecie_do_12.config(text=f"Cięcie do D12: {ciecie_do_12_count} szt. {ciecie_do_12_total:.2f} PLN")
        self.suma_ciecie_ponad_12.config(text=f"Cięcie ponad D12: {ciecie_ponad_12_count} szt. {ciecie_ponad_12_total:.2f} PLN")
        self.suma_zanizenia.config(text=f"Zaniżenia: {zanizenia_count} szt. {zanizenia_total:.2f} PLN")
        self.suma_uslug_dodatkowych.config(text=f"SUMA: {uslugi_total:.2f} PLN")
        self.suma_uslug_label.config(text=f"Suma usług: {uslugi_total:.2f} PLN")
        self.suma_powlekanie_label.config(text=f"Suma powlekanie: {powlekanie_total:.2f} PLN")
        self.suma_total_label.config(text=f"Suma: {total:.2f} PLN")

    def delete_selected(self):
        """Usuwa wybraną pozycję i aktualizuje etykiety cen."""
        if self.cart.delete_selected(self.cart_tree, self.client_name):
            self.cart.update_cart_display(self.cart_tree)
            self.update_price_labels()

    def edit_selected(self):
        """Edytuje wybraną pozycję i aktualizuje etykiety cen."""
        if self.cart.edit_selected(self.cart_tree, self.root, self):
            self.cart.update_cart_display(self.cart_tree)
            self.update_price_labels()

    def clear_cart(self):
        """Czyści koszyk i aktualizuje etykiety cen."""
        if len(self.cart.items) > 0:
            if not messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić koszyk?"):
                return
        self.cart.clear_cart(self.client_name)
        self.client_name.set("- -")
        self.cart.update_cart_display(self.cart_tree)
        self.update_price_labels()

    def save_cart(self):
        """Zapisuje koszyk do pliku."""
        self.cart.save_to_file_with_dialog(self.client_name, self.root)

    def load_cart(self):
        """Wczytuje koszyk z pliku po potwierdzeniu."""
        if len(self.cart.items) > 0:
            if not messagebox.askyesno("Potwierdzenie", "Wczytanie koszyka spowoduje utratę aktualnego. Kontynuować?"):
                return
        if self.cart.load_from_file_with_dialog(self.client_name, self.root, self.cart_tree):
            self.update_price_labels()
        self.main_app.cart.load_from_file(self.main_app.client_name)
        self.main_app.cart.update_cart_display(self.main_app.cart_tree)

    def generate_pdf(self):
        """Generuje raport PDF."""
        self.root.generate_report()