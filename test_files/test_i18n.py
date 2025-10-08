#!/usr/bin/env python3
"""
国际化(i18n)功能测试脚本
测试多语言支持的核心功能
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from src.core.i18n import tr, set_language, get_available_languages, get_current_language, get_current_language_name
from src.ui.language_selector import LanguageMenu, LanguageButton


class I18nTestWindow(QMainWindow):
    """国际化测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(f"{tr('app.title')} - {tr('menu.language')} {tr('dialog.confirm')}")
        self.setGeometry(100, 100, 800, 600)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 标题标签
        title_label = QLabel(f"🌍 {tr('app.title')} - {tr('menu.language')}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 当前语言信息
        current_lang = get_current_language()
        current_lang_name = get_current_language_name()
        lang_info = QLabel(f"{tr('settings.language')}: {current_lang_name} ({current_lang})")
        lang_info.setStyleSheet("font-size: 16px; padding: 10px;")
        lang_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lang_info)
        self.lang_info_label = lang_info
        
        # 翻译示例文本区域
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.update_text_area()
        layout.addWidget(self.text_area)
        
        # 语言切换按钮
        button_layout = QVBoxLayout()
        
        available_langs = get_available_languages()
        for locale_code, locale_name in sorted(available_langs.items()):
            btn = QPushButton(f"🌐 {locale_name} ({locale_code})")
            btn.clicked.connect(lambda checked, code=locale_code: self.change_language(code))
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        
        # 创建菜单栏
        self.create_menu()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        menubar.clear()
        
        # 文件菜单
        file_menu = menubar.addMenu(tr("menu.file"))
        file_menu.addAction(tr("menu.file.new"))
        file_menu.addAction(tr("menu.file.open"))
        file_menu.addAction(tr("menu.file.save"))
        file_menu.addSeparator()
        file_menu.addAction(tr("menu.file.exit"))
        
        # 编辑菜单
        edit_menu = menubar.addMenu(tr("menu.edit"))
        edit_menu.addAction(tr("menu.edit.undo"))
        edit_menu.addAction(tr("menu.edit.redo"))
        edit_menu.addSeparator()
        edit_menu.addAction(tr("menu.edit.cut"))
        edit_menu.addAction(tr("menu.edit.copy"))
        edit_menu.addAction(tr("menu.edit.paste"))
        
        # 查看菜单
        view_menu = menubar.addMenu(tr("menu.view"))
        view_menu.addAction(tr("menu.view.zoom_in"))
        view_menu.addAction(tr("menu.view.zoom_out"))
        view_menu.addAction(tr("menu.view.reset_zoom"))
        
        # 语言菜单（使用语言选择器组件）
        language_menu = LanguageMenu(self)
        menubar.addMenu(language_menu)
        language_menu.language_changed.connect(self.on_language_changed)
        
        # 帮助菜单
        help_menu = menubar.addMenu(tr("menu.help"))
        help_menu.addAction(tr("menu.help.about"))
        help_menu.addAction(tr("menu.help.documentation"))
    
    def update_text_area(self):
        """更新文本区域内容"""
        content = f"""
📖 {tr('menu.help.documentation')}

{tr('about.title')}
{tr('about.description')}

{tr('menu.file')}:
  • {tr('menu.file.new')} ({tr('menu.file.new_shortcut')})
  • {tr('menu.file.open')} ({tr('menu.file.open_shortcut')})
  • {tr('menu.file.save')} ({tr('menu.file.save_shortcut')})

{tr('menu.edit')}:
  • {tr('menu.edit.undo')} ({tr('menu.edit.undo_shortcut')})
  • {tr('menu.edit.redo')} ({tr('menu.edit.redo_shortcut')})
  • {tr('menu.edit.cut')} ({tr('menu.edit.cut_shortcut')})
  • {tr('menu.edit.copy')} ({tr('menu.edit.copy_shortcut')})
  • {tr('menu.edit.paste')} ({tr('menu.edit.paste_shortcut')})

{tr('statusbar.ready')} ✅
{tr('message.operation_completed')} ✅
{tr('dialog.confirm')} / {tr('dialog.cancel')}

{tr('common.search')}: {tr('common.find_next')} / {tr('common.find_previous')}

{tr('explorer.title')}:
  • {tr('explorer.new_file')}
  • {tr('explorer.new_folder')}
  • {tr('explorer.rename')}
  • {tr('explorer.delete')}
  • {tr('explorer.refresh')}

{tr('about.copyright')}
"""
        self.text_area.setPlainText(content)
    
    def change_language(self, locale_code):
        """切换语言"""
        print(f"切换语言到: {locale_code}")
        set_language(locale_code)
        self.refresh_ui()
    
    def on_language_changed(self, locale_code):
        """语言切换事件（从菜单触发）"""
        print(f"语言已切换: {locale_code}")
        self.refresh_ui()
    
    def refresh_ui(self):
        """刷新UI"""
        # 更新窗口标题
        self.setWindowTitle(f"{tr('app.title')} - {tr('menu.language')} {tr('dialog.confirm')}")
        
        # 更新语言信息
        current_lang = get_current_language()
        current_lang_name = get_current_language_name()
        self.lang_info_label.setText(
            f"{tr('settings.language')}: {current_lang_name} ({current_lang})"
        )
        
        # 更新文本区域
        self.update_text_area()
        
        # 重新创建菜单栏
        self.create_menu()
        
        print(f"UI已刷新为: {current_lang_name}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("i18n Test")
    
    window = I18nTestWindow()
    window.show()
    
    print("=" * 60)
    print("🌍 国际化(i18n)测试窗口")
    print("=" * 60)
    print(f"当前语言: {get_current_language_name()} ({get_current_language()})")
    print(f"可用语言: {list(get_available_languages().values())}")
    print("=" * 60)
    print("\n测试说明：")
    print("1. 查看窗口中显示的翻译文本")
    print("2. 点击按钮切换不同语言")
    print("3. 使用菜单栏的'语言'菜单切换")
    print("4. 观察所有文本是否正确翻译")
    print("=" * 60)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

