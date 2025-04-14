import sys
import os
import json

def load_voice_list():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # thư mục giải nén tạm thời của PyInstaller
    else:
        base_path = os.path.dirname(__file__)

    file_path = os.path.join(base_path, 'voice_custom_names.json')
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    return data

voice_list = load_voice_list()
