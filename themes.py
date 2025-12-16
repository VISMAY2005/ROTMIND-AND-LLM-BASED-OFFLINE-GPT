# themes.py
import tkinter as tk
from tkinter import ttk
import json
import os

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"theme": "dark"}

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

def apply_theme(root, theme="dark"):
    style = ttk.Style(root)
    if theme == "dark":
        root.configure(bg="#0f1720")
        style.configure("TFrame", background="#0f1720")
        style.configure("TLabel", background="#0f1720", foreground="#bdecb6")
        style.configure("TButton", background="#111827", foreground="#bdecb6")
    else:
        root.configure(bg="#f5f7fb")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("TLabel", background="#f5f7fb", foreground="#111827")
        style.configure("TButton", background="#e6e9ef", foreground="#111827")
    # tweak some default fonts
    style.configure("TEntry", padding=4)
    save_config({"theme": theme})
    return theme

def toggle_theme(root, current_theme):
    new_theme = "light" if current_theme == "dark" else "dark"
    apply_theme(root, new_theme)
    return new_theme
