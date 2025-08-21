import tkinter as tk
#from config.doc_report import generate_report
from config.utils import resource_path
from ui.main_menu.bottom_mainmenu import BottomSection
from ui.main_menu.cart_display import CartDisplay
from ui.main_menu.left_main_menu import LeftMenu
from ui.main_menu.top_mainmenu import TopMenu
from core.cart_main import CartMain

class ToolPricingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ProgNar – System Regeneracji i Wyceny Narzędzi")
        self.root.geometry("1500x500")
        self.root.iconbitmap(True,resource_path("img/icon.ico"))
        self.cart = CartMain()
        self.client_name = tk.StringVar(value="- -")
        self.cart.load_from_file(self.client_name)
        self.temp_client_data = {}

        # Tworzenie lewego menu
        self.left_menu = LeftMenu(self.root, self.cart,self.client_name, self)

        self.right_frame = tk.Frame(self.root, width=750)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Tworzenie górnej sekcji z etykietą klienta
        self.top_menu = TopMenu(self.right_frame, self.client_name, self)

        # Tworzenie tabeli koszyka
        self.cart_display = CartDisplay(self.right_frame, self.root, self.cart, self)
        self.cart_tree = self.cart_display.get_cart_tree()

        #ODPALAMY BOTTOM SECTION
        self.bottom = BottomSection(
            parent=self.right_frame,
            cart=self.cart,
            cart_tree=self.cart_tree,
            client_name=self.client_name,
            root=self.root,
            main_app = self
        )

    def handle_save(self):
        """Handles the save action"""
        self.cart.update_cart_display(self.cart_tree)  # Directly update the cart display
        self.bottom.update_price_labels()

    def generate_report(self):
        generate_report(self.client_name, self)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToolPricingApp(root)
    root.mainloop()