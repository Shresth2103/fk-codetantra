import time
import tkinter as tk
import subprocess
import pyperclip
import os
import threading
from pynput import keyboard

class MyOverlayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CodeTantra Bypass Overlay")
        
        # Floating window styling
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.geometry("320x100+50+50")
        self.root.configure(bg="#1e1e1e")
        
        # Header label
        self.title_label = tk.Label(
            self.root,
            text="⚡ CodeTantra Bypass Overlay",
            fg="#f1c40f",
            bg="#1e1e1e",
            font=("Arial", 12, "bold")
        )
        self.title_label.pack(pady=5)
        
        # Status / Instructions label
        self.status_label = tk.Label(
            self.root,
            text="Hotkey: Ctrl+Shift+V to Auto-Type",
            fg="#b0b0b0",
            bg="#1e1e1e",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=2)
        
        # Action Button (manual fallback)
        self.type_btn = tk.Button(
            self.root,
            text="🚀 Auto-Type Clipboard (3s delay)",
            command=self.delayed_auto_type_threaded,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=4
        )
        self.type_btn.pack(pady=5)
        
        # Enable dragging the borderless window
        self.title_label.bind("<B1-Motion>", self.move_window)
        self.root.bind("<B1-Motion>", self.move_window)

        # Start the global background hotkey listener
        self.start_global_listener()

    def execute_auto_type(self):
        clipboard_text = pyperclip.paste()
        if not clipboard_text:
            self.status_label.config(text="❌ Clipboard is empty!", fg="#e74c3c")
            return

        for i in range(3, 0, -1):
            self.status_label.config(text=f"Switch to CodeTantra... {i}s", fg="#f1c40f")
            self.root.update()
            time.sleep(1)
            
        self.status_label.config(text="Typing...", fg="#2ecc71")
        self.root.update()
        
        # Sanitize string for AppleScript
        escaped_text = clipboard_text.replace("\\", "\\\\").replace('"', '\\"')
        applescript = f'tell application "System Events" to keystroke "{escaped_text}"'
        
        os.system(f"osascript -e '{applescript}'")
        self.status_label.config(text="✅ Auto-type complete!", fg="#2ecc71")

    def delayed_auto_type_threaded(self):
        # Run typing in a separate thread so the UI doesn't freeze
        threading.Thread(target=self.execute_auto_type, daemon=True).start()

    def start_global_listener(self):
        def on_activate():
            self.delayed_auto_type_threaded()

        # Global hotkey combination (Ctrl + Shift + V)
        hotkey_combo = '<ctrl>+<shift>+v'
        
        def listener_thread():
            with keyboard.GlobalHotKeys({hotkey_combo: on_activate}) as listener:
                listener.join()

        t = threading.Thread(target=listener_thread, daemon=True)
        t.start()

    def move_window(self, event):
        self.root.geometry(f"+{event.x_root}+{event.y_root}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MyOverlayApp()
    app.run()