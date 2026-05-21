# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files

datas = [
    ('Proyecto_AES_MMS.py', '.'),
    ('Proyecto_AES_Internet.py', '.'),
    ('Proyecto_AES_Youtube.py', '.'),
    ('Proyecto_AES_Twitter.py', '.'),
    ('Proyecto_AES_Messenger.py', '.'),
    ('Proyecto_AES_Gmail.py', '.'),
    ('common.py', '.'),
]
binaries = []
hiddenimports = []

for pkg in ('uiautomator2', 'adbutils', 'whichcraft', 'retry', 'requests', 'urllib3',
            'packaging', 'deprecated', 'PIL', 'lxml', 'apkutils2', 'cigam',
            'pyadb', 'pure_python_adb'):
    try:
        tmp = collect_all(pkg)
        datas += tmp[0]; binaries += tmp[1]; hiddenimports += tmp[2]
    except Exception:
        try:
            hiddenimports += collect_submodules(pkg)
            datas += collect_data_files(pkg)
        except Exception:
            pass

a = Analysis(
    ['run_all_AES.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['hooks'],
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
    name='run_all_AES',
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
