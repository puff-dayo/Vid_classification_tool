# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    ['src2\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('src2', 'src2')],
    hiddenimports=['mpv'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
os.environ["LANG"] = "en_US.UTF-8"
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='VCT',
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
    icon=['src2\\resource\\main_icon.png'],
)
