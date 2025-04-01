import json
import customtkinter as ctk

def load_codes():
    try:
        with open("codes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_codes(codes):
    with open("codes.json", "w") as f:
        json.dump(codes, f, indent=4)

def add_code_entry(code, description):
    codes = load_codes()
    codes.append({"code": code, "description": description})
    save_codes(codes)

def display_codes(textbox):
    textbox.delete(1.0, ctk.END)
    codes = load_codes()
    for code in codes:
        textbox.insert(ctk.END, f"Code: {code['code']}, Description: {code['description']}\n")

def create_gui():
    app = ctk.CTk()
    app.geometry("1000x1000")
    app.title("OPEN VHS")

    code_entry = ctk.CTkEntry(app, placeholder_text="Enter code")
    code_entry.pack(pady=10)

    desc_entry = ctk.CTkEntry(app, placeholder_text="Enter description")
    desc_entry.pack(pady=10)

    textbox = ctk.CTkTextbox(app, height=15, width=40)
    textbox.pack(pady=10)

    def on_submit():
        code = code_entry.get()
        description = desc_entry.get()
        if code and description:
            add_code_entry(code, description)
            display_codes(textbox)
            code_entry.delete(0, ctk.END)
            desc_entry.delete(0, ctk.END)

    submit_button = ctk.CTkButton(app, text="Add Vhs codes", command=on_submit)
    submit_button.pack(pady=10)

    giant_textbox = None

    def view_all_codes():
        nonlocal giant_textbox
        if giant_textbox is not None:
            giant_textbox.destroy()
        giant_textbox = ctk.CTkTextbox(app, height=500, width=550)
        giant_textbox.pack(pady=10, padx=10)
        display_codes(giant_textbox)

    view_button = ctk.CTkButton(app, text="View all vhs codes", command=view_all_codes)
    view_button.pack(pady=10)

    app.mainloop()

create_gui()
