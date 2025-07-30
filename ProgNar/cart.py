# cart.py - Moduł zarządzający wspólnym koszykiem

class Cart:
    def __init__(self):
        # Inicjalizacja pustego koszyka
        self.items = []

    def add_item(self, name, params, quantity, sharpening_price, cutting_price, coating_price):
        # Dodaje pozycję do koszyka
        self.items.append({
            'name': name,
            'params': params,
            'quantity': quantity,
            'sharpening_price': sharpening_price,
            'cutting_price': cutting_price,
            'coating_price': coating_price
        })

    def remove_item(self, index):
        # Usuwa pozycję z koszyka
        if 0 <= index < len(self.items):
            self.items.pop(index)