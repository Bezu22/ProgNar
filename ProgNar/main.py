# main.py - Główny moduł aplikacji z menu głównym i koszykiem

import tkinter as tk

from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cart import Cart
from tools_menu.frezy_menu import FrezyMenu
from tools_menu.wiertla_menu import WiertlaMenu
from ProgNar.tools_menu.pozostale_menu import PozostaleMenu
from ProgNar.tools_menu.uslugi_menu import UslugiMenu
from ProgNar.config.utils import format_price
from cenniki import CennikiMenu

class ToolPricingApp:
    """Główna klasa aplikacji z menu głównym i koszykiem."""
    def __init__(self, root):
        """
        Inicjalizuje aplikację.
        Args:
            root (tk.Tk): Główne okno aplikacji.
        """
        # Inicjalizacja głównego okna
        self.root = root
        self.root.title("ProgNar – System Regeneracji i Wyceny Narzędzi")
        self.root.geometry("1200x500")  # Rozszerzone okno

        self.cart = Cart()

        # Lewa ramka dla menu
        self.left_frame = tk.Frame(self.root, width=450, bg="lightgrey")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Etykieta tytułu
        tk.Label(self.left_frame, text="ProgNar", bg="lightgrey", padx=60, font=("Arial", 18)).pack(pady=20)

        # Ramka dla przycisków Frezy i Wiertła (w jednej linii)
        button_row_frame = tk.Frame(self.left_frame, bg="lightgrey")
        button_row_frame.pack(pady=10)

        # Przygotowanie obrazów dla przycisków
        try:
            # Wczytanie i przeskalowanie obrazów
            mill_img = Image.open("img/mill.jpg").resize((50, 50), Image.Resampling.LANCZOS)
            drill_img = Image.open("img/drill.jpg").resize((50, 50), Image.Resampling.LANCZOS)
            special_img = Image.open("img/special.jpg").resize((150, 50), Image.Resampling.LANCZOS)
            uslugi_img = Image.open("img/uslugi.png").resize((120, 40), Image.Resampling.LANCZOS)
            logo_img = Image.open("img/logo.png").resize((150, 50), Image.Resampling.LANCZOS)
            self.mill_photo = ImageTk.PhotoImage(mill_img)
            self.drill_photo = ImageTk.PhotoImage(drill_img)
            self.special_photo = ImageTk.PhotoImage(special_img)
            self.uslugi_photo = ImageTk.PhotoImage(uslugi_img)
            self.logo_photo = ImageTk.PhotoImage(logo_img)

            # Ramka dla przycisku Frezy
            frezy_frame = tk.Frame(button_row_frame, bg="lightgrey")
            frezy_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(frezy_frame, text="Frezy", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(
                frezy_frame,
                image=self.mill_photo,
                command=self.show_frezy_menu,
                width=50,
                height=50
            ).pack()

            # Ramka dla przycisku Wiertła
            wiertla_frame = tk.Frame(button_row_frame, bg="lightgrey")
            wiertla_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(wiertla_frame, text="Wiertła", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(
                wiertla_frame,
                image=self.drill_photo,
                command=self.show_wiertla_menu,
                width=50,
                height=50
            ).pack()
        except Exception as e:
            print(f"Błąd wczytywania obrazów: {e}")

            # Fallback: Przyciski tekstowe
            frezy_frame = tk.Frame(button_row_frame, bg="lightgrey")
            frezy_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(frezy_frame, text="Frezy", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(frezy_frame, text="Frezy", font=("Arial", 14), command=self.show_frezy_menu).pack()

            wiertla_frame = tk.Frame(button_row_frame, bg="lightgrey")
            wiertla_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(wiertla_frame, text="Wiertła", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(wiertla_frame, text="Wiertła", font=("Arial", 14), command=self.show_wiertla_menu).pack()

            pozostale_frame = tk.Frame(button_row_frame, bg="lightgrey")
            pozostale_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(pozostale_frame, text="Pozostałe", bg="lightgrey", font=("Arial", 10)).pack()
            tk.Button(pozostale_frame, text="Pozostałe", font=("Arial", 14), command=self.show_pozostale_menu, width=15).pack()

        # Ramka dla przycisku Pozostałe
        pozostale_frame = tk.Frame(self.left_frame, bg="lightgrey")
        pozostale_frame.pack(pady=5)
        tk.Label(pozostale_frame, text="Pozostałe", bg="lightgrey", font=("Arial", 10)).pack()
        try:
            tk.Button(
                pozostale_frame,
                image=self.special_photo,
                command=self.show_pozostale_menu,
                width=150,
                height=50
            ).pack()
        except AttributeError:
            tk.Button(pozostale_frame, text="Pozostałe", font=("Arial", 14), command=self.show_pozostale_menu, width=15).pack()

        # Ramka dla przycisku Usługi
        uslugi_frame = tk.Frame(self.left_frame, bg="lightgrey")
        uslugi_frame.pack(pady=5)
        tk.Label(uslugi_frame, text="Usługi", bg="lightgrey", font=("Arial", 10)).pack()
        try:
            tk.Button(
                uslugi_frame,
                image=self.uslugi_photo,
                command=self.show_uslugi_menu,
                width=150,
                height=50
            ).pack()
        except AttributeError:
            tk.Button(uslugi_frame, text="Usługi", font=("Arial", 14), command=self.show_uslugi_menu, width=15).pack()

        # Przycisk Wyjście
        tk.Button(self.left_frame, text="Wyjście", font=("Arial", 14), command=self.root.quit).pack(pady=20)

        # Ramka dla loga
        logo_frame = tk.Frame(self.left_frame, bg="lightgrey")
        logo_frame.pack(pady=5)
        try:
            tk.Button(
                logo_frame,
                image=self.logo_photo,
                command=self.show_cenniki_menu,
                relief="flat",
                borderwidth=0,
                bg="lightgrey",
                activebackground="lightgrey"
            ).pack()
        except AttributeError:
            tk.Label(logo_frame, text="Logo niedostępne", bg="lightgrey", font=("Arial", 10)).pack()

        # Prawa ramka dla koszyka
        self.right_frame = tk.Frame(self.root, width=750)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Ramka dla tabeli i suwaków
        tree_scroll_frame = tk.Frame(self.right_frame, borderwidth=1, relief="solid")
        tree_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tabela koszyka
        columns = ("LP", "Nazwa", "Srednica", "fiChwyt", "Ilosc zebow", "Ilosc sztuk", "ciecie", "Cena/szt", "Wartosc", "Powlekanie", "L", "Cena powlekania/szt", "Wartosc powlekania", "Uwagi")
        self.cart_tree = ttk.Treeview(tree_scroll_frame, columns=columns, show="headings")
        self.cart_tree.heading("LP", text="L.P.")
        self.cart_tree.heading("Nazwa", text="Nazwa")
        self.cart_tree.heading("Srednica", text="φOD")
        self.cart_tree.heading("fiChwyt", text="φChwyt")
        self.cart_tree.heading("Ilosc zebow", text="z")
        self.cart_tree.heading("Ilosc sztuk", text="Ilość sztuk")
        self.cart_tree.heading("ciecie", text="cięcie")
        self.cart_tree.heading("Cena/szt", text="Cena/szt")
        self.cart_tree.heading("Wartosc", text="Netto")
        self.cart_tree.heading("Powlekanie", text="Powłoka")
        self.cart_tree.heading("L", text="L")
        self.cart_tree.heading("Cena powlekania/szt", text="Cena powlekania/szt")
        self.cart_tree.heading("Wartosc powlekania", text="Wartość powlekania")
        self.cart_tree.heading("Uwagi", text="Uwagi")

        # Ustawienie szerokości kolumn
        self.cart_tree.column("LP", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Nazwa", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Srednica", width=60, anchor=tk.CENTER)
        self.cart_tree.column("fiChwyt", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Ilosc zebow", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Ilosc sztuk", width=80, anchor=tk.CENTER)
        self.cart_tree.column("ciecie", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Cena/szt", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Wartosc", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Powlekanie", width=100, anchor=tk.CENTER)
        self.cart_tree.column("L", width=60, anchor=tk.CENTER)
        self.cart_tree.column("Cena powlekania/szt", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Wartosc powlekania", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Uwagi", width=100, anchor=tk.CENTER)

        # Suwak pionowy
        v_scrollbar = ttk.Scrollbar(tree_scroll_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=v_scrollbar.set)

        # Suwak poziomy
        h_scrollbar = ttk.Scrollbar(tree_scroll_frame, orient=tk.HORIZONTAL, command=self.cart_tree.xview)
        self.cart_tree.configure(xscrollcommand=h_scrollbar.set)

        # Układ tabeli i suwaków
        self.cart_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        tree_scroll_frame.grid_rowconfigure(0, weight=1)
        tree_scroll_frame.grid_columnconfigure(0, weight=1)

        # Przyciski
        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Usuń wybraną pozycję", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edytuj wybraną pozycję", command=self.edit_selected).pack(side=tk.LEFT, padx=5)

        # Etykiety sum
        self.suma_uslug_label = tk.Label(self.right_frame, text="Suma usług: 0.00 PLN")
        self.suma_uslug_label.pack(pady=5)
        self.suma_powlekanie_label = tk.Label(self.right_frame, text="Suma powlekanie: 0.00 PLN")
        self.suma_powlekanie_label.pack(pady=5)
        self.suma_total_label = tk.Label(self.right_frame, text="Suma: 0.00 PLN", font=("Arial", 12, "bold"))
        self.suma_total_label.pack(pady=5)

        # Inicjalizacja koszyka
        self.update_cart_display()

    def show_frezy_menu(self):
        """Otwiera menu frezów."""
        FrezyMenu(self.root, self.cart, main_app=self)

    def show_wiertla_menu(self):
        """Otwiera menu wierteł."""
        WiertlaMenu(self.root, self.cart, main_app=self)

    def show_pozostale_menu(self):
        """Otwiera menu pozostałych pozycji."""
        PozostaleMenu(self.root, self.cart, main_app=self)

    def show_uslugi_menu(self):
        """Otwiera menu usług."""
        UslugiMenu(self.root, self.cart, main_app=self)

    def show_cenniki_menu(self):
        """Otwiera menu cennika."""
        CennikiMenu()

    def delete_selected(self):
        """Usuwa wybraną pozycję z koszyka."""
        selected = self.cart_tree.selection()
        if selected:
            index = self.cart_tree.index(selected[0])
            self.cart.remove_item(index)
            self.update_cart_display()

    def edit_selected(self):
        """Otwiera menu edycji dla wybranej pozycji."""
        selected = self.cart_tree.selection()
        if selected:
            index = int(selected[0])  # iid to str(idx)
            item = self.cart.items[index]
            if item['name'] == "Frezy":
                FrezyMenu(self.root, self.cart, main_app=self, edit_index=index)
            elif item['name'] == "Wiertła":
                WiertlaMenu(self.root, self.cart, main_app=self, edit_index=index)
            elif item['name'] == "Pozostałe":
                PozostaleMenu(self.root, self.cart, main_app=self, edit_index=index)
            elif item['name'] == "Usługi":
                UslugiMenu(self.root, self.cart, main_app=self, edit_index=index)
            else:
                messagebox.showwarning("Błąd", "Nieznany typ pozycji.")
        else:
            messagebox.showwarning("Błąd", "Nie wybrano żadnej pozycji.")

    def update_cart_display(self):
        """Aktualizuje wyświetlanie koszyka."""
        # Czyszczenie tabeli
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        # Wypełnianie tabeli
        for idx, item in enumerate(self.cart.items):
            name = item['params'].get('Typ', item['name'])
            srednica = item['params'].get('Srednica', '')
            fi_chwyt = item['params'].get('fiChwyt', '')
            ilosc_zebow = item['params'].get('Ilosc ostrzy', '')
            ilosc_sztuk = item['quantity']
            ciecie = item['params'].get('ciecie', '-')
            cena_szt = format_price(item['sharpening_price'] + item.get('cutting_price', 0.0))
            wartosc = format_price((item['sharpening_price'] + item.get('cutting_price', 0.0)) * ilosc_sztuk)
            powlekanie = item['params'].get('Powloka', 'BRAK')
            dlugosc = item['params'].get('Długość całkowita', '')
            cena_powlekania_szt = format_price(item['coating_price']) if item['coating_price'] > 0 else "-"
            wartosc_powlekania = format_price(item['coating_price'] * ilosc_sztuk) if item['coating_price'] > 0 else "-"
            uwagi = item['params'].get('Uwagi', '-')
            self.cart_tree.insert("", tk.END, iid=str(idx), values=(
                idx + 1, name, srednica, fi_chwyt, ilosc_zebow, ilosc_sztuk, ciecie,
                cena_szt, wartosc, powlekanie, dlugosc, cena_powlekania_szt, wartosc_powlekania, uwagi))

        # Obliczanie sum
        suma_uslug = sum((item['sharpening_price'] + item.get('cutting_price', 0.0)) * item['quantity'] for item in self.cart.items)
        suma_powlekanie = sum(item['coating_price'] * item['quantity'] for item in self.cart.items if item['coating_price'] > 0)
        suma_total = suma_uslug + suma_powlekanie

        # Aktualizacja etykiet
        self.suma_uslug_label.config(text=f"Suma usług: {format_price(suma_uslug)} PLN")
        self.suma_powlekanie_label.config(text=f"Suma powlekanie: {format_price(suma_powlekanie)} PLN")
        self.suma_total_label.config(text=f"Suma: {format_price(suma_total)} PLN")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToolPricingApp(root)
    root.mainloop()