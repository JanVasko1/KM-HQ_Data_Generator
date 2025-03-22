# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-KM_HQ_Testing\\Lib\\site-packages\\iconipy\\assets', 'iconipy\\assets'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-KM_HQ_Testing\\Lib\\site-packages\\holidays', 'holidays'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-KM_HQ_Testing\\Lib\\site-packages\\CTkColorPicker', 'CTkColorPicker'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-KM_HQ_Testing\\Lib\\site-packages\\CTkMessagebox', 'CTkMessagebox')],
    hiddenimports=['iconipy', 'CTkColorPicker', 'holidays', 'CTkMessagebox'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pyinstrument'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HQDataGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Libs\\GUI\\Icons\\HQ_Data_Generator.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HQDataGenerator',
)
