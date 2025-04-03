import json
import customtkinter as ctk

# Load and Save Functions
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

def delete_code(code_to_delete):
    codes = load_codes()
    codes = [code for code in codes if code["code"] != code_to_delete]  # Remove the selected code
    save_codes(codes)

def display_codes(scrollable_frame):
    # Clear the existing content
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    codes = load_codes()
    for code_data in codes:
        code_frame = ctk.CTkFrame(scrollable_frame, fg_color="#2b2b2b")  # Dark background for better appearance
        code_frame.pack(pady=5, padx=10, fill="x")

        code_label = ctk.CTkLabel(code_frame, text=f"Code: {code_data['code']}\nDescription: {code_data['description']}", anchor="w", justify="left", text_color=get_text_color())
        code_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

        delete_button = ctk.CTkButton(code_frame, text="Delete", fg_color="red", command=lambda c=code_data['code']: on_delete(c, scrollable_frame))
        delete_button.pack(side="right", padx=10, pady=5)

# Sorting Function
sort_order = {"key": "code", "reverse": False}

def sort_codes(scrollable_frame):
    global sort_order
    codes = load_codes()
    
    sort_order["reverse"] = not sort_order["reverse"]
    sorted_codes = sorted(codes, key=lambda x: x[sort_order["key"]].lower(), reverse=sort_order["reverse"])
    
    save_codes(sorted_codes)
    display_codes(scrollable_frame)

# Create GUI
def get_canvas_color():
    mode = ctk.get_appearance_mode()
    return "#2b2b2b" if mode == "Dark" else "#f0f0f0"  # Light background for light mode

def get_frame_color():
    mode = ctk.get_appearance_mode()
    if mode == "Dark":
        return "#2b2b2b"  # Dark background for dark mode
    else:
        return "#FFC0CB"  # Pink background for light mode

def get_text_color():
    mode = ctk.get_appearance_mode()
    return "white" if mode == "Dark" else "black"  # White text for dark mode, black text for light mode

def create_gui():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("dark-blue")
    
    global submit_button, view_button, mode_button, sort_button, canvas, scrollable_frame, scrollbar
    
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("OPEN VHS")

    input_frame = ctk.CTkFrame(app)
    input_frame.pack(pady=10, padx=10, fill="x")

    code_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter code", width=250)
    code_entry.pack(side="left", padx=5, pady=10)

    desc_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter description", width=250)
    desc_entry.pack(side="left", padx=5, pady=10)

    submit_button = ctk.CTkButton(input_frame, text="Add VHS Code", command=lambda: on_submit(code_entry, desc_entry, scrollable_frame))
    submit_button.pack(side="left", padx=5, pady=10)

    # Dynamic Background Handling for Scrollable Frame
    canvas = ctk.CTkCanvas(app, height=400, width=780, bg=get_canvas_color(), highlightthickness=0)
    canvas.pack(pady=10, padx=10, fill="both", expand=True)

    scrollable_frame = ctk.CTkFrame(canvas, fg_color="transparent")  # Transparent frame to blend with theme
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_configure)

    scrollbar = ctk.CTkScrollbar(app, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Sort Button
    sort_button = ctk.CTkButton(app, text="Sort Codes (Toggle)", command=lambda: sort_codes(scrollable_frame))
    sort_button.pack(pady=5)

    # Toggle Mode Button
    mode_button = ctk.CTkButton(app, text="Toggle Light/Dark Mode", command=toggle_mode)
    mode_button.pack(pady=5)

    display_codes(scrollable_frame)  # Show initial codes
    app.mainloop()

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

def toggle_mode():
    current_mode = ctk.get_appearance_mode().lower()
    new_mode = "light" if current_mode == "dark" else "dark"
    ctk.set_appearance_mode(new_mode)

    # Update canvas background dynamically
    canvas.configure(bg=get_canvas_color())

    # Update frame and other UI elements colors dynamically
    scrollable_frame.configure(fg_color=get_frame_color())
    scrollbar.configure(fg_color=get_frame_color())

    # Update text color dynamically
    for label in scrollable_frame.winfo_children():
        if isinstance(label, ctk.CTkLabel):
            label.configure(text_color=get_text_color())

create_gui()
