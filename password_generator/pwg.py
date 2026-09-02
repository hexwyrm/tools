#!/usr/bin/env python3
# Author: Hexwyrm - 12/22/2025

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import secrets
import string

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexwyrm's PassWord Generator (PWG)")
        self.root.resizable(False, False)

        # --- Frame Setup ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0)

        # --- Checkboxes (default OFF) ---
        self.upper_var = tk.BooleanVar(value=False)
        self.lower_var = tk.BooleanVar(value=False)
        self.num_var = tk.BooleanVar(value=False)
        self.sym_var = tk.BooleanVar(value=False)

        ttk.Label(main_frame, text="Character Options:").grid(row=0, column=0, sticky="w")

        ttk.Checkbutton(main_frame, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(main_frame, text="Lowercase (a-z)", variable=self.lower_var).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(main_frame, text="Numbers (0-9)", variable=self.num_var).grid(row=3, column=0, sticky="w")
        ttk.Checkbutton(main_frame, text="Symbols (!@#$...)", variable=self.sym_var).grid(row=4, column=0, sticky="w")

        # --- Length Selector (default 16) ---
        ttk.Label(main_frame, text="Password Length (1–55):").grid(row=5, column=0, pady=(10, 0), sticky="w")

        self.length_spin = ttk.Spinbox(
            main_frame,
            from_=1,
            to=55,
            width=5,
            justify="center"
        )
        self.length_spin.set(16)
        self.length_spin.grid(row=6, column=0, sticky="w")

        # --- Generate Button ---
        self.generate_button = ttk.Button(main_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=7, column=0, pady=10, sticky="we")

        # --- Output Field (readonly + centered) ---
        ttk.Label(main_frame, text="Generated Password:").grid(row=8, column=0, sticky="w")

        self.output_entry = ttk.Entry(main_frame, width=40, justify="center", state="readonly")
        self.output_entry.grid(row=9, column=0, pady=5, sticky="we")

        # --- Copy Button ---
        self.copy_button = ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=10, column=0, pady=(5, 0), sticky="we")

    def generate_password(self):
        length = int(self.length_spin.get())

        char_pool = ""

        if self.upper_var.get():
            char_pool += string.ascii_uppercase
        if self.lower_var.get():
            char_pool += string.ascii_lowercase
        if self.num_var.get():
            char_pool += string.digits
        if self.sym_var.get():
            char_pool += string.punctuation

        if not char_pool:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        password = "".join(secrets.choice(char_pool) for _ in range(length))

        # Update readonly entry
        self.output_entry.config(state="normal")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, password)
        self.output_entry.config(state="readonly")

    def copy_to_clipboard(self):
        password = self.output_entry.get()
        if not password:
            messagebox.showwarning("Warning", "No password to copy.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    PasswordGeneratorGUI(root)
    root.mainloop()
