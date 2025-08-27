"""
搜索对话框 - Chango Editor

提供完整的查找和替换功能，支持统计显示和循环查找
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, 
    QTextEdit, QTabWidget, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut, QTextCursor, QFont
import re


class SearchDialog(QDialog):
    """搜索和替换对话框"""
    
    def __init__(self, parent=None, start_mode="find"):
        super().__init__(parent)
        self.parent_editor = parent
        self.start_mode = start_mode
        
        # 搜索状态
        self.current_matches = []  # 所有匹配位置
        self.current_match_index = -1  # 当前匹配索引
        self.last_search_text = ""
        
        self.setWindowTitle("查找和替换")
        self.setModal(True)  # 改为模态对话框
        self.resize(500, 320)
        
        # 初始化UI
        self._init_ui()
        self._connect_signals()
        self._apply_style()
        
        # 连接主题变化信号
        if parent and hasattr(parent, 'theme_manager'):
            parent.theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # 如果编辑器有选中文本，自动填入查找框
        if parent and hasattr(parent, 'textCursor'):
            cursor = parent.textCursor()
            if cursor.hasSelection():
                selected_text = cursor.selectedText()
                self.find_input.setText(selected_text)
        
        # 设置默认焦点
        if start_mode == "find":
            self.tab_widget.setCurrentIndex(0)
        else:
            self.tab_widget.setCurrentIndex(1)
        
        print(f"搜索对话框初始化完成 (起始模式: {start_mode})")
    
    def _init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 查找标签页
        find_tab = QWidget()
        find_layout = self._create_find_layout()
        find_tab.setLayout(find_layout)
        self.tab_widget.addTab(find_tab, "查找")
        
        # 替换标签页
        replace_tab = QWidget()
        replace_layout = self._create_replace_layout()
        replace_tab.setLayout(replace_layout)
        self.tab_widget.addTab(replace_tab, "替换")
        
        layout.addWidget(self.tab_widget)
        
        # 统计信息显示
        self.stats_label = QLabel("准备搜索...")
        stats_font = QFont()
        stats_font.setPointSize(9)
        self.stats_label.setFont(stats_font)
        self.stats_label.setStyleSheet("color: #666; padding: 4px;")
        layout.addWidget(self.stats_label)
        
        # 选项区域
        options_layout = self._create_options_layout()
        layout.addLayout(options_layout)
        
        # 按钮区域
        buttons_layout = self._create_buttons_layout()
        layout.addLayout(buttons_layout)
    
    def _create_find_layout(self):
        """创建查找布局"""
        layout = QGridLayout()
        
        # 查找文本
        layout.addWidget(QLabel("查找内容:"), 0, 0)
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("请输入要查找的文本...")
        layout.addWidget(self.find_input, 0, 1)
        
        return layout
    
    def _create_replace_layout(self):
        """创建替换布局"""
        layout = QGridLayout()
        
        # 查找文本（替换标签页使用相同的输入框）
        layout.addWidget(QLabel("查找内容:"), 0, 0)
        self.find_input_replace = QLineEdit()
        self.find_input_replace.setPlaceholderText("请输入要查找的文本...")
        layout.addWidget(self.find_input_replace, 0, 1)
        
        # 替换文本
        layout.addWidget(QLabel("替换为:"), 1, 0)
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("请输入替换文本...")
        layout.addWidget(self.replace_input, 1, 1)
        
        return layout
    
    def _create_options_layout(self):
        """创建选项布局"""
        layout = QHBoxLayout()
        
        # 选项复选框
        self.case_sensitive_cb = QCheckBox("区分大小写")
        self.whole_words_cb = QCheckBox("全词匹配")
        self.regex_cb = QCheckBox("正则表达式")
        
        layout.addWidget(self.case_sensitive_cb)
        layout.addWidget(self.whole_words_cb)
        layout.addWidget(self.regex_cb)
        layout.addStretch()
        
        return layout
    
    def _create_buttons_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        
        # 查找按钮
        self.find_next_btn = QPushButton("查找下一个")
        self.find_previous_btn = QPushButton("查找上一个")
        self.find_all_btn = QPushButton("查找全部")
        
        layout.addWidget(self.find_next_btn)
        layout.addWidget(self.find_previous_btn)
        layout.addWidget(self.find_all_btn)
        
        # 分隔符
        layout.addStretch()
        
        # 替换按钮
        self.replace_btn = QPushButton("替换")
        self.replace_all_btn = QPushButton("全部替换")
        
        layout.addWidget(self.replace_btn)
        layout.addWidget(self.replace_all_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        return layout
    
    def _connect_signals(self):
        """连接信号"""
        # 按钮信号
        self.find_next_btn.clicked.connect(self._on_find_next)
        self.find_previous_btn.clicked.connect(self._on_find_previous)
        self.find_all_btn.clicked.connect(self._on_find_all)
        self.replace_btn.clicked.connect(self._on_replace_current)
        self.replace_all_btn.clicked.connect(self._on_replace_all)
        
        # 输入框信号
        self.find_input.returnPressed.connect(self._on_find_next)
        self.find_input.textChanged.connect(self._on_search_text_changed)
        
        self.find_input_replace.returnPressed.connect(self._on_find_next)
        self.find_input_replace.textChanged.connect(self._on_search_text_changed)
        
        # 标签页切换信号
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
        # 选项变化信号
        self.case_sensitive_cb.toggled.connect(self._on_options_changed)
        self.whole_words_cb.toggled.connect(self._on_options_changed)
        self.regex_cb.toggled.connect(self._on_options_changed)
        
        # ESC键关闭对话框
        shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        shortcut.activated.connect(self.close)
    
    def _apply_style(self):
        """应用样式"""
        # 获取主题管理器
        parent = self.parent()
        theme_manager = None
        
        # 向上查找主题管理器
        while parent:
            if hasattr(parent, 'theme_manager'):
                theme_manager = parent.theme_manager
                break
            parent = parent.parent()
        
        # 使用主题颜色或默认暗色主题
        if theme_manager:
            theme = theme_manager.get_current_theme()
            colors = theme.get("colors", {})
        else:
            colors = {
                'background': '#2b2b2b',
                'foreground': '#ffffff',
                'menu_background': '#3c3c3c',
                'menu_foreground': '#ffffff',
                'selection': '#0078d4',
                'line_highlight': '#404040'
            }
        
        style = f"""
        QDialog {{
            background-color: {colors.get('background', '#2b2b2b')};
            color: {colors.get('foreground', '#ffffff')};
        }}
        QTabWidget {{
            background-color: {colors.get('background', '#2b2b2b')};
        }}
        QTabWidget::pane {{
            border: 1px solid #555555;
            background-color: {colors.get('background', '#2b2b2b')};
        }}
        QTabBar::tab {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            padding: 8px 16px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {colors.get('background', '#2b2b2b')};
            border-bottom: 1px solid {colors.get('background', '#2b2b2b')};
        }}
        QLabel {{
            color: {colors.get('foreground', '#ffffff')};
        }}
        QLineEdit {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 3px;
        }}
        QLineEdit:focus {{
            border-color: {colors.get('selection', '#0078d4')};
        }}
        QPushButton {{
            background-color: {colors.get('selection', '#0078d4')};
            color: #ffffff;
            border: none;
            padding: 6px 12px;
            border-radius: 3px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #106ebe;
        }}
        QPushButton:pressed {{
            background-color: #005a9e;
        }}
        QPushButton:disabled {{
            background-color: #555555;
            color: #888888;
        }}
        QCheckBox {{
            color: {colors.get('foreground', '#ffffff')};
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 1px solid #555555;
            background-color: {colors.get('menu_background', '#3c3c3c')};
            border-radius: 2px;
        }}
        QCheckBox::indicator:checked {{
            background-color: {colors.get('selection', '#0078d4')};
            border-color: {colors.get('selection', '#0078d4')};
        }}
        """
        self.setStyleSheet(style)
    
    def _on_theme_changed(self, theme_name):
        """主题改变时的处理"""
        self._apply_style()
    
    def _get_current_search_text(self):
        """获取当前查找文本"""
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:  # 查找标签页
            return self.find_input.text()
        else:  # 替换标签页
            return self.find_input_replace.text()
    
    def _sync_search_inputs(self):
        """同步两个标签页的搜索输入框"""
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:  # 从查找标签页同步到替换标签页
            self.find_input_replace.setText(self.find_input.text())
        else:  # 从替换标签页同步到查找标签页
            self.find_input.setText(self.find_input_replace.text())
    
    def _on_tab_changed(self, index):
        """标签页切换时的处理"""
        self._sync_search_inputs()
        
        # 设置焦点到相应的输入框
        if index == 0:  # 查找标签页
            self.find_input.setFocus()
        else:  # 替换标签页
            self.find_input_replace.setFocus()
    
    def _on_search_text_changed(self):
        """搜索文本改变时的处理"""
        self._sync_search_inputs()
        # 清除之前的搜索结果
        self.current_matches = []
        self.current_match_index = -1
        self.last_search_text = ""
        self._update_stats_display("准备搜索...")
    
    def _on_options_changed(self):
        """搜索选项改变时的处理"""
        # 清除之前的搜索结果
        self.current_matches = []
        self.current_match_index = -1
        self.last_search_text = ""
        self._update_stats_display("搜索选项已改变，准备搜索...")
    
    def _find_all_matches(self, text):
        """查找所有匹配项"""
        if not text or not self.parent_editor:
            return []
        
        matches = []
        doc_text = self.parent_editor.toPlainText()
        
        case_sensitive = self.case_sensitive_cb.isChecked()
        whole_words = self.whole_words_cb.isChecked()
        regex = self.regex_cb.isChecked()
        
        try:
            if regex:
                # 正则表达式查找
                pattern_flags = 0 if case_sensitive else re.IGNORECASE
                pattern = re.compile(text, pattern_flags)
                
                for match in pattern.finditer(doc_text):
                    matches.append((match.start(), match.end()))
            else:
                # 普通文本查找
                search_text = text if case_sensitive else text.lower()
                target_text = doc_text if case_sensitive else doc_text.lower()
                
                if whole_words:
                    # 全词匹配
                    import re
                    word_pattern = r'\b' + re.escape(text) + r'\b'
                    pattern_flags = 0 if case_sensitive else re.IGNORECASE
                    pattern = re.compile(word_pattern, pattern_flags)
                    
                    for match in pattern.finditer(doc_text):
                        matches.append((match.start(), match.end()))
                else:
                    # 简单文本查找
                    start = 0
                    while True:
                        pos = target_text.find(search_text, start)
                        if pos == -1:
                            break
                        matches.append((pos, pos + len(text)))
                        start = pos + 1
                        
        except re.error as e:
            QMessageBox.warning(self, "正则表达式错误", f"正则表达式有误: {e}")
            return []
        
        return matches
    
    def _update_stats_display(self, text):
        """更新统计信息显示"""
        self.stats_label.setText(text)
    
    def _on_find_all(self):
        """查找全部"""
        text = self._get_current_search_text()
        if not text:
            QMessageBox.information(self, "提示", "请输入要查找的内容")
            return
        
        # 查找所有匹配项
        self.current_matches = self._find_all_matches(text)
        self.last_search_text = text
        
        if self.current_matches:
            self.current_match_index = 0
            self._highlight_current_match()
            self._update_stats_display(f"找到 {len(self.current_matches)} 个匹配项，当前: 第 1 个")
        else:
            self._update_stats_display(f"未找到匹配项: '{text}'")
    
    def _on_find_next(self):
        """查找下一个"""
        text = self._get_current_search_text()
        if not text:
            QMessageBox.information(self, "提示", "请输入要查找的内容")
            return
        
        # 如果搜索文本改变了，重新查找所有匹配项
        if text != self.last_search_text:
            self._on_find_all()
            return
        
        if not self.current_matches:
            self._on_find_all()
            return
        
        # 移到下一个匹配项
        if self.current_match_index < len(self.current_matches) - 1:
            self.current_match_index += 1
            self._highlight_current_match()
            self._update_stats_display(f"找到 {len(self.current_matches)} 个匹配项，当前: 第 {self.current_match_index + 1} 个")
        else:
            # 已经是最后一个，询问是否回到第一个
            reply = QMessageBox.question(
                self, "已到达最后", 
                f"已到达最后一个匹配项。是否从第一个重新开始？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_match_index = 0
                self._highlight_current_match()
                self._update_stats_display(f"找到 {len(self.current_matches)} 个匹配项，当前: 第 1 个 (重新开始)")
    
    def _on_find_previous(self):
        """查找上一个"""
        text = self._get_current_search_text()
        if not text:
            QMessageBox.information(self, "提示", "请输入要查找的内容")
            return
        
        # 如果搜索文本改变了，重新查找所有匹配项
        if text != self.last_search_text:
            self._on_find_all()
            if self.current_matches:
                self.current_match_index = len(self.current_matches) - 1
                self._highlight_current_match()
                self._update_stats_display(f"找到 {len(self.current_matches)} 个匹配项，当前: 第 {self.current_match_index + 1} 个")
            return
        
        if not self.current_matches:
            self._on_find_all()
            return
        
        # 移到上一个匹配项
        if self.current_match_index > 0:
            self.current_match_index -= 1
            self._highlight_current_match()
            self._update_stats_display(f"找到 {len(self.current_matches)} 个匹配项，当前: 第 {self.current_match_index + 1} 个")
        else:
            # 已经是第一个，询问是否回到最后一个
            reply = QMessageBox.question(
                self, "已到达开头", 
                f"已到达第一个匹配项。是否从最后一个重新开始？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_match_index = len(self.current_matches) - 1
                self._highlight_current_match()
                self._update_stats_display(f"找到 {len(self.current_matches)} 个匹配项，当前: 第 {self.current_match_index + 1} 个 (从尾部开始)")
    
    def _highlight_current_match(self):
        """高亮当前匹配项"""
        if not self.current_matches or self.current_match_index < 0:
            return
        
        start, end = self.current_matches[self.current_match_index]
        
        # 选中匹配的文本
        cursor = QTextCursor(self.parent_editor.document())
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        self.parent_editor.setTextCursor(cursor)
        self.parent_editor.ensureCursorVisible()
    
    def _on_replace_current(self):
        """替换当前选中项"""
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            QMessageBox.information(self, "提示", "请切换到替换标签页进行替换操作")
            return
        
        find_text = self.find_input_replace.text()
        replace_text = self.replace_input.text()
        
        if not find_text:
            QMessageBox.information(self, "提示", "请输入要查找的内容")
            return
        
        if not self.current_matches or self.current_match_index < 0:
            QMessageBox.information(self, "提示", "请先查找到要替换的内容")
            return
        
        # 获取当前匹配项的位置
        start, end = self.current_matches[self.current_match_index]
        
        # 替换文本
        cursor = QTextCursor(self.parent_editor.document())
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        cursor.insertText(replace_text)
        
        # 更新匹配项列表（重新查找）
        self.current_matches = self._find_all_matches(find_text)
        self.last_search_text = find_text
        
        if self.current_matches:
            # 调整当前索引
            if self.current_match_index >= len(self.current_matches):
                self.current_match_index = len(self.current_matches) - 1
            
            if self.current_match_index >= 0:
                self._highlight_current_match()
                self._update_stats_display(f"已替换，剩余 {len(self.current_matches)} 个匹配项，当前: 第 {self.current_match_index + 1} 个")
            else:
                self._update_stats_display("已替换，没有更多匹配项")
        else:
            self._update_stats_display("已替换，没有更多匹配项")
    
    def _on_replace_all(self):
        """全部替换"""
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            QMessageBox.information(self, "提示", "请切换到替换标签页进行替换操作")
            return
        
        find_text = self.find_input_replace.text()
        replace_text = self.replace_input.text()
        
        if not find_text:
            QMessageBox.information(self, "提示", "请输入要查找的内容")
            return
        
        # 使用编辑器的全部替换功能
        case_sensitive = self.case_sensitive_cb.isChecked()
        whole_words = self.whole_words_cb.isChecked()
        regex = self.regex_cb.isChecked()
        
        count = self.parent_editor.replace_all(find_text, replace_text, case_sensitive, whole_words, regex)
        
        # 清除搜索状态
        self.current_matches = []
        self.current_match_index = -1
        self.last_search_text = ""
        
        self._update_stats_display(f"全部替换完成，共替换 {count} 处")
        QMessageBox.information(self, "替换完成", f"已替换 {count} 处")
    
    def show_and_focus(self):
        """显示对话框并聚焦到相应的输入框"""
        self.show()
        
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            self.find_input.setFocus()
            self.find_input.selectAll()
        else:
            self.find_input_replace.setFocus()
            self.find_input_replace.selectAll()
        
        self.raise_()
        self.activateWindow()
