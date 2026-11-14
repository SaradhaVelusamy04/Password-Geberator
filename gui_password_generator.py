"""
Task 1 (Easy) – Password Generator (GUI Edition)
Auspify Technologies - Python Developer Internship

Features:
- Sleek modern Tkinter interface
- Slider for length (4 - 64)
- Checkboxes for Uppercase, Lowercase, Numbers, Symbols, Ambiguous Exclusion
- Live visual strength meter (color-coded)
- Copy to clipboard with instant notification
- History log of generated passwords
"""

import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import math


class PasswordGeneratorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Auspify Password Generator - Task 1")
        self.root.geometry("540x620")
        self.root.minsize(500, 580)
        self.root.configure(bg="#0f172a")

        self.setup_styles()
        self.build_ui()
        self.generate()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # General configurations
        self.style.configure(".", background="#0f172a", foreground="#f8fafc")
        self.style.configure("TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#38bdf8")
        self.style.configure("Sub.TLabel", font=("Segoe UI", 9), foreground="#94a3b8")
        self.style.configure("TCheckbutton", background="#0f172a", foreground="#cbd5e1", font=("Segoe UI", 10))
        self.style.map("TCheckbutton", background=[("active", "#0f172a")], foreground=[("active", "#38bdf8")])

    def build_ui(self):
        container = tk.Frame(self.root, bg="#0f172a", padx=24, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(container, text="Auspify Password Generator", style="Header.TLabel")
        header.pack(anchor="w")
        sub = ttk.Label(container, text="Generate cryptographically secure & customizable passwords", style="Sub.TLabel")
        sub.pack(anchor="w", pady=(2, 16))

        # Result display box
        res_frame = tk.Frame(container, bg="#1e293b", bd=1, relief=tk.SOLID, padx=12, pady=10)
        res_frame.pack(fill=tk.X, pady=(0, 12))

        self.pwd_var = tk.StringVar(value="")
        self.pwd_entry = tk.Entry(
            res_frame,
            textvariable=self.pwd_var,
            font=("Consolas", 14, "bold"),
            bg="#1e293b",
            fg="#38bdf8",
            bd=0,
            justify="center"
        )
        self.pwd_entry.pack(fill=tk.X, pady=(2, 8))

        # Action Buttons row (Copy + Refresh)
        btn_row = tk.Frame(res_frame, bg="#1e293b")
        btn_row.pack(fill=tk.X)

        self.copy_btn = tk.Button(
            btn_row,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        self.copy_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 6))

        self.regen_btn = tk.Button(
            btn_row,
            text="Generate New",
            command=self.generate,
            bg="#059669",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        self.regen_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(6, 0))

        # Strength Meter Indicator
        meter_frame = tk.Frame(container, bg="#0f172a")
        meter_frame.pack(fill=tk.X, pady=(4, 14))

        self.strength_label = tk.Label(
            meter_frame,
            text="Strength: Strong",
            bg="#0f172a",
            fg="#22c55e",
            font=("Segoe UI", 10, "bold")
        )
        self.strength_label.pack(anchor="w")

        self.strength_bar = ttk.Progressbar(meter_frame, length=100, mode="determinate")
        self.strength_bar.pack(fill=tk.X, pady=(4, 2))

        # Configuration Frame
        config_frame = tk.LabelFrame(
            container,
            text=" Customization Options ",
            bg="#0f172a",
            fg="#94a3b8",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=10
        )
        config_frame.pack(fill=tk.X, pady=(0, 14))

        # Length Slider
        len_top = tk.Frame(config_frame, bg="#0f172a")
        len_top.pack(fill=tk.X)
        ttk.Label(len_top, text="Password Length:").pack(side=tk.LEFT)
        self.len_val_label = ttk.Label(len_top, text="16", font=("Segoe UI", 10, "bold"))
        self.len_val_label.pack(side=tk.RIGHT)

        self.length_var = tk.IntVar(value=16)
        self.slider = ttk.Scale(
            config_frame,
            from_=6,
            to=48,
            variable=self.length_var,
            command=self.on_slider_change
        )
        self.slider.pack(fill=tk.X, pady=(4, 10))

        # Checkboxes
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambig_var = tk.BooleanVar(value=False)

        cb1 = ttk.Checkbutton(config_frame, text="Include Uppercase Letters (A-Z)", variable=self.upper_var, command=self.generate)
        cb1.pack(anchor="w", pady=2)
        cb2 = ttk.Checkbutton(config_frame, text="Include Lowercase Letters (a-z)", variable=self.lower_var, command=self.generate)
        cb2.pack(anchor="w", pady=2)
        cb3 = ttk.Checkbutton(config_frame, text="Include Numbers (0-9)", variable=self.digits_var, command=self.generate)
        cb3.pack(anchor="w", pady=2)
        cb4 = ttk.Checkbutton(config_frame, text="Include Symbols (!@#$%...)", variable=self.symbols_var, command=self.generate)
        cb4.pack(anchor="w", pady=2)
        cb5 = ttk.Checkbutton(config_frame, text="Exclude Ambiguous (l, 1, I, o, 0, O)", variable=self.exclude_ambig_var, command=self.generate)
        cb5.pack(anchor="w", pady=2)

        # History Box
        hist_frame = tk.LabelFrame(
            container,
            text=" Recent Passwords History ",
            bg="#0f172a",
            fg="#94a3b8",
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=6
        )
        hist_frame.pack(fill=tk.BOTH, expand=True)

        self.hist_list = tk.Listbox(
            hist_frame,
            bg="#1e293b",
            fg="#cbd5e1",
            selectbackground="#2563eb",
            bd=0,
            font=("Consolas", 9)
        )
        self.hist_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.hist_list.bind("<Double-Button-1>", self.copy_from_history)

        scroll = ttk.Scrollbar(hist_frame, orient=tk.VERTICAL, command=self.hist_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.hist_list.config(yscrollcommand=scroll.set)

    def on_slider_change(self, val):
        self.len_val_label.config(text=str(int(float(val))))
        self.generate()

    def generate(self):
        length = self.length_var.get()
        upper = string.ascii_uppercase if self.upper_var.get() else ""
        lower = string.ascii_lowercase if self.lower_var.get() else ""
        digits = string.digits if self.digits_var.get() else ""
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?" if self.symbols_var.get() else ""

        if self.exclude_ambig_var.get():
            ambig = set("il1Lo0O")
            upper = "".join(c for c in upper if c not in ambig)
            lower = "".join(c for c in lower if c not in ambig)
            digits = "".join(c for c in digits if c not in ambig)
            symbols = "".join(c for c in symbols if c not in ambig)

        pool = upper + lower + digits + symbols
        guaranteed = []
        if upper: guaranteed.append(secrets.choice(upper))
        if lower: guaranteed.append(secrets.choice(lower))
        if digits: guaranteed.append(secrets.choice(digits))
        if symbols: guaranteed.append(secrets.choice(symbols))

        if not pool:
            self.pwd_var.set("Please select at least one character type")
            self.strength_label.config(text="Strength: Invalid", fg="#ef4444")
            self.strength_bar['value'] = 0
            return

        if length < len(guaranteed):
            length = len(guaranteed)
            self.length_var.set(length)
            self.len_val_label.config(text=str(length))

        needed = length - len(guaranteed)
        chars = guaranteed + [secrets.choice(pool) for _ in range(needed)]
        secrets.SystemRandom().shuffle(chars)
        password = "".join(chars)

        self.pwd_var.set(password)
        self.update_strength(password, len(pool))
        
        # Add to history
        self.hist_list.insert(0, password)
        if self.hist_list.size() > 25:
            self.hist_list.delete(tk.END)

    def update_strength(self, pwd: str, pool_size: int):
        entropy = len(pwd) * math.log2(pool_size) if pool_size > 0 else 0
        if entropy < 35:
            self.strength_label.config(text="Strength: Weak (Entropy: {:.1f} bits)".format(entropy), fg="#ef4444")
            self.strength_bar['value'] = 25
        elif entropy < 55:
            self.strength_label.config(text="Strength: Moderate (Entropy: {:.1f} bits)".format(entropy), fg="#f59e0b")
            self.strength_bar['value'] = 55
        elif entropy < 75:
            self.strength_label.config(text="Strength: Strong (Entropy: {:.1f} bits)".format(entropy), fg="#10b981")
            self.strength_bar['value'] = 80
        else:
            self.strength_label.config(text="Strength: Very Strong (Entropy: {:.1f} bits)".format(entropy), fg="#38bdf8")
            self.strength_bar['value'] = 100

    def copy_to_clipboard(self):
        pwd = self.pwd_var.get()
        if not pwd or pwd.startswith("Please"):
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        self.copy_btn.config(text="Copied to Clipboard!", bg="#10b981")
        self.root.after(1500, lambda: self.copy_btn.config(text="Copy to Clipboard", bg="#2563eb"))

    def copy_from_history(self, event):
        sel = self.hist_list.curselection()
        if sel:
            pwd = self.hist_list.get(sel[0])
            self.pwd_var.set(pwd)
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Copied", f"Copied to clipboard:\n{pwd}")


def main():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
