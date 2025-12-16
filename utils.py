# utils.py
import json
from tkinter import filedialog, messagebox
from fpdf import FPDF
import os

CONFIG_FILE = "config.json"
HISTORY_DIR = "chat_history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")

def ensure_data_dirs():
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR, exist_ok=True)
    # ensure history file exists
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def save_chat_to_file(chat_widget):
    content = chat_widget.get("1.0", "end").strip()
    if content:
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Chat saved to {file}")
    else:
        messagebox.showwarning("Empty", "No chat to save.")

def save_as_pdf(chat_widget):
    content = chat_widget.get("1.0", "end").strip()
    if not content:
        messagebox.showwarning("Empty", "No chat content to save.")
        return

    file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file:
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 8, txt=line)

    try:
        pdf.output(file)
        messagebox.showinfo("Saved", f"Chat saved as PDF to {file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save PDF: {e}")
