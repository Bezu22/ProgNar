import json
from datetime import datetime

class CartStateManager:
    def __init__(self, path="data/temp_cart.json"):
        self.path = path
        self.state = self._load()

    def _load(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"client": {}, "items": []}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=4)

    def set_client(self, client_data):
        self.state["client"] = client_data
        self.save()

    def add_item(self, item_data):
        item_data["added_at"] = datetime.now().isoformat()
        self.state["items"].append(item_data)
        self.save()

    def remove_item(self, index):
        if 0 <= index < len(self.state["items"]):
            del self.state["items"][index]
            self.save()

    def clear_cart(self):
        self.state["items"] = []
        self.save()

    def get_total_price(self):
        return sum(
            item.get("sharpening_price", 0)
            + item.get("cutting_price", 0)
            + item.get("coating_price", 0)
            for item in self.state["items"]
        )

    def get_state(self):
        return self.state