
"""app.py - Tkinter GUI for the Steganography Tool"""
import os
import sys

# Always add this file's directory to path so steganography.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import steganography

BG       = "#1e1e2e"
PANEL_BG = "#2a2a3e"
FG       = "#cdd6f4"
ACCENT_G = "#a6e3a1"
ACCENT_B = "#89b4fa"
BTN_FG   = "#1e1e2e"
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_T   = ("Segoe UI", 13, "bold")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Steganography Tool - Hide Text in Images, ( Made  By - Md Shahbaz ) ")
        self.minsize(700, 500)
        self.configure(bg=BG)
        self.current_image = None
        self.image_path = None
        self._tk_preview = None
        self._center_window(780, 580)
        self._build_ui()

    def _center_window(self, w, h):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Title
        title_frame = tk.Frame(self, bg=BG)
        title_frame.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(title_frame, text="Steganography Tool",
                 font=FONT_T, bg=BG, fg=ACCENT_G).pack(side="left")
        tk.Label(title_frame, text="  |  Hide secret text inside images",
                 font=FONT, bg=BG, fg=FG).pack(side="left")

        # Two-panel layout
        content = tk.Frame(self, bg=BG)
        content.pack(fill="both", expand=True, padx=16, pady=8)
        self._build_left_panel(content)
        self._build_right_panel(content)

    def _build_left_panel(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG)
        frame.pack(side="left", fill="y", padx=(0, 8), ipadx=10, ipady=10)

        tk.Label(frame, text="Image", font=FONT_B,
                 bg=PANEL_BG, fg=FG).pack(pady=(8, 4))

        tk.Button(frame, text="Open Image", font=FONT_B,
                  bg=ACCENT_B, fg=BTN_FG, relief="flat", cursor="hand2",
                  command=self.on_open_image).pack(pady=(0, 10), ipadx=8, ipady=4)

        self.canvas = tk.Canvas(frame, width=280, height=240,
                                bg="#13131f", highlightthickness=1,
                                highlightbackground="#44475a")
        self.canvas.pack(padx=8)
        self.canvas.create_text(140, 120, text="No image loaded",
                                fill="#6c7086", font=FONT)

        self.status_var = tk.StringVar(value="")
        tk.Label(frame, textvariable=self.status_var,
                 font=("Segoe UI", 9), bg=PANEL_BG, fg="#6c7086",
                 wraplength=280, justify="center").pack(pady=(6, 4))

    def _build_right_panel(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG)
        frame.pack(side="left", fill="both", expand=True, ipadx=10, ipady=10)

        tk.Label(frame, text="Secret Message", font=FONT_B,
                 bg=PANEL_BG, fg=FG).pack(anchor="w", padx=8, pady=(8, 2))

        self.msg_input = tk.Text(frame, height=6, font=FONT,
                                 bg="#13131f", fg=FG, insertbackground=FG,
                                 relief="flat", bd=4, wrap="word")
        self.msg_input.pack(fill="x", padx=8)

        btn_row = tk.Frame(frame, bg=PANEL_BG)
        btn_row.pack(fill="x", padx=8, pady=10)

        tk.Button(btn_row, text="  Encode  ", font=FONT_B,
                  bg=ACCENT_G, fg=BTN_FG, relief="flat", cursor="hand2",
                  command=self.on_encode).pack(side="left", ipadx=8, ipady=6, padx=(0, 8))

        tk.Button(btn_row, text="  Decode  ", font=FONT_B,
                  bg=ACCENT_B, fg=BTN_FG, relief="flat", cursor="hand2",
                  command=self.on_decode).pack(side="left", ipadx=8, ipady=6)

        tk.Label(frame, text="Decoded Message", font=FONT_B,
                 bg=PANEL_BG, fg=FG).pack(anchor="w", padx=8, pady=(4, 2))

        self.output = scrolledtext.ScrolledText(
            frame, height=7, font=FONT,
            bg="#13131f", fg=ACCENT_G, insertbackground=FG,
            relief="flat", bd=4, wrap="word", state="disabled")
        self.output.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _update_preview(self, img):
        preview = img.copy()
        preview.thumbnail((280, 240))
        self._tk_preview = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(140, 120, anchor="center", image=self._tk_preview)

    def _set_output(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.config(state="disabled")

    def on_open_image(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"),
                       ("All files", "*.*")]
        )
        if not path:
            return
        try:
            img = Image.open(path)
            img.verify()
            img = Image.open(path)
            self.current_image = img
            self.image_path = path
            self._update_preview(img)
            fname = os.path.basename(path)
            w, h = img.size
            self.status_var.set(f"{fname}\n{w} x {h} px")
        except Exception as e:
            messagebox.showerror("Invalid File",
                                 "Not a supported image format (PNG, JPG, BMP).")

    def on_encode(self):
        if self.current_image is None:
            messagebox.showerror("No Image", "Please load an image first.")
            return
        message = self.msg_input.get("1.0", "end-1c")
        if not message or not message.strip():
            messagebox.showerror("Empty Message",
                                 "Please enter a non-empty message to encode.")
            return
        try:
            stego = steganography.encode(self.current_image, message)
        except ValueError as e:
            messagebox.showerror("Encoding Error", str(e))
            return
        save_path = filedialog.asksaveasfilename(
            title="Save stego image",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )
        if not save_path:
            return
        stego.save(save_path, "PNG")
        messagebox.showinfo("Success", f"Message encoded and saved!\n{save_path}")

    def on_decode(self):
        if self.current_image is None:
            messagebox.showerror("No Image", "Please load an image first.")
            return
        result = steganography.decode(self.current_image)
        if not result:
            messagebox.showinfo("No Hidden Message",
                                "No hidden message was found in this image.")
            self._set_output("")
        else:
            self._set_output(result)


if __name__ == "__main__":
    app = App()
    app.mainloop()
