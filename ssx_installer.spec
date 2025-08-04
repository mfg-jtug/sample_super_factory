# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ssx_installer.py'],
    pathex=[],
    binaries=[],
    datas=[('Shape.zip', '.'), ('ssf_curry.json', '.'), ('サンプルスーパーファクトリー.xlsx', '.'), ('Preferences.tps', '.'), ('ssx.png', '.')],
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
    name='ssx_installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
