# TTS.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    # Liệt kê tất cả file .py bạn dùng
    ['app.py', 'ui.py', 'tts.py', 'voices.py'],
    pathex=['.'],   # Thư mục hiện tại
    binaries=[],
    datas=[
        # Copy icon, ảnh
        ('icon.ico', '.'),        # Đặt icon.ico vào thư mục gốc trong dist
        ('lytran.jpg', '.'),      # Đặt lytran.jpg vào thư mục gốc
        ('voice_custom_names.json', '.'),  # JSON nếu code bạn cần
        
        # Copy toàn bộ thư mục music (chứa mp3)
        # Nếu muốn copy từng file mp3, bạn thêm thủ công; hoặc copy cả folder:
        ('music', 'music'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Nếu bạn dùng python-vlc và cần dll, bỏ comment & sửa đường dẫn cài VLC cho đúng:
#
# a.binaries += [
#    (r"C:\Program Files\VideoLAN\VLC\libvlc.dll", "."),  
#    (r"C:\Program Files\VideoLAN\VLC\libvlccore.dll", ".")
# ]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LyTranTTS',   # Tên file .exe tạo ra
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,      # True = hiển thị console, False = ẩn
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

# COLLECT sẽ tạo 1 thư mục dist/LyTranTTS/ chứa .exe + data
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LyTranTTS'
)
