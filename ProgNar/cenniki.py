import tkinter as tk
from tkinter import messagebox
import json
import os
from config.utils import resource_path

class CennikiMenu:
    JSON_FILES = {
        "Frezy": resource_path("data/cennik_frezy.json"),
        "Wiertła": resource_path("data/cennik_wiertla.json"),
        "Pozostałe": resource_path("data/cennik_pozostale.json"),
        "Usługi": resource_path("data/cennik_uslugi.json"),
        "Powłoki": resource_path("data/cennik_powloki.json")
    }

    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        self.create_main_window()

    def load_json(self, file_path):
        if not os.path.exists(file_path):
            messagebox.showerror("Błąd", f"Plik {file_path} nie istnieje.")
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Błąd", f"Plik {file_path} ma niepoprawny format JSON.")
            return None

    def save_json(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {str(e)}")
            return False

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title("Edytor Cenników")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(pady=20, fill="x")

        label = tk.Label(self.main_frame, text="Wybierz cennik do edycji:", font=("Arial", 14, "bold"), bg="#f0f0f0")
        label.pack(anchor="w", padx=20)

        cennik_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        cennik_frame.pack(fill="x", padx=20)

        self.cennik_buttons = {}
        for cennik in self.JSON_FILES.keys():
            button = tk.Button(cennik_frame, text=cennik, font=("Arial", 12), bg="#4CAF50", fg="white",
                               activebackground="#45a049", command=lambda c=cennik: self.open_editor(c))
            button.pack(pady=5, fill="x")
            self.cennik_buttons[cennik] = button

        exit_button = tk.Button(self.main_frame, text="Zakończ", font=("Arial", 12), bg="#f44336", fg="white",
                                activebackground="#d32f2f", command=self.root.destroy)
        exit_button.pack(pady=30, fill="x", padx=20)

        self.root.mainloop()

    def open_editor(self, cennik):
        file_path = self.JSON_FILES.get(cennik)
        if not file_path:
            messagebox.showerror("Błąd", f"Nieznany cennik: {cennik}")
            return

        data = self.load_json(file_path)
        if data is None:
            return

        self.editor_window = tk.Toplevel()
        self.editor_window.title(f"Edytor - {cennik}")
        self.editor_window.geometry("1000x800")
        self.editor_window.configure(bg="#e0e0e0")

        canvas = tk.Canvas(self.editor_window, bg="#e0e0e0")
        scrollbar = tk.Scrollbar(self.editor_window, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#e0e0e0")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        if cennik == "Frezy":
            self.display_frezy_data(data, file_path)
        elif cennik == "Wiertła":
            self.display_wiertla_data(data, file_path)
        elif cennik == "Pozostałe":
            self.display_pozostale_data(data, file_path)
        else:
            messagebox.showinfo("Info", f"Edycja dla '{cennik}' nie jest jeszcze zaimplementowana.")
            self.editor_window.destroy()

    def display_frezy_data(self, data, file_path):
        row = 0
        for subtype, subtype_data in data.items():
            subtype_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=2, relief="groove")
            subtype_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
            tk.Label(subtype_frame, text=subtype, font=("Arial", 14, "bold"), bg="#ffffff", fg="#333333").pack(anchor="w", padx=10, pady=5)
            row += 1

            ostrzy_data = subtype_data.get("ilosc_ostrzy", {})
            for ilosc_ostrzy, ostrzy_content in ostrzy_data.items():
                ostrzy_frame = tk.Frame(self.scrollable_frame, bg="#f5f5f5", bd=1, relief="sunken")
                ostrzy_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
                tk.Label(ostrzy_frame, text=f"Ilość ostrzy: {ilosc_ostrzy}", font=("Arial", 12, "italic"), bg="#f5f5f5", fg="#555555").pack(anchor="w", padx=10, pady=5)
                row += 1

                items_frame = tk.Frame(self.scrollable_frame, bg="#e0e0e0")
                items_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=20)
                row += 1

                for i, item in enumerate(ostrzy_content.get("cennik", [])):
                    zakres_srednicy = item.get("zakres_srednicy", "Brak danych")
                    item_frame = tk.Frame(items_frame, bg="#e0e0e0")
                    item_frame.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="n")
                    tk.Label(item_frame, text=f"Średnica: {zakres_srednicy}", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(anchor="w")

                    for key, value in item.get("ceny", {}).items():
                        price_frame = tk.Frame(item_frame, bg="#e0e0e0")
                        price_frame.pack(fill="x")
                        tk.Label(price_frame, text=f"{key}:", font=("Arial", 10), bg="#e0e0e0", fg="#333333", width=15, anchor="e").pack(side="left")
                        entry = tk.Entry(price_frame, width=10, font=("Arial", 10))
                        entry.insert(0, f"{value:.2f}")
                        entry.bind("<FocusOut>", lambda event, e=entry: self.format_entry(e, 2))
                        entry.pack(side="left", padx=5)
                        entry._path = (subtype, "ilosc_ostrzy", ilosc_ostrzy, "cennik", i, "ceny", key)

                tk.Frame(self.scrollable_frame, bg="#cccccc", height=1).grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
                row += 1

        self.add_editor_buttons(row, file_path, data)

    def display_wiertla_data(self, data, file_path):
        row = 0
        for subtype, subtype_data in data.items():
            subtype_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=2, relief="groove")
            subtype_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
            tk.Label(subtype_frame, text=subtype, font=("Arial", 14, "bold"), bg="#ffffff", fg="#333333").pack(
                anchor="w", padx=10, pady=5)
            row += 1

            items_frame = tk.Frame(self.scrollable_frame, bg="#e0e0e0")
            items_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=20)
            row += 1

            for i, item in enumerate(subtype_data.get("zakres_srednicy", [])):
                zakres_srednicy = item.get("zakres_srednicy", "Brak danych")
                item_frame = tk.Frame(items_frame, bg="#e0e0e0")
                item_frame.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="n")
                tk.Label(item_frame, text=f"Średnica: {zakres_srednicy}", font=("Arial", 10, "bold"), bg="#e0e0e0",
                         fg="#333333").pack(anchor="w")

                for key, value in item.get("ceny", {}).items():
                    price_frame = tk.Frame(item_frame, bg="#e0e0e0")
                    price_frame.pack(fill="x")
                    tk.Label(price_frame, text=f"{key}:", font=("Arial", 10), bg="#e0e0e0", fg="#333333", width=15,
                             anchor="e").pack(side="left")
                    entry = tk.Entry(price_frame, width=10, font=("Arial", 10))
                    entry.insert(0, f"{value:.2f}")
                    entry.bind("<FocusOut>", lambda event, e=entry: self.format_entry(e, 2))
                    entry.pack(side="left", padx=5)
                    entry._path = (subtype, "zakres_srednicy", i, "ceny", key)

            tk.Frame(self.scrollable_frame, bg="#cccccc", height=1).grid(row=row, column=0, columnspan=4, sticky="ew",
                                                                         padx=10, pady=5)
            row += 1

        self.add_editor_buttons(row, file_path, data)

    def display_pozostale_data(self, data, file_path):
        row = 0
        for subtype, subtype_data in data.items():
            subtype_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=2, relief="groove")
            subtype_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
            tk.Label(subtype_frame, text=subtype, font=("Arial", 14, "bold"), bg="#ffffff", fg="#333333").pack(anchor="w", padx=10, pady=5)
            row += 1

            for ilosc_ostrzy, ostrzy_data in subtype_data.get("ilosc_ostrzy", {}).items():
                ostrzy_frame = tk.Frame(self.scrollable_frame, bg="#f5f5f5", bd=1, relief="sunken")
                ostrzy_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
                tk.Label(ostrzy_frame, text=f"Ilość ostrzy: {ilosc_ostrzy}", font=("Arial", 12, "italic"), bg="#f5f5f5", fg="#555555").pack(anchor="w", padx=10, pady=5)
                row += 1

                items_frame = tk.Frame(self.scrollable_frame, bg="#e0e0e0")
                items_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=20)
                row += 1

                for i, item in enumerate(ostrzy_data.get("cennik", [])):
                    zakres_srednicy = item.get("zakres_srednicy", "Brak danych")
                    item_frame = tk.Frame(items_frame, bg="#e0e0e0")
                    item_frame.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="n")
                    tk.Label(item_frame, text=f"Średnica: {zakres_srednicy}", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(anchor="w")

                    for key, value in item.get("ceny", {}).items():
                        price_frame = tk.Frame(item_frame, bg="#e0e0e0")
                        price_frame.pack(fill="x")
                        tk.Label(price_frame, text=f"{key}:", font=("Arial", 10), bg="#e0e0e0", fg="#333333", width=15, anchor="e").pack(side="left")
                        entry = tk.Entry(price_frame, width=10, font=("Arial", 10))
                        entry.insert(0, f"{value:.2f}")
                        entry.bind("<FocusOut>", lambda event, e=entry: self.format_entry(e, 2))
                        entry.pack(side="left", padx=5)
                        entry._path = (subtype, "ilosc_ostrzy", ilosc_ostrzy, "cennik", i, "ceny", key)

                tk.Frame(self.scrollable_frame, bg="#cccccc", height=1).grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
                row += 1

        self.add_editor_buttons(row, file_path, data)

    def add_editor_buttons(self, row, file_path, data):
        exit_button = tk.Button(self.scrollable_frame, text="Zakończ", font=("Arial", 12), bg="#f44336", fg="white",
                                activebackground="#d32f2f", command=self.editor_window.destroy)
        exit_button.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")

        save_button = tk.Button(self.scrollable_frame, text="Zapisz zmiany", font=("Arial", 12), bg="#2196F3",
                                fg="white", activebackground="#1e88e5", command=lambda: self.save_changes(file_path, data))
        save_button.grid(row=row, column=2, columnspan=2, pady=10, sticky="ew")

    def format_entry(self, entry, decimal_places):
        try:
            value = entry.get().strip()
            if value:
                formatted_value = f"{float(value):.{decimal_places}f}"
                entry.delete(0, tk.END)
                entry.insert(0, formatted_value)
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadzono niepoprawną wartość ceny (musi być liczbą).")
            entry.delete(0, tk.END)
            entry.insert(0, "0.00")

    def save_changes(self, file_path, data):
        def find_entries(widget, entries):
            if isinstance(widget, tk.Entry) and hasattr(widget, '_path'):
                entries.append(widget)
            for child in widget.winfo_children():
                find_entries(child, entries)

        try:
            entries = []
            find_entries(self.scrollable_frame, entries)

            for entry in entries:
                path = entry._path
                current = data
                for key in path[:-1]:
                    if isinstance(current, list):
                        current = current[int(key)]
                    else:
                        current = current[key]
                current[path[-1]] = float(entry.get())

            if self.save_json(file_path, data):
                messagebox.showinfo("Sukces", "Zmiany zostały zapisane.")
                self.editor_window.destroy()
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadzono niepoprawną wartość ceny (musi być liczbą).")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisywania: {str(e)}")

if __name__ == "__main__":
    app = CennikiMenu()