"""
文件浏览器 - Chango Editor

树形结构实现，支持文件夹展开/折叠
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QMenu, QMessageBox, QInputDialog, QLineEdit, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QFont


class FileExplorer(QWidget):
    """文件浏览器组件（树形结构）"""
    
    # 信号定义
    file_selected = pyqtSignal(str)          # 文件被选中（双击）
    folder_selected = pyqtSignal(str)        # 文件夹被选中
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置最小宽度
        self.setMinimumWidth(200)
        
        # 当前根目录
        self.root_path = os.getcwd()
        
        # 初始化UI
        self._init_ui()
        
        # 刷新文件树
        self.refresh()
        
        print("文件浏览器初始化完成")
    
    def _init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 当前路径标签
        self.path_label = QLabel()
        self.path_label.setWordWrap(True)
        self.path_label.setMaximumHeight(60)  # 增加高度支持换行
        self.path_label.setMinimumHeight(20)  # 设置最小高度
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # 支持鼠标选择
        layout.addWidget(self.path_label)
        
        # 按钮容器
        button_layout = QHBoxLayout()
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        button_layout.setContentsMargins(0, 0, 0, 0)  # 去除边距
        button_layout.setSpacing(5)  # 按钮间距
        
        # 上级目录按钮
        self.up_button = QPushButton("⬆️")
        self.up_button.setMaximumHeight(25)
        self.up_button.setMaximumWidth(30)
        self.up_button.setToolTip("上级目录")
        self.up_button.clicked.connect(self.go_up)
        button_layout.addWidget(self.up_button)
        
        # 刷新按钮
        self.refresh_button = QPushButton("🔄")
        self.refresh_button.setMaximumHeight(25)
        self.refresh_button.setMaximumWidth(30)
        self.refresh_button.setToolTip("刷新文件列表")
        self.refresh_button.clicked.connect(self.refresh)
        button_layout.addWidget(self.refresh_button)
        
        # 添加一个小的空隙
        button_layout.addSpacing(10)
        
        # 展开全部按钮
        self.expand_all_button = QPushButton("⬇️")
        self.expand_all_button.setMaximumHeight(25)
        self.expand_all_button.setMaximumWidth(30)
        self.expand_all_button.setToolTip("展开全部文件夹")
        self.expand_all_button.clicked.connect(self.expand_all)
        button_layout.addWidget(self.expand_all_button)
        
        # 收起全部按钮
        self.collapse_all_button = QPushButton("⬆️")
        self.collapse_all_button.setMaximumHeight(25)
        self.collapse_all_button.setMaximumWidth(30)
        self.collapse_all_button.setToolTip("收起全部文件夹")
        self.collapse_all_button.clicked.connect(self.collapse_all)
        button_layout.addWidget(self.collapse_all_button)
        
        button_layout.addStretch()  # 添加弹性空间，让按钮靠左
        layout.addWidget(button_widget)
        
        # 文件树
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel("文件/文件夹")
        
        # 优化布局设置
        self.file_tree.setIndentation(12)  # 减少缩进，默认是20
        self.file_tree.setRootIsDecorated(True)  # 显示根装饰
        self.file_tree.setItemsExpandable(True)
        self.file_tree.setExpandsOnDoubleClick(False)  # 禁用双击展开，用我们自定义的逻辑
        
        # 隐藏标题栏以节省空间
        self.file_tree.setHeaderHidden(True)
        
        self.file_tree.itemClicked.connect(self._on_item_clicked)
        self.file_tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.file_tree.itemExpanded.connect(self._on_item_expanded)
        self.file_tree.itemCollapsed.connect(self._on_item_collapsed)
        layout.addWidget(self.file_tree)
        
        # 设置右键菜单
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self._show_context_menu)
        
        # 添加到布局
        self.setLayout(layout)
        
        # 应用样式
        self._apply_style()
    
    def _apply_style(self):
        """应用样式"""
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
                QTreeWidget {{
                    background-color: {colors.get('background', '#2b2b2b')};
                    color: {colors.get('foreground', '#ffffff')};
                    border: none;
                    outline: none;
                    alternate-background-color: {colors.get('line_highlight', '#2a2a2a')};
                }}
                QTreeWidget::item {{
                    height: 22px;
                    padding: 2px;
                    border: none;
                }}
                QTreeWidget::item:hover {{
                    background-color: {colors.get('selection', '#404040')};
                }}
                QTreeWidget::item:selected {{
                    background-color: {colors.get('selection', '#0078d4')};
                }}
                QTreeWidget::branch:closed:has-children {{
                    image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFeSURBVCiRpZM9SwNBEIafgwQSCxsLwcJaG1sLG0uxsLGwsLCwsLBQsLGwsLCwsLGwsLCwsLCwsLGwsLCwsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLBQsLGwsLCwsLGwsLBQsLBQsLGwsLBQsLBQsLBQsLGwsLGwsLBQsLGwsLGwsLBQsLGwsLGwsLGwsLBQsLGwsLGwsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQ==);
                }}
                QTreeWidget::branch:open:has-children {{
                    image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFhSURBVCiRpZM9SwNBEIafgwQSCxsLwcJaG1sLG0uxsLGwsLCwsLBQsLGwsLCwsLGwsLCwsLCwsLGwsLCwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLCwsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLBQsLGwsLCwsLBQsLGwsLCwsLBQsLGwsLBQsLGwsLCwsLGwsLBQsLBQsLGwsLBQsLBQsLBQsLGwsLGwsLBQsLGwsLGwsLBQsLGwsLGwsLGwsLBQsLGwsLGwsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQsLBQ==);
                }}
                QHeaderView::section {{
                    background-color: {colors.get('menu_background', '#3c3c3c')};
                    color: {colors.get('menu_foreground', '#ffffff')};
                    border: none;
                    padding: 4px;
                    font-weight: bold;
                }}
                QLabel {{
                    background-color: {colors.get('menu_background', '#3c3c3c')};
                    color: {colors.get('menu_foreground', '#ffffff')};
                    padding: 5px;
                    border: 1px solid #555555;
                }}
                QPushButton {{
                    background-color: {colors.get('menu_background', '#3c3c3c')};
                    color: {colors.get('menu_foreground', '#ffffff')};
                    border: 1px solid #555555;
                    padding: 3px;
                }}
                QPushButton:hover {{
                    background-color: {colors.get('selection', '#4a4a4a')};
                }}
                """
                self.setStyleSheet(style)
                return
        except Exception as e:
            print(f"应用主题样式失败: {e}")
        
        # 回退到默认暗色主题
        style = """
        QTreeWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            border: none;
            outline: none;
            alternate-background-color: #2a2a2a;
        }
        QTreeWidget::item {
            height: 22px;
            padding: 2px;
            border: none;
        }
        QTreeWidget::item:hover {
            background-color: #404040;
        }
        QTreeWidget::item:selected {
            background-color: #0078d4;
        }
        QTreeWidget::branch:closed:has-children {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgMkw4IDZMNCA5IiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMSIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4=);
        }
        QTreeWidget::branch:open:has-children {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIgNEw2IDhMOSA0IiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMSIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4=);
        }
        QHeaderView::section {
            background-color: #3c3c3c;
            color: #ffffff;
            border: none;
            padding: 4px;
            font-weight: bold;
        }
        QLabel {
            background-color: #3c3c3c;
            color: #ffffff;
            padding: 5px;
            border: 1px solid #555555;
        }
        QPushButton {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px;
        }
        QPushButton:hover {
            background-color: #4a4a4a;
        }
        """
        self.setStyleSheet(style)
    
    def set_root_path(self, path):
        """设置根路径"""
        if os.path.exists(path) and os.path.isdir(path):
            self.root_path = path
            self.refresh()
            print(f"设置根路径: {path}")
        else:
            print(f"路径不存在: {path}")
    
    def get_root_path(self):
        """获取根路径"""
        return self.root_path
    
    def refresh(self):
        """刷新文件树"""
        self.file_tree.clear()
        
        # 更新路径标签
        # 为长路径设置省略显示和工具提示
        display_path = self.root_path
        if len(self.root_path) > 50:
            # 如果路径太长，显示开头...结尾的形式
            display_path = f"{self.root_path[:20]}...{self.root_path[-27:]}"
        
        self.path_label.setText(display_path)
        self.path_label.setToolTip(f"当前路径: {self.root_path}")  # 悬浮显示完整路径
        
        try:
            # 创建根节点
            root_item = QTreeWidgetItem([os.path.basename(self.root_path) or self.root_path])
            root_item.setData(0, Qt.ItemDataRole.UserRole, self.root_path)
            self.file_tree.addTopLevelItem(root_item)
            
            # 加载根目录内容
            self._load_directory_content(root_item, self.root_path)
            
            # 默认展开根节点
            root_item.setExpanded(True)
                    
        except PermissionError:
            error_item = QTreeWidgetItem(["❌ 无法访问此目录"])
            self.file_tree.addTopLevelItem(error_item)
        except Exception as e:
            error_item = QTreeWidgetItem([f"❌ 错误: {e}"])
            self.file_tree.addTopLevelItem(error_item)
    
    def _load_directory_content(self, parent_item, dir_path):
        """加载目录内容到树节点"""
        try:
            items = os.listdir(dir_path)
            items.sort()
            
            # 分别收集文件夹和文件
            folders = []
            files = []
            
            for item in items:
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    folders.append((item, item_path))
                elif os.path.isfile(item_path):
                    files.append((item, item_path))
            
            # 先添加文件夹
            for item_name, item_path in folders:
                folder_item = QTreeWidgetItem([f"📁 {item_name}"])
                folder_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                parent_item.addChild(folder_item)
                
                # 为文件夹添加一个占位符子项，使其可展开
                placeholder = QTreeWidgetItem(["加载中..."])
                folder_item.addChild(placeholder)
            
            # 再添加文件
            for item_name, item_path in files:
                # 根据文件扩展名显示不同图标
                ext = os.path.splitext(item_name)[1].lower()
                if ext in ['.py', '.pyw']:
                    icon = '🐍'
                elif ext in ['.js', '.jsx']:
                    icon = '📜'
                elif ext in ['.ts', '.tsx']:
                    icon = '🔷'
                elif ext in ['.html', '.htm']:
                    icon = '🌐'
                elif ext in ['.css', '.scss', '.sass', '.less']:
                    icon = '🎨'
                elif ext in ['.txt', '.md', '.rst']:
                    icon = '📄'
                elif ext in ['.json', '.xml', '.yaml', '.yml']:
                    icon = '📋'
                elif ext in ['.cpp', '.c', '.h', '.hpp']:
                    icon = '⚙️'
                elif ext in ['.java']:
                    icon = '☕'
                elif ext in ['.cs']:
                    icon = '🔷'
                elif ext in ['.php']:
                    icon = '🐘'
                elif ext in ['.rb']:
                    icon = '💎'
                elif ext in ['.go']:
                    icon = '🐹'
                elif ext in ['.rs']:
                    icon = '🦀'
                else:
                    icon = '📄'
                
                file_item = QTreeWidgetItem([f"{icon} {item_name}"])
                file_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                parent_item.addChild(file_item)
        
        except PermissionError:
            error_item = QTreeWidgetItem(["❌ 无法访问"])
            parent_item.addChild(error_item)
        except Exception as e:
            error_item = QTreeWidgetItem([f"❌ 错误: {e}"])
            parent_item.addChild(error_item)
    
    def go_up(self):
        """返回上级目录"""
        parent_path = os.path.dirname(self.root_path)
        if parent_path != self.root_path:  # 不是根目录
            self.set_root_path(parent_path)
    
    def _on_item_clicked(self, item):
        """处理项目单击事件"""
        item_path = item.data(0, Qt.ItemDataRole.UserRole)
        
        if not item_path:
            return
        
        if os.path.isdir(item_path):
            # 文件夹单击：切换展开/折叠状态，不改变工作目录
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
            print(f"单击切换文件夹展开状态: {item_path}")
    
    def _on_item_double_clicked(self, item):
        """处理项目双击事件"""
        item_path = item.data(0, Qt.ItemDataRole.UserRole)
        
        if not item_path:
            return
        
        if os.path.isdir(item_path):
            # 文件夹双击：进入该文件夹，改变工作目录
            self.set_root_path(item_path)
            self.folder_selected.emit(item_path)
            print(f"双击进入文件夹: {item_path}")
        else:
            # 文件：发射选中信号
            self.file_selected.emit(item_path)
            print(f"双击打开文件: {item_path}")
    
    def _on_item_expanded(self, item):
        """处理项目展开事件"""
        item_path = item.data(0, Qt.ItemDataRole.UserRole)
        
        if not item_path or not os.path.isdir(item_path):
            return
        
        # 移除占位符并加载实际内容
        if item.childCount() == 1:
            first_child = item.child(0)
            if first_child.text(0) == "加载中...":
                item.removeChild(first_child)
                self._load_directory_content(item, item_path)
                print(f"展开文件夹: {item_path}")
    
    def _on_item_collapsed(self, item):
        """处理项目折叠事件"""
        item_path = item.data(0, Qt.ItemDataRole.UserRole)
        print(f"折叠文件夹: {item_path}")
    
    def _show_context_menu(self, position):
        """显示右键菜单"""
        item = self.file_tree.itemAt(position)
        
        menu = QMenu(self)
        
        if item:
            item_path = item.data(0, Qt.ItemDataRole.UserRole)
            
            if item_path and os.path.exists(item_path):
                is_dir = os.path.isdir(item_path)
                
                if is_dir:
                    # 文件夹菜单
                    set_root_action = QAction("设为根目录", self)
                    set_root_action.triggered.connect(lambda: self.set_root_path(item_path))
                    menu.addAction(set_root_action)
                    
                    # 展开/折叠
                    if item.isExpanded():
                        collapse_action = QAction("折叠", self)
                        collapse_action.triggered.connect(lambda: item.setExpanded(False))
                        menu.addAction(collapse_action)
                    else:
                        expand_action = QAction("展开", self)
                        expand_action.triggered.connect(lambda: item.setExpanded(True))
                        menu.addAction(expand_action)
                else:
                    # 文件菜单
                    open_action = QAction("打开文件", self)
                    open_action.triggered.connect(lambda: self.file_selected.emit(item_path))
                    menu.addAction(open_action)
        
        # 通用菜单
        menu.addSeparator()
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh)
        menu.addAction(refresh_action)
        
        # 显示菜单
        menu.exec(self.file_tree.mapToGlobal(position))
    
    def get_selected_path(self):
        """获取当前选中的路径"""
        current_item = self.file_tree.currentItem()
        if current_item:
            return current_item.data(0, Qt.ItemDataRole.UserRole)
        return None
    
    def expand_all(self):
        """展开所有文件夹"""
        self.file_tree.expandAll()
        print("已展开所有文件夹")
    
    def collapse_all(self):
        """收起所有文件夹"""
        self.file_tree.collapseAll()
        print("已收起所有文件夹")