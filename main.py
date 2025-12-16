import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json, os, threading, time
from datetime import datetime

from llm_client import LLMClient
from memory_engine import MemoryEngine
from utils import save_chat_to_file, save_as_pdf, ensure_data_dirs
from themes import apply_theme, toggle_theme

# Ensure data folders exist
ensure_data_dirs()

# === Splash Screen ===
def show_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("420x200+500+300")
    splash.configure(bg="white")
    label = tk.Label(splash, text="ROT-MIND", font=("Segoe UI", 28, "bold"), fg="#222", bg="white")
    label.place(relx=0.5, rely=0.5, anchor="center")
    splash.update()
    time.sleep(1.0)
    splash.destroy()

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ROT-MIND")
        self.root.geometry("1000x700")
        self.memory = MemoryEngine()           # vector DB + embeddings
        self.llm = LLMClient(model_name="mock")# change model_name or configure for real provider
        self.theme = "dark"
        self.chat_history_file = "chat_history/history.json"
        self.current_chat = []
        self.current_title = "New Chat"
        self.last_prompt = ""

        apply_theme(self.root, self.theme)
        self.build_ui()
        self.load_chat_history()

    def build_ui(self):
        top = ttk.Frame(self.root)
        top.pack(side=tk.TOP, fill=tk.X, pady=8)

        ttk.Label(top, text="Model:").pack(side=tk.LEFT, padx=6)
        self.model_var = tk.StringVar(value="mock")
        ttk.Combobox(top, textvariable=self.model_var, values=["mock", "openai", "mistral"], state="readonly").pack(side=tk.LEFT)
        ttk.Button(top, text="New Chat", command=self.new_chat).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Toggle Theme", command=self.toggle_theme).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Save", command=lambda: save_chat_to_file(self.chat_box)).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="PDF", command=lambda: save_as_pdf(self.chat_box)).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Delete", command=self.delete_chat).pack(side=tk.LEFT, padx=4)

        self.chat_box = ScrolledText(self.root, font=("Consolas", 11), wrap=tk.WORD)
        self.chat_box.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        self.chat_box.config(state=tk.DISABLED)

        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=6)

        self.user_input = ttk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", lambda e: self.send_message())

        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side=tk.LEFT, padx=6)
        ttk.Button(input_frame, text="Regenerate", command=self.regenerate).pack(side=tk.LEFT, padx=4)
        ttk.Button(input_frame, text="Deep Search", command=self.deep_search).pack(side=tk.LEFT, padx=4)

        sidebar_frame = ttk.Frame(self.root)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(sidebar_frame, text="Chats").pack(anchor="nw")
        self.sidebar = tk.Listbox(sidebar_frame, width=28)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=4)
        self.sidebar.bind("<<ListboxSelect>>", self.select_chat)

    def insert_text(self, sender, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{sender}: ", "bold")
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.tag_config("bold", font=("Consolas", 11, "bold"))
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def send_message(self):
        prompt = self.user_input.get().strip()
        if not prompt:
            return
        self.insert_text("You", prompt)
        self.last_prompt = prompt
        self.user_input.delete(0, tk.END)
        # Save to memory as user message context
        self.memory.add_document(prompt, metadata={"role":"user", "ts": datetime.utcnow().isoformat()})
        threading.Thread(target=self.get_response, args=(prompt,), daemon=True).start()

    def get_response(self, prompt):
        # Stream tokens into chat box
        self.insert_text("ROT-MIND", "")
        self.chat_box.config(state=tk.NORMAL)
        full_response = ""
        try:
            for token in self.llm.stream_chat(prompt, memory=self.memory):
                # token may be small strings; insert gradually
                self.chat_box.insert(tk.END, token)
                full_response += token
                self.chat_box.see(tk.END)
                self.root.update()
            # after stream, append newline for neatness
            self.chat_box.insert(tk.END, "\n")
        except Exception as e:
            self.insert_text("ROT-MIND", f"[Error] {e}")
            self.chat_box.config(state=tk.DISABLED)
            return
        self.chat_box.config(state=tk.DISABLED)

        # Save Q/A to current chat and memory
        self.current_chat.append({"user": prompt, "bot": full_response})
        self.memory.add_document(full_response, metadata={"role":"assistant", "ts": datetime.utcnow().isoformat()})
        self.save_to_history()

    def regenerate(self):
        if self.last_prompt:
            self.send_message()

    def deep_search(self):
        if not self.last_prompt:
            messagebox.showinfo("Info", "Ask something first!")
            return
        # Get context from memory and use it as extra prompt
        context = self.memory.search(self.last_prompt, top_k=3)
        deep_prompt = f"Context retrieved:\n{context}\n\nUser: {self.last_prompt}"
        self.insert_text("You (deep)", self.last_prompt)
        threading.Thread(target=self.get_response, args=(deep_prompt,), daemon=True).start()

    def new_chat(self):
        self.current_chat = []
        self.current_title = datetime.now().strftime("Chat %Y-%m-%d %H:%M:%S")
        self.sidebar.insert(tk.END, self.current_title)
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.delete(1.0, tk.END)
        self.chat_box.config(state=tk.DISABLED)

    def toggle_theme(self):
        self.theme = toggle_theme(self.root, self.theme)

    def delete_chat(self):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.delete(1.0, tk.END)
        self.chat_box.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)

    def save_to_history(self):
        if not os.path.exists("chat_history"):
            os.makedirs("chat_history")
        history = {}
        # try to load existing
        if os.path.exists(self.chat_history_file):
            try:
                with open(self.chat_history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = {}
        history[self.current_title] = self.current_chat
        with open(self.chat_history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def load_chat_history(self):
        if not os.path.exists(self.chat_history_file):
            return
        try:
            with open(self.chat_history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for title in data:
                    self.sidebar.insert(tk.END, title)
        except Exception:
            pass

    def select_chat(self, event):
        selection = event.widget.curselection()
        if selection:
            idx = selection[0]
            title = self.sidebar.get(idx)
            with open(self.chat_history_file, "r", encoding="utf-8") as f:
                chats = json.load(f)
                self.chat_box.config(state=tk.NORMAL)
                self.chat_box.delete(1.0, tk.END)
                for pair in chats[title]:
                    self.insert_text("You", pair.get("user", ""))
                    self.insert_text("ROT-MIND", pair.get("bot", ""))
                self.chat_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_splash(root)
    root.deiconify()
    app = ChatApp(root)
    root.mainloop()
