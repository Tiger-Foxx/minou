# -*- mode: python ; coding: utf-8 -*-
import os

# Chemins du projet
project_path = os.path.abspath('.')
assets_path = os.path.join(project_path, 'assets')

block_cipher = None

# Analyse des dépendances
a = Analysis(
    ['main.py'],
    pathex=[project_path],
    binaries=[],
    datas=[
        (os.path.join(assets_path, 'cat'), 'assets/cat'),
        (os.path.join(assets_path, 'dog'), 'assets/dog'),
        (os.path.join(assets_path, 'food'), 'assets/food'),
        (os.path.join(assets_path, 'poop'), 'assets/poop'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtWidgets', 
        'PyQt5.QtGui',
        'PyQt5.QtMultimedia',
        'google.generativeai',
        'psutil'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Modules lourds mais SANS distutils pour éviter l'erreur
        'tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy',
        'IPython', 'jupyter', 'notebook', 'sphinx', 'pytest',
        'setuptools', 'wheel', 'pip',
        
        # Modules PyQt5 non utilisés
        'PyQt5.QtWebEngine', 'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebKit', 'PyQt5.QtWebKitWidgets',
        'PyQt5.QtSql', 'PyQt5.QtTest', 'PyQt5.QtXml',
        'PyQt5.QtOpenGL', 'PyQt5.QtSvg', 'PyQt5.QtBluetooth',
        
        # Autres exclusions
        'sqlite3', 'email', 'html', 'http', 'urllib',
        'xml', 'xmlrpc', 'pydoc', 'doctest'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Minou',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,    
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo.png'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='Minou'
)