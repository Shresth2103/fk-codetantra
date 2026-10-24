import os
import subprocess
import time
import tkinter as tk
import pyperclip


class MyOverlayApp:

  def __init__(self):
    self.root = tk.Tk()
    self.root.title("MyOverlay")

    # Floating window styling
    self.root.attributes("-topmost", True)
    self.root.overrideredirect(True)
    self.root.geometry("380x140+50+50")
    self.root.configure(bg="#1e1e1e")

    # Header label
    self.title_label = tk.Label(
        self.root,
        text="⚡ CodeTantra Bypass Overlay",
        fg="#f1c40f",
        bg="#1e1e1e",
        font=("Helvetica", 13, "bold"),
    )
    self.title_label.pack(pady=8)

    # Status indicator
    self.status_label = tk.Label(
        self.root,
        text="Cmd+Shift+C: Capture Screen | Cmd+Shift+V: Auto-Type",
        fg="#a0a0a0",
        bg="#1e1e1e",
        font=("Helvetica", 10),
    )
    self.status_label.pack(pady=4)

    # Key bindings
    self.root.bind("<Command-Shift-C>", lambda e: self.capture_screen())
    self.root.bind("<Command-Shift-V>", lambda e: self.auto_type_clipboard())

    # Window dragging functionality
    self.title_label.bind("<B1-Motion>", self.move_window)

  def capture_screen(self):
    """Triggers macOS native interactive screen capture to clipboard."""
    subprocess.run(["screencapture", "-c", "-s"])
    self.status_label.config(
        text="📸 Screen area captured to clipboard!", fg="#2ecc71"
    )

  def auto_type_clipboard(self):
    """Simulates keystrokes of the current clipboard text via AppleScript."""
    text = pyperclip.paste()
    if not text:
      self.status_label.config(text="⚠️ Clipboard is empty!", fg="#e74c3c")
      return

    self.status_label.config(
        text="⌨️ Typing in 2 seconds... Click into editor!", fg="#3498db"
    )
    self.root.update()
    time.sleep(2)

    # Sanitize string for AppleScript
    escaped_text = text.replace("\\", "\\\\").replace('"', '\\"')
    applescript = f'tell application "System Events" to keystroke "{escaped_text}"'

    os.system(f"osascript -e '{applescript}'")
    self.status_label.config(text="✅ Auto-type complete!", fg="#2ecc71")

  def move_window(self, event):
    self.root.geometry(f"+{event.x_root}+{event.y_root}")

  def run(self):
    self.root.mainloop()


if __name__ == "__main__":
    app = MyOverlayApp()
    app.run()
