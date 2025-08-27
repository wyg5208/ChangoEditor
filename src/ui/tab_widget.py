"""
标签页管理器 - Chango Editor

主要功能：
- 管理多个编辑器标签页
- 处理标签页的创建、关闭、切换
- 管理文件与标签页的关联
- 处理未保存更改的提示
"""

import os
from PyQt6.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout, QMessageBox,
    QTabBar, QApplication, QMenu
)
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QUrl
from PyQt6.QtGui import QFont

from core.editor import TextEditor


class TabWidget(QTabWidget):
    """标签页管理器"""
    
    # 信号定义
    current_editor_changed = pyqtSignal(object)  # 当前编辑器改变
    tab_count_changed = pyqtSignal(int)          # 标签页数量改变
    file_content_changed = pyqtSignal(str)       # 文件内容改变
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置标签页属性
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setElideMode(Qt.TextElideMode.ElideMiddle)  # 长文件名省略
        
        # 启用拖拽功能
        self.setAcceptDrops(True)
        
        # 连接信号
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self._on_current_changed)
        
        # 添加右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
        # 存储编辑器映射
        self.editors = {}  # {index: editor}
        self.file_paths = {}  # {index: file_path}
        
        # 未命名文件计数
        self.untitled_count = 0
        
        # 应用样式
        self._apply_tab_style()
        
        print("标签页管理器初始化完成")
    
    def new_tab(self, file_path=None, content="", display_name=None):
        """创建新标签页"""
        # 创建编辑器
        editor = TextEditor()
        
        # 设置内容
        if content:
            editor.setPlainText(content)
        
        # 确定标签名称
        if file_path:
            tab_name = os.path.basename(file_path)
            editor.set_file_path(file_path)
        elif display_name:
            # 使用用户指定的显示名称
            tab_name = display_name
            file_path = None
        else:
            self.untitled_count += 1
            tab_name = f"未命名-{self.untitled_count}"
            file_path = None
        
        # 创建标签页容器
        tab_container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(editor)
        tab_container.setLayout(layout)
        
        # 添加标签页
        index = self.addTab(tab_container, tab_name)
        
        # 设置工具提示
        if file_path:
            self.setTabToolTip(index, f"文件路径: {file_path}")
        else:
            self.setTabToolTip(index, "新建文件（尚未保存）")
        
        # 存储映射关系
        self.editors[index] = editor
        self.file_paths[index] = file_path
        
        # 连接编辑器信号
        editor.textChanged.connect(lambda: self._on_content_changed(index))
        editor.cursorPositionChanged.connect(lambda: self._on_cursor_changed(index))
        editor.file_path_changed.connect(lambda path: self._on_file_path_changed(index, path))
        
        # 切换到新标签页
        self.setCurrentIndex(index)
        
        # 现在编辑器已经在界面层次中，应用主题（重要：必须在添加到界面后才能找到主题管理器）
        # 使用QTimer延迟执行，确保界面完全构建好
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, editor.update_theme)
        
        # 设置焦点
        editor.setFocus()
        
        # 发射信号
        self.tab_count_changed.emit(self.count())
        self.current_editor_changed.emit(editor)
        
        print(f"创建新标签页: {tab_name} (索引: {index})")
        return index
    
    def open_file(self, file_path):
        """打开文件"""
        # 检查文件是否已经打开
        for index, path in self.file_paths.items():
            if path == file_path:
                self.setCurrentIndex(index)
                return True
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 创建新标签页
            index = self.new_tab(file_path, content)
            
            # 标记为已保存状态
            editor = self.editors[index]
            editor.document().setModified(False)
            
            print(f"成功打开文件: {file_path}")
            return True
            
        except UnicodeDecodeError:
            try:
                # 尝试其他编码
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
                
                index = self.new_tab(file_path, content)
                editor = self.editors[index]
                editor.document().setModified(False)
                
                print(f"使用GBK编码打开文件: {file_path}")
                return True
            except Exception as e:
                print(f"打开文件失败: {file_path}, 错误: {e}")
                return False
        except Exception as e:
            print(f"打开文件失败: {file_path}, 错误: {e}")
            return False
    
    def close_tab(self, index):
        """关闭标签页"""
        if index < 0 or index >= self.count():
            return False
        
        editor = self.editors.get(index)
        if not editor:
            return False
        
        # 检查是否有未保存更改
        if editor.document().isModified():
            file_path = self.file_paths.get(index, "未命名")
            filename = os.path.basename(file_path) if file_path else "未命名"
            
            reply = QMessageBox.question(
                self,
                "确认关闭",
                f"文件 '{filename}' 有未保存的更改，是否保存？",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )
            
            if reply == QMessageBox.StandardButton.Save:
                if not editor.save():
                    return False  # 保存失败，取消关闭
            elif reply == QMessageBox.StandardButton.Cancel:
                return False  # 用户取消
            # Discard: 直接关闭
        
        # 移除标签页
        self.removeTab(index)
        
        # 清理映射关系
        if index in self.editors:
            del self.editors[index]
        if index in self.file_paths:
            del self.file_paths[index]
        
        # 更新其他标签页的索引映射
        self._update_index_mappings()
        
        # 发射信号
        self.tab_count_changed.emit(self.count())
        
        # 如果没有标签页了，发射空编辑器信号
        if self.count() == 0:
            self.current_editor_changed.emit(None)
        
        print(f"关闭标签页: 索引 {index}")
        return True
    
    def close_all_tabs(self):
        """关闭所有标签页"""
        while self.count() > 0:
            if not self.close_tab(0):
                return False  # 用户取消或保存失败
        return True
    
    def get_current_editor(self):
        """获取当前编辑器"""
        index = self.currentIndex()
        return self.editors.get(index)
    
    def get_current_file_path(self):
        """获取当前文件路径"""
        index = self.currentIndex()
        return self.file_paths.get(index)
    
    def has_unsaved_changes(self):
        """检查是否有未保存的更改"""
        for editor in self.editors.values():
            if editor.document().isModified():
                return True
        return False
    
    def save_all(self):
        """保存所有文件"""
        success_count = 0
        for index, editor in self.editors.items():
            if editor.document().isModified():
                if editor.save():
                    success_count += 1
                else:
                    print(f"保存失败: 索引 {index}")
        
        print(f"批量保存完成，成功保存 {success_count} 个文件")
        return success_count
    
    def _on_current_changed(self, index):
        """当前标签页改变"""
        editor = self.editors.get(index)
        self.current_editor_changed.emit(editor)
        
        if editor:
            editor.setFocus()
    
    def _on_content_changed(self, index):
        """内容改变时的处理"""
        editor = self.editors.get(index)
        if not editor:
            return
        
        # 更新标签页标题
        self._update_tab_title(index)
        
        # 发射信号
        file_path = self.file_paths.get(index, "")
        self.file_content_changed.emit(file_path)
    
    def _on_cursor_changed(self, index):
        """光标位置改变"""
        # TODO: 可以在这里更新状态栏的行列信息
        pass
    
    def _on_file_path_changed(self, index, file_path):
        """文件路径改变事件处理"""
        # 更新文件路径映射
        self.file_paths[index] = file_path
        
        # 更新标签页标题
        if file_path:
            tab_name = os.path.basename(file_path)
            # 更新工具提示
            self.setTabToolTip(index, f"文件路径: {file_path}")
        else:
            tab_name = f"未命名-{self.untitled_count}"
            # 更新工具提示
            self.setTabToolTip(index, "新建文件（尚未保存）")
        
        self.setTabText(index, tab_name)
        print(f"标签页 {index} 标题已更新为: {tab_name}")
    
    def _update_tab_title(self, index):
        """更新标签页标题"""
        editor = self.editors.get(index)
        if not editor:
            return
        
        file_path = self.file_paths.get(index)
        if file_path:
            title = os.path.basename(file_path)
        else:
            title = self.tabText(index).split(' *')[0]  # 移除修改标记
        
        # 添加修改标记
        if editor.document().isModified():
            title += " *"
        
        self.setTabText(index, title)
    
    def _update_index_mappings(self):
        """更新索引映射（标签页关闭后重新整理）"""
        new_editors = {}
        new_file_paths = {}
        
        for i in range(self.count()):
            # 找到对应的编辑器
            widget = self.widget(i)
            if widget:
                layout = widget.layout()
                if layout and layout.count() > 0:
                    editor = layout.itemAt(0).widget()
                    if isinstance(editor, TextEditor):
                        new_editors[i] = editor
                        # 从旧映射中找到对应的文件路径
                        for old_index, old_editor in self.editors.items():
                            if old_editor is editor:
                                new_file_paths[i] = self.file_paths.get(old_index)
                                break
        
        self.editors = new_editors
        self.file_paths = new_file_paths
    
    def get_all_file_paths(self):
        """获取所有已打开文件的路径"""
        return [path for path in self.file_paths.values() if path]
    
    def get_tab_count(self):
        """获取标签页数量"""
        return self.count()
    
    def switch_to_next_tab(self):
        """切换到下一个标签页"""
        if self.count() > 1:
            next_index = (self.currentIndex() + 1) % self.count()
            self.setCurrentIndex(next_index)
    
    def switch_to_previous_tab(self):
        """切换到上一个标签页"""
        if self.count() > 1:
            prev_index = (self.currentIndex() - 1) % self.count()
            self.setCurrentIndex(prev_index)
    
    def _apply_tab_style(self):
        """应用标签页样式"""
        # 如果主窗口有主题管理器，使用主题样式
        try:
            main_window = self.parent()
            while main_window and not hasattr(main_window, 'theme_manager'):
                main_window = main_window.parent()
            
            if main_window and hasattr(main_window, 'theme_manager'):
                # 从主题管理器获取样式
                theme = main_window.theme_manager.get_current_theme()
                colors = theme.get("colors", {})
                
                style = f"""
                QTabWidget::pane {{
                    border: 1px solid #555555;
                    background-color: {colors.get('background', '#2b2b2b')};
                }}
                QTabWidget::tab-bar {{
                    alignment: left;
                }}
                QTabBar::tab {{
                    background-color: {colors.get('menu_background', '#3c3c3c')};
                    color: {colors.get('menu_foreground', '#ffffff')};
                    border: 1px solid #555555;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    min-width: 80px;
                    max-width: 200px;
                }}
                QTabBar::tab:selected {{
                    background-color: {colors.get('background', '#2b2b2b')};
                    border-bottom: 1px solid {colors.get('background', '#2b2b2b')};
                }}
                QTabBar::tab:hover {{
                    background-color: {colors.get('selection', '#404040')};
                }}
                QTabBar::tab:!selected {{
                    margin-top: 2px;
                }}
                QTabBar::close-button {{
                    image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAsElEQVQokZ2SMQ6CMBiF/0KIwQVn43FwNpxJnQwJM4P3YHAy7HoGhgY34xE4gJ5AzGATOxgGwpKXtN/3vue1/QFAKSUm4Dz7rvGxXK6lVnr7vCeEELiuq+M4jsfjUT3PQ1VVqq5rHYYBvV5PNE2DpmlQSunGGAMA4vGYbNvGarWCbdsAAEEQIIQQSimhlAoA4LoOgiBACAHn8xlKKYRhiOv1qsdzHAeCIEAIgSAI6Lokk8k4z3OWZdlMJhPZtm2HYZhlWZax1WpFAH4A8K/P5e4J9OUAAAAASUVORK5CYII=);
                    subcontrol-position: right;
                }}
                QTabBar::close-button:hover {{
                    background-color: #ff6b6b;
                    border-radius: 2px;
                }}
                """
                self.setStyleSheet(style)
                return
        except Exception as e:
            print(f"应用主题样式失败: {e}")
        
        # 回退到默认暗色主题
        style = """
        QTabWidget::pane {
            border: 1px solid #555555;
            background-color: #2b2b2b;
        }
        QTabWidget::tab-bar {
            alignment: left;
        }
        QTabBar::tab {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 80px;
            max-width: 200px;
        }
        QTabBar::tab:selected {
            background-color: #2b2b2b;
            border-bottom: 1px solid #2b2b2b;
        }
        QTabBar::tab:hover {
            background-color: #404040;
        }
        QTabBar::tab:!selected {
            margin-top: 2px;
        }
        QTabBar::close-button {
            image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAsElEQVQokZ2SMQ6CMBiF/0KIwQVn43FwNpxJnQwJM4P3YHAy7HoGhgY34xE4gJ5AzGATOxgGwpKXtN/3vue1/QFAKSUm4Dz7rvGxXK6lVnr7vCeEELiuq+M4jsfjUT3PQ1VVqq5rHYYBvV5PNE2DpmlQSunGGAMA4vGYbNvGarWCbdsAAEEQIIQQSimhlAoA4LoOgiBACAHn8xlKKYRhiOv1qsdzHAeCIEAIgSAI6Lokk8k4z3OWZdlMJhPZtm2HYZhlWZax1WpFAH4A8K/P5e4J9OUAAAAASUVORK5CYII=);
            subcontrol-position: right;
        }
        QTabBar::close-button:hover {
            background-color: #ff6b6b;
            border-radius: 2px;
        }
        """
        self.setStyleSheet(style)
    
    def _show_context_menu(self, position):
        """显示右键菜单"""
        # 获取点击位置的标签页索引
        tab_index = self.tabBar().tabAt(position)
        
        if tab_index >= 0:
            menu = QMenu(self)
            
            # 关闭当前标签
            close_action = QAction("关闭", self)
            close_action.triggered.connect(lambda: self.close_tab(tab_index))
            menu.addAction(close_action)
            
            # 关闭其他标签
            if self.count() > 1:
                close_others_action = QAction("关闭其他", self)
                close_others_action.triggered.connect(lambda: self._close_other_tabs(tab_index))
                menu.addAction(close_others_action)
                
                # 关闭右侧标签
                if tab_index < self.count() - 1:
                    close_right_action = QAction("关闭右侧", self)
                    close_right_action.triggered.connect(lambda: self._close_tabs_to_right(tab_index))
                    menu.addAction(close_right_action)
                
                # 关闭左侧标签
                if tab_index > 0:
                    close_left_action = QAction("关闭左侧", self)
                    close_left_action.triggered.connect(lambda: self._close_tabs_to_left(tab_index))
                    menu.addAction(close_left_action)
            
            menu.addSeparator()
            
            # 复制文件路径
            file_path = self.file_paths.get(tab_index)
            if file_path:
                copy_path_action = QAction("复制文件路径", self)
                copy_path_action.triggered.connect(lambda: self._copy_file_path(file_path))
                menu.addAction(copy_path_action)
                
                # 在文件管理器中显示
                show_in_explorer_action = QAction("在文件管理器中显示", self)
                show_in_explorer_action.triggered.connect(lambda: self._show_in_explorer(file_path))
                menu.addAction(show_in_explorer_action)
            
            # 显示菜单
            menu.exec(self.mapToGlobal(position))
    
    def _close_other_tabs(self, keep_index):
        """关闭除指定索引外的所有标签页"""
        # 从后往前关闭，避免索引变化
        for i in range(self.count() - 1, -1, -1):
            if i != keep_index:
                self.close_tab(i)
    
    def _close_tabs_to_right(self, index):
        """关闭指定索引右侧的所有标签页"""
        for i in range(self.count() - 1, index, -1):
            self.close_tab(i)
    
    def _close_tabs_to_left(self, index):
        """关闭指定索引左侧的所有标签页"""
        for i in range(index - 1, -1, -1):
            self.close_tab(i)
    
    def _copy_file_path(self, file_path):
        """复制文件路径到剪贴板"""
        from PyQt6.QtGui import QClipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(file_path)
        print(f"已复制文件路径: {file_path}")
    
    def _show_in_explorer(self, file_path):
        """在文件管理器中显示文件"""
        import subprocess
        import platform
        
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.run(["explorer", "/select,", file_path])
            elif system == "Darwin":  # macOS
                subprocess.run(["open", "-R", file_path])
            elif system == "Linux":
                subprocess.run(["xdg-open", os.path.dirname(file_path)])
            print(f"在文件管理器中显示: {file_path}")
        except Exception as e:
            print(f"无法在文件管理器中显示文件: {e}")
    
    def find_tab_by_file_path(self, file_path):
        """根据文件路径查找标签页索引"""
        for index, path in self.file_paths.items():
            if path == file_path:
                return index
        return -1
    
    def duplicate_current_tab(self):
        """复制当前标签页"""
        current_index = self.currentIndex()
        current_editor = self.editors.get(current_index)
        
        if current_editor:
            # 获取当前编辑器的内容
            content = current_editor.toPlainText()
            file_path = self.file_paths.get(current_index)
            
            # 创建新标签页
            new_index = self.new_tab(content=content)
            
            # 如果有文件路径，设置为副本
            if file_path:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                extension = os.path.splitext(file_path)[1]
                new_name = f"{base_name}_副本{extension}"
                self.setTabText(new_index, new_name)
            
            print(f"已复制标签页: 索引 {current_index} -> {new_index}")
            return new_index
        
        return -1
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            # 检查是否包含文件
            urls = event.mimeData().urls()
            has_files = any(url.isLocalFile() and os.path.isfile(url.toLocalFile()) for url in urls)
            if has_files:
                event.acceptProposedAction()
                # 设置拖拽效果
                self.setStyleSheet(self.styleSheet() + """
                    QTabWidget::pane {
                        border: 2px dashed #0078d4;
                        background-color: rgba(0, 120, 212, 0.1);
                    }
                """)
                return
        event.ignore()
    
    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        # 恢复原始样式
        self._apply_tab_style()
        event.accept()
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        # 恢复原始样式
        self._apply_tab_style()
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            opened_files = []
            
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if os.path.isfile(file_path):
                        # 检查文件扩展名，只打开支持的文件类型
                        _, ext = os.path.splitext(file_path)
                        supported_extensions = {
                            '.py', '.pyw', '.js', '.jsx', '.ts', '.tsx',
                            '.html', '.htm', '.css', '.scss', '.sass', '.less',
                            '.cpp', '.c', '.h', '.hpp', '.cxx', '.cc', '.hxx',
                            '.java', '.cs', '.php', '.rb', '.go', '.rs',
                            '.swift', '.kt', '.scala', '.sh', '.bash', '.ps1',
                            '.bat', '.cmd', '.json', '.xml', '.yaml', '.yml',
                            '.sql', '.csv', '.md', '.txt', '.rst'
                        }
                        
                        if ext.lower() in supported_extensions or ext == '':
                            if self.open_file(file_path):
                                opened_files.append(file_path)
                                print(f"通过拖拽打开文件: {file_path}")
                            else:
                                print(f"拖拽打开文件失败: {file_path}")
                        else:
                            print(f"不支持的文件类型: {file_path} (扩展名: {ext})")
            
            if opened_files:
                event.acceptProposedAction()
                # 显示成功消息
                file_count = len(opened_files)
                # 寻找主窗口来显示状态消息
                main_window = self
                while main_window.parent():
                    main_window = main_window.parent()
                    if hasattr(main_window, 'statusbar'):
                        main_window.statusbar.showMessage(
                            f"成功通过拖拽打开 {file_count} 个文件", 3000
                        )
                        break
                print(f"拖拽成功打开 {file_count} 个文件: {opened_files}")
            else:
                event.ignore()
        else:
            event.ignore()
