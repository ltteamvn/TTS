import os
import sys
import json
from pathlib import Path

# Đường dẫn mặc định
default_download_parent = str(Path.home() / "Downloads")
default_download_folder = os.path.join(default_download_parent, "LyTran-TTS")

documents_dir = os.path.join(str(Path.home()), "Documents")
DATA_FOLDER = os.path.join(documents_dir, "LyTranTTS")
os.makedirs(DATA_FOLDER, exist_ok=True)

CONFIG_FILE = os.path.join(DATA_FOLDER, "config.json")
OUTPUT_FOLDER = os.path.join(DATA_FOLDER, "output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
OUTPUT_FILE_PATH = os.path.join(OUTPUT_FOLDER, "output.mp3")

if getattr(sys, 'frozen', False):
    resource_base = sys._MEIPASS
    app_path = os.path.dirname(sys.executable)
else:
    resource_base = os.path.dirname(__file__)
    app_path = os.path.dirname(__file__)

ICON_FILE = os.path.join(resource_base, "icon.ico")
LYTRAN_IMAGE = os.path.join(resource_base, "lytran.jpg")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading config:", e)
    return {
        "app_ui_language": "Tiếng Việt",
        "tts_voice_language": "Tiếng Việt",
        "download_folder": default_download_folder,
        "last_text": "",
        "last_gender": "Nam",
        "last_voice": "",
        "history_data": []
    }

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)
