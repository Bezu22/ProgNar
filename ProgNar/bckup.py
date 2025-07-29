# Importowanie bibliotek
import tkinter as tk
from tkinter import messagebox
import json


# Funkcja wczytująca dane z pliku JSON
def load_pricing_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Funkcja określająca przedział ilościowy na podstawie liczby sztuk
def get_quantity_range(quantity, price_ranges):
    max_range = None
    max_end = 0
    for range_key in price_ranges:
        if '-' in range_key:  # Zakres typu "2-4 szt."
            start, end = map(int, range_key.replace(' szt.', '').split('-'))
            if start <= quantity <= end:
                return range_key
            if end > max_end:  # Zapamiętujemy zakres z największym końcem
                max_end = end
                max_range = range_key
        elif range_key.startswith('1 szt.'):  # Pojedyncza sztuka
            if quantity == 1:
                return range_key
            if 1 > max_end:  # "1 szt." jako potencjalny maksymalny zakres
                max_end = 1
                max_range = range_key
    # Jeśli ilość przekracza maksymalny zakres, zwracamy najwyższy zakres
    if quantity > max_end:
        return max_range
    return None


# Funkcja generująca raport do pliku txt
def generate_report(approved_tools):
    total_sum = sum(tool["cena_calkowita"] for tool in approved_tools)
    with open('raport.txt', 'w', encoding='utf-8') as file:
        file.write("=== Raport wyceny narzędzi skrawających ===\n\n")
        for i, tool in enumerate(approved_tools, 1):
            file.write(f"Narzędzie {i}:\n")
            file.write(f"Typ frezu: {tool['typ_frezu']}\n")
            file.write(f"Ilość ostrzy: {tool['ilosc_ostrzy']}\n")
            file.write(f"Zakres średnicy: {tool['zakres_srednicy']} mm\n")
            file.write(f"Ilość sztuk: {tool['ilosc_sztuk']}\n")
            file.write(f"Cena jednostkowa: {tool['cena_jednostkowa']:.2f} PLN\n")
            file.write(f"Cena całkowita: {tool['cena_calkowita']:.2f} PLN\n")
            file.write("\n")
        file.write(f"Suma za wszystkie pozycje: {total_sum:.2f} PLN\n")
        file.write("====================================\n")
    messagebox.showinfo("Sukces", "Raport został wygenerowany i zapisany do pliku 'raport.txt'.")


# Główna klasa aplikacji Tkinter
class ToolPricingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wycena Narzędzi Skrawających")
        self.root.minsize(800, 400)  # Stały rozmiar okna
        self.root.maxsize(800, 1000)
        self.root.configure(bg="#333333")  # Ciemnoszare tło
        self.pricing_data = load_pricing_data('data/cennik_frezy.json')
        self.approved_tools = []  # Lista zatwierdzonych narzędzi
        self.current_tool = {}  # Przechowuje bieżące wybory
        self.show_main_menu()

    def clear_window(self):
        # Usuwanie wszystkich elementów z okna
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#333333")  # Przywrócenie tła po wyczyszczeniu

    def show_cart(self, parent_frame):
        # Ramka na koszyk
        cart_frame = tk.Frame(parent_frame, bg="#444444", bd=2, relief="groove")
        cart_frame.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="nsew")

        tk.Label(cart_frame, text="Koszyk:", font=("Arial", 12, "bold"), fg="white", bg="#444444").grid(row=0, column=0,
                                                                                                        pady=5,
                                                                                                        sticky="w")

        # Wyświetlanie zatwierdzonych narzędzi
        for i, tool in enumerate(self.approved_tools):
            tool_frame = tk.Frame(cart_frame, bg="#444444")
            tool_frame.grid(row=i + 1, column=0, sticky="w", pady=2)

            # Skrócone informacje o narzędziu
            tool_info = f"{tool['typ_frezu']} ({tool['ilosc_ostrzy']}, {tool['zakres_srednicy']} mm, {tool['ilosc_sztuk']} szt.)"
            tk.Label(tool_frame, text=tool_info, wraplength=260, fg="white", bg="#444444").grid(row=0, column=0,
                                                                                                sticky="w")

            # Przycisk usuwania
            tk.Button(tool_frame, text="X", bg="#666666", fg="white",
                      command=lambda idx=i: self.remove_tool(idx)).grid(row=0, column=1, padx=5)

    def remove_tool(self, index):
        # Potwierdzenie usunięcia
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć to narzędzie z koszyka?"):
            self.approved_tools.pop(index)
            messagebox.showinfo("Sukces", "Narzędzie zostało usunięte z koszyka.")
            self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        # Główna ramka na menu, separator i koszyk
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, minsize=500)  # 500px dla menu
        main_frame.grid_columnconfigure(1, minsize=2)  # 2px dla separatora
        main_frame.grid_columnconfigure(2, minsize=300)  # 300px dla koszyka

        # Separator pionowy
        separator = tk.Frame(main_frame, bg="#555555", width=2)
        separator.grid(row=0, column=1, sticky="ns")

        # Lewa strona: Menu
        menu_frame = tk.Frame(main_frame, bg="#333333")
        menu_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")


        tk.Label(menu_frame, text="Wycena Narzędzi Skrawających", font=("Arial", 14, "bold"), fg="white",
                 bg="#333333").grid(row=0, column=0, columnspan=3, pady=10)
        tk.Label(menu_frame, text="Wybierz typ frezu:", font=("Arial", 12), fg="white", bg="#333333").grid(row=1,
                                                                                                           column=0,
                                                                                                           columnspan=3,
                                                                                                           pady=5)

        # Siatka dla typów frezów
        tool_types = list(self.pricing_data.keys())
        for i, tool_type in enumerate(tool_types):
            row = i // 3 + 2
            col = i % 3
            tk.Button(menu_frame, text=tool_type, bg="#555555", fg="white", width=15,
                      command=lambda t=tool_type: self.select_tool_type(t)).grid(row=row, column=col, padx=5, pady=5,
                                                                                 sticky="w")

        # Opcja raportu i wyjścia
        button_row = len(tool_types) // 3 + 3
        if self.approved_tools:
            tk.Button(menu_frame, text="Generuj raport", bg="#555555", fg="white", width=15,
                      command=self.generate_report).grid(row=button_row, column=0, padx=5, pady=5, sticky="w")
        tk.Button(menu_frame, text="Wyjście", bg="#555555", fg="white", width=15,
                  command=self.root.quit).grid(row=button_row, column=1, padx=5, pady=5, sticky="w")

        # Prawa strona: Koszyk
        self.show_cart(main_frame)

    def select_tool_type(self, tool_type):
        self.current_tool["typ_frezu"] = tool_type
        self.clear_window()
        # Główna ramka na menu, separator i koszyk
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, minsize=500)
        main_frame.grid_columnconfigure(1, minsize=2)
        main_frame.grid_columnconfigure(2, minsize=300)

        # Separator pionowy
        separator = tk.Frame(main_frame, bg="#555555", width=2)
        separator.grid(row=0, column=1, sticky="ns")

        # Lewa strona: Menu
        menu_frame = tk.Frame(main_frame, bg="#333333")
        menu_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")


        tk.Label(menu_frame, text="Wycena Narzędzi Skrawających", font=("Arial", 14, "bold"), fg="white",
                 bg="#333333").grid(row=0, column=0, columnspan=3, pady=10)
        tk.Label(menu_frame, text=f"Wybrano: {tool_type}\nWybierz ilość ostrzy:",
                 font=("Arial", 12), fg="white", bg="#333333").grid(row=1, column=0, columnspan=3, pady=5)

        # Siatka dla ilości ostrzy
        blade_counts = list(self.pricing_data[tool_type]["ilosc_ostrzy"].keys())
        for i, blade_count in enumerate(blade_counts):
            row = i // 3 + 2
            col = i % 3
            tk.Button(menu_frame, text=blade_count, bg="#555555", fg="white", width=15,
                      command=lambda b=blade_count: self.select_blade_count(b)).grid(row=row, column=col, padx=5,
                                                                                     pady=5, sticky="w")

        tk.Button(menu_frame, text="Wróć", bg="#555555", fg="white", width=15,
                  command=self.show_main_menu).grid(row=len(blade_counts) // 3 + 3, column=0, padx=5, pady=5,
                                                    sticky="w")

        # Prawa strona: Koszyk
        self.show_cart(main_frame)

    def select_blade_count(self, blade_count):
        self.current_tool["ilosc_ostrzy"] = blade_count
        self.clear_window()
        # Główna ramka na menu, separator i koszyk
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, minsize=500)
        main_frame.grid_columnconfigure(1, minsize=2)
        main_frame.grid_columnconfigure(2, minsize=300)

        # Separator pionowy
        separator = tk.Frame(main_frame, bg="#555555", width=2)
        separator.grid(row=0, column=1, sticky="ns")

        # Lewa strona: Menu
        menu_frame = tk.Frame(main_frame, bg="#333333")
        menu_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")


        tk.Label(menu_frame, text="Wycena Narzędzi Skrawających", font=("Arial", 14, "bold"), fg="white",
                 bg="#333333").grid(row=0, column=0, columnspan=3, pady=10)
        tk.Label(menu_frame, text=f"Wybrano ilość ostrzy: {blade_count}\nWybierz zakres średnicy:",
                 font=("Arial", 12), fg="white", bg="#333333").grid(row=1, column=0, columnspan=3, pady=5)

        # Siatka dla zakresów średnic
        diameter_ranges = self.pricing_data[self.current_tool["typ_frezu"]]["ilosc_ostrzy"][blade_count]["cennik"]
        for i, diameter in enumerate(diameter_ranges):
            row = i // 3 + 2
            col = i % 3
            tk.Button(menu_frame, text=f"{diameter['zakres_srednicy']} mm", bg="#555555", fg="white", width=15,
                      command=lambda d=diameter: self.select_diameter(d)).grid(row=row, column=col, padx=5, pady=5,
                                                                               sticky="w")

        tk.Button(menu_frame, text="Wróć", bg="#555555", fg="white", width=15,
                  command=self.show_main_menu).grid(row=len(diameter_ranges) // 3 + 3, column=0, padx=5, pady=5,
                                                    sticky="w")

        # Prawa strona: Koszyk
        self.show_cart(main_frame)

    def select_diameter(self, diameter):
        self.current_tool["zakres_srednicy"] = diameter['zakres_srednicy']
        self.current_tool["ceny"] = diameter["ceny"]
        self.show_quantity_input()

    def show_quantity_input(self):
        self.clear_window()
        # Główna ramka na menu, separator i koszyk
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, minsize=500)
        main_frame.grid_columnconfigure(1, minsize=2)
        main_frame.grid_columnconfigure(2, minsize=300)

        # Separator pionowy
        separator = tk.Frame(main_frame, bg="#555555", width=2)
        separator.grid(row=0, column=1, sticky="ns")

        # Lewa strona: Pole wprowadzania ilości
        menu_frame = tk.Frame(main_frame, bg="#333333")
        menu_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")


        tk.Label(menu_frame, text="Wycena Narzędzi Skrawających", font=("Arial", 14, "bold"), fg="white",
                 bg="#333333").grid(row=0, column=0, columnspan=3, pady=10)
        tk.Label(menu_frame, text="Podaj ilość sztuk (minimum 1):", font=("Arial", 12), fg="white", bg="#333333").grid(
            row=1, column=0, columnspan=3, pady=5)
        self.quantity_entry = tk.Entry(menu_frame, bg="#666666", fg="white", insertbackground="white")
        self.quantity_entry.grid(row=2, column=0, columnspan=3, pady=5)

        tk.Button(menu_frame, text="Potwierdź", bg="#555555", fg="white", width=15,
                  command=self.process_quantity).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Button(menu_frame, text="Wróć", bg="#555555", fg="white", width=15,
                  command=self.show_main_menu).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Prawa strona: Koszyk
        self.show_cart(main_frame)

    def process_quantity(self):
        try:
            quantity = int(self.quantity_entry.get())
            if quantity < 1:
                messagebox.showerror("Błąd", "Ilość musi być większa lub równa 1.")
                return
            self.current_tool["ilosc_sztuk"] = quantity

            # Określenie ceny jednostkowej
            price_ranges = list(self.current_tool["ceny"].keys())
            quantity_range = get_quantity_range(quantity, price_ranges)
            if quantity_range is None:
                messagebox.showerror("Błąd", "Nieprawidłowa ilość sztuk dla dostępnych zakresów.")
                return

            unit_price = self.current_tool["ceny"][quantity_range]
            total_price = unit_price * quantity
            self.current_tool["cena_jednostkowa"] = unit_price
            self.current_tool["cena_calkowita"] = total_price

            self.show_summary()
        except ValueError:
            messagebox.showerror("Błąd", "Proszę podać liczbę.")

    def show_summary(self):
        self.clear_window()
        # Główna ramka na menu, separator i koszyk
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, minsize=500)
        main_frame.grid_columnconfigure(1, minsize=2)
        main_frame.grid_columnconfigure(2, minsize=300)

        # Separator pionowy
        separator = tk.Frame(main_frame, bg="#555555", width=2)
        separator.grid(row=0, column=1, sticky="ns")

        # Lewa strona: Podsumowanie
        menu_frame = tk.Frame(main_frame, bg="#333333")
        menu_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")


        tk.Label(menu_frame, text="Wycena Narzędzi Skrawających", font=("Arial", 14, "bold"), fg="white",
                 bg="#333333").grid(row=0, column=0, columnspan=3, pady=10)
        tk.Label(menu_frame, text="=== Podsumowanie ===", font=("Arial", 12, "bold"), fg="white", bg="#333333").grid(
            row=1, column=0, columnspan=3, pady=10)
        tk.Label(menu_frame, text=f"Typ frezu: {self.current_tool['typ_frezu']}", fg="white", bg="#333333").grid(row=2,
                                                                                                                 column=0,
                                                                                                                 columnspan=3,
                                                                                                                 sticky="w")
        tk.Label(menu_frame, text=f"Ilość ostrzy: {self.current_tool['ilosc_ostrzy']}", fg="white", bg="#333333").grid(
            row=3, column=0, columnspan=3, sticky="w")
        tk.Label(menu_frame, text=f"Zakres średnicy: {self.current_tool['zakres_srednicy']} mm", fg="white",
                 bg="#333333").grid(row=4, column=0, columnspan=3, sticky="w")
        tk.Label(menu_frame, text=f"Ilość sztuk: {self.current_tool['ilosc_sztuk']}", fg="white", bg="#333333").grid(
            row=5, column=0, columnspan=3, sticky="w")
        tk.Label(menu_frame, text=f"Cena jednostkowa: {self.current_tool['cena_jednostkowa']:.2f} PLN", fg="white",
                 bg="#333333").grid(row=6, column=0, columnspan=3, sticky="w")
        tk.Label(menu_frame, text=f"Cena całkowita: {self.current_tool['cena_calkowita']:.2f} PLN", fg="white",
                 bg="#333333").grid(row=7, column=0, columnspan=3, sticky="w")
        tk.Label(menu_frame, text="==================", fg="white", bg="#333333").grid(row=8, column=0, columnspan=3,
                                                                                       pady=10)

        tk.Button(menu_frame, text="Zatwierdź", bg="#555555", fg="white", width=15,
                  command=self.approve_tool).grid(row=9, column=0, padx=5, pady=5, sticky="w")
        tk.Button(menu_frame, text="Odrzuć", bg="#555555", fg="white", width=15,
                  command=self.show_main_menu).grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Prawa strona: Koszyk
        self.show_cart(main_frame)

    def approve_tool(self):
        # Zapisanie zatwierdzonego narzędzia
        self.approved_tools.append(self.current_tool.copy())
        messagebox.showinfo("Sukces", "Narzędzie zostało zatwierdzone i zapisane.")
        self.show_main_menu()

    def generate_report(self):
        generate_report(self.approved_tools)
        # Pytanie o opróżnienie koszyka
        if messagebox.askyesno("Opróżnienie koszyka", "Czy chcesz opróżnić koszyk?"):
            self.approved_tools.clear()
            messagebox.showinfo("Sukces", "Koszyk został opróżniony.")
        self.show_main_menu()


# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = ToolPricingApp(root)
    root.mainloop()