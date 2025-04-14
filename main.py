import customtkinter as ctk
import tkinter as tk
from config import load_config, save_config, ICON_FILE
from updater import check_for_updates
from ui_views import build_ui
import sys

def on_closing(app, config, ui_text, components):
    text_input = components.get("text_input")
    current_text = text_input.get("1.0", "end-1c")
    if current_text == ui_text["placeholder_text"]:
        current_text = ""
    config["last_text"] = current_text
    config["tts_voice_language"] = components.get("tts_lang_dropdown").get()
    save_config(config)
    app.destroy()

def main():
    config = load_config()
    ui_text = {
        "app_title": "Ly Tran TTS (v1.0.3)",
        "label_header": "Công cụ chuyển văn bản thành giọng nói miễn phí",
        "placeholder_text": "Nhập hoặc dán văn bản...",
        "word_char_count": "{words} từ - {chars} ký tự",
        "label_select_language": "Ngôn ngữ TTS:",
        "label_select_gender": "Giới tính:",
        "label_select_voice": "Giọng đọc:",
        "button_convert": "Chuyển đổi",
        "button_preview_voice": "Nghe thử giọng",
        "button_open_text": "Mở file",
        "button_download_audio": "Tải âm thanh",
        "button_clear_text": "Xóa văn bản",
        "button_history": "Lịch sử",
        "button_add_bgm": "Thêm nhạc nền",
        "button_stop_bgm": "Dừng nhạc nền",
        "tab_tts": "TTS",
        "tab_settings": "Cài đặt",
        "tab_about": "Giới thiệu",
        "label_parent_folder": "Chọn thư mục lưu:",
        "label_default_language": "Ngôn ngữ giao diện:",
        "button_save_settings": "Lưu cài đặt",
        "about_app_desc": "Phần mềm này được phát triển bởi Lý Trần và chia sẻ miễn phí.\nTheo dõi để cập nhật nhiều phần mềm hữu ích khác.",
        "about_facebook_button": "Facebook",
        "about_coffee_button": "Mời tác giả 1 ly cafe",
        "about_author_name": "Lý Trần",
        "about_zalo_button": "Zalo: +84876437046",
        "history_title": "Lịch sử chuyển đổi",
        "history_no_data": "Chưa có dữ liệu.",
        "history_clear_all": "Xóa tất cả",
        "history_close": "Đóng",
        "toast_opened_file": "Đã mở file văn bản!",
        "toast_converting_wait": "Đang chuyển đổi, vui lòng chờ...",
        "toast_conversion_success": "Chuyển đổi thành công!",
        "toast_please_enter_text_voice": "Vui lòng nhập văn bản và chọn giọng nói!",
        "toast_voice_not_found": "Không tìm thấy giọng đọc tương ứng!",
        "toast_text_cleared": "Đã xóa văn bản!",
        "toast_imported_from_history": "Đã lấy văn bản từ lịch sử!",
        "toast_voice_selected": "Đã chọn giọng đọc!",
        "toast_no_voice_for_preview": "Chưa chọn giọng để nghe thử!",
        "toast_bgm_selected": "Đã chọn nhạc nền!",
        "toast_file_saved": "Đã lưu file tại:\n{path}",
        "toast_error_saving": "Lỗi khi lưu: {error}",
        "bgm_title": "Chọn nhạc nền",
        "bgm_volume_label": "Âm lượng nhạc nền ({volume}%)",
        "bgm_mode_available": "Nhạc có sẵn",
        "bgm_mode_custom": "Nhạc tùy chỉnh",
        "bgm_close_button": "Đóng",
        "bgm_preview_button": "Nghe thử",
        "bgm_choose_button": "Chọn",
        "bgm_dialog_title": "Chọn nhạc nền tùy chỉnh",
        "button_choose_voice": "Chọn giọng này",
        "button_close": "Đóng"
    }
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("green")
    app = ctk.CTk()
    app.title(ui_text["app_title"])
    app.geometry("900x600")
    app.resizable(True, True)
    try:
        app.iconbitmap(ICON_FILE)
    except Exception as e:
        print("Icon load error:", e)
    components = build_ui(app, config, ui_text, None)
    app.config_data = config
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app, config, ui_text, components))
    app.after(2000, lambda: check_for_updates(app))
    app.mainloop()

if __name__ == "__main__":
    main()
