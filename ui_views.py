import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime
import os
import vlc
import threading
import webbrowser
from pathlib import Path
from PIL import Image, ImageTk
from ui_helpers import create_flat_button, create_green_button, show_rounded_toast_in_app, open_folder_in_explorer
from ui_components import ScrollableComboBox, AudioPlayerFrame
import requests
from bs4 import BeautifulSoup
import asyncio
from tts_engine import convert_text_to_speech
from voices import voice_list

# Các hằng số cho UI
MAIN_BG = "#FFFFFF"
BOX_BG = "#FFFFFF"
TEXT_COLOR = "#2C3E50"
ACCENT_COLOR = "#18985d"
BORDER_COLOR = "#C8E6C9"
BORDER_WIDTH = 1
CONVERSION_THRESHOLD = 100

AVAILABLE_BGM = [
    {"title": "Everyday Song – Emotional Inspiring Music", "path": os.path.join(os.path.dirname(__file__), "music", "everyday_song.mp3")},
    {"title": "New Beautiful Day – Aleksei Gorobetc",       "path": os.path.join(os.path.dirname(__file__), "music", "NewBeautifulDay.MP3")},
    {"title": "Gửi Anh Xa Nhớ – Bích Phương",               "path": os.path.join(os.path.dirname(__file__), "music", "anh_xa_nho.mp3")},
    {"title": "Dấu Mưa - Trung Quân",                       "path": os.path.join(os.path.dirname(__file__), "music", "DauMua.mp3")},
    {"title": "Đừng Ai Nhắc Về Anh Ấy - Trà My",             "path": os.path.join(os.path.dirname(__file__), "music", "DungAiNhacVeAnhAy.mp3")},
    {"title": "Về Quê - Trần Mạnh Tuấn",                    "path": os.path.join(os.path.dirname(__file__), "music", "VeQue.mp3")},
    {"title": "Tâm Sự Với Người Lạ - Tiên Cookie",          "path": os.path.join(os.path.dirname(__file__), "music", "w0uizohpor.mp3")}
]

# — Các hàm xử lý nội dung post từ URL —
def extract_post_content(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["header", "footer"]):
        tag.decompose()
    article = soup.find("article")
    if article:
        content = article.get_text(separator="\n")
    elif soup.body:
        content = soup.body.get_text(separator="\n")
    else:
        content = soup.get_text(separator="\n")
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return "\n".join(lines)

def get_text_from_url(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return None, str(e)
    content = extract_post_content(resp.text)
    return content, None

# — Các hàm hiển thị và xử lý giao diện pop-up –
def show_url_fetch_preview(app, text_input, ui_text):
    preview_frame = ctk.CTkFrame(app, fg_color=BOX_BG, corner_radius=10,
                                 border_width=BORDER_WIDTH, border_color=BORDER_COLOR)
    preview_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.3)
    header = ctk.CTkLabel(preview_frame, text="Nhập URL để tải nội dung bài post",
                          font=("Arial", 16), text_color=TEXT_COLOR)
    header.pack(pady=10)
    url_entry = ctk.CTkEntry(preview_frame, width=400, font=("Arial", 14))
    url_entry.pack(pady=10)
    fetch_button = create_green_button(preview_frame, text="Tải nội dung", command=lambda: fetch_and_import(url_entry, preview_frame, app, text_input, ui_text))
    fetch_button.pack(pady=10)
    close_button = create_flat_button(preview_frame, text="Đóng", icon="✕",
                                      command=lambda: preview_frame.destroy())
    close_button.pack(pady=5)

def fetch_and_import(url_entry, preview_frame, app, text_input, ui_text):
    url = url_entry.get().strip()
    if not url:
        show_rounded_toast_in_app(app, "URL trống!", "error", 3000)
        return
    def run():
        content, error = get_text_from_url(url)
        def update_text():
            if error:
                show_rounded_toast_in_app(app, f"Lỗi: {error}", "error", 3000)
            else:
                text_input.delete("1.0", "end")
                text_input.insert("1.0", content)
                update_word_char_count(text_input, ui_text)
                show_rounded_toast_in_app(app, "Đã nạp nội dung!", "success", 3000)
            preview_frame.destroy()
        app.after(0, update_text)
    threading.Thread(target=run).start()

def show_history_preview(app, ui_text, history_data, text_input):
    preview_frame = ctk.CTkFrame(app, fg_color=BOX_BG, corner_radius=10,
                                 border_width=BORDER_WIDTH, border_color=BORDER_COLOR)
    preview_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
    header = ctk.CTkLabel(preview_frame, text=ui_text["history_title"],
                          font=("Arial", 18, "bold"), text_color=TEXT_COLOR)
    header.pack(pady=10)
    scrollable = ctk.CTkScrollableFrame(preview_frame, fg_color=BOX_BG)
    scrollable.pack(fill="both", expand=True, padx=10, pady=10)
    if not history_data:
        no_data = ctk.CTkLabel(scrollable, text=ui_text["history_no_data"], text_color=TEXT_COLOR)
        no_data.pack(pady=10)
    else:
        for item in reversed(history_data):
            item_frame = ctk.CTkFrame(scrollable, fg_color="#f1f8e9", corner_radius=8)
            item_frame.pack(fill="x", padx=5, pady=5)
            time_label = ctk.CTkLabel(item_frame, text=item["time"], text_color=TEXT_COLOR, anchor="w")
            time_label.pack(fill="x", padx=10, pady=2)
            lang_voice_label = ctk.CTkLabel(item_frame, text=f"{item['lang']} - {item['voice']}",
                                            text_color=TEXT_COLOR, anchor="w")
            lang_voice_label.pack(fill="x", padx=10, pady=2)
            text_label = ctk.CTkLabel(item_frame, text=item["text"], text_color=TEXT_COLOR,
                                      wraplength=500, anchor="w", justify="left")
            text_label.pack(fill="x", padx=10, pady=2)
            def make_import_command(t):
                return lambda: (import_text_from_history(t, text_input, app, ui_text), preview_frame.destroy())
            use_btn = create_flat_button(item_frame, text="➡", command=make_import_command(item["text"]),
                                         font=("Arial", 12))
            use_btn.pack(side="right", padx=10, pady=5)
    btn_frame = ctk.CTkFrame(preview_frame, fg_color=BOX_BG)
    btn_frame.pack(fill="x", padx=10, pady=10)
    def clear_all_history():
        history_data.clear()
        show_rounded_toast_in_app(app, ui_text["history_clear_all"] + "!", "success", 3000)
        preview_frame.destroy()
    clear_all_btn = create_flat_button(btn_frame, text=ui_text["history_clear_all"],
                                       icon="🗑", command=clear_all_history, font=("Arial", 12))
    clear_all_btn.pack(side="left", padx=5)
    close_btn = create_flat_button(btn_frame, text=ui_text["history_close"], icon="✕",
                                   command=preview_frame.destroy, font=("Arial", 12))
    close_btn.pack(side="right", padx=5)

def show_bg_music_preview(app, ui_text, bg_music_config):
    preview_frame = ctk.CTkFrame(app, fg_color=BOX_BG, corner_radius=10,
                                 border_width=BORDER_WIDTH, border_color=BORDER_COLOR)
    preview_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
    header = ctk.CTkLabel(preview_frame, text=ui_text["bgm_title"],
                          font=("Arial", 18, "bold"), text_color=TEXT_COLOR)
    header.pack(pady=10)
    volume_var = tk.IntVar(value=30)
    volume_label = ctk.CTkLabel(preview_frame, text=ui_text["bgm_volume_label"].format(volume=volume_var.get()),
                                text_color=TEXT_COLOR, font=("Arial", 12))
    volume_label.pack(pady=5)
    def on_volume_change(value):
        val = int(float(value))
        if val > 70:
            val = 70
        volume_var.set(val)
        volume_label.configure(text=ui_text["bgm_volume_label"].format(volume=val))
    volume_slider = ctk.CTkSlider(preview_frame, from_=0, to=70, command=on_volume_change)
    volume_slider.set(volume_var.get())
    volume_slider.pack(fill="x", padx=20, pady=5)
    mode_var = tk.StringVar(value="có_sẵn")
    mode_frame = ctk.CTkFrame(preview_frame, fg_color=BOX_BG)
    mode_frame.pack(pady=5)
    radio_available = ctk.CTkRadioButton(mode_frame, text=ui_text["bgm_mode_available"],
                                         variable=mode_var, value="có_sẵn", command=lambda: switch_mode())
    radio_available.pack(side="left", padx=10)
    radio_custom = ctk.CTkRadioButton(mode_frame, text=ui_text["bgm_mode_custom"],
                                      variable=mode_var, value="tùy_chỉnh", command=lambda: switch_mode())
    radio_custom.pack(side="left", padx=10)
    frame_available = ctk.CTkFrame(preview_frame, fg_color=BOX_BG)
    frame_available.pack(fill="both", expand=True, padx=10, pady=10)
    frame_custom = ctk.CTkFrame(preview_frame, fg_color=BOX_BG)
    frame_custom.pack(fill="both", expand=True, padx=10, pady=10)
    frame_custom.pack_forget()
    preview_player = [None]
    def stop_preview():
        if preview_player[0]:
            preview_player[0].stop()
            preview_player[0].release()
            preview_player[0] = None
    def preview_music(file_path):
        stop_preview()
        if os.path.isfile(file_path):
            import vlc
            inst = vlc.Instance()
            preview_player[0] = inst.media_player_new()
            media = inst.media_new(file_path)
            preview_player[0].set_media(media)
            preview_player[0].audio_set_volume(volume_var.get())
            preview_player[0].play()
    def choose_music(file_path):
        stop_preview()
        bg_music_config["path"] = file_path
        bg_music_config["volume"] = volume_var.get()
        preview_frame.destroy()
        show_rounded_toast_in_app(app, ui_text["toast_bgm_selected"], "success", 3000)
    for bgm in AVAILABLE_BGM:
        row = ctk.CTkFrame(frame_available, fg_color="#f1f8e9", corner_radius=5)
        row.pack(fill="x", pady=5)
        title_label = ctk.CTkLabel(row, text=bgm["title"], anchor="w", text_color=TEXT_COLOR)
        title_label.pack(side="left", padx=10, pady=5, expand=True, fill="x")
        preview_btn = ctk.CTkButton(row, text=ui_text["bgm_preview_button"], width=70,
                                    command=lambda p=bgm["path"]: preview_music(p))
        preview_btn.pack(side="right", padx=5)
        choose_btn = ctk.CTkButton(row, text=ui_text["bgm_choose_button"], width=70,
                                   command=lambda p=bgm["path"]: choose_music(p))
        choose_btn.pack(side="right", padx=5)
    selected_custom_path = [None]
    def browse_file():
        file_path = filedialog.askopenfilename(title=ui_text["bgm_dialog_title"],
                                               filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.aac")])
        if file_path:
            preview_music(file_path)
            selected_custom_path[0] = file_path
            choose_btn_custom.configure(state="normal", command=lambda: choose_music(file_path))
    custom_label = ctk.CTkLabel(frame_custom, text=ui_text["bgm_dialog_title"], text_color=TEXT_COLOR)
    custom_label.pack(pady=10)
    browse_button = ctk.CTkButton(frame_custom, text="Browse...", command=browse_file)
    browse_button.pack()
    choose_btn_custom = ctk.CTkButton(frame_custom, text=ui_text["bgm_choose_button"], state="disabled")
    choose_btn_custom.pack(pady=5)
    def switch_mode():
        if mode_var.get() == "có_sẵn":
            frame_custom.pack_forget()
            frame_available.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            frame_available.pack_forget()
            frame_custom.pack(fill="both", expand=True, padx=10, pady=10)
    close_btn = ctk.CTkButton(preview_frame, text=ui_text["bgm_close_button"],
                              command=lambda: (stop_preview(), preview_frame.destroy()))
    close_btn.pack(pady=5)

def show_about_tab(about_frame, ui_text):
    for widget in about_frame.winfo_children():
        widget.destroy()
    about_frame.configure(fg_color=MAIN_BG)
    container = ctk.CTkFrame(about_frame, fg_color=MAIN_BG, corner_radius=20)
    container.pack(fill="both", expand=True, pady=20, padx=20)
    try:
        from PIL import Image
        from config import LYTRAN_IMAGE
        avatar_raw = Image.open(LYTRAN_IMAGE).convert("RGB")
        avatar_raw = avatar_raw.resize((130, 130), Image.LANCZOS)
        avatar_img = ctk.CTkImage(light_image=avatar_raw, dark_image=avatar_raw, size=(130, 130))
    except:
        avatar_img = None
    if avatar_img:
        avatar_label = ctk.CTkLabel(container, image=avatar_img, text="")
        avatar_label.pack(pady=10)
    desc_label = ctk.CTkLabel(container, text=ui_text["about_app_desc"], font=("Arial", 15),
                              text_color=TEXT_COLOR, wraplength=600, justify="center", fg_color="transparent")
    desc_label.pack(pady=(10,10))
    button_frame = ctk.CTkFrame(container, fg_color="transparent")
    button_frame.pack(pady=10)
    fb_button = ctk.CTkButton(button_frame, text=ui_text["about_facebook_button"], fg_color=ACCENT_COLOR,
                              hover_color="#388E3C", text_color="white", corner_radius=8,
                              font=("Arial", 13),
                              command=lambda: webbrowser.open("https://www.facebook.com/groups/622526090937760/"))
    fb_button.pack(side="left", padx=10)
    coffee_button = ctk.CTkButton(button_frame, text=ui_text["about_coffee_button"], fg_color=ACCENT_COLOR,
                                  hover_color="#388E3C", text_color="white", corner_radius=8,
                                  font=("Arial", 13),
                                  command=lambda: webbrowser.open("https://www.paypal.com/paypalme/lytran98?country.x=VN&locale.x=vi_VN"))
    coffee_button.pack(side="left", padx=10)
    zalo_button = ctk.CTkButton(button_frame, text=ui_text["about_zalo_button"], fg_color=ACCENT_COLOR,
                                hover_color="#388E3C", text_color="white", corner_radius=8,
                                font=("Arial", 13),
                                command=lambda: webbrowser.open("https://zalo.me/+84876437046"))
    zalo_button.pack(side="left", padx=10)

def update_word_char_count(text_input, ui_text):
    content = text_input.get("1.0", "end-1c").strip()
    if content == "" or content == ui_text["placeholder_text"]:
        text_input.master.word_char_count_label.configure(text=ui_text["word_char_count"].format(words=0, chars=0))
    else:
        words = content.split()
        word_count = len(words)
        char_count = len(content)
        text_input.master.word_char_count_label.configure(text=ui_text["word_char_count"].format(words=word_count, chars=char_count))

def update_voices(tts_lang_dropdown, gender_var, voice_dropdown, voice_var, config, ui_text):
    selected_lang = tts_lang_dropdown.get()
    current_gender = gender_var.get()
    if selected_lang in voice_list and current_gender in voice_list[selected_lang]:
        voices = [v["display_name"] for v in voice_list[selected_lang][current_gender]]
        voice_dropdown.configure(values=voices)
        if voices:
            if config.get("last_voice") in voices:
                voice_var.set(config["last_voice"])
            else:
                voice_var.set(voices[0])
        else:
            voice_var.set("")
    else:
        voice_dropdown.configure(values=[])
        voice_var.set("")

def open_file(text_input, ui_text, app):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            current_text = text_input.get("1.0", "end-1c")
            if current_text == ui_text["placeholder_text"]:
                text_input.delete("1.0", "end")
                text_input.configure(text_color="#2C3E50")
            text_input.delete("1.0", "end")
            text_input.insert("1.0", f.read())
        update_word_char_count(text_input, ui_text)
        show_rounded_toast_in_app(app, ui_text["toast_opened_file"], "info", 3000)

def import_text_from_history(text, text_input, app, ui_text):
    current = text_input.get("1.0", "end-1c")
    if current == ui_text["placeholder_text"]:
        text_input.delete("1.0", "end")
    text_input.configure(text_color="#2C3E50")
    text_input.delete("1.0", "end")
    text_input.insert("1.0", text)
    text_input.focus()
    update_word_char_count(text_input, ui_text)
    show_rounded_toast_in_app(app, ui_text["toast_imported_from_history"], "info", 3000)

def on_text_focus_in(event, ui_text):
    text_input = event.widget
    current = text_input.get("1.0", "end-1c")
    if current == ui_text["placeholder_text"]:
        text_input.delete("1.0", "end")
        text_input.configure(text_color="#2C3E50")

def on_text_focus_out(event, ui_text):
    text_input = event.widget
    current = text_input.get("1.0", "end-1c")
    if current.strip() == "":
        text_input.delete("1.0", "end")
        text_input.insert("1.0", ui_text["placeholder_text"])
        text_input.configure(text_color="#aaaaaa")
        update_word_char_count(text_input, ui_text)

def build_ui(app, config, ui_text, voice_list_global):
    # Tạo tab chính
    tabview = ctk.CTkTabview(app, width=900, height=600)
    tabview.pack(fill="both", expand=True)
    tabview.add(ui_text["tab_tts"])
    tabview.add(ui_text["tab_settings"])
    tabview.add(ui_text["tab_about"])
    
    # Tab TTS
    tts_frame = tabview.tab(ui_text["tab_tts"])
    tts_frame.configure(fg_color=MAIN_BG)
    tts_frame.rowconfigure(0, weight=0)
    tts_frame.rowconfigure(1, weight=1)
    tts_frame.rowconfigure(2, weight=0)
    tts_frame.rowconfigure(3, weight=0)
    tts_frame.rowconfigure(4, weight=0)
    tts_frame.rowconfigure(5, weight=0)
    tts_frame.columnconfigure(0, weight=1)
    header_label = ctk.CTkLabel(tts_frame, text=ui_text["label_header"],
                                font=("Arial", 20, "bold"), text_color=TEXT_COLOR)
    header_label.grid(row=0, column=0, pady=(10,10))
    text_frame = ctk.CTkFrame(tts_frame, fg_color=BOX_BG, corner_radius=BORDER_WIDTH,
                              border_width=BORDER_WIDTH, border_color=BORDER_COLOR)
    text_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    text_frame.rowconfigure(0, weight=1)
    text_frame.columnconfigure(0, weight=1)
    text_input = ctk.CTkTextbox(text_frame, corner_radius=BORDER_WIDTH, border_width=BORDER_WIDTH,
                                border_color=BORDER_COLOR, fg_color="#ffffff", text_color="#2C3E50",
                                font=("Arial", 13), wrap="word")
    text_input.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    last_text = config.get("last_text", "")
    if last_text.strip() == "":
        text_input.insert("1.0", ui_text["placeholder_text"])
        text_input.configure(text_color="#aaaaaa")
    else:
        text_input.insert("1.0", last_text)
        text_input.configure(text_color="#2C3E50")
    text_input.bind("<FocusIn>", lambda e: on_text_focus_in(e, ui_text))
    text_input.bind("<FocusOut>", lambda e: on_text_focus_out(e, ui_text))
    text_input.bind("<KeyRelease>", lambda e: update_word_char_count(text_input, ui_text))
    word_char_count_label = ctk.CTkLabel(text_frame, text=ui_text["word_char_count"].format(words=0, chars=0),
                                         font=("Arial", 12), text_color=TEXT_COLOR, anchor="w")
    word_char_count_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0,10))
    text_frame.word_char_count_label = word_char_count_label  # Để cập nhật chữ, từ
    
    # Khung cấu hình (chọn ngôn ngữ, giới tính, giọng)
    config_frame = ctk.CTkFrame(tts_frame, fg_color=MAIN_BG)
    config_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
    config_frame.columnconfigure((0,1,2), weight=1)
    lang_label = ctk.CTkLabel(config_frame, text=ui_text["label_select_language"],
                              text_color=TEXT_COLOR, anchor="w", font=("Arial", 12))
    lang_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tts_lang_var = config.get("tts_voice_language", "Tiếng Việt")
    tts_lang_dropdown = ScrollableComboBox(config_frame, values=list(voice_list.keys()),
                                           width=180, height=30, default_value=tts_lang_var,
                                           command=lambda val: None)
    tts_lang_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    gender_label = ctk.CTkLabel(config_frame, text=ui_text["label_select_gender"],
                                text_color=TEXT_COLOR, anchor="w", font=("Arial", 12))
    gender_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    gender_var = tk.StringVar(value=config.get("last_gender", "Nam"))
    gender_dropdown = ctk.CTkComboBox(config_frame, values=["Nam", "Nữ"], variable=gender_var,
                                      command=lambda _: update_voices(tts_lang_dropdown, gender_var, voice_dropdown, voice_var, config, ui_text))
    gender_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    voice_label = ctk.CTkLabel(config_frame, text=ui_text["label_select_voice"],
                               text_color=TEXT_COLOR, anchor="w", font=("Arial", 12))
    voice_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    voice_var = tk.StringVar(value=config.get("last_voice", ""))
    voice_dropdown = ctk.CTkComboBox(config_frame, variable=voice_var)
    voice_dropdown.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    update_voices(tts_lang_dropdown, gender_var, voice_dropdown, voice_var, config, ui_text)
    
    # Thanh trượt: pitch và tốc độ giọng
    sliders_frame = ctk.CTkFrame(tts_frame, fg_color=MAIN_BG)
    sliders_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
    pitch_frame = ctk.CTkFrame(sliders_frame)
    pitch_frame.pack(side="left", expand=True, fill="both", padx=10)
    pitch_label_slider = ctk.CTkLabel(pitch_frame, text="Cao độ giọng (Bình Thường)", text_color=TEXT_COLOR,
                                      font=("Arial", 12))
    pitch_label_slider.pack(pady=(5,2))
    pitch_var = tk.IntVar(value=0)
    PITCH_LEVELS = ["Rất Thấp", "Thấp", "Bình Thường", "Cao", "Rất Cao"]
    PITCH_VALUES = [-4, -2, 0, 2, 4]
    def on_pitch_slider(value):
        index = int(round(float(value)))
        pitch_label_slider.configure(text=f"Cao độ giọng ({PITCH_LEVELS[index]})")
        pitch_var.set(PITCH_VALUES[index])
    pitch_slider = ctk.CTkSlider(pitch_frame, from_=0, to=4, command=on_pitch_slider, number_of_steps=4)
    pitch_slider.set(2)
    pitch_slider.pack(fill="x", padx=10, pady=2)
    rate_frame = ctk.CTkFrame(sliders_frame)
    rate_frame.pack(side="left", expand=True, fill="both", padx=10)
    rate_label_slider = ctk.CTkLabel(rate_frame, text="Tốc độ giọng (Bình Thường)", text_color=TEXT_COLOR,
                                     font=("Arial", 12))
    rate_label_slider.pack(pady=(5,2))
    rate_var = tk.IntVar(value=0)
    RATE_LEVELS  = ["Rất Chậm", "Chậm", "Bình Thường", "Nhanh", "Rất Nhanh"]
    RATE_VALUES  = [-2, -1, 0, 1, 2]
    def on_rate_slider(value):
        index = int(round(float(value)))
        rate_label_slider.configure(text=f"Tốc độ giọng ({RATE_LEVELS[index]})")
        rate_var.set(RATE_VALUES[index])
    rate_slider = ctk.CTkSlider(rate_frame, from_=0, to=4, command=on_rate_slider, number_of_steps=4)
    rate_slider.set(2)
    rate_slider.pack(fill="x", padx=10, pady=2)
    
    # Các nút chức năng (chuyển đổi, nghe thử, mở file, tải âm thanh, …)
    action_frame = ctk.CTkFrame(tts_frame, fg_color=MAIN_BG)
    action_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
    action_frame.columnconfigure((0,1,2,3,4), weight=1)
    convert_button = create_green_button(action_frame, text=ui_text["button_convert"],
                                         command=lambda: convert_text(app, ui_text, text_input, voice_var, tts_lang_dropdown, gender_var, rate_var, pitch_var, os.path.join(config.get("download_folder", ""), "output", "output.mp3"), audio_player))
    convert_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    preview_button = create_flat_button(action_frame, text=ui_text["button_preview_voice"],
                                        icon="🔊", command=lambda: show_preview_panel(app, ui_text, tts_lang_dropdown, gender_var, voice_dropdown, voice_var, text_input, convert_button, os.path.join(config.get("download_folder", ""), "output", "output.mp3"), audio_player))
    preview_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    open_button = create_flat_button(action_frame, text=ui_text["button_open_text"],
                                     icon="📂", command=lambda: open_file(text_input, ui_text, app))
    open_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    download_button = create_flat_button(action_frame, text=ui_text["button_download_audio"],
                                         icon="⬇", command=lambda: download_audio(app, ui_text, os.path.join(config.get("download_folder", ""), "output", "output.mp3"), config))
    download_button.configure(state="disabled")
    download_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
    url_button = create_flat_button(action_frame, text="Tải nội dung từ URL",
                                    icon="🔗", command=lambda: show_url_fetch_preview(app, text_input, ui_text))
    url_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
    clear_button = create_flat_button(action_frame, text=ui_text["button_clear_text"],
                                      icon="🗑", command=lambda: clear_text(text_input, ui_text, app))
    clear_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    history_button = create_flat_button(action_frame, text=ui_text["button_history"],
                                        icon="🕒", command=lambda: show_history_preview(app, ui_text, config.get("history_data", []), text_input))
    history_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    bg_music_button = create_flat_button(action_frame, text=ui_text["button_add_bgm"],
                                         icon="🎵", command=lambda: show_bg_music_preview(app, ui_text, config.setdefault("bg_music_config", {"path": None, "volume":30})))
    bg_music_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    stop_bg_button = create_flat_button(action_frame, text=ui_text["button_stop_bgm"],
                                        icon="⏹", command=lambda: stop_background_music())
    stop_bg_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
    
    audio_player = AudioPlayerFrame(tts_frame, width=800, height=70)
    audio_player.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
    
    # Tab Settings
    settings_frame = tabview.tab(ui_text["tab_settings"])
    settings_frame.configure(fg_color=MAIN_BG)
    settings_label = ctk.CTkLabel(settings_frame, text=ui_text["tab_settings"],
                                  font=("Arial", 18, "bold"), text_color=TEXT_COLOR)
    settings_label.pack(pady=10)
    download_frame = ctk.CTkFrame(settings_frame, fg_color=BOX_BG, corner_radius=BORDER_WIDTH,
                                  border_width=BORDER_WIDTH, border_color=BORDER_COLOR)
    download_frame.pack(pady=10, padx=20, fill="x")
    dl_label = ctk.CTkLabel(download_frame, text=ui_text["label_parent_folder"],
                            text_color=TEXT_COLOR, font=("Arial", 12))
    dl_label.pack(side="left", padx=10, pady=10)
    parent_folder_var = tk.StringVar(value=str(Path(config.get("download_folder", ""))).rsplit(os.sep,1)[0])
    dl_entry = ctk.CTkEntry(download_frame, textvariable=parent_folder_var, font=("Arial", 12))
    dl_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
    def choose_folder():
        folder = filedialog.askdirectory(title="Chọn thư mục để lưu TTS")
        if folder:
            parent_folder_var.set(folder)
    dl_button = create_flat_button(download_frame, text="Chọn", icon="📁", command=choose_folder)
    dl_button.pack(side="left", padx=5)
    lang_frame = ctk.CTkFrame(settings_frame, fg_color=BOX_BG, corner_radius=BORDER_WIDTH,
                              border_width=BORDER_WIDTH, border_color=BORDER_COLOR)
    lang_frame.pack(pady=10, padx=20, fill="x")
    lang_setting_label = ctk.CTkLabel(lang_frame, text=ui_text["label_default_language"],
                                      text_color=TEXT_COLOR, font=("Arial", 12))
    lang_setting_label.pack(side="left", padx=10, pady=10)
    default_lang_var = tk.StringVar(value=config.get("app_ui_language", "Tiếng Việt"))
    default_lang_combo = ctk.CTkComboBox(lang_frame, values=["Tiếng Việt", "English"],
                                        variable=default_lang_var, font=("Arial", 12))
    default_lang_combo.pack(side="left", padx=10, pady=10)
    def save_settings():
        parent_folder = parent_folder_var.get()
        new_folder = os.path.join(parent_folder, "LyTran-TTS")
        config["download_folder"] = new_folder
        config["app_ui_language"] = default_lang_var.get()
        show_rounded_toast_in_app(app, "Cài đặt đã được lưu và giao diện đã cập nhật!", "success", 3000)
    save_btn = create_green_button(settings_frame, text=ui_text["button_save_settings"], command=save_settings)
    save_btn.pack(pady=20)
    
    # Tab About
    about_frame = tabview.tab(ui_text["tab_about"])
    show_about_tab(about_frame, ui_text)
    
    return {
        "text_input": text_input,
        "tts_lang_dropdown": tts_lang_dropdown,
        "gender_var": gender_var,
        "voice_dropdown": voice_dropdown,
        "voice_var": voice_var,
        "convert_button": convert_button,
        "download_button": download_button,
        "audio_player": audio_player,
        "output_file_path": os.path.join(config.get("download_folder", ""), "output", "output.mp3"),
    }

def convert_text(app, ui_text, text_input, voice_var, tts_lang_dropdown, gender_var, rate_var, pitch_var, output_file_path, audio_player):
    # Đây là hàm chuyển đổi văn bản thành giọng nói
    global conversion_in_progress, last_conversion
    if conversion_in_progress:
        show_rounded_toast_in_app(app, ui_text["toast_converting_wait"], "info", 3000)
        return
    text = text_input.get("1.0", "end").strip()
    selected_voice_name = voice_var.get()
    selected_lang = tts_lang_dropdown.get()
    selected_gender = gender_var.get()
    if text == ui_text["placeholder_text"]:
        text = ""
    current_params = {"text": text, "voice": selected_voice_name, "lang": selected_lang, "gender": selected_gender}
    if last_conversion is not None and current_params == last_conversion:
        show_rounded_toast_in_app(app, "Văn bản này đã được chuyển đổi.", "info", 3000)
        return
    if text and selected_voice_name:
        voice_code = None
        for v in voice_list.get(selected_lang, {}).get(selected_gender, []):
            if v["display_name"] == selected_voice_name:
                voice_code = v["voice_code"]
                break
        if voice_code:
            conversion_in_progress = True
            # Bắt đầu hiệu ứng quay icon chuyển đổi
            start_rotate_icon(audio_player.master.children[list(audio_player.master.children.keys())[0]], ui_text)
            download_button = app.nametowidget(audio_player.master.children[list(audio_player.master.children.keys())[0]].winfo_name())
            download_button.configure(state="disabled")
            def thread_convert_tts():
                convert_text_to_speech(text, voice_code, output_file_path, rate_value=rate_var.get(), pitch_value=pitch_var.get())
                def done():
                    global conversion_in_progress, last_conversion
                    stop_rotate_icon(audio_player.master.children[list(audio_player.master.children.keys())[0]], ui_text)
                    download_button.configure(state="normal")
                    audio_player.load_file(output_file_path, autoplay=True)
                    config_history = app.config_data.get("history_data", [])
                    config_history.append({
                        "time": datetime.now().strftime("%H:%M %d/%m/%Y"),
                        "voice": selected_voice_name,
                        "lang": selected_lang,
                        "text": text
                    })
                    app.config_data["history_data"] = config_history
                    show_rounded_toast_in_app(app, ui_text["toast_conversion_success"], "success", 3000)
                    conversion_in_progress = False
                    last_conversion = current_params
                app.after(0, done)
            threading.Thread(target=thread_convert_tts).start()
            show_rounded_toast_in_app(app, ui_text["toast_converting_wait"], "info", 3000)
        else:
            show_rounded_toast_in_app(app, ui_text["toast_voice_not_found"], "error", 3000)
    else:
        show_rounded_toast_in_app(app, ui_text["toast_please_enter_text_voice"], "info", 3000)

def download_audio(app, ui_text, output_file_path, config):
    download_folder = config.get("download_folder", "")
    os.makedirs(download_folder, exist_ok=True)
    base_name = "LyTranTTS"
    extension = ".mp3"
    file_name = f"{base_name}{extension}"
    full_save_path = os.path.join(download_folder, file_name)
    counter = 0
    while os.path.exists(full_save_path):
        counter += 1
        file_name = f"{base_name}-{counter}{extension}"
        full_save_path = os.path.join(download_folder, file_name)
    try:
        with open(output_file_path, "rb") as src:
            data = src.read()
        with open(full_save_path, "wb") as dst:
            dst.write(data)
        show_rounded_toast_in_app(app, ui_text["toast_file_saved"].format(path=full_save_path),
                                  "success", 4000, open_folder_path=full_save_path)
    except Exception as e:
        show_rounded_toast_in_app(app, ui_text["toast_error_saving"].format(error=str(e)), "error", 3000)

def clear_text(text_input, ui_text, app):
    text_input.delete("1.0", "end")
    update_word_char_count(text_input, ui_text)
    show_rounded_toast_in_app(app, ui_text["toast_text_cleared"], "info", 3000)

def stop_background_music():
    # Placeholder: nếu có cài đặt nhạc nền
    pass
