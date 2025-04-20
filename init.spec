# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GUI\\init.py'],
    pathex=[],
    binaries=[],
    datas=[('GUI/new_logo.jpg', 'GUI'), ('GUI/new_logo.sjpg', 'GUI'), ('GUI/loading.png', 'GUI'), ('GUI/Метран.jpg', 'GUI'), ('GUI/photo.jpg', 'GUI'), ('GUI/main.jpg', 'GUI'), ('GUI/menu.ui', 'GUI'), ('GUI/admin.ui', 'GUI'), ('GUI/Work.ui', 'GUI'), ('GUI/Tests.ui', 'GUI'), ('GUI/Packing.ui', 'GUI'), ('GUI/Mark.ui', 'GUI'), ('GUI/Error.ui', 'GUI')],
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
    name='init',
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
    icon=['GUI\\favicon.ico'],
)
