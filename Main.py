import logging
import json
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import random
import os

# Constants
CONFIG_PATH = os.path.join(os.path.sep, "path", "to", "config")
STORE_ITEMS_FILE = os.path.join(CONFIG_PATH, "store_items.json")
CODES_FILE = os.path.join(os.getcwd(), "codes.json")
PLUGIN_FOLDER = os.path.join(CONFIG_PATH, "plugins")
SETTINGS_FILE = os.path.join(CONFIG_PATH, "settings.json")
VERSION = "1.0.0"

# Set up logging
logging.basicConfig(level=logging.INFO)

# === Helper Functions ===
def get_canvas_color(mode):
    return "#2b2b2b" if mode == "Dark" else "#f0f0f0"

def get_frame_color(mode):
    return "#2b2b2b" if mode == "Dark" else "#FFC0CB"

def get_text_color(mode):
    return "white" if mode == "Dark" else "black"

def load_settings():
    """Load user settings from a JSON file."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            logging.error("Failed to load settings.")
            return {}
    return {}

def save_settings(settings):
    """Save user settings to a JSON file."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        logging.error(f"Error saving settings: {e}")

# === Plugin: Store Manager ===
class StoreManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛒 Store Price & Discount Manager")
        self.geometry("1000x600")
        self.minsize(900, 500)
        ctk.set_default_color_theme("blue")
        self.items = {}
        self.build_ui()
        self.load_items()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=get_frame_color(ctk.get_appearance_mode()),
                        foreground=get_text_color(ctk.get_appearance_mode()),
                        fieldbackground=get_frame_color(ctk.get_appearance_mode()),
                        bordercolor=get_frame_color(ctk.get_appearance_mode()),
                        borderwidth=0)
        style.map("Treeview", background=[("selected", "#6a6a6a")])

        topbar = ctk.CTkFrame(self, fg_color=get_frame_color(ctk.get_appearance_mode()))
        topbar.pack(fill="x", padx=10, pady=10)

        self.mode_switch = ctk.CTkSwitch(
            topbar, text="Dark Mode", command=self.toggle_mode,
            onvalue="Dark", offvalue="Light"
        )
        self.mode_switch.select() if ctk.get_appearance_mode() == "Dark" else self.mode_switch.deselect()
        self.mode_switch.pack(side="right", padx=10)

        title_label = ctk.CTkLabel(topbar, text="🛒 Store Price & Discount Manager",
                                   font=ctk.CTkFont(size=20, weight="bold"), text_color=get_text_color(ctk.get_appearance_mode()))
        title_label.pack(side="left", padx=10)

        input_frame = ctk.CTkFrame(self, fg_color=get_frame_color(ctk.get_appearance_mode()))
        input_frame.pack(fill="x", padx=20, pady=10)

        self.name_entry = ctk.CTkEntry(input_frame, placeholder_text="Item Name")
        self.name_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.price_entry = ctk.CTkEntry(input_frame, placeholder_text="Base Price")
        self.price_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.discount_entry = ctk.CTkEntry(input_frame, placeholder_text="Discount (optional)")
        self.discount_entry.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.percent_var = ctk.BooleanVar(value=True)
        self.percent_check = ctk.CTkCheckBox(input_frame, text="Percent Discount", variable=self.percent_var)
        self.percent_check.grid(row=0, column=3, padx=10, pady=10)

        self.add_button = ctk.CTkButton(input_frame, text="➕ Add Item", command=self.add_item)
        self.add_button.grid(row=0, column=4, padx=10, pady=10)
        input_frame.columnconfigure((0, 1, 2, 4), weight=1)

        table_frame = ctk.CTkFrame(self, fg_color=get_frame_color(ctk.get_appearance_mode()))
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Item Name", "Base Price", "Discount", "Final Price"), show="headings", style="Treeview")
        self.tree.heading("Item Name", text="Item Name")
        self.tree.heading("Base Price", text="Base Price")
        self.tree.heading("Discount", text="Discount")
        self.tree.heading("Final Price", text="Final Price")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_item(self):
        name = self.name_entry.get().strip()
        price_text = self.price_entry.get().strip()
        discount_text = self.discount_entry.get().strip()

        if not name:
            self.show_message("⚠️ Enter an item name.")
            return

        if not price_text.replace('.', '', 1).isdigit():
            self.show_message("⚠️ Enter a valid price.")
            return

        if discount_text and not discount_text.replace('.', '', 1).isdigit():
            self.show_message("⚠️ Enter a valid discount.")
            return

        price = float(price_text)
        discount = float(discount_text) if discount_text else 0
        is_percent = self.percent_var.get()

        self.items[name] = {
            "price": price,
            "discount": discount,
            "is_percent": is_percent
        }
        self.save_items()
        self.update_table()
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.discount_entry.delete(0, "end")

        logging.info(f"Added item: {name}, Price: {price}, Discount: {discount}, Percent: {is_percent}")

    def calculate_final_price(self, price, discount, is_percent):
        return round(price * (1 - discount / 100), 2) if is_percent else round(price - discount, 2)

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for name, data in self.items.items():
            price = data["price"]
            discount = data["discount"]
            is_percent = data["is_percent"]
            final = self.calculate_final_price(price, discount, is_percent)
            discount_str = f"{discount}%" if is_percent else f"${discount}"
            self.tree.insert("", "end", values=(name, f"${price:.2f}", discount_str, f"${final:.2f}"))

    def save_items(self):
        try:
            with open(STORE_ITEMS_FILE, "w") as f:
                json.dump(self.items, f, indent=4)
        except IOError as e:
            self.show_message(f"Error saving items: {e}")

    def load_items(self):
        if os.path.exists(STORE_ITEMS_FILE):
            try:
                with open(STORE_ITEMS_FILE, "r") as f:
                    self.items = json.load(f)
                self.update_table()
            except (IOError, json.JSONDecodeError) as e:
                self.show_message(f"Error loading items: {e}")

    def show_message(self, msg):
        messagebox.showinfo("Info", msg)

    def toggle_mode(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.update_ui_colors()
        logging.info(f"Mode toggled to: {new_mode}")

    def update_ui_colors(self):
        mode = ctk.get_appearance_mode()
        self.configure(fg_color=get_frame_color(mode))
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=get_frame_color(mode))

def open_store_manager():
    store_app = StoreManagerApp()
    store_app.mainloop()
    logging.info("Store Manager plugin opened.")

# === VHS App Core ===
def load_codes():
    try:
        with open(CODES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading codes: {e}")
        return []

def save_codes(codes):
    try:
        with open(CODES_FILE, "w") as f:
            json.dump(codes, f, indent=4)
    except json.JSONDecodeError as e:
        print(f"Error saving codes: {e}")

def add_code_entry(code, description):
    codes = load_codes()
    codes.append({"code": code, "description": description})
    save_codes(codes)

def delete_code(code_to_delete):
    codes = load_codes()
    codes = [code for code in codes if code["code"] != code_to_delete]
    save_codes(codes)

def display_codes(scrollable_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    codes = load_codes()
    for code_data in codes:
        code_frame = ctk.CTkFrame(scrollable_frame, fg_color=get_frame_color(ctk.get_appearance_mode()))
        code_frame.pack(pady=5, padx=10, fill="x")
        code_label = ctk.CTkLabel(code_frame, text=f"Code: {code_data['code']}\nDescription: {code_data['description']}",
                                  anchor="w", justify="left", text_color=get_text_color(ctk.get_appearance_mode()))
        code_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        delete_button = ctk.CTkButton(code_frame, text="Delete", fg_color="red",
                                      command=lambda c=code_data['code']: on_delete(c, scrollable_frame))
        delete_button.pack(side="right", padx=10, pady=5)

def sort_codes(scrollable_frame):
    codes = load_codes()
    sorted_codes = sorted(codes, key=lambda x: x["code"].lower())
    save_codes(sorted_codes)
    display_codes(scrollable_frame)

def on_submit(code_entry, desc_entry, scrollable_frame):
    code = code_entry.get().strip()
    description = desc_entry.get().strip()
    if code and description:
        add_code_entry(code, description)
        display_codes(scrollable_frame)
        code_entry.delete(0, ctk.END)
        desc_entry.delete(0, ctk.END)

def on_delete(code, scrollable_frame):
    delete_code(code)
    display_codes(scrollable_frame)

def create_gui():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("dark-blue")

    global submit_button, sort_button, mode_button, canvas, scrollable_frame, scrollbar, app

    app = ctk.CTk()
    app.geometry("800x600")
    app.title("OPEN VHS — Moonlight Edition")

    menubar = tk.Menu(app)
    plugin_menu = tk.Menu(menubar, tearoff=0)
    plugin_menu.add_command(label="Open Store Manager", command=open_store_manager)
    menubar.add_cascade(label="Plugins", menu=plugin_menu)
    app.configure(menu=menubar)

    input_frame = ctk.CTkFrame(app, fg_color=get_frame_color(ctk.get_appearance_mode()))
    input_frame.pack(pady=10, padx=10, fill="x")

    code_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter code", width=250)
    code_entry.pack(side="left", padx=5, pady=10)

    desc_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter description", width=250)
    desc_entry.pack(side="left", padx=5, pady=10)

    submit_button = ctk.CTkButton(input_frame, text="Add VHS Code",
                                  command=lambda: on_submit(code_entry, desc_entry, scrollable_frame))
    submit_button.pack(side="left", padx=5, pady=10)

    scrollable_frame = ctk.CTkScrollableFrame(app, fg_color="transparent", height=400, width=780)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    sort_button = ctk.CTkButton(app, text="Sort Codes", command=lambda: sort_codes(scrollable_frame))
    sort_button.pack(pady=5)

    mode_button = ctk.CTkButton(app, text="Toggle Light/Dark Mode",
                                command=lambda: ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark"))
    mode_button.pack(pady=5)

    display_codes(scrollable_frame)
    app.mainloop()

def splash_screen():
    splash = ctk.CTk()
    splash.geometry("400x250")
    splash.overrideredirect(True)
    splash.title("Welcome")

    canvas_splash = tk.Canvas(splash, bg="#0e0e1f", highlightthickness=0)
    canvas_splash.pack(fill="both", expand=True)

    stars = []
    for _ in range(80):
        x, y = random.randint(0, 400), random.randint(0, 250)
        size = random.randint(1, 3)
        stars.append(canvas_splash.create_oval(x, y, x + size, y + size, fill="white", outline=""))

    canvas_splash.create_text(200, 125, text="🌙 Open.VHS\nMoonlight Edition",
                              fill="white", font=("Courier", 18, "bold"), justify="center")

    def animate():
        for star in stars:
            coords = canvas_splash.coords(star)
            if coords:
                if coords[1] > 250:
                    canvas_splash.move(star, 0, -250)
                else:
                    canvas_splash.move(star, 0, 1)
        splash.after(50, animate)

    animate()
    splash.after(2500, lambda: (splash.destroy(), create_gui()))
    splash.mainloop()

# Run the splash screen to start the app
splash_screen()
