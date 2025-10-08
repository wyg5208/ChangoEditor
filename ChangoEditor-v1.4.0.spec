# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('resources\\themes\\dark.json', 'resources/themes'), ('resources\\themes\\deep_blue.json', 'resources/themes'), ('resources\\themes\\forest.json', 'resources/themes'), ('resources\\themes\\light.json', 'resources/themes'), ('resources\\themes\\light_yellow.json', 'resources/themes'), ('resources\\themes\\monokai.json', 'resources/themes'), ('resources\\themes\\ocean.json', 'resources/themes'), ('resources\\i18n\\locales\\en_US.json', 'resources/i18n/locales'), ('resources\\i18n\\locales\\es_ES.json', 'resources/i18n/locales'), ('resources\\i18n\\locales\\ja_JP.json', 'resources/i18n/locales'), ('resources\\i18n\\locales\\ko_KR.json', 'resources/i18n/locales'), ('resources\\i18n\\locales\\ms_MY.json', 'resources/i18n/locales'), ('resources\\i18n\\locales\\ru_RU.json', 'resources/i18n/locales'), ('resources\\i18n\\locales\\zh_CN.json', 'resources/i18n/locales'), ('resources\\i18n\\locales\\zh_TW.json', 'resources/i18n/locales'), ('resources/icons/chango_editor.svg', 'resources/icons'), ('resources/icons/chango_editor.png', 'resources/icons'), ('resources/icons/chango_editor.ico', 'resources/icons')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.QtPrintSupport', 'pygments', 'pygments.lexers', 'pygments.formatters', 'pygments.lexers.python', 'pygments.lexers.web', 'pygments.lexers.shell', 'pygments.lexers.data', 'chardet', 'watchdog', 'watchdog.observers', 'watchdog.events', 'git', 'gitdb', 'smmap', 'src', 'src.ui', 'src.ui.main_window', 'src.ui.tab_widget', 'src.ui.file_explorer', 'src.ui.search_dialog', 'src.ui.new_file_dialog', 'src.ui.split_view', 'src.ui.language_selector', 'src.core', 'src.core.editor', 'src.core.document', 'src.core.selection', 'src.core.undo_redo', 'src.core.i18n', 'src.utils', 'src.utils.syntax', 'src.utils.themes', 'src.utils.settings', 'src.utils.file_templates', 'src.utils.file_watcher', 'src.utils.git_utils'],
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
    name='ChangoEditor-v1.4.0',
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
