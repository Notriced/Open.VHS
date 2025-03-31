import json
import customtkinter as ctk

# Load codes from a JSON file
def load_codes():
    try:
        with open("codes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist yet

# Save codes to the JSON file
def save_codes(codes):
    with open("codes.json", "w") as f:
        json.dump(codes, f, indent=4)

# Function to add a new code entry to the list
def add_code_entry(code, description):
    codes = load_codes()  # Load current codes
    codes.append({"code": code, "description": description})  # Append new code
    save_codes(codes)  # Save the updated list to the file

# Function to display the current codes in the textbox
def display_codes(textbox):
    textbox.delete(1.0, ctk.END)  # Clear the current textbox
    codes = load_codes()  # Load current codes
    for code in codes:
        textbox.insert(ctk.END, f"Code: {code['code']}, Description: {code['description']}\n")  # Add to textbox

# Function to create the GUI
def create_gui():
    app = ctk.CTk()
    app.geometry("1000x1000")  # Extra large window size to fit the huge textbox
    app.title("OPEN VHS")

    # Entry for code
    code_entry = ctk.CTkEntry(app, placeholder_text="Enter code")
    code_entry.pack(pady=10)

    # Entry for description
    desc_entry = ctk.CTkEntry(app, placeholder_text="Enter description")
    desc_entry.pack(pady=10)

    # Initial smaller textbox for showing the codes (this is what appears first)
    textbox = ctk.CTkTextbox(app, height=15, width=40)
    textbox.pack(pady=10)

    # Function to be called when the user submits the form
    def on_submit():
        code = code_entry.get()  # Get code input
        description = desc_entry.get()  # Get description input
        if code and description:  # Check if both fields are filled
            add_code_entry(code, description)  # Add the new code
            display_codes(textbox)  # Display the current codes in the textbox
            code_entry.delete(0, ctk.END)  # Clear the code entry
            desc_entry.delete(0, ctk.END)  # Clear the description entry

    # Submit button to add the code
    submit_button = ctk.CTkButton(app, text="Add Vhs codes", command=on_submit)
    submit_button.pack(pady=10)

    # Placeholder for the giant textbox
    giant_textbox = None

    # Button to view current codes in the giant textbox
    def view_all_codes():
        nonlocal giant_textbox  # Access the placeholder

        # If a giant textbox already exists, remove it
        if giant_textbox is not None:
            giant_textbox.destroy()

        # Create a new huge textbox specifically for viewing all codes
        giant_textbox = ctk.CTkTextbox(app, height=500, width=550)  # Super large size for viewing all codes
        giant_textbox.pack(pady=10, padx=10)  # Add padding around the textbox
        display_codes(giant_textbox)  # Display the current codes in the new giant textbox

    view_button = ctk.CTkButton(app, text="View all vhs codes", command=view_all_codes)
    view_button.pack(pady=10)

    # Start the GUI application
    app.mainloop()

# Run the application
create_gui()