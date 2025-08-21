import tkinter as tk
from tkinter import ttk, messagebox
from config.cart_io import save_cart_to_file

class RemarksMenu:
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
        self.cart = cart
        self.item_index = item_index
        self.main_app = main_app

        # Tworzenie okna
        self.window = tk.Toplevel(parent)
        self.window.title("Edycja uwag")
        self.window.geometry("400x300")
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
        self.remarks_text = tk.Text(self.main_frame, height=3, width=40, font=("Arial", 10))
        self.remarks_text.pack(pady=5, fill=tk.BOTH, expand=True)
        if current_remarks != '-':
            self.remarks_text.insert(tk.END, current_remarks)
            self.remarks_text.config(state='normal', bg="white")
        else:
            self.remarks_text.config(state='disabled', bg="#d3d3d3")

        # Przycisk zapisu
        tk.Button(
            self.main_frame,
            text="Zapisz",
            command=self.save_remarks,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10)

        # Przycisk anulowania
        tk.Button(
            self.main_frame,
            text="Anuluj",
            command=self.window.destroy,
            font=("Arial", 12),
            bg="#f44336",
            fg="white"
        ).pack(pady=5)

    def toggle_remarks_field(self):
        """Włącza/wyłącza pole tekstowe na podstawie stanu checkboxa."""
        if self.remarks_active_var.get():
            self.remarks_text.config(state='normal', bg="white")
            self.remarks_text.focus_set()
        else:
            self.remarks_text.delete("1.0", tk.END)
            self.remarks_text.config(state='disabled', bg="#d3d3d3")

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