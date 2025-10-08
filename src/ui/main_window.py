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
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QFont

from core.editor import TextEditor
from ui.tab_widget import TabWidget
from utils.themes import ThemeManager
from ui.file_explorer import FileExplorer
from utils.icon_provider import Icons, IconProvider
from src.core.i18n import tr, get_i18n_manager
from src.ui.language_selector import LanguageMenu


class MainWindow(QMainWindow):
    """主窗口类"""
    
    # 信号定义
    file_opened = pyqtSignal(str)
    file_saved = pyqtSignal(str)
    file_closed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # 初始化国际化（在所有UI创建之前）
        self.i18n = get_i18n_manager()
        self.i18n.language_changed.connect(self._on_language_changed)
        
        self.setWindowTitle(tr("app.title"))
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化主题管理器
        self.theme_manager = ThemeManager()
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # 设置应用图标
        self._set_window_icon()
        
        # 初始化图标系统
        self._init_icons()
        
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
        
        print(f"Chango Editor 主窗口初始化完成 - 语言: {self.i18n.get_current_locale_name()}")
    
    def _init_icons(self):
        """初始化图标系统"""
        # 获取当前主题
        theme = self.theme_manager.get_current_theme()
        colors = theme.get("colors", {})
        
        # 根据主题选择图标颜色
        icon_color = colors.get('foreground', '#ffffff')
        
        # 初始化图标集合（尺寸18x18）
        Icons.init_icons(color=icon_color, size=18)
        
        print(f"图标系统已初始化 - 颜色: {icon_color}, 尺寸: 18x18")
    
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
        file_menu = menubar.addMenu(tr("menu.file.title"))
        
        # 新建文件
        new_action = QAction(tr("menu.file.new.text"), self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip(tr("menu.file.new.tip"))
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # 打开文件
        open_action = QAction(tr("menu.file.open.text"), self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip(tr("menu.file.open.tip"))
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # 打开文件夹
        open_folder_action = QAction(tr("menu.file.open_folder.text"), self)
        open_folder_action.setShortcut(QKeySequence("Ctrl+Shift+O"))
        open_folder_action.setStatusTip(tr("menu.file.open_folder.tip"))
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        # 保存文件
        save_action = QAction(tr("menu.file.save.text"), self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip(tr("menu.file.save.tip"))
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # 另存为
        save_as_action = QAction(tr("menu.file.save_as.text"), self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip(tr("menu.file.save_as.tip"))
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # 关闭当前文件
        close_current_action = QAction(tr("menu.file.close_current.text"), self)
        close_current_action.setShortcut(QKeySequence("Ctrl+W"))
        close_current_action.setStatusTip(tr("menu.file.close_current.tip"))
        close_current_action.triggered.connect(self.close_current_file)
        file_menu.addAction(close_current_action)
        
        # 关闭所有文件
        close_all_action = QAction(tr("menu.file.close_all.text"), self)
        close_all_action.setShortcut(QKeySequence("Ctrl+Shift+W"))
        close_all_action.setStatusTip(tr("menu.file.close_all.tip"))
        close_all_action.triggered.connect(self.close_all_files)
        file_menu.addAction(close_all_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction(tr("menu.file.exit.text"), self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip(tr("menu.file.exit.tip"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu(tr("menu.edit.title"))
        
        # 撤销
        self.undo_action = QAction(tr("menu.edit.undo.text"), self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.setStatusTip(tr("menu.edit.undo.tip"))
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        edit_menu.addAction(self.undo_action)
        
        # 重做
        self.redo_action = QAction(tr("menu.edit.redo.text"), self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.setStatusTip(tr("menu.edit.redo.tip"))
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)
        
        edit_menu.addSeparator()
        
        # 剪切
        self.cut_action = QAction(tr("menu.edit.cut.text"), self)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.setStatusTip(tr("menu.edit.cut.tip"))
        self.cut_action.triggered.connect(self.cut)
        self.cut_action.setEnabled(False)
        edit_menu.addAction(self.cut_action)
        
        # 复制
        self.copy_action = QAction(tr("menu.edit.copy.text"), self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.setStatusTip(tr("menu.edit.copy.tip"))
        self.copy_action.triggered.connect(self.copy)
        self.copy_action.setEnabled(False)
        edit_menu.addAction(self.copy_action)
        
        # 粘贴
        self.paste_action = QAction(tr("menu.edit.paste.text"), self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.setStatusTip(tr("menu.edit.paste.tip"))
        self.paste_action.triggered.connect(self.paste)
        edit_menu.addAction(self.paste_action)
        
        # 查看菜单
        view_menu = menubar.addMenu(tr("menu.view.title"))
        
        # 显示/隐藏文件浏览器
        toggle_explorer_action = QAction(tr("menu.view.file_explorer.text"), self)
        toggle_explorer_action.setCheckable(True)
        toggle_explorer_action.setChecked(True)
        toggle_explorer_action.setStatusTip(tr("menu.view.file_explorer.tip"))
        toggle_explorer_action.triggered.connect(self._toggle_file_explorer)
        view_menu.addAction(toggle_explorer_action)
        
        # 独立的主题菜单
        theme_menu = menubar.addMenu(tr("menu.theme.title"))
        
        # 添加主题切换选项
        theme_names = self.theme_manager.get_theme_names()
        self.theme_actions = {}
        from PyQt6.QtGui import QActionGroup
        self.theme_group = QActionGroup(self)
        
        for theme_name in theme_names:
            theme = self.theme_manager.get_theme(theme_name)
            # 使用翻译键获取主题名称，如果没有翻译则使用原始名称
            theme_display_name = tr(f"menu.theme.{theme_name}")
            if theme_display_name == f"menu.theme.{theme_name}":
                # 如果翻译键不存在，使用主题文件中的名称
                theme_display_name = theme.get('name', theme_name)
            
            action = QAction(theme_display_name, self)
            action.setCheckable(True)
            action.setActionGroup(self.theme_group)
            action.triggered.connect(lambda checked, name=theme_name: self._change_theme(name))
            
            # 设置当前主题为选中状态
            if theme_name == self.theme_manager.current_theme:
                action.setChecked(True)
            
            theme_menu.addAction(action)
            self.theme_actions[theme_name] = action
        
        # 搜索菜单
        search_menu = menubar.addMenu(tr("menu.search.title"))
        
        # 查找
        find_action = QAction(tr("menu.search.find.text"), self)
        find_action.setShortcut(QKeySequence.StandardKey.Find)
        find_action.setStatusTip(tr("menu.search.find.tip"))
        find_action.triggered.connect(self.show_find_dialog)
        search_menu.addAction(find_action)
        
        # 替换
        replace_action = QAction(tr("menu.search.replace.text"), self)
        replace_action.setShortcut(QKeySequence.StandardKey.Replace)
        replace_action.setStatusTip(tr("menu.search.replace.tip"))
        replace_action.triggered.connect(self.show_replace_dialog)
        search_menu.addAction(replace_action)
        
        # ===== 语言菜单 (新增) =====
        self.language_menu = LanguageMenu(self)
        menubar.addMenu(self.language_menu)
        
        # 帮助菜单
        help_menu = menubar.addMenu(tr("menu.help.title"))
        
        # 使用说明
        user_guide_action = QAction(tr("menu.help.user_guide.text"), self)
        user_guide_action.setStatusTip(tr("menu.help.user_guide.tip"))
        user_guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(user_guide_action)
        
        # 分隔符
        help_menu.addSeparator()
        
        # 关于
        about_action = QAction(tr("menu.help.about.text"), self)
        about_action.setStatusTip(tr("menu.help.about.tip"))
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """创建工具栏 - 使用现代化SVG图标"""
        toolbar = QToolBar(tr("toolbar.main"))
        self._toolbar = toolbar  # 保存引用以便后续更新
        self.addToolBar(toolbar)
        
        # 设置图标大小为18x18（适中清晰）
        toolbar.setIconSize(QSize(18, 18))
        
        # 设置工具栏样式
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        
        # 新建按钮
        new_btn = toolbar.addAction(Icons.FILE_NEW, tr("toolbar.new.text"))
        new_btn.setToolTip(tr("toolbar.new.tooltip"))
        new_btn.setStatusTip(tr("toolbar.new.tip"))
        new_btn.triggered.connect(self.new_file)
        
        # 打开文件按钮
        open_btn = toolbar.addAction(Icons.FOLDER_OPEN, tr("toolbar.open_file.text"))
        open_btn.setToolTip(tr("toolbar.open_file.tooltip"))
        open_btn.setStatusTip(tr("toolbar.open_file.tip"))
        open_btn.triggered.connect(self.open_file)
        
        # 打开文件夹按钮
        open_folder_btn = toolbar.addAction(Icons.FOLDER, tr("toolbar.open_folder.text"))
        open_folder_btn.setToolTip(tr("toolbar.open_folder.tooltip"))
        open_folder_btn.setStatusTip(tr("toolbar.open_folder.tip"))
        open_folder_btn.triggered.connect(self.open_folder)
        
        # 保存按钮
        save_btn = toolbar.addAction(Icons.SAVE, tr("toolbar.save.text"))
        save_btn.setToolTip(tr("toolbar.save.tooltip"))
        save_btn.setStatusTip(tr("toolbar.save.tip"))
        save_btn.triggered.connect(self.save_file)
        
        toolbar.addSeparator()
        
        # 关闭当前按钮
        close_current_btn = toolbar.addAction(Icons.TIMES_CIRCLE, tr("toolbar.close_current.text"))
        close_current_btn.setToolTip(tr("toolbar.close_current.tooltip"))
        close_current_btn.setStatusTip(tr("toolbar.close_current.tip"))
        close_current_btn.triggered.connect(self.close_current_file)
        
        # 关闭所有按钮
        close_all_btn = toolbar.addAction(Icons.FOLDER_TIMES, tr("toolbar.close_all.text"))
        close_all_btn.setToolTip(tr("toolbar.close_all.tooltip"))
        close_all_btn.setStatusTip(tr("toolbar.close_all.tip"))
        close_all_btn.triggered.connect(self.close_all_files)
        
        toolbar.addSeparator()
        
        # 撤销按钮
        self.undo_btn = toolbar.addAction(Icons.UNDO, tr("toolbar.undo.text"))
        self.undo_btn.setToolTip(tr("toolbar.undo.tooltip"))
        self.undo_btn.setStatusTip(tr("toolbar.undo.tip"))
        self.undo_btn.triggered.connect(self.undo)
        self.undo_btn.setEnabled(False)
        
        # 重做按钮
        self.redo_btn = toolbar.addAction(Icons.REDO, tr("toolbar.redo.text"))
        self.redo_btn.setToolTip(tr("toolbar.redo.tooltip"))
        self.redo_btn.setStatusTip(tr("toolbar.redo.tip"))
        self.redo_btn.triggered.connect(self.redo)
        self.redo_btn.setEnabled(False)
        
        toolbar.addSeparator()
        
        # 清除按钮
        clear_btn = toolbar.addAction(Icons.TRASH, tr("toolbar.clear.text"))
        clear_btn.setToolTip(tr("toolbar.clear.tooltip"))
        clear_btn.setStatusTip(tr("toolbar.clear.tip"))
        clear_btn.triggered.connect(self.clear_all)
        
        # 全选按钮
        select_all_btn = toolbar.addAction(Icons.CHECK_CIRCLE, tr("toolbar.select_all.text"))
        select_all_btn.setToolTip(tr("toolbar.select_all.tooltip"))
        select_all_btn.setStatusTip(tr("toolbar.select_all.tip"))
        select_all_btn.triggered.connect(self.select_all)
        
        # 复制按钮
        self.copy_btn = toolbar.addAction(Icons.COPY, tr("toolbar.copy.text"))
        self.copy_btn.setToolTip(tr("toolbar.copy.tooltip"))
        self.copy_btn.setStatusTip(tr("toolbar.copy.tip"))
        self.copy_btn.triggered.connect(self.copy)
        self.copy_btn.setEnabled(False)
        
        # 粘贴按钮
        self.paste_btn = toolbar.addAction(Icons.PASTE, tr("toolbar.paste.text"))
        self.paste_btn.setToolTip(tr("toolbar.paste.tooltip"))
        self.paste_btn.setStatusTip(tr("toolbar.paste.tip"))
        self.paste_btn.triggered.connect(self.paste)
        
        # 全选+复制组合按钮（使用文字代替图标，更清晰）
        self.select_copy_btn = toolbar.addAction(tr("toolbar.select_copy.text"))
        self.select_copy_btn.setToolTip(tr("toolbar.select_copy.tooltip"))
        self.select_copy_btn.setStatusTip(tr("toolbar.select_copy.tip"))
        self.select_copy_btn.triggered.connect(self.select_all_and_copy)
        
        toolbar.addSeparator()
        
        # 查找按钮
        find_btn = toolbar.addAction(Icons.SEARCH, tr("toolbar.find.text"))
        find_btn.setToolTip(tr("toolbar.find.tooltip"))
        find_btn.setStatusTip(tr("toolbar.find.tip"))
        find_btn.triggered.connect(self.show_find_dialog)
        
        # 替换按钮
        replace_btn = toolbar.addAction(Icons.EXCHANGE, tr("toolbar.replace.text"))
        replace_btn.setToolTip(tr("toolbar.replace.tooltip"))
        replace_btn.setStatusTip(tr("toolbar.replace.tip"))
        replace_btn.triggered.connect(self.show_replace_dialog)
    
    def _create_statusbar(self):
        """创建状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # 显示就绪状态
        self.statusbar.showMessage(tr("statusbar.ready"), 2000)
        
        # ===== 语言切换按钮 (右下角 - 最方便的位置) =====
        from src.ui.language_selector import LanguageButton
        self.language_button = LanguageButton(self)
        self.language_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #555;
                border-radius: 3px;
                padding: 4px 12px;
                background-color: transparent;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-color: #777;
            }
        """)
        self.statusbar.addPermanentWidget(self.language_button)
        
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
        
        # 重新初始化图标以匹配新主题
        self._init_icons()
        # 重新创建工具栏以应用新图标
        self._recreate_toolbar()
        
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
    
    def _recreate_toolbar(self):
        """重新创建工具栏以应用新图标"""
        # 移除旧工具栏
        for toolbar in self.findChildren(QToolBar):
            self.removeToolBar(toolbar)
        
        # 创建新工具栏
        self._create_toolbar()
    
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
    
    def open_folder(self):
        """打开文件夹"""
        # 获取最近打开的目录
        last_dir = self._get_last_opened_directory()
        
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            last_dir,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        
        if folder_path:
            # 设置文件浏览器的根路径
            if hasattr(self, 'file_explorer') and self.file_explorer:
                self.file_explorer.set_root_path(folder_path)
                self.statusbar.showMessage(f"已打开文件夹: {folder_path}", 3000)
                # 保存最近打开的目录
                self._save_last_opened_directory(folder_path)
                print(f"打开文件夹: {folder_path}")
            else:
                QMessageBox.warning(self, "错误", "文件浏览器不可用")
    
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
            # 使用在线版本的用户指南
            online_guide_url = "https://madechango.com/static/changoeditor/user-guide.html"
            
            # 在默认浏览器中打开在线用户指南
            webbrowser.open(online_guide_url)
            self.statusbar.showMessage("已在浏览器中打开在线使用指南", 3000)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "错误", 
                f"打开使用指南时出错：\n{str(e)}\n\n请检查网络连接，或手动访问：\nhttps://madechango.com/static/changoeditor/user-guide.html"
            )

    def show_about(self):
        """显示关于对话框"""
        about_text = (
            f"<h3>{tr('about.header')}</h3>"
            f"<p>{tr('about.intro')}</p>"
            f"<p><b>🎨 {tr('about.latest_features')}</b></p>"
            "<ul>"
            f"<li>{tr('about.feature_themes')}</li>"
            f"<li>{tr('about.feature_zero_config')}</li>"
            f"<li>{tr('about.feature_scenarios')}</li>"
            f"<li>{tr('about.feature_realtime')}</li>"
            "</ul>"
            f"<p><b>📁 {tr('about.v133_features')}</b></p>"
            "<ul>"
            f"<li>{tr('about.feature_folder')}</li>"
            f"<li>{tr('about.feature_path')}</li>"
            f"<li>{tr('about.feature_icons')}</li>"
            "</ul>"
            f"<p><b>✨ {tr('about.core_features')}</b></p>"
            "<ul>"
            f"<li>{tr('about.feature_7themes')}</li>"
            f"<li>{tr('about.feature_editing')}</li>"
            f"<li>{tr('about.feature_search')}</li>"
            f"<li>{tr('about.feature_file_mgmt')}</li>"
            f"<li>{tr('about.feature_toolbar')}</li>"
            "</ul>"
            f"<p><b>🎮 {tr('about.shortcuts_title')}</b></p>"
            f"<p>{tr('about.shortcuts_line1')}</p>"
            f"<p>{tr('about.shortcuts_line2')}</p>"
            f"<p><b>{tr('about.update_date')}</b>{tr('about.date')}</p>"
            f"<p>{tr('about.copyright')}</p>"
        )
        
        QMessageBox.about(
            self,
            tr("about.title"),
            about_text
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
    
    def select_all_and_copy(self):
        """全选并复制操作"""
        editor = self.tab_widget.get_current_editor()
        if editor:
            # 先全选
            editor.selectAll()
            # 再复制
            editor.copy()
            self.statusbar.showMessage("✓ 已全选并复制到剪贴板", 2000)
    
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
    
    # ========== 多语言支持 ==========
    
    def _on_language_changed(self, locale: str):
        """
        语言切换事件处理
        
        Args:
            locale: 新语言代码，如 "zh_CN", "en_US", "ja_JP"
        """
        print(f"🎯 MainWindow: _on_language_changed被调用！locale={locale}")
        print(f"🎯 MainWindow: 当前语言名称={self.i18n.get_current_locale_name()}")
        
        # 刷新UI
        print(f"🎯 MainWindow: 准备调用refresh_ui()")
        self.refresh_ui()
        
        # 显示提示消息
        print(f"🎯 MainWindow: 显示状态栏提示")
        self.statusbar.showMessage(
            tr("message.language_changed", language=self.i18n.get_current_locale_name()),
            3000
        )
    
    def refresh_ui(self):
        """
        刷新所有UI文本（语言切换后调用）
        这个方法会重新创建菜单栏和工具栏，确保所有文本使用新语言显示
        """
        print(f"🔄 MainWindow: refresh_ui开始执行")
        
        # 1. 更新窗口标题
        print(f"🔄 MainWindow: 更新窗口标题")
        self.setWindowTitle(tr("app.title"))
        
        # 2. 重新创建菜单栏
        print(f"🔄 MainWindow: 清空并重建菜单栏")
        self.menuBar().clear()
        self._create_menus()
        
        # 3. 重新创建工具栏
        print(f"🔄 MainWindow: 清空并重建工具栏")
        # 移除旧工具栏
        if hasattr(self, '_toolbar'):
            self.removeToolBar(self._toolbar)
        # 重新创建工具栏
        self._create_toolbar()
        
        # 4. 更新状态栏提示
        if hasattr(self, 'language_button'):
            # 语言按钮会自动更新，因为它监听了语言切换信号
            print(f"🔄 MainWindow: 语言按钮存在")
        else:
            print(f"⚠️ MainWindow: 语言按钮不存在")
        
        # 5. 更新状态栏消息
        print(f"🔄 MainWindow: 更新状态栏消息")
        self.statusbar.showMessage(tr("statusbar.ready"), 1000)
        
        print(f"✅ MainWindow: UI已刷新为: {self.i18n.get_current_locale_name()}")


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
