
def update_button_styles(buttons, selected_value):
    """Aktualizuje style przycisków na podstawie wybranej wartości."""
    for value, btn in buttons.items():
        is_selected = (value == selected_value)
        btn.config(
            bg="lightgreen" if is_selected else "SystemButtonFace",
            relief="sunken" if is_selected else "raised"
        )
