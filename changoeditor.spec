# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('resources/themes/dark.json', 'resources/themes'), ('resources/themes/light.json', 'resources/themes'), ('resources/icons/chango_editor.svg', 'resources/icons'), ('resources/icons/chango_editor.png', 'resources/icons'), ('resources/icons/chango_editor.ico', 'resources/icons')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.QtPrintSupport', 'pygments', 'pygments.lexers', 'pygments.formatters', 'pygments.lexers.python', 'pygments.lexers.web', 'pygments.lexers.shell', 'pygments.lexers.data', 'chardet', 'watchdog', 'watchdog.observers', 'watchdog.events', 'git', 'gitdb', 'smmap', 'src', 'src.ui', 'src.ui.main_window', 'src.ui.tab_widget', 'src.ui.file_explorer', 'src.ui.search_dialog', 'src.ui.new_file_dialog', 'src.ui.split_view', 'src.core', 'src.core.editor', 'src.core.document', 'src.core.selection', 'src.core.undo_redo', 'src.utils', 'src.utils.syntax', 'src.utils.themes', 'src.utils.settings', 'src.utils.file_templates', 'src.utils.file_watcher', 'src.utils.git_utils'],
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
    name='ChangoEditor',
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
    icon=['resources\\icons\\chango_editor.ico'],
)
