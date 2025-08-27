"""
新建文件对话框 - Chango Editor

提供文件模板选择和基本信息设置
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit,
    QCheckBox, QFileDialog, QMessageBox, QTabWidget, QWidget,
    QListWidget, QListWidgetItem, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from utils.file_templates import FileTemplates


class NewFileDialog(QDialog):
    """新建文件对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建文件")
        self.setModal(True)
        self.resize(800, 600)
        
        # 文件信息
        self.file_info = {
            'type': 'text',
            'content': '',
            'save_path': None
        }
        
        # 初始化UI
        self._init_ui()
        
        # 连接信号
        self._connect_signals()
        
        # 设置默认值
        self._set_defaults()
        
        print("新建文件对话框初始化完成")
    
    def _init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 8, 15, 10)  # 优化边距：上边距减少到8px
        layout.setSpacing(6)  # 进一步减少控件间距
        
        # 标题
        title_label = QLabel("选择文件类型和模板")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setMaximumHeight(30)  # 限制标题高度
        title_label.setContentsMargins(0, 0, 0, 0)  # 移除标题内边距
        layout.addWidget(title_label)
        
        # 主要内容区域
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：模板选择
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 5, 0)  # 减少边距
        left_layout.setSpacing(5)  # 减少间距
        
        # 模板类型标签
        template_label = QLabel("文件模板:")
        template_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        left_layout.addWidget(template_label)
        
        # 模板列表
        self.template_list = QListWidget()
        self.template_list.setMaximumWidth(250)
        self.template_list.setMinimumHeight(300)  # 设置最小高度
        left_layout.addWidget(self.template_list)
        
        # 填充模板列表
        templates = FileTemplates.get_available_templates()
        
        # 添加空文件选项
        empty_item = QListWidgetItem("空文件")
        empty_item.setData(Qt.ItemDataRole.UserRole, ('', ''))
        self.template_list.addItem(empty_item)
        
        # 添加模板选项
        for display_name, extension in templates.items():
            item = QListWidgetItem(display_name)
            item.setData(Qt.ItemDataRole.UserRole, (extension, display_name))
            self.template_list.addItem(item)
        
        # 设置默认选择
        self.template_list.setCurrentRow(0)
        
        left_widget.setLayout(left_layout)
        content_splitter.addWidget(left_widget)
        
        # 右侧：预览和设置
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(5, 0, 0, 0)  # 减少边距
        right_layout.setSpacing(8)  # 减少间距
        
        # 文件信息设置
        info_layout = QGridLayout()
        info_layout.setVerticalSpacing(8)  # 减少垂直间距
        info_layout.setHorizontalSpacing(10)  # 适当的水平间距
        
        # 文件名
        info_layout.addWidget(QLabel("文件名:"), 0, 0)
        self.filename_edit = QLineEdit()
        self.filename_edit.setPlaceholderText("输入文件名（可选）")
        info_layout.addWidget(self.filename_edit, 0, 1)
        
        # 保存选项
        self.save_checkbox = QCheckBox("立即保存到文件")
        info_layout.addWidget(self.save_checkbox, 1, 0, 1, 2)
        
        # 保存路径
        self.path_label = QLabel("保存路径:")
        self.path_label.setEnabled(False)
        info_layout.addWidget(self.path_label, 2, 0)
        
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setEnabled(False)
        self.path_edit.setPlaceholderText("选择保存位置")
        path_layout.addWidget(self.path_edit)
        
        self.browse_button = QPushButton("浏览...")
        self.browse_button.setEnabled(False)
        path_layout.addWidget(self.browse_button)
        
        path_widget = QWidget()
        path_widget.setLayout(path_layout)
        info_layout.addWidget(path_widget, 2, 1)
        
        right_layout.addLayout(info_layout)
        
        # 模板预览
        preview_label = QLabel("模板预览:")
        preview_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        right_layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 9))
        right_layout.addWidget(self.preview_text)
        
        right_widget.setLayout(right_layout)
        content_splitter.addWidget(right_widget)
        
        # 设置分割器比例
        content_splitter.setSizes([250, 550])
        layout.addWidget(content_splitter)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 5, 0, 0)  # 减少上边距
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setMinimumWidth(80)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.create_button = QPushButton("创建")
        self.create_button.setMinimumWidth(80)
        self.create_button.setDefault(True)
        self.create_button.clicked.connect(self.accept)
        button_layout.addWidget(self.create_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 应用样式
        self._apply_style()
        
        # 如果有父窗口，连接主题变化信号
        if self.parent() and hasattr(self.parent(), 'theme_manager'):
            self.parent().theme_manager.theme_changed.connect(self._on_theme_changed)
    
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
        QListWidget {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            outline: none;
        }}
        QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid #555555;
        }}
        QListWidget::item:selected {{
            background-color: {colors.get('selection', '#0078d4')};
        }}
        QListWidget::item:hover {{
            background-color: {colors.get('line_highlight', '#404040')};
        }}
        QTextEdit {{
            background-color: {colors.get('background', '#1e1e1e')};
            color: {colors.get('foreground', '#d4d4d4')};
            border: 1px solid #555555;
            font-family: 'Consolas', 'Courier New', monospace;
        }}
        QPushButton {{
            background-color: {colors.get('selection', '#0078d4')};
            color: #ffffff;
            border: none;
            padding: 8px 16px;
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
        QSplitter::handle {{
            background-color: #555555;
        }}
        """
        self.setStyleSheet(style)
    
    def _on_theme_changed(self, theme_name):
        """主题改变时的处理"""
        self._apply_style()
    
    def _connect_signals(self):
        """连接信号"""
        self.template_list.currentItemChanged.connect(self._on_template_changed)
        self.save_checkbox.toggled.connect(self._on_save_toggled)
        self.browse_button.clicked.connect(self._browse_save_path)
        self.filename_edit.textChanged.connect(self._update_preview)
        self.filename_edit.textChanged.connect(self._on_filename_changed)
    
    def _set_defaults(self):
        """设置默认值"""
        # 更新预览
        self._update_preview()
    
    def _on_template_changed(self, current, previous):
        """模板选择改变"""
        if current:
            self._update_preview()
            # 模板改变时也需要更新保存路径
            self._update_save_path_filename()
    
    def _on_filename_changed(self):
        """文件名输入改变时更新保存路径"""
        self._update_save_path_filename()
    
    def _update_save_path_filename(self):
        """更新保存路径中的文件名"""
        # 只有在勾选了立即保存且路径框有内容时才更新
        if not self.save_checkbox.isChecked() or not self.path_edit.text():
            return
        
        current_path = self.path_edit.text()
        filename_input = self.filename_edit.text().strip()
        
        # 获取当前模板的扩展名
        current_item = self.template_list.currentItem()
        extension = ""
        if current_item:
            extension, display_name = current_item.data(Qt.ItemDataRole.UserRole)
        
        # 确定新的文件名
        if filename_input:
            # 用户输入了文件名，使用用户输入的文件名
            if extension and not filename_input.endswith(extension):
                new_filename = f"{filename_input}{extension}"
            else:
                new_filename = filename_input
        else:
            # 用户没有输入文件名，使用默认文件名
            if extension:
                new_filename = f"新建文件{extension}"
            else:
                new_filename = "新建文件.txt"
        
        # 更新路径
        # 智能判断路径类型：如果路径有文件扩展名或不是现有目录，视为文件路径
        if (os.path.splitext(current_path)[1] or  # 有文件扩展名
            not os.path.isdir(current_path)):     # 不是现有目录
            # 当前路径是文件路径（或准备作为文件路径），替换文件名
            directory = os.path.dirname(current_path)
            new_path = os.path.join(directory, new_filename)
        else:
            # 当前路径是现有目录路径，添加文件名
            new_path = os.path.join(current_path, new_filename)
        
        self.path_edit.setText(new_path)
    
    def _on_save_toggled(self, checked):
        """保存选项切换"""
        self.path_label.setEnabled(checked)
        self.path_edit.setEnabled(checked)
        self.browse_button.setEnabled(checked)
        
        if checked and not self.path_edit.text():
            # 自动设置默认保存路径 - 设置为完整文件路径
            current_dir = os.getcwd()
            
            # 获取文件扩展名
            current_item = self.template_list.currentItem()
            if current_item:
                extension, display_name = current_item.data(Qt.ItemDataRole.UserRole)
                if extension:
                    default_name = f"新建文件{extension}"
                else:
                    default_name = "新建文件.txt"
            else:
                default_name = "新建文件.txt"
            
            # 设置完整的文件路径
            default_path = os.path.join(current_dir, default_name)
            self.path_edit.setText(default_path)
            
            # 如果用户已经输入了文件名，更新路径中的文件名
            self._update_save_path_filename()
    
    def _browse_save_path(self):
        """浏览保存路径"""
        current_item = self.template_list.currentItem()
        if current_item:
            extension, display_name = current_item.data(Qt.ItemDataRole.UserRole)
            
            # 构建文件过滤器
            if extension:
                filter_name = display_name.replace(f' ({extension})', '')
                file_filter = f"{filter_name} (*{extension});;所有文件 (*)"
                default_name = f"新建文件{extension}"
            else:
                file_filter = "所有文件 (*)"
                default_name = "新建文件.txt"
            
            # 获取当前路径
            current_path = self.path_edit.text() or os.getcwd()
            if os.path.isdir(current_path):
                default_path = os.path.join(current_path, default_name)
            else:
                default_path = default_name
            
            # 显示保存对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存新文件",
                default_path,
                file_filter
            )
            
            if file_path:
                self.path_edit.setText(file_path)
                
                # 从路径中提取文件名
                filename = os.path.basename(file_path)
                name_without_ext = os.path.splitext(filename)[0]
                self.filename_edit.setText(name_without_ext)
    
    def _update_preview(self):
        """更新预览"""
        current_item = self.template_list.currentItem()
        if current_item:
            extension, display_name = current_item.data(Qt.ItemDataRole.UserRole)
            
            if extension:
                # 获取模板内容
                template_content = FileTemplates.get_template(extension)
                
                # 替换模板中的占位符
                filename = self.filename_edit.text() or "新建文件"
                template_content = template_content.replace("Your Name", "PyEditor User")
                
                self.preview_text.setPlainText(template_content)
                self.file_info['content'] = template_content
                self.file_info['type'] = display_name
            else:
                # 空文件
                self.preview_text.setPlainText("# 这将创建一个空文件")
                self.file_info['content'] = ""
                self.file_info['type'] = "空文件"
    
    def get_file_info(self):
        """获取文件信息"""
        # 更新保存路径
        if self.save_checkbox.isChecked() and self.path_edit.text():
            self.file_info['save_path'] = self.path_edit.text()
        else:
            self.file_info['save_path'] = None
        
        # 更新文件名
        filename = self.filename_edit.text().strip()
        if filename:
            self.file_info['filename'] = filename
        else:
            self.file_info['filename'] = None
        
        # 添加扩展名信息
        current_item = self.template_list.currentItem()
        if current_item:
            extension, display_name = current_item.data(Qt.ItemDataRole.UserRole)
            self.file_info['extension'] = extension
        else:
            self.file_info['extension'] = '.txt'
        
        return self.file_info
    
    def accept(self):
        """接受对话框"""
        # 验证输入
        if self.save_checkbox.isChecked():
            save_path = self.path_edit.text()
            if not save_path:
                QMessageBox.warning(self, "警告", "请选择保存路径")
                return
            
            # 检查文件是否已存在
            if os.path.exists(save_path):
                reply = QMessageBox.question(
                    self,
                    "文件已存在",
                    f"文件 '{save_path}' 已存在，是否覆盖？",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    return
        
        # 最后更新文件信息
        self.get_file_info()
        super().accept()
