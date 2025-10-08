"""
语言选择器UI组件
提供语言切换菜单和对话框
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QMenu, QDialog, QVBoxLayout, QHBoxLayout, 
    QRadioButton, QButtonGroup, QPushButton, QLabel,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QActionGroup, QIcon

from src.core.i18n import get_i18n_manager, tr

logger = logging.getLogger(__name__)


class LanguageMenu(QMenu):
    """
    语言选择菜单
    可以集成到主窗口的菜单栏中
    """
    
    # 语言切换信号
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        初始化语言菜单
        
        Args:
            parent: 父窗口
        """
        super().__init__(tr("menu.language"), parent)
        self.parent_window = parent
        self.i18n = get_i18n_manager()
        
        # 动作组（用于单选）
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)
        
        # 初始化菜单
        self.init_menu()
        
        # 监听语言切换事件
        self.i18n.language_changed.connect(self.on_language_changed_external)
    
    def init_menu(self):
        """初始化语言菜单项"""
        # 清空现有菜单
        self.clear()
        
        # 获取可用语言
        available_langs = self.i18n.get_available_locales()
        current_locale = self.i18n.get_current_locale()
        
        # 创建语言选项
        for locale_code, locale_name in sorted(available_langs.items()):
            action = QAction(locale_name, self)
            action.setCheckable(True)
            action.setData(locale_code)
            
            # 标记当前语言
            if locale_code == current_locale:
                action.setChecked(True)
            
            # 连接事件
            action.triggered.connect(self.on_language_action_triggered)
            
            # 添加到菜单和动作组
            self.addAction(action)
            self.action_group.addAction(action)
        
        logger.debug(f"Language menu initialized with {len(available_langs)} languages")
    
    def on_language_action_triggered(self):
        """语言菜单项被点击"""
        print("🔍 LanguageMenu: 语言菜单被点击")  # 调试
        
        action = self.sender()
        if not action:
            print("❌ LanguageMenu: 无法获取sender")
            return
        
        locale_code = action.data()
        old_locale = self.i18n.get_current_locale()
        
        print(f"🔍 LanguageMenu: 当前语言={old_locale}, 目标语言={locale_code}")
        
        if locale_code == old_locale:
            print(f"⚠️ LanguageMenu: 语言已经是 {locale_code}")
            return
        
        # 切换语言
        print(f"🔄 LanguageMenu: 正在切换语言 {old_locale} → {locale_code}")
        self.i18n.set_locale(locale_code)
        
        # 发出信号
        print(f"📡 LanguageMenu: 发出language_changed信号")
        self.language_changed.emit(locale_code)
        
        # 刷新主窗口UI
        if self.parent_window and hasattr(self.parent_window, 'refresh_ui'):
            print(f"✅ LanguageMenu: 调用主窗口refresh_ui()")
            self.parent_window.refresh_ui()
        else:
            print(f"❌ LanguageMenu: 主窗口没有refresh_ui方法")
    
    def on_language_changed_external(self, locale: str):
        """
        外部语言切换事件（来自其他组件）
        
        Args:
            locale: 新语言代码
        """
        # 更新菜单标题
        self.setTitle(tr("menu.language"))
        
        # 更新选中状态
        for action in self.actions():
            action.setChecked(action.data() == locale)
        
        logger.debug(f"Language menu updated for locale: {locale}")
    
    def refresh_ui(self):
        """刷新UI文本"""
        self.setTitle(tr("menu.language"))
        
        # 更新所有语言选项的名称
        available_langs = self.i18n.get_available_locales()
        for action in self.actions():
            locale_code = action.data()
            locale_name = available_langs.get(locale_code, locale_code)
            action.setText(locale_name)


class LanguageDialog(QDialog):
    """
    语言选择对话框
    提供更友好的语言选择界面
    """
    
    # 语言切换信号
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        初始化语言对话框
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.i18n = get_i18n_manager()
        self.selected_locale = self.i18n.get_current_locale()
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(tr("menu.language"))
        self.setModal(True)
        self.setMinimumWidth(400)
        
        # 主布局
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel(tr("settings.language"))
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 说明文字
        info_label = QLabel(tr("message.language_changed"))
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # 语言选项组
        self.button_group = QButtonGroup(self)
        available_langs = self.i18n.get_available_locales()
        current_locale = self.i18n.get_current_locale()
        
        for locale_code, locale_name in sorted(available_langs.items()):
            radio = QRadioButton(locale_name)
            radio.setProperty("locale_code", locale_code)
            
            if locale_code == current_locale:
                radio.setChecked(True)
            
            self.button_group.addButton(radio)
            layout.addWidget(radio)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 取消按钮
        cancel_btn = QPushButton(tr("dialog.cancel"))
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        # 确定按钮
        ok_btn = QPushButton(tr("dialog.ok"))
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.on_ok_clicked)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def on_ok_clicked(self):
        """确定按钮被点击"""
        # 获取选中的语言
        checked_button = self.button_group.checkedButton()
        if not checked_button:
            self.reject()
            return
        
        selected_locale = checked_button.property("locale_code")
        old_locale = self.i18n.get_current_locale()
        
        if selected_locale == old_locale:
            self.accept()
            return
        
        # 切换语言
        logger.info(f"Switching language from {old_locale} to {selected_locale}")
        self.i18n.set_locale(selected_locale)
        
        # 发出信号
        self.language_changed.emit(selected_locale)
        
        # 显示提示
        QMessageBox.information(
            self,
            tr("dialog.success"),
            tr("message.language_changed", language=self.i18n.get_current_locale_name())
        )
        
        self.accept()


class LanguageButton(QPushButton):
    """
    语言切换按钮
    可以放置在工具栏或状态栏
    """
    
    # 语言切换信号
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        初始化语言按钮
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.i18n = get_i18n_manager()
        
        # 设置按钮文本
        self.update_text()
        
        # 连接点击事件
        self.clicked.connect(self.show_language_menu)
        
        # 监听语言切换事件
        self.i18n.language_changed.connect(self.on_language_changed)
    
    def update_text(self):
        """更新按钮文本"""
        current_locale = self.i18n.get_current_locale()
        locale_name = self.i18n.get_current_locale_name()
        
        # 显示语言代码和名称
        self.setText(f"🌐 {locale_name}")
        self.setToolTip(tr("menu.language") + f": {locale_name}")
    
    def show_language_menu(self):
        """显示语言选择菜单"""
        print("🔍 LanguageButton: 按钮被点击，显示菜单")  # 调试
        
        menu = QMenu(self)
        available_langs = self.i18n.get_available_locales()
        current_locale = self.i18n.get_current_locale()
        
        print(f"🔍 LanguageButton: 当前语言={current_locale}, 可用语言={list(available_langs.keys())}")
        
        action_group = QActionGroup(menu)
        action_group.setExclusive(True)
        
        for locale_code, locale_name in sorted(available_langs.items()):
            action = QAction(locale_name, menu)
            action.setCheckable(True)
            action.setData(locale_code)
            
            if locale_code == current_locale:
                action.setChecked(True)
            
            action.triggered.connect(self.on_language_selected)
            menu.addAction(action)
            action_group.addAction(action)
        
        # 在按钮下方显示菜单
        print("🔍 LanguageButton: 显示弹出菜单")
        menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
    
    def on_language_selected(self):
        """语言被选中"""
        print("🔍 LanguageButton: 语言选项被点击")  # 调试
        
        action = self.sender()
        if not action:
            print("❌ LanguageButton: 无法获取sender")
            return
        
        locale_code = action.data()
        old_locale = self.i18n.get_current_locale()
        
        print(f"🔍 LanguageButton: 当前语言={old_locale}, 目标语言={locale_code}")
        
        if locale_code == old_locale:
            print(f"⚠️ LanguageButton: 语言已经是 {locale_code}")
            return
        
        # 切换语言
        print(f"🔄 LanguageButton: 正在切换语言 {old_locale} → {locale_code}")
        self.i18n.set_locale(locale_code)
        
        # 发出信号
        print(f"📡 LanguageButton: 发出language_changed信号")
        self.language_changed.emit(locale_code)
    
    def on_language_changed(self, locale: str):
        """
        语言切换事件处理
        
        Args:
            locale: 新语言代码
        """
        self.update_text()
        logger.debug(f"Language button updated for locale: {locale}")


# ============================================================================
# 工具函数
# ============================================================================

def show_language_dialog(parent=None) -> Optional[str]:
    """
    显示语言选择对话框
    
    Args:
        parent: 父窗口
    
    Returns:
        选中的语言代码，如果取消则返回None
    """
    dialog = LanguageDialog(parent)
    
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return get_i18n_manager().get_current_locale()
    
    return None


logger.info("Language selector module loaded successfully")

