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
        right_button_frame = tk.Frame(bottom_frame,relief="solid",bd = 2)
        right_button_frame.pack(side=tk.RIGHT, padx=10)

        left_buttons_frame = tk.Frame(right_button_frame,relief='solid' , bd = 1)
        left_buttons_frame.pack(side = tk.LEFT,anchor = 'nw')

        tk.Button(left_buttons_frame, text="Edytuj wybraną pozycję", command=self.edit_selected).pack(pady=6)
        tk.Button(left_buttons_frame, text="Usuń wybraną pozycję", command=self.delete_selected).pack(pady = 6)

        right_labels_frame = tk.Frame(right_button_frame,relief="solid", bd=2)
        right_labels_frame.pack(side=tk.RIGHT)

        self.suma_szlif_label = tk.Label(right_labels_frame, anchor="e", justify="right", text="Suma szlifowanie: 0.00 PLN")
        self.suma_szlif_label.pack(pady=2,fill = 'x')
        self.suma_uslug_label = tk.Label(right_labels_frame, anchor="e", justify="right", text="Suma usługi: 0.00 PLN")
        self.suma_uslug_label.pack(pady=2,fill = 'x')
        self.suma_powlekanie_label = tk.Label(right_labels_frame, anchor="e", justify="right", text="Suma powlekanie: 0.00 PLN")
        self.suma_powlekanie_label.pack(pady=2,fill = 'x')

        self.suma_total_label = tk.Label(right_labels_frame, anchor="e", justify="right", text="Suma: 0.00 PLN", font=("Arial", 12, "bold"))
        self.suma_total_label.pack(pady=5,fill = 'x')

        tk.Button(
            right_labels_frame,
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
        szlifowanie_total = 0.0
        powlekanie_total = 0.0
        total = 0.0

        for item in self.cart.items:
            srednica = float(item.get("Srednica"))
            razem_ciecie = float(item.get("Razem ciecie"))
            razen_zanizenia = float(item.get("Razem zanieznia"))
            razem_szlifowanie = float(item.get("Razem szlifowanie"))
            try:
                razem_powlekanie = float(item.get("Razem powloka"))
            except ValueError:
                razem_powlekanie = 0.0
                continue


            if srednica < 12.1:
                ciecie_do_12_total += razem_ciecie
                ciecie_do_12_count += 1
            else:
                ciecie_ponad_12_total += razem_ciecie
                ciecie_ponad_12_count += 1

            zanizenia_total += razen_zanizenia

            szlifowanie_total += razem_szlifowanie

            uslugi_total = ciecie_ponad_12_total + ciecie_do_12_total + zanizenia_total

            powlekanie_total += razem_powlekanie


            total = szlifowanie_total + uslugi_total + powlekanie_total

            #Zapis CENOWY
        zanizenia_count = int(zanizenia_total / 10)

        self.suma_ciecie_do_12.config(text=f"Cięcie do D12: {ciecie_do_12_count} szt. {ciecie_do_12_total:.2f} PLN")
        self.suma_ciecie_ponad_12.config(text=f"Cięcie ponad D12: {ciecie_ponad_12_count} szt. {ciecie_ponad_12_total:.2f} PLN")
        self.suma_zanizenia.config(text=f"Zaniżenia: {zanizenia_count} szt. {zanizenia_total:.2f} PLN")

        '''
        self.suma_ciecie_do_12.config(text=f"Cięcie do D12: {ciecie_do_12_count} szt. {ciecie_do_12_total:.2f} PLN")
        self.suma_ciecie_ponad_12.config(text=f"Cięcie ponad D12: {ciecie_ponad_12_count} szt. {ciecie_ponad_12_total:.2f} PLN")
        self.suma_zanizenia.config(text=f"Zaniżenia: {zanizenia_count} szt. {zanizenia_total:.2f} PLN")
        self.suma_uslug_dodatkowych.config(text=f"SUMA: {uslugi_total:.2f} PLN")
        self.suma_uslug_label.config(text=f"Suma usług: {uslugi_total:.2f} PLN")
        self.suma_powlekanie_label.config(text=f"Suma powlekanie: {powlekanie_total:.2f} PLN")
        self.suma_total_label.config(text=f"Suma: {total:.2f} PLN")
        '''

    def delete_selected(self):
        """Usuwa wybraną pozycję i aktualizuje etykiety cen."""
        if self.cart.delete_selected(self.cart_tree, self.client_name):
            self.update_price_labels()  # Aktualizuj etykiety cen po usunięciu
        # Widok koszyka jest już aktualizowany w CartMain.delete_selected

    def edit_selected(self):
        self.cart.edit_selected(self.cart_tree,
                                   self.root,self.cart,
                                   self.client_name,self.main_app.handle_frezy_save)




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