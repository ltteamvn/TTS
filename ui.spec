# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui.py', 'voices.py', 'tts.py'],
    pathex=[],
    binaries=[('C:/Program Files/VideoLAN/VLC/libvlc.dll', '.'), ('C:/Program Files/VideoLAN/VLC/libvlccore.dll', '.')],
    datas=[('lytran.jpg', '.'), ('music', 'music'), ('voice_custom_names.json', '.'), ('C:/Program Files/VideoLAN/VLC/plugins', 'plugins'), ('C:/Users/ADMIN/AppData/Local/Programs/Python/Python310/Lib/site-packages/customtkinter/assets', 'customtkinter/assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
