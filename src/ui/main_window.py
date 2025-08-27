"""
主窗口 - Chango Editor

主要功能：
- 设置应用程序主窗口
- 创建菜单栏和工具栏
- 管理整体布局
- 处理窗口事件
"""

import sys,os,webbrowser
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QMenuBar, QToolBar, QStatusBar, QSplitter,
    QApplication, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QFont
from PyQt6.QtCore import QSize

from core.editor import TextEditor
from ui.tab_widget import TabWidget
from utils.themes import ThemeManager
from ui.file_explorer import FileExplorer


class MainWindow(QMainWindow):
    """主窗口类"""
    
    # 信号定义
    file_opened = pyqtSignal(str)
    file_saved = pyqtSignal(str)
    file_closed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chango Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化主题管理器
        self.theme_manager = ThemeManager()
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # 设置应用图标
        self._set_window_icon()
        
        # 初始化UI组件
        self._init_ui()
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()
        self._setup_connections()
        
        # 设置默认字体
        self._setup_fonts()
        
        # 应用主题
        self._apply_current_theme()
        
        # 最近打开的目录
        self.last_opened_directory = os.getcwd()
        
        print("Chango Editor 主窗口初始化完成")
    
    def _init_ui(self):
        """初始化用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局（水平分割器）
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建文件浏览器
        self.file_explorer = FileExplorer()
        main_splitter.addWidget(self.file_explorer)
        
        # 创建编辑区域（标签页管理器）
        self.tab_widget = TabWidget()
        main_splitter.addWidget(self.tab_widget)
        
        # 设置分割器比例（文件浏览器:编辑器 = 1:4）
        main_splitter.setSizes([200, 800])
        
        # 设置主布局
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(main_splitter)
        central_widget.setLayout(layout)
    
    def _create_menus(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        # 新建文件
        new_action = QAction("新建(&N)", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip("创建新文件")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # 打开文件
        open_action = QAction("打开(&O)", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("打开文件")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # 保存文件
        save_action = QAction("保存(&S)", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip("保存当前文件")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # 另存为
        save_as_action = QAction("另存为(&A)", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip("另存为新文件")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # 关闭当前文件
        close_current_action = QAction("关闭当前文件(&C)", self)
        close_current_action.setShortcut(QKeySequence("Ctrl+W"))
        close_current_action.setStatusTip("关闭当前文件")
        close_current_action.triggered.connect(self.close_current_file)
        file_menu.addAction(close_current_action)
        
        # 关闭所有文件
        close_all_action = QAction("关闭所有文件(&L)", self)
        close_all_action.setShortcut(QKeySequence("Ctrl+Shift+W"))
        close_all_action.setStatusTip("关闭所有文件")
        close_all_action.triggered.connect(self.close_all_files)
        file_menu.addAction(close_all_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("退出应用程序")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")
        
        # 撤销
        self.undo_action = QAction("撤销(&U)", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.setStatusTip("撤销上一个操作")
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        edit_menu.addAction(self.undo_action)
        
        # 重做
        self.redo_action = QAction("重做(&R)", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.setStatusTip("重做上一个操作")
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)
        
        edit_menu.addSeparator()
        
        # 剪切
        self.cut_action = QAction("剪切(&T)", self)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.setStatusTip("剪切选中文本")
        self.cut_action.triggered.connect(self.cut)
        self.cut_action.setEnabled(False)
        edit_menu.addAction(self.cut_action)
        
        # 复制
        self.copy_action = QAction("复制(&C)", self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.setStatusTip("复制选中文本")
        self.copy_action.triggered.connect(self.copy)
        self.copy_action.setEnabled(False)
        edit_menu.addAction(self.copy_action)
        
        # 粘贴
        self.paste_action = QAction("粘贴(&P)", self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.setStatusTip("粘贴剪贴板内容")
        self.paste_action.triggered.connect(self.paste)
        edit_menu.addAction(self.paste_action)
        
        # 查看菜单
        view_menu = menubar.addMenu("查看(&V)")
        
        # 显示/隐藏文件浏览器
        toggle_explorer_action = QAction("文件浏览器(&E)", self)
        toggle_explorer_action.setCheckable(True)
        toggle_explorer_action.setChecked(True)
        toggle_explorer_action.setStatusTip("显示/隐藏文件浏览器")
        toggle_explorer_action.triggered.connect(self._toggle_file_explorer)
        view_menu.addAction(toggle_explorer_action)
        
        # 独立的主题菜单
        theme_menu = menubar.addMenu("主题(&T)")
        
        # 添加主题切换选项
        theme_names = self.theme_manager.get_theme_names()
        self.theme_actions = {}
        from PyQt6.QtGui import QActionGroup
        self.theme_group = QActionGroup(self)
        
        for theme_name in theme_names:
            theme = self.theme_manager.get_theme(theme_name)
            action = QAction(theme.get('name', theme_name), self)
            action.setCheckable(True)
            action.setActionGroup(self.theme_group)
            action.triggered.connect(lambda checked, name=theme_name: self._change_theme(name))
            
            # 设置当前主题为选中状态
            if theme_name == self.theme_manager.current_theme:
                action.setChecked(True)
            
            theme_menu.addAction(action)
            self.theme_actions[theme_name] = action
        
        # 搜索菜单
        search_menu = menubar.addMenu("搜索(&S)")
        
        # 查找
        find_action = QAction("查找(&F)", self)
        find_action.setShortcut(QKeySequence.StandardKey.Find)
        find_action.setStatusTip("在当前文件中查找")
        find_action.triggered.connect(self.show_find_dialog)
        search_menu.addAction(find_action)
        
        # 替换
        replace_action = QAction("替换(&R)", self)
        replace_action.setShortcut(QKeySequence.StandardKey.Replace)
        replace_action.setStatusTip("查找并替换")
        replace_action.triggered.connect(self.show_replace_dialog)
        search_menu.addAction(replace_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        # 使用说明
        user_guide_action = QAction("使用说明(&U)", self)
        user_guide_action.setStatusTip("查看详细的使用指南")
        user_guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(user_guide_action)
        
        # 分隔符
        help_menu.addSeparator()
        
        # 关于
        about_action = QAction("关于 Chango Editor(&A)", self)
        about_action.setStatusTip("关于 Chango Editor")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("主工具栏")
        self.addToolBar(toolbar)
        
        # 设置图标大小
        toolbar.setIconSize(QIcon().actualSize(QSize(20, 20)))
        
        # 新建按钮
        new_btn = toolbar.addAction("📄")
        new_btn.setToolTip("新建 (Ctrl+N)")
        new_btn.setStatusTip("创建新文件")
        new_btn.triggered.connect(self.new_file)
        
        # 打开按钮
        open_btn = toolbar.addAction("📂")
        open_btn.setToolTip("打开 (Ctrl+O)")
        open_btn.setStatusTip("打开文件")
        open_btn.triggered.connect(self.open_file)
        
        # 保存按钮
        save_btn = toolbar.addAction("💾")
        save_btn.setToolTip("保存 (Ctrl+S)")
        save_btn.setStatusTip("保存当前文件")
        save_btn.triggered.connect(self.save_file)
        
        toolbar.addSeparator()
        
        # 关闭当前按钮
        close_current_btn = toolbar.addAction("❌")
        close_current_btn.setToolTip("关闭当前 (Ctrl+W)")
        close_current_btn.setStatusTip("关闭当前文件")
        close_current_btn.triggered.connect(self.close_current_file)
        
        # 关闭所有按钮
        close_all_btn = toolbar.addAction("🗂️")
        close_all_btn.setToolTip("关闭所有 (Ctrl+Shift+W)")
        close_all_btn.setStatusTip("关闭所有文件")
        close_all_btn.triggered.connect(self.close_all_files)
        
        toolbar.addSeparator()
        
        # 撤销按钮
        self.undo_btn = toolbar.addAction("↶")
        self.undo_btn.setToolTip("撤销 (Ctrl+Z)")
        self.undo_btn.setStatusTip("撤销上一个操作")
        self.undo_btn.triggered.connect(self.undo)
        self.undo_btn.setEnabled(False)
        
        # 重做按钮
        self.redo_btn = toolbar.addAction("↷")
        self.redo_btn.setToolTip("重做 (Ctrl+Y)")
        self.redo_btn.setStatusTip("重做上一个操作")
        self.redo_btn.triggered.connect(self.redo)
        self.redo_btn.setEnabled(False)
        
        toolbar.addSeparator()
        
        # 清除按钮
        clear_btn = toolbar.addAction("🗑️")
        clear_btn.setToolTip("清除 (Ctrl+Delete)")
        clear_btn.setStatusTip("清除当前编辑区所有内容")
        clear_btn.triggered.connect(self.clear_all)
        
        # 全选按钮
        select_all_btn = toolbar.addAction("🔘")
        select_all_btn.setToolTip("全选 (Ctrl+A)")
        select_all_btn.setStatusTip("选中当前编辑区所有内容")
        select_all_btn.triggered.connect(self.select_all)
        
        # 复制按钮
        self.copy_btn = toolbar.addAction("📋")
        self.copy_btn.setToolTip("复制 (Ctrl+C)")
        self.copy_btn.setStatusTip("复制选中的文本")
        self.copy_btn.triggered.connect(self.copy)
        self.copy_btn.setEnabled(False)
        
        # 粘贴按钮
        self.paste_btn = toolbar.addAction("📰")
        self.paste_btn.setToolTip("粘贴 (Ctrl+V)")
        self.paste_btn.setStatusTip("在当前光标处粘贴剪贴板内容")
        self.paste_btn.triggered.connect(self.paste)
        
        toolbar.addSeparator()
        
        # 查找按钮
        find_btn = toolbar.addAction("🔍")
        find_btn.setToolTip("查找 (Ctrl+F)")
        find_btn.setStatusTip("在当前文件中查找")
        find_btn.triggered.connect(self.show_find_dialog)
        
        # 替换按钮
        replace_btn = toolbar.addAction("🔄")
        replace_btn.setToolTip("替换 (Ctrl+H)")
        replace_btn.setStatusTip("查找并替换")
        replace_btn.triggered.connect(self.show_replace_dialog)
    
    def _create_statusbar(self):
        """创建状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # 显示就绪状态
        self.statusbar.showMessage("就绪", 2000)
        
        # 添加永久状态信息
        self.statusbar.addPermanentWidget(
            self.statusbar.__class__().addWidget(
                self.statusbar.__class__().addLabel("行: 1, 列: 1")
            ) if hasattr(self.statusbar, 'addLabel') else None
        )
    
    def _setup_connections(self):
        """设置信号连接"""
        # 文件浏览器信号连接
        self.file_explorer.file_selected.connect(self.open_file_from_path)
        
        # 标签页信号连接
        self.tab_widget.current_editor_changed.connect(self._on_editor_changed)
    
    def _setup_fonts(self):
        """设置字体"""
        # 设置默认编程字体
        font = QFont("Consolas", 11)
        if not font.exactMatch():
            font = QFont("Courier New", 11)
        font.setFixedPitch(True)
        QApplication.instance().setFont(font)
    
    def _set_window_icon(self):
        """设置窗口图标"""
        # 尝试多个可能的图标路径 - 按优先级排序 (PNG > ICO > SVG)
        base_paths = [
            # 开发环境路径
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            # PyInstaller打包后的临时目录路径
            getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
            # 打包后的路径（资源文件在同级目录）
            os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
        ]
        
        # 图标文件按优先级排序
        icon_names = [
            'chango_editor.png',  # 最佳兼容性
            'chango_editor.ico',  # Windows标准
            'chango_editor.svg'   # 矢量图，作为备用
        ]
        
        possible_paths = []
        for base_path in base_paths:
            for icon_name in icon_names:
                possible_paths.append(os.path.join(base_path, 'resources', 'icons', icon_name))
        
        icon_set = False
        for icon_path in possible_paths:
            if os.path.exists(icon_path):
                try:
                    icon = QIcon(icon_path)
                    if not icon.isNull():
                        self.setWindowIcon(icon)
                        print(f"设置应用图标: {icon_path}")
                        icon_set = True
                        break
                except Exception as e:
                    print(f"加载图标失败 {icon_path}: {e}")
                    continue
        
        if not icon_set:
            # 使用默认图标
            self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
            print("使用默认应用图标")
            print(f"尝试的图标路径:")
            for path in possible_paths:
                print(f"  - {path} (存在: {os.path.exists(path)})")
    
    def _apply_current_theme(self):
        """应用当前主题"""
        stylesheet = self.theme_manager.get_theme_stylesheet()
        self.setStyleSheet(stylesheet)
        
        # 同时设置应用程序级别的样式，影响所有对话框
        self._apply_global_theme()
        print(f"应用主题: {self.theme_manager.current_theme}")
    
    def _apply_global_theme(self):
        """应用全局主题样式到所有对话框"""
        theme = self.theme_manager.get_current_theme()
        colors = theme.get("colors", {})
        
        # 全局样式表，影响所有QMessageBox、QFileDialog等
        global_style = f"""
        QDialog {{
            background-color: {colors.get('background', '#2b2b2b')};
            color: {colors.get('foreground', '#ffffff')};
        }}
        QMessageBox {{
            background-color: {colors.get('background', '#2b2b2b')};
            color: {colors.get('foreground', '#ffffff')};
        }}
        QMessageBox QLabel {{
            color: {colors.get('foreground', '#ffffff')};
        }}
        QMessageBox QPushButton {{
            background-color: {colors.get('selection', '#0078d4')};
            color: #ffffff;
            border: none;
            padding: 6px 12px;
            border-radius: 3px;
            font-weight: bold;
            min-width: 80px;
        }}
        QMessageBox QPushButton:hover {{
            background-color: #106ebe;
        }}
        QMessageBox QPushButton:pressed {{
            background-color: #005a9e;
        }}
        QFileDialog {{
            background-color: {colors.get('background', '#2b2b2b')};
            color: {colors.get('foreground', '#ffffff')};
        }}
        QFileDialog QLabel {{
            color: {colors.get('foreground', '#ffffff')};
        }}
        QFileDialog QLineEdit {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            padding: 4px;
            border-radius: 3px;
        }}
        QFileDialog QPushButton {{
            background-color: {colors.get('selection', '#0078d4')};
            color: #ffffff;
            border: none;
            padding: 6px 12px;
            border-radius: 3px;
            font-weight: bold;
        }}
        QFileDialog QPushButton:hover {{
            background-color: #106ebe;
        }}
        QFileDialog QListView {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            outline: none;
        }}
        QFileDialog QListView::item:selected {{
            background-color: {colors.get('selection', '#0078d4')};
        }}
        QFileDialog QTreeView {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            outline: none;
        }}
        QFileDialog QTreeView::item:selected {{
            background-color: {colors.get('selection', '#0078d4')};
        }}
        QFileDialog QComboBox {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            padding: 4px;
            border-radius: 3px;
        }}
        """
        
        # 设置到应用程序，影响所有窗口和对话框
        QApplication.instance().setStyleSheet(global_style)
    
    def _change_theme(self, theme_name: str):
        """切换主题"""
        if self.theme_manager.set_theme(theme_name):
            self._apply_current_theme()
            # 通知所有子组件主题已改变
            self._on_theme_changed(theme_name)
    
    def _on_theme_changed(self, theme_name: str):
        """主题改变事件处理"""
        # 应用全局主题样式
        self._apply_global_theme()
        
        # 更新标签页组件样式
        if hasattr(self, 'tab_widget'):
            self.tab_widget._apply_tab_style()
            
            # 更新所有编辑器的主题
            for index, editor in self.tab_widget.editors.items():
                if editor and hasattr(editor, 'update_theme'):
                    editor.update_theme()
        
        # 更新文件浏览器样式
        if hasattr(self, 'file_explorer'):
            self.file_explorer._apply_style()
        
        print(f"主题已切换到: {theme_name}")
    
    def _toggle_file_explorer(self, checked):
        """切换文件浏览器显示状态"""
        self.file_explorer.setVisible(checked)
    
    def _on_editor_changed(self, editor):
        """编辑器切换时的处理"""
        if editor:
            # 更新状态栏
            self.statusbar.showMessage(f"当前文件: {editor.get_file_path() or '未命名'}")
            
            # 连接编辑器信号以更新菜单状态
            editor.textChanged.connect(self._update_edit_actions)
            editor.selectionChanged.connect(self._update_edit_actions)
            editor.undoAvailable.connect(self._update_undo_action)
            editor.redoAvailable.connect(self._update_redo_action)
            
            # 初始更新菜单状态
            self._update_edit_actions()
            self._update_undo_action(editor.document().isUndoAvailable())
            self._update_redo_action(editor.document().isRedoAvailable())
        else:
            self.statusbar.showMessage("就绪")
            # 禁用所有编辑动作
            self._disable_edit_actions()
    
    # 文件操作方法
    def new_file(self):
        """新建文件"""
        # 显示新建文件对话框
        from ui.new_file_dialog import NewFileDialog
        dialog = NewFileDialog(self)
        
        if dialog.exec() == dialog.DialogCode.Accepted:
            file_info = dialog.get_file_info()
            
            # 确定标签页显示名称
            display_name = None
            if file_info.get('filename'):
                display_name = file_info['filename']
            
            # 创建新标签页
            index = self.tab_widget.new_tab(
                content=file_info.get('content', ''),
                display_name=display_name
            )
            editor = self.tab_widget.get_current_editor()
            
            if editor and file_info:
                # 设置文件路径（如果指定了保存路径）
                if file_info['save_path']:
                    editor.set_file_path(file_info['save_path'])
                    # 保存文件
                    if editor.save():
                        self.statusbar.showMessage(f"创建文件: {file_info['save_path']}", 3000)
                        self.file_saved.emit(file_info['save_path'])
                        # 刷新文件浏览区
                        self._refresh_file_explorer_for_path(file_info['save_path'])
                    else:
                        self.statusbar.showMessage("创建文件失败", 3000)
                else:
                    # 只是创建了内存中的文件
                    self.statusbar.showMessage(f"创建新文件: {file_info['type']}", 2000)
                
                # 存储文件类型信息用于后续保存
                if file_info.get('type'):
                    editor.preferred_file_type = file_info['type']
                    editor.preferred_extension = file_info.get('extension', '')
        else:
            # 如果用户取消，创建一个空的文本文件
            self.tab_widget.new_tab()
            self.statusbar.showMessage("创建新文件", 2000)
    
    def open_file(self):
        """打开文件"""
        # 构建详细的文件过滤器
        filters = [
            "所有支持的文件 (*.py *.js *.ts *.html *.css *.cpp *.c *.h *.java *.cs *.php *.rb *.go *.rs *.sql *.json *.xml *.md *.txt)",
            "Python文件 (*.py *.pyw)",
            "JavaScript文件 (*.js *.jsx)",
            "TypeScript文件 (*.ts *.tsx)",
            "Web文件 (*.html *.htm *.css *.scss *.sass *.less)",
            "C/C++文件 (*.c *.cpp *.cxx *.cc *.h *.hpp *.hxx)",
            "Java文件 (*.java)",
            "C#文件 (*.cs)",
            "其他编程语言 (*.php *.rb *.go *.rs *.swift *.kt *.scala)",
            "脚本文件 (*.sh *.bash *.ps1 *.bat *.cmd)",
            "数据文件 (*.json *.xml *.yaml *.yml *.sql *.csv)",
            "文档文件 (*.md *.txt *.rst)",
            "所有文件 (*)"
        ]
        
        # 获取最近打开的目录
        last_dir = self._get_last_opened_directory()
        
        file_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "打开文件",
            last_dir,
            ";;".join(filters)
        )
        
        if file_path:
            self.open_file_from_path(file_path)
            # 保存最近打开的目录
            self._save_last_opened_directory(os.path.dirname(file_path))
    
    def open_file_from_path(self, file_path):
        """从路径打开文件"""
        if self.tab_widget.open_file(file_path):
            self.statusbar.showMessage(f"已打开: {file_path}", 3000)
            self.file_opened.emit(file_path)
        else:
            QMessageBox.warning(self, "错误", f"无法打开文件: {file_path}")
    
    def save_file(self):
        """保存文件"""
        current_editor = self.tab_widget.get_current_editor()
        if current_editor:
            # 检查是否是首次保存（没有文件路径）
            if not current_editor.get_file_path():
                # 首次保存，使用另存为对话框（会传递TAB名称）
                self.save_file_as()
            else:
                # 已有路径，直接保存
                if current_editor.save():
                    self.statusbar.showMessage("文件已保存", 2000)
                    self.file_saved.emit(current_editor.get_file_path())
                    # 刷新文件浏览区
                    self._refresh_file_explorer_for_path(current_editor.get_file_path())
                else:
                    QMessageBox.warning(self, "错误", "保存文件失败")
    
    def save_file_as(self):
        """另存为文件"""
        current_editor = self.tab_widget.get_current_editor()
        if current_editor:
            # 使用与打开文件相同的过滤器
            filters = [
                "所有支持的文件 (*.py *.js *.ts *.html *.css *.cpp *.c *.h *.java *.cs *.php *.rb *.go *.rs *.sql *.json *.xml *.md *.txt)",
                "Python文件 (*.py *.pyw)",
                "JavaScript文件 (*.js *.jsx)",
                "TypeScript文件 (*.ts *.tsx)",
                "Web文件 (*.html *.htm *.css *.scss *.sass *.less)",
                "C/C++文件 (*.c *.cpp *.cxx *.cc *.h *.hpp *.hxx)",
                "Java文件 (*.java)",
                "C#文件 (*.cs)",
                "其他编程语言 (*.php *.rb *.go *.rs *.swift *.kt *.scala)",
                "脚本文件 (*.sh *.bash *.ps1 *.bat *.cmd)",
                "数据文件 (*.json *.xml *.yaml *.yml *.sql *.csv)",
                "文档文件 (*.md *.txt *.rst)",
                "所有文件 (*)"
            ]
            
            # 获取当前文件路径作为默认位置
            current_path = current_editor.get_file_path()
            if current_path:
                default_path = current_path
            else:
                # 获取当前TAB页面的显示名称
                current_index = self.tab_widget.currentIndex()
                tab_name = self.tab_widget.tabText(current_index)
                
                # 如果TAB名称不是默认的"未命名-X"格式，使用TAB名称作为默认文件名
                if not tab_name.startswith("未命名-"):
                    # 确保文件名有合适的扩展名
                    if not os.path.splitext(tab_name)[1]:
                        # 检查是否有记住的文件扩展名
                        if hasattr(current_editor, 'preferred_extension') and current_editor.preferred_extension:
                            tab_name += current_editor.preferred_extension
                        else:
                            tab_name += ".txt"
                    default_path = os.path.join(self._get_last_opened_directory(), tab_name)
                else:
                    # 对于未命名文件，检查是否有记住的扩展名
                    if hasattr(current_editor, 'preferred_extension') and current_editor.preferred_extension:
                        default_filename = f"未命名{current_editor.preferred_extension}"
                    else:
                        default_filename = "未命名.txt"
                    default_path = os.path.join(self._get_last_opened_directory(), default_filename)
            
            # 构建对话框标题
            current_index = self.tab_widget.currentIndex()
            tab_name = self.tab_widget.tabText(current_index)
            if current_path:
                dialog_title = "另存为"
            else:
                if not tab_name.startswith("未命名-"):
                    dialog_title = f"保存文件: {tab_name}"
                else:
                    dialog_title = "保存文件"
            
            file_path, selected_filter = QFileDialog.getSaveFileName(
                self,
                dialog_title,
                default_path,
                ";;".join(filters)
            )
            
            if file_path:
                if current_editor.save_as(file_path):
                    self.statusbar.showMessage(f"文件已保存为: {file_path}", 3000)
                    self.file_saved.emit(file_path)
                    # 保存最近打开的目录
                    self._save_last_opened_directory(os.path.dirname(file_path))
                    # 刷新文件浏览区
                    self._refresh_file_explorer_for_path(file_path)
                else:
                    QMessageBox.warning(self, "错误", "保存文件失败")
    
    def _refresh_file_explorer_for_path(self, file_path):
        """为指定文件路径刷新文件浏览区"""
        try:
            if file_path and os.path.exists(file_path):
                # 获取文件所在目录
                file_dir = os.path.dirname(file_path)
                
                # 如果文件浏览区显示的是该目录或父目录，则刷新
                if hasattr(self, 'file_explorer') and self.file_explorer:
                    current_root = self.file_explorer.root_path
                    
                    # 检查是否在当前显示的目录中
                    if file_dir.startswith(current_root):
                        self.file_explorer.refresh()
                        print(f"文件浏览区已刷新: {file_path}")
                    else:
                        # 如果不在当前目录，可以选择切换到文件所在目录
                        # 这里保持当前行为，只在当前目录下刷新
                        print(f"文件在当前浏览目录外，未刷新浏览区: {file_path}")
        except Exception as e:
            print(f"刷新文件浏览区时出错: {e}")

    def show_user_guide(self):
        """显示使用指南"""
        try:
            # 获取用户指南文件的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            guide_path = os.path.join(project_root, "docs", "user_guide.html")
            
            if os.path.exists(guide_path):
                # 在默认浏览器中打开用户指南
                webbrowser.open(f"file:///{guide_path.replace(os.sep, '/')}")
                self.statusbar.showMessage("已在浏览器中打开使用指南", 3000)
            else:
                QMessageBox.warning(
                    self,
                    "文件未找到",
                    f"无法找到使用指南文件：\n{guide_path}\n\n请确保docs/user_guide.html文件存在。"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "错误",
                f"打开使用指南时出错：\n{str(e)}"
            )

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            "关于 Chango Editor",
            "<h3>Chango Editor v1.2.0 🚀</h3>"
            "<p>一个强大的类似于 Sublime Text 的代码编辑器，基于 Python 和 PyQt6 构建</p>"
            "<p><b>🎯 v1.2.0 最新功能：</b></p>"
            "<ul>"
            "<li>🎨 工具栏全面图标化 - 直观的图标界面设计</li>"
            "<li>📁 文件浏览器增强 - 展开/收起全部功能</li>"
            "<li>💡 智能工具提示 - 显示功能名称和快捷键</li>"
            "<li>🌍 界面国际化 - 现代化专业设计</li>"
            "<li>📖 详细使用指南 - 帮助菜单新增使用说明</li>"
            "</ul>"
            "<p><b>✨ 核心特性：</b></p>"
            "<ul>"
            "<li>🎨 智能主题系统 - 深色/明亮主题无缝切换</li>"
            "<li>📝 强大编辑功能 - 支持20+语言语法高亮</li>"
            "<li>🔍 高级搜索替换 - 正则表达式支持</li>"
            "<li>📁 树形文件浏览器 - 支持展开/折叠和拖拽</li>"
            "<li>⚡ 快捷操作工具栏 - 完整的快捷键支持</li>"
            "</ul>"
            "<p><b>🎮 快捷键参考：</b></p>"
            "<p>Ctrl+N 新建 | Ctrl+O 打开 | Ctrl+S 保存 | Ctrl+F 查找 | Ctrl+H 替换</p>"
            "<p><b>更新时间：</b>2025年8月27日</p>"
            "<p>© 2025 Chango Team | MIT License</p>"
        )
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 检查是否有未保存的文件
        if self.tab_widget.has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                "确认退出",
                "有未保存的更改，确定要退出吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        # 保存窗口状态
        # TODO: 实现设置保存
        
        event.accept()
        print("PyEditor Lite 已退出")
    
    def _get_last_opened_directory(self):
        """获取最近打开的目录"""
        return self.last_opened_directory if os.path.exists(self.last_opened_directory) else os.getcwd()
    
    def _save_last_opened_directory(self, directory):
        """保存最近打开的目录"""
        if os.path.exists(directory):
            self.last_opened_directory = directory
    
    # 编辑操作方法
    def undo(self):
        """撤销操作"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            editor.undo()
            self.statusbar.showMessage("已撤销", 1000)
    
    def redo(self):
        """重做操作"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            editor.redo()
            self.statusbar.showMessage("已重做", 1000)
    
    def cut(self):
        """剪切操作"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            editor.cut()
            self.statusbar.showMessage("已剪切", 1000)
    
    def copy(self):
        """复制操作"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            editor.copy()
            self.statusbar.showMessage("已复制", 1000)
    
    def paste(self):
        """粘贴操作"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            editor.paste()
            self.statusbar.showMessage("已粘贴", 1000)
    
    def select_all(self):
        """全选操作"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            editor.selectAll()
            self.statusbar.showMessage("已全选", 1000)
    
    def clear_all(self):
        """清除所有内容（可撤销）"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            # 选中所有文本并删除，这样可以被撤销
            editor.selectAll()
            editor.insertPlainText("")
            self.statusbar.showMessage("已清除所有内容", 1000)
    
    def close_current_file(self):
        """关闭当前文件"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.tab_widget.close_tab(current_index)
            self.statusbar.showMessage("已关闭当前文件", 1000)
        else:
            QMessageBox.information(self, "提示", "没有打开的文件")
    
    def close_all_files(self):
        """关闭所有文件"""
        if self.tab_widget.count() == 0:
            QMessageBox.information(self, "提示", "没有打开的文件")
            return
        
        # 检查是否有未保存的文件
        if self.tab_widget.has_unsaved_changes():
            reply = QMessageBox.question(
                self, "确认关闭", 
                "有文件未保存，确定要关闭所有文件吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # 关闭所有标签页
        count = self.tab_widget.count()
        for i in range(count - 1, -1, -1):  # 从后往前关闭，避免索引变化
            self.tab_widget.close_tab(i)
        
        self.statusbar.showMessage(f"已关闭所有文件 ({count} 个)", 2000)
    
    def show_find_dialog(self):
        """显示查找对话框"""
        editor = self.tab_widget.get_current_editor()
        if not editor:
            QMessageBox.information(self, "提示", "没有打开的文件")
            return
        
        # 检查是否已经有搜索对话框打开
        if hasattr(self, 'search_dialog') and self.search_dialog.isVisible():
            # 切换到查找标签页
            self.search_dialog.tab_widget.setCurrentIndex(0)
            self.search_dialog.show_and_focus()
            return
        
        from ui.search_dialog import SearchDialog
        self.search_dialog = SearchDialog(editor, start_mode="find")
        self.search_dialog.show_and_focus()
    
    def show_replace_dialog(self):
        """显示替换对话框"""
        editor = self.tab_widget.get_current_editor()
        if not editor:
            QMessageBox.information(self, "提示", "没有打开的文件")
            return
        
        # 检查是否已经有搜索对话框打开
        if hasattr(self, 'search_dialog') and self.search_dialog.isVisible():
            # 切换到替换标签页
            self.search_dialog.tab_widget.setCurrentIndex(1)
            self.search_dialog.show_and_focus()
            return
        
        from ui.search_dialog import SearchDialog
        self.search_dialog = SearchDialog(editor, start_mode="replace")
        self.search_dialog.show_and_focus()
    
    def _update_edit_actions(self):
        """更新编辑动作状态"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            # 检查是否有选中文本
            has_selection = editor.textCursor().hasSelection()
            self.cut_action.setEnabled(has_selection)
            self.copy_action.setEnabled(has_selection)
            self.copy_btn.setEnabled(has_selection)
            
            # 检查剪贴板是否有内容（PyQt6中clipboard.text()返回str）
            clipboard = QApplication.clipboard()
            clipboard_text = clipboard.text()
            has_clipboard_content = bool(clipboard_text and clipboard_text.strip())
            self.paste_action.setEnabled(has_clipboard_content)
            self.paste_btn.setEnabled(has_clipboard_content)
        else:
            self._disable_edit_actions()
    
    def _update_undo_action(self, available):
        """更新撤销动作状态"""
        self.undo_action.setEnabled(available)
        self.undo_btn.setEnabled(available)
    
    def _update_redo_action(self, available):
        """更新重做动作状态"""
        self.redo_action.setEnabled(available)
        self.redo_btn.setEnabled(available)
    
    def _disable_edit_actions(self):
        """禁用所有编辑动作"""
        self.undo_action.setEnabled(False)
        self.redo_action.setEnabled(False)
        self.cut_action.setEnabled(False)
        self.copy_action.setEnabled(False)
        self.paste_action.setEnabled(False)
        
        self.undo_btn.setEnabled(False)
        self.redo_btn.setEnabled(False)
        self.copy_btn.setEnabled(False)
        self.paste_btn.setEnabled(False)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("PyEditor Lite")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("PyEditor Team")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
