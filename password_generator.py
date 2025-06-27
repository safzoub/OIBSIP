import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("420x380")
        self.root.resizable(False, False)

        self.length_var = tk.IntVar(value=12)
        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        options_frame = tk.LabelFrame(self.root, text="Options", padx=10, pady=10)
        options_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(options_frame, text="Password Length:").grid(row=0, column=0, sticky="w")
        tk.Spinbox(options_frame, from_=6, to=64, textvariable=self.length_var, width=5).grid(row=0, column=1, sticky="w")

        tk.Checkbutton(options_frame, text="Include Uppercase (A-Z)", variable=self.include_upper).grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(options_frame, text="Include Lowercase (a-z)", variable=self.include_lower).grid(row=2, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(options_frame, text="Include Digits (0-9)", variable=self.include_digits).grid(row=3, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(options_frame, text="Include Symbols (!@#...)", variable=self.include_symbols).grid(row=4, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(options_frame, text="Exclude Ambiguous (O,0,l,I)", variable=self.exclude_ambiguous).grid(row=5, column=0, columnspan=2, sticky="w")

        self.output = tk.Entry(self.root, font=("Courier New", 14), justify="center", state="readonly")
        self.output.pack(padx=10, pady=10, fill="x")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Generate", width=12, command=self.generate_password).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Copy", width=10, command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear", width=10, command=lambda: self.set_output("")).grid(row=0, column=2, padx=5)

    def generate_password(self):
        length = self.length_var.get()
        char_pools = []

        if self.include_upper.get():
            char_pools.append(string.ascii_uppercase)
        if self.include_lower.get():
            char_pools.append(string.ascii_lowercase)
        if self.include_digits.get():
            char_pools.append(string.digits)
        if self.include_symbols.get():
            char_pools.append(string.punctuation)

        if not char_pools:
            messagebox.showwarning("No Options", "Please select at least one character type.")
            return

        all_chars = ''.join(char_pools)
        if self.exclude_ambiguous.get():
            for ch in 'O0Il':
                all_chars = all_chars.replace(ch, '')

        password = [random.choice(pool) for pool in char_pools]
        password += random.choices(all_chars, k=length - len(password))
        random.shuffle(password)

        self.set_output(''.join(password))

    def set_output(self, text):
        self.output.configure(state="normal")
        self.output.delete(0, tk.END)
        self.output.insert(0, text)
        self.output.configure(state="readonly")

    def copy_to_clipboard(self):
        pwd = self.output.get()
        if pwd:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
