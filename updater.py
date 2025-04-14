import threading
import requests
import subprocess
import os
import sys
import webbrowser
import customtkinter as ctk

CURRENT_VERSION = "1.0.4"
UPDATE_INFO_URL = "https://drive.google.com/uc?export=download&id=1FbvrlPhxV_rvgII81Q6i0K9ipk6ATvbG"

def check_for_updates(app):
    def run_check():
        try:
            resp = requests.get(UPDATE_INFO_URL, timeout=10)
            resp.raise_for_status()
            update_info = resp.json()  # Ví dụ: {"version": "1.1.0", "update_url": "..." }
            new_version = update_info.get("version", "")
            update_url = update_info.get("update_url", "")
            if new_version and update_url and new_version != CURRENT_VERSION:
                app.after(0, lambda: show_update_overlay(app, new_version, update_url))
        except Exception as e:
            print("[Update] Không thể kiểm tra cập nhật:", e)
    threading.Thread(target=run_check).start()

def show_update_overlay(app, new_version, update_url):
    overlay = ctk.CTkFrame(app, fg_color="#FFFFFF")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    message = f"Bạn cần cập nhật phiên bản mới ({new_version}) để sử dụng.\nVui lòng nhấn 'Tải xuống' để cập nhật."
    label = ctk.CTkLabel(overlay, text=message, font=("Arial", 16), text_color="#2C3E50")
    label.pack(expand=True, pady=20)
    download_btn = ctk.CTkButton(overlay, text="Tải xuống", font=("Arial", 16),
                                 fg_color="#18985d", text_color="white",
                                 hover_color="#388E3C",
                                 command=lambda: webbrowser.open(update_url))
    download_btn.pack(pady=10)

def download_and_update(update_url):
    try:
        update_file_path = os.path.join(os.path.dirname(sys.executable), "LyTranTTS-Setup.exe")
        r = requests.get(update_url, stream=True)
        r.raise_for_status()
        with open(update_file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        if os.path.getsize(update_file_path) < 1 * 1024 * 1024:
            print("[Update] File tải về có kích thước quá nhỏ, có thể file bị lỗi.")
            return
        subprocess.Popen([update_file_path])
        os._exit(0)
    except Exception as e:
        print("[Update] Lỗi khi tải/cập nhật:", e)
