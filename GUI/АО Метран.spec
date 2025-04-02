# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['button.py'],
    pathex=[],
    binaries=[],
    datas=[('favicon.ico', '.'), ('loading.png', '.'), ('main.jpg', '.'), ('photo.jpg', '.'), ('new_logo.jpg', '.'), ('Метран.jpg', '.')],
    hiddenimports=['PySide6', 'PySide6.QtCharts', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'logger', 'config', 'database', 'detail_work', 'error_test', 'COM'],
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
    name='АО Метран',
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
    icon=['favicon.ico'],
)
