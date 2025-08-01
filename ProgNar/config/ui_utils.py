import tkinter as tk

def update_button_styles(buttons, selected_value):
    """Aktualizuje style przycisków na podstawie wybranej wartości."""
    for value, btn in buttons.items():
        btn.config(bg="lightgreen" if value == selected_value else "SystemButtonFace",
                   relief="sunken" if value == selected_value else "raised")