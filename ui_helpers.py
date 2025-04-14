import subprocess
import sys
import os
import tkinter as tk
import customtkinter as ctk

def create_flat_button(parent, text, icon="", bg_color="#ffffff", hover_color="#f1f8e9",
                       corner_radius=6, font=("Arial", 14), command=None, text_color="#2C3E50"):
    return ctk.CTkButton(master=parent, text=f"{icon} {text}", command=command,
                         corner_radius=corner_radius, fg_color=bg_color, hover_color=hover_color,
                         text_color=text_color, font=font)

def create_green_button(parent, text, command=None, corner_radius=6, font=("Arial", 14)):
    return ctk.CTkButton(master=parent, text=text, command=command,
                         corner_radius=corner_radius, fg_color="#18985d", text_color="white",
                         hover_color="#388E3C", font=font)

def open_folder_in_explorer(file_path):
    abs_path = os.path.abspath(file_path)
    if sys.platform.startswith("win"):
        subprocess.Popen(f'explorer /select,"{abs_path}"')
    else:
        # Với macOS hoặc Linux
        subprocess.Popen(["xdg-open", os.path.dirname(abs_path)])

def show_rounded_toast_in_app(parent, message, icon_type="info", duration=4000, open_folder_path=None):
    toast_width = 320
    toast_height = 60
    toast_frame = ctk.CTkFrame(master=parent, corner_radius=10, fg_color="#F1F8E9",
                               width=toast_width, height=toast_height)
    toast_frame.place(relx=1.0, x=-20, y=20, anchor="ne")
    if icon_type == "error":
        icon_text = "❌"
        icon_color = "#f44336"
    elif icon_type == "success":
        icon_text = "✔️"
        icon_color = "#18985d"
    else:
        icon_text = "ℹ"
        icon_color = "#4CAF50"
    top_row = ctk.CTkFrame(toast_frame, fg_color="transparent")
    top_row.pack(fill="x", expand=True, padx=10, pady=5)
    icon_label = ctk.CTkLabel(top_row, text=icon_text, text_color=icon_color,
                              fg_color="transparent", width=30, font=("Arial", 16))
    icon_label.pack(side="left")
    msg_label = ctk.CTkLabel(top_row, text=message, fg_color="transparent",
                             text_color="#2C3E50", wraplength=toast_width-80, font=("Arial", 13))
    msg_label.pack(side="left", fill="x", expand=True)
    if open_folder_path:
        open_btn = ctk.CTkButton(top_row, text="Mở thư mục", width=80, fg_color="#c8e6c9",
                                 text_color="#2C3E50", corner_radius=5, font=("Arial", 12),
                                 command=lambda: open_folder_in_explorer(open_folder_path))
        open_btn.pack(side="right", padx=5)
    def close_toast():
        toast_frame.destroy()
    close_btn = ctk.CTkButton(top_row, text="✕", width=30, fg_color="#c8e6c9",
                              text_color="#2C3E50", corner_radius=5, command=close_toast,
                              font=("Arial", 12))
    close_btn.pack(side="right", padx=5)
    progress = ctk.CTkProgressBar(toast_frame, corner_radius=0, height=5)
    progress.pack(fill="x", side="bottom")
    progress.set(1.0)
    steps = 100
    interval = duration // steps
    def update_progress(i=0):
        if not toast_frame.winfo_exists():
            return
        ratio = 1.0 - (i / steps)
        progress.set(ratio)
        if i < steps:
            toast_frame.after(interval, lambda: update_progress(i+1))
        else:
            if toast_frame.winfo_exists():
                toast_frame.destroy()
    update_progress()
