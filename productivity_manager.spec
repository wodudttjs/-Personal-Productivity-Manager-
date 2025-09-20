# PyInstaller spec for Personal Productivity Manager (Tkinter GUI)

import os
from PyInstaller.utils.hooks import collect_submodules


block_cipher = None


hiddenimports = [
    # Ensure TkAgg backend is bundled (only backend we need)
    "matplotlib.backends.backend_tkagg",
]


a = Analysis(
    ["productivity_manager/main.py"],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={
        # Limit matplotlib to TkAgg backend to avoid pulling Qt dependencies
        "matplotlib": {"backends": ["TkAgg"]},
    },
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="productivity-manager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI app (no console)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
