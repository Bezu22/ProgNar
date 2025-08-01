import tkinter as tk
from config.ui_utils import update_button_styles

class BladesMenu:
    """Klasa obsługująca wybór ilości ostrzy (zębów) w interfejsie."""
    def __init__(self, parent, z_var, update_callback, z_options=["1", "2", "3", "4", "5", "6"], default_z="4"):
        """
        Inicjalizuje menu wyboru ilości ostrzy.
        Args:
            parent: Widget nadrzędny (np. Toplevel lub Frame).
            z_var: Tkinter StringVar dla ilości ostrzy.
            update_callback: Funkcja do wywołania po zmianie ilości ostrzy.
            z_options: Lista dostępnych opcji ostrzy (np. ["1", "2", "3"] dla wierteł).
            default_z: Domyślna wartość ilości ostrzy.
        """
        self.parent = parent
        self.z_var = z_var
        self.z_var.set(default_z)
        self.update_callback = update_callback
        self.z_options = z_options

        # Etykieta
        tk.Label(self.parent, text="Wybierz ilość ostrzy:", font=("Arial", 12)).pack(pady=5)

        # Przyciski
        self.z_frame = tk.Frame(self.parent)
        self.z_frame.pack(pady=5)
        self.z_buttons = {}
        for z in self.z_options:
            btn = tk.Button(self.z_frame, text=z, width=6,
                            command=lambda v=z: self.select_z(v))
            btn.pack(side="left", padx=2)
            self.z_buttons[z] = btn
        update_button_styles(self.z_buttons, default_z)

        # Pole tekstowe
        self.z_entry = tk.Entry(self.parent, textvariable=self.z_var, width=10)
        self.z_entry.pack(pady=5)
        self.z_entry.bind("<KeyRelease>", self.on_z_entry_change)

    def select_z(self, z_value):
        """Ustawia wybraną ilość ostrzy i aktualizuje styl przycisku."""
        self.z_var.set(z_value)
        self.z_entry.delete(0, tk.END)
        self.z_entry.insert(0, z_value)
        update_button_styles(self.z_buttons, z_value)
        self.update_callback()

    def on_z_entry_change(self, event=None):
        """Odznacza przyciski ostrzy przy wpisywaniu w pole tekstowe."""
        update_button_styles(self.z_buttons, None)
        self.update_callback()