"""
主题管理 - Chango Editor

主要功能：
- 加载和管理主题文件
- 应用主题样式
- 主题切换功能
- 主题配置管理
"""

import json
import os
import sys
from typing import Dict, List, Optional
from PyQt6.QtCore import QObject, pyqtSignal


class ThemeManager(QObject):
    """主题管理器"""
    
    # 信号定义
    theme_changed = pyqtSignal(str)  # 主题改变信号
    
    def __init__(self, theme_dir: str = None):
        super().__init__()
        # 支持多种环境的主题目录路径
        if theme_dir:
            self.theme_dir = theme_dir
        else:
            # 尝试多个可能的主题目录路径
            possible_paths = [
                # 开发环境路径
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                    'resources', 'themes'
                ),
                # PyInstaller打包后的临时目录路径
                os.path.join(
                    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
                    'resources', 'themes'
                ),
                # 打包后的路径（资源文件在同级目录）
                os.path.join(
                    os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)),
                    'resources', 'themes'
                )
            ]
            
            self.theme_dir = None
            for path in possible_paths:
                if os.path.exists(path):
                    self.theme_dir = path
                    break
            
            # 如果所有路径都不存在，使用第一个作为默认值
            if not self.theme_dir:
                self.theme_dir = possible_paths[0]
        
        self.themes: Dict[str, dict] = {}
        self.current_theme = "dark"
        self._load_themes()
    
    def _load_themes(self):
        """加载所有主题文件"""
        if not os.path.exists(self.theme_dir):
            print(f"主题目录不存在: {self.theme_dir}")
            self._create_default_themes()
            return
        
        for filename in os.listdir(self.theme_dir):
            if filename.endswith('.json'):
                theme_name = os.path.splitext(filename)[0]
                theme_path = os.path.join(self.theme_dir, filename)
                try:
                    with open(theme_path, 'r', encoding='utf-8') as f:
                        theme_data = json.load(f)
                        # 更新主题描述中的应用名称
                        if 'description' in theme_data:
                            theme_data['description'] = theme_data['description'].replace('PyEditor Lite', 'Chango Editor')
                        self.themes[theme_name] = theme_data
                        print(f"加载主题: {theme_name}")
                except Exception as e:
                    print(f"加载主题失败 {filename}: {e}")
    
    def _create_default_themes(self):
        """创建默认主题"""
        os.makedirs(self.theme_dir, exist_ok=True)
        
        # 暗色主题
        dark_theme = {
            "name": "Dark Theme",
            "description": "Chango Editor 暗色主题",
            "colors": {
                "background": "#1e1e1e",
                "foreground": "#d4d4d4",
                "selection": "#264f78",
                "line_highlight": "#2a2a2a",
                "line_number_background": "#3c3c3c",
                "line_number_foreground": "#969696",
                "menu_background": "#3c3c3c",
                "menu_foreground": "#ffffff",
                "toolbar_background": "#3c3c3c",
                "toolbar_foreground": "#ffeb3b",
                "statusbar_background": "#3c3c3c",
                "statusbar_foreground": "#ffffff"
            },
            "syntax": {
                "keyword": "#569cd6",
                "string": "#ce9178",
                "comment": "#6a9955",
                "number": "#b5cea8",
                "function": "#dcdcaa",
                "class": "#4ec9b0",
                "operator": "#d4d4d4",
                "builtin": "#569cd6",
                "error": "#f44747",
                "decorator": "#ffc649"
            }
        }
        
        # 亮色主题
        light_theme = {
            "name": "Light Theme",
            "description": "Chango Editor 亮色主题",
            "colors": {
                "background": "#ffffff",
                "foreground": "#000000",
                "selection": "#add6ff",
                "line_highlight": "#f5f5f5",
                "line_number_background": "#f0f0f0",
                "line_number_foreground": "#808080",
                "menu_background": "#f0f0f0",
                "menu_foreground": "#000000",
                "toolbar_background": "#f0f0f0",
                "toolbar_foreground": "#000000",
                "statusbar_background": "#f0f0f0",
                "statusbar_foreground": "#000000"
            },
            "syntax": {
                "keyword": "#0000ff",
                "string": "#a31515",
                "comment": "#008000",
                "number": "#098658",
                "function": "#795e26",
                "class": "#2b91af",
                "operator": "#000000",
                "builtin": "#0000ff",
                "error": "#ff0000",
                "decorator": "#808000"
            }
        }
        
        # 保存主题文件
        for theme_name, theme_data in [("dark", dark_theme), ("light", light_theme)]:
            theme_path = os.path.join(self.theme_dir, f"{theme_name}.json")
            with open(theme_path, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, indent=2, ensure_ascii=False)
        
        self.themes = {"dark": dark_theme, "light": light_theme}
    
    def get_theme_names(self) -> List[str]:
        """获取所有主题名称"""
        return list(self.themes.keys())
    
    def get_theme(self, theme_name: str) -> Optional[dict]:
        """获取指定主题"""
        return self.themes.get(theme_name)
    
    def get_current_theme(self) -> dict:
        """获取当前主题"""
        return self.themes.get(self.current_theme, self.themes.get("dark", {}))
    
    def set_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        if theme_name in self.themes:
            old_theme = self.current_theme
            self.current_theme = theme_name
            self.theme_changed.emit(theme_name)
            print(f"主题切换: {old_theme} -> {theme_name}")
            return True
        return False
    
    def get_theme_stylesheet(self, theme_name: str = None) -> str:
        """获取主题样式表"""
        theme = self.get_theme(theme_name or self.current_theme)
        if not theme:
            return ""
        
        colors = theme.get("colors", {})
        
        # 生成样式表
        stylesheet = f"""
        /* 主窗口样式 */
        QMainWindow {{
            background-color: {colors.get('background', '#2b2b2b')};
            color: {colors.get('foreground', '#ffffff')};
        }}
        
        /* 菜单栏样式 */
        QMenuBar {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: none;
            padding: 2px;
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        QMenuBar::item:selected {{
            background-color: {colors.get('selection', '#4a4a4a')};
        }}
        QMenuBar::item:pressed {{
            background-color: {colors.get('selection', '#4a4a4a')};
        }}
        
        /* 菜单样式 */
        QMenu {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 6px 24px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {colors.get('selection', '#4a4a4a')};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: #555555;
            margin: 4px 0px;
        }}
        
        /* 工具栏样式 */
        QToolBar {{
            background-color: {colors.get('toolbar_background', '#3c3c3c')};
            color: {colors.get('toolbar_foreground', '#ffffff')};
            border: none;
            spacing: 2px;
            padding: 4px;
        }}
        QToolBar::separator {{
            background-color: #555555;
            width: 1px;
            margin: 0 4px;
        }}
        QToolButton {{
            background-color: transparent;
            color: {colors.get('toolbar_foreground', '#ffffff')};
            border: none;
            padding: 4px;
            border-radius: 4px;
            font-weight: bold;
        }}
        QToolButton:hover {{
            background-color: {colors.get('selection', '#4a4a4a')};
            color: {colors.get('toolbar_foreground', '#ffffff')};
        }}
        QToolButton:pressed {{
            background-color: {colors.get('selection', '#4a4a4a')};
            color: {colors.get('toolbar_foreground', '#ffffff')};
        }}
        
        /* 状态栏样式 */
        QStatusBar {{
            background-color: {colors.get('statusbar_background', '#3c3c3c')};
            color: {colors.get('statusbar_foreground', '#ffffff')};
            border-top: 1px solid #555555;
            padding: 2px;
        }}
        
        /* 分割器样式 */
        QSplitter::handle {{
            background-color: #555555;
        }}
        QSplitter::handle:hover {{
            background-color: #666666;
        }}
        
        /* 标签页样式 */
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
        
        /* 文件浏览器样式 */
        QListWidget {{
            background-color: {colors.get('background', '#2b2b2b')};
            color: {colors.get('foreground', '#ffffff')};
            border: none;
            outline: none;
        }}
        QListWidget::item {{
            height: 22px;
            padding: 2px;
        }}
        QListWidget::item:hover {{
            background-color: {colors.get('selection', '#404040')};
        }}
        QListWidget::item:selected {{
            background-color: {colors.get('selection', '#0078d4')};
        }}
        
        /* 按钮样式 */
        QPushButton {{
            background-color: {colors.get('menu_background', '#3c3c3c')};
            color: {colors.get('menu_foreground', '#ffffff')};
            border: 1px solid #555555;
            padding: 6px 12px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {colors.get('selection', '#4a4a4a')};
        }}
        QPushButton:pressed {{
            background-color: {colors.get('selection', '#4a4a4a')};
        }}
        
        /* 标签样式 */
        QLabel {{
            background-color: transparent;
            color: {colors.get('foreground', '#ffffff')};
        }}
        """
        
        return stylesheet
