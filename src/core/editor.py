"""
文本编辑器 - Chango Editor

主要功能：
- 基础文本编辑功能
- 语法高亮支持
- 行号显示
- 基本的撤销/重做
- 文件保存/加载
"""

import os
from PyQt6.QtWidgets import (
    QPlainTextEdit, QWidget, QHBoxLayout, QTextEdit,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt6.QtGui import (
    QColor, QPainter, QTextFormat, QFont, QFontMetrics,
    QTextCursor, QTextCharFormat, QPaintEvent, QTextDocument
)

from utils.syntax import SyntaxHighlighter


class LineNumberArea(QWidget):
    """行号区域"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class TextEditor(QPlainTextEdit):
    """文本编辑器组件"""
    
    # 信号定义
    file_path_changed = pyqtSignal(str)      # 文件路径改变
    content_saved = pyqtSignal()             # 内容已保存
    cursor_position_changed = pyqtSignal(int, int)  # 光标位置改变
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 文件相关属性
        self.file_path = None
        self.file_encoding = 'utf-8'
        
        # 创建行号区域
        self.line_number_area = LineNumberArea(self)
        
        # 连接信号
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)
        
        # 初始化设置
        self._init_editor()
        
        # 创建语法高亮器
        self.syntax_highlighter = None
        self._setup_syntax_highlighting()
        
        print("文本编辑器初始化完成")
    
    def _init_editor(self):
        """初始化编辑器设置"""
        # 设置字体
        font = QFont("Consolas", 11)
        if not font.exactMatch():
            font = QFont("Courier New", 11)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # 设置制表符宽度（4个空格）
        font_metrics = QFontMetrics(font)
        tab_width = 4 * font_metrics.horizontalAdvance(' ')
        self.setTabStopDistance(tab_width)
        
        # 设置行号区域宽度
        self.update_line_number_area_width(0)
        
        # 禁用编辑器的拖拽功能，让TabWidget处理文件拖拽
        self.setAcceptDrops(False)
        
        # 应用主题样式
        self._apply_theme_style()
        
        # 高亮当前行
        self.highlight_current_line()
        
        # 设置编辑器样式
        self._apply_editor_style()
    
    def _apply_editor_style(self):
        """应用编辑器样式"""
        style = """
        QPlainTextEdit {
            background-color: #1e1e1e;
            color: #d4d4d4;
            border: none;
            selection-background-color: #264f78;
        }
        """
        self.setStyleSheet(style)
    
    def _setup_syntax_highlighting(self):
        """设置语法高亮"""
        self.syntax_highlighter = SyntaxHighlighter(self.document())
        
        # 根据文件扩展名设置语言
        if self.file_path:
            self._detect_and_set_language()
    
    def _detect_and_set_language(self):
        """检测并设置语言"""
        if not self.file_path:
            return
        
        _, ext = os.path.splitext(self.file_path)
        ext = ext.lower()
        
        # 扩展的语言映射
        language_map = {
            # Python
            '.py': 'python',
            '.pyw': 'python',
            '.pyx': 'python',
            
            # JavaScript/TypeScript
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            
            # Web
            '.html': 'html',
            '.htm': 'html',
            '.xhtml': 'html',
            '.css': 'css',
            '.scss': 'css',
            '.sass': 'css',
            '.less': 'css',
            
            # C/C++
            '.c': 'c',
            '.h': 'c',
            '.cpp': 'cpp',
            '.cxx': 'cpp',
            '.cc': 'cpp',
            '.hpp': 'cpp',
            '.hxx': 'cpp',
            
            # C#
            '.cs': 'csharp',
            
            # Java
            '.java': 'java',
            
            # Other languages
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'matlab',
            '.lua': 'lua',
            '.perl': 'perl',
            '.pl': 'perl',
            
            # Shell scripts
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'bash',
            '.fish': 'bash',
            '.ps1': 'powershell',
            '.bat': 'batch',
            '.cmd': 'batch',
            
            # Data formats
            '.sql': 'sql',
            '.xml': 'xml',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.toml': 'toml',
            '.ini': 'ini',
            '.cfg': 'ini',
            '.conf': 'ini',
            
            # Documentation
            '.md': 'markdown',
            '.markdown': 'markdown',
            '.rst': 'rst',
            '.txt': 'text',
            
            # Misc
            '.dockerfile': 'dockerfile',
            '.gitignore': 'text',
            '.gitattributes': 'text',
            '.editorconfig': 'ini',
        }
        
        language = language_map.get(ext, 'text')
        if self.syntax_highlighter:
            self.syntax_highlighter.set_language(language)
            print(f"设置语法高亮语言: {language}")
    
    def line_number_area_width(self):
        """计算行号区域宽度"""
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, _):
        """更新行号区域宽度"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """更新行号区域"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                       self.line_number_area.width(), 
                                       rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )
    
    def line_number_area_paint_event(self, event):
        """绘制行号区域"""
        painter = QPainter(self.line_number_area)
        
        # 获取主题颜色
        bg_color = QColor(60, 60, 60)  # 默认背景色
        fg_color = QColor(150, 150, 150)  # 默认前景色
        
        try:
            main_window = self.parent()
            while main_window and not hasattr(main_window, 'theme_manager'):
                main_window = main_window.parent()
            
            if main_window and hasattr(main_window, 'theme_manager'):
                theme = main_window.theme_manager.get_current_theme()
                colors = theme.get("colors", {})
                
                bg_color = QColor(colors.get('line_number_background', '#3c3c3c'))
                fg_color = QColor(colors.get('line_number_foreground', '#969696'))
        except Exception as e:
            print(f"获取行号主题颜色失败: {e}")
        
        painter.fillRect(event.rect(), bg_color)
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        # 设置行号颜色
        painter.setPen(fg_color)
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    0, top, self.line_number_area.width() - 3, 
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight, number
                )
            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
    
    def highlight_current_line(self):
        """高亮当前行"""
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            # 获取主题颜色
            line_color = QColor(40, 40, 40)  # 默认颜色
            
            try:
                main_window = self.parent()
                while main_window and not hasattr(main_window, 'theme_manager'):
                    main_window = main_window.parent()
                
                if main_window and hasattr(main_window, 'theme_manager'):
                    theme = main_window.theme_manager.get_current_theme()
                    colors = theme.get("colors", {})
                    line_color = QColor(colors.get('line_highlight', '#2a2a2a'))
            except Exception as e:
                print(f"获取当前行高亮颜色失败: {e}")
            
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def _on_cursor_position_changed(self):
        """光标位置改变事件"""
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.cursor_position_changed.emit(line, column)
    
    def set_file_path(self, file_path):
        """设置文件路径"""
        self.file_path = file_path
        self.file_path_changed.emit(file_path or "")
        
        # 重新设置语法高亮
        self._detect_and_set_language()
    
    def get_file_path(self):
        """获取文件路径"""
        return self.file_path
    
    def load_file(self, file_path):
        """加载文件"""
        try:
            # 尝试UTF-8编码
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.file_encoding = 'utf-8'
        except UnicodeDecodeError:
            try:
                # 尝试GBK编码
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
                self.file_encoding = 'gbk'
            except Exception as e:
                print(f"无法读取文件 {file_path}: {e}")
                return False
        except Exception as e:
            print(f"无法读取文件 {file_path}: {e}")
            return False
        
        # 设置内容
        self.setPlainText(content)
        self.set_file_path(file_path)
        
        # 标记为未修改
        self.document().setModified(False)
        
        print(f"成功加载文件: {file_path} (编码: {self.file_encoding})")
        return True
    
    def save(self):
        """保存文件"""
        if not self.file_path:
            return self.save_as()
        
        return self._save_to_file(self.file_path)
    
    def save_as(self, file_path=None):
        """另存为文件"""
        if not file_path:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存文件",
                "",
                "所有文件 (*);;"
                "Python文件 (*.py);;"
                "JavaScript文件 (*.js);;"
                "HTML文件 (*.html);;"
                "CSS文件 (*.css);;"
                "文本文件 (*.txt)"
            )
        
        if file_path:
            if self._save_to_file(file_path):
                self.set_file_path(file_path)
                return True
        
        return False
    
    def _save_to_file(self, file_path):
        """保存到指定文件"""
        try:
            content = self.toPlainText()
            with open(file_path, 'w', encoding=self.file_encoding) as f:
                f.write(content)
            
            # 标记为未修改
            self.document().setModified(False)
            
            # 发射保存信号
            self.content_saved.emit()
            
            print(f"文件已保存: {file_path}")
            return True
            
        except Exception as e:
            print(f"保存文件失败 {file_path}: {e}")
            QMessageBox.warning(self, "保存错误", f"无法保存文件: {e}")
            return False
    
    def is_modified(self):
        """检查是否已修改"""
        return self.document().isModified()
    
    def get_text(self):
        """获取文本内容"""
        return self.toPlainText()
    
    def set_text(self, text):
        """设置文本内容"""
        self.setPlainText(text)
    
    def insert_text(self, text):
        """在光标位置插入文本"""
        cursor = self.textCursor()
        cursor.insertText(text)
    
    def get_selected_text(self):
        """获取选中的文本"""
        return self.textCursor().selectedText()
    
    def get_current_line(self):
        """获取当前行号（从1开始）"""
        return self.textCursor().blockNumber() + 1
    
    def get_current_column(self):
        """获取当前列号（从1开始）"""
        return self.textCursor().columnNumber() + 1
    
    def goto_line(self, line_number):
        """跳转到指定行"""
        if line_number < 1:
            line_number = 1
        
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        
        for _ in range(line_number - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Down)
        
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
    
    def find_text(self, text, case_sensitive=False, whole_words=False, regex=False, forward=True):
        """查找文本"""
        if not text:
            return False
        
        # 设置查找标志
        flags = QTextDocument.FindFlag(0)
        if not forward:
            flags |= QTextDocument.FindFlag.FindBackward
        if case_sensitive:
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if whole_words:
            flags |= QTextDocument.FindFlag.FindWholeWords
        
        cursor = self.textCursor()
        
        if regex:
            # 正则表达式查找
            import re
            pattern_flags = 0 if case_sensitive else re.IGNORECASE
            
            try:
                pattern = re.compile(text, pattern_flags)
            except re.error as e:
                print(f"正则表达式错误: {e}")
                return False
            
            # 获取文档内容
            doc_text = self.toPlainText()
            start_pos = cursor.position()
            
            if forward:
                match = pattern.search(doc_text, start_pos)
            else:
                # 向前查找：从开始到当前位置
                matches = list(pattern.finditer(doc_text[:start_pos]))
                match = matches[-1] if matches else None
            
            if match:
                # 选中匹配的文本
                new_cursor = QTextCursor(self.document())
                new_cursor.setPosition(match.start())
                new_cursor.setPosition(match.end(), QTextCursor.MoveMode.KeepAnchor)
                self.setTextCursor(new_cursor)
                self.ensureCursorVisible()
                return True
            
        else:
            # 普通文本查找
            found_cursor = self.document().find(text, cursor, flags)
            if not found_cursor.isNull():
                self.setTextCursor(found_cursor)
                self.ensureCursorVisible()
                return True
        
        return False
    
    def replace_current(self, find_text, replace_text, case_sensitive=False, whole_words=False, regex=False):
        """替换当前选中的文本"""
        cursor = self.textCursor()
        
        if not cursor.hasSelection():
            return False
        
        selected_text = cursor.selectedText()
        
        # 检查选中的文本是否匹配查找条件
        if regex:
            import re
            pattern_flags = 0 if case_sensitive else re.IGNORECASE
            try:
                pattern = re.compile(find_text, pattern_flags)
                if pattern.fullmatch(selected_text):
                    cursor.insertText(replace_text)
                    return True
            except re.error:
                return False
        else:
            # 普通文本匹配
            if case_sensitive:
                matches = selected_text == find_text
            else:
                matches = selected_text.lower() == find_text.lower()
            
            if whole_words:
                # 检查是否为完整单词（简化实现）
                import re
                word_pattern = r'\b' + re.escape(find_text) + r'\b'
                pattern_flags = 0 if case_sensitive else re.IGNORECASE
                matches = bool(re.fullmatch(word_pattern, selected_text, pattern_flags))
            
            if matches:
                cursor.insertText(replace_text)
                return True
        
        return False
    
    def replace_all(self, find_text, replace_text, case_sensitive=False, whole_words=False, regex=False):
        """替换所有匹配的文本"""
        if not find_text:
            return 0
        
        count = 0
        doc_text = self.toPlainText()
        
        if regex:
            # 正则表达式替换
            import re
            pattern_flags = 0 if case_sensitive else re.IGNORECASE
            
            try:
                pattern = re.compile(find_text, pattern_flags)
                new_text, count = pattern.subn(replace_text, doc_text)
                
                if count > 0:
                    # 保存当前光标位置
                    cursor_pos = self.textCursor().position()
                    
                    # 替换整个文档内容
                    self.setPlainText(new_text)
                    
                    # 恢复光标位置（调整长度变化）
                    new_cursor = self.textCursor()
                    new_pos = min(cursor_pos, len(new_text))
                    new_cursor.setPosition(new_pos)
                    self.setTextCursor(new_cursor)
                
            except re.error as e:
                print(f"正则表达式错误: {e}")
                return 0
                
        else:
            # 普通文本替换
            search_text = find_text
            if not case_sensitive:
                doc_text_lower = doc_text.lower()
                search_text = find_text.lower()
            
            if whole_words:
                # 全词匹配替换
                import re
                word_pattern = r'\b' + re.escape(find_text) + r'\b'
                pattern_flags = 0 if case_sensitive else re.IGNORECASE
                
                new_text, count = re.subn(word_pattern, replace_text, doc_text, flags=pattern_flags)
                
                if count > 0:
                    self.setPlainText(new_text)
            else:
                # 简单文本替换
                if case_sensitive:
                    new_text = doc_text.replace(find_text, replace_text)
                    count = doc_text.count(find_text)
                else:
                    # 大小写不敏感替换（保持原始大小写）
                    import re
                    pattern = re.compile(re.escape(find_text), re.IGNORECASE)
                    matches = list(pattern.finditer(doc_text))
                    count = len(matches)
                    
                    if count > 0:
                        # 从后往前替换，避免位置偏移
                        new_text = doc_text
                        for match in reversed(matches):
                            start, end = match.span()
                            new_text = new_text[:start] + replace_text + new_text[end:]
                        
                        self.setPlainText(new_text)
        
        return count
    
    def _apply_theme_style(self):
        """应用主题样式"""
        # 获取主题管理器
        try:
            main_window = self.parent()
            search_depth = 0
            while main_window and not hasattr(main_window, 'theme_manager') and search_depth < 10:
                main_window = main_window.parent()
                search_depth += 1
            
            if main_window and hasattr(main_window, 'theme_manager'):
                theme = main_window.theme_manager.get_current_theme()
                colors = theme.get("colors", {})
                current_theme_name = main_window.theme_manager.current_theme
                
                # 应用编辑器样式
                style = f"""
                QPlainTextEdit {{
                    background-color: {colors.get('background', '#1e1e1e')};
                    color: {colors.get('foreground', '#d4d4d4')};
                    border: none;
                    selection-background-color: {colors.get('selection', '#264f78')};
                }}
                """
                self.setStyleSheet(style)
                
                # 更新行号区域样式
                if hasattr(self, 'line_number_area'):
                    self.line_number_area.update()
                
                print(f"编辑器应用主题成功: {current_theme_name}, 背景色: {colors.get('background', '#1e1e1e')}")
                return True
            else:
                print(f"未找到主题管理器，搜索深度: {search_depth}, main_window类型: {type(main_window)}")
        except Exception as e:
            print(f"编辑器应用主题失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 使用默认暗色样式
        print("应用默认暗色主题")
        self.setStyleSheet("""
        QPlainTextEdit {
            background-color: #1e1e1e;
            color: #d4d4d4;
            border: none;
            selection-background-color: #264f78;
        }
        """)
        return False
    
    def update_theme(self):
        """更新主题（供外部调用）"""
        self._apply_theme_style()
        self.highlight_current_line()
