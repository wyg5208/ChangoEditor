"""
Chango Editor - 主入口文件

轻量级Python代码编辑器
提供类似Sublime Text的编辑体验

使用方法:
    python main.py [文件路径]
"""

import sys
import os
import io

# 设置控制台输出编码为UTF-8，避免中文乱码
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except (AttributeError, io.UnsupportedOperation):
        pass

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 添加src目录到Python路径 - 支持打包后的环境
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 添加项目根目录到路径，以支持开发环境
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# 导入主窗口 - 使用多种方式确保兼容性
try:
    # 尝试直接导入（适用于打包后的环境）
    from ui.main_window import MainWindow
except ImportError:
    try:
        # 尝试相对导入（适用于开发环境）
        from .ui.main_window import MainWindow
    except ImportError:
        # 最后尝试从src目录导入
        sys.path.insert(0, os.path.join(current_dir, '..', 'src'))
        from ui.main_window import MainWindow


def setup_application():
    """设置应用程序"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("Chango Editor")
    app.setApplicationVersion("1.3.4")
    app.setOrganizationName("Chango Team")
    app.setOrganizationDomain("chango-editor.com")
    
    # 设置高DPI支持 (PyQt6中属性名可能不同)
    try:
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        # PyQt6 可能不需要这些设置或属性名不同
        print("跳过高DPI设置（PyQt6版本可能不需要）")
    
    # 设置默认字体
    font = QFont("Consolas", 10)
    if not font.exactMatch():
        font = QFont("Courier New", 10)
    font.setFixedPitch(True)
    app.setFont(font)
    
    return app


def main():
    """主函数"""
    # 创建应用程序
    app = setup_application()
    
    # 创建主窗口
    window = MainWindow()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            window.open_file_from_path(file_path)
            print(f"从命令行打开文件: {file_path}")
    
    # 显示窗口
    window.show()
    
    print("Chango Editor 启动完成")
    print("=" * 50)
    print("欢迎使用 Chango Editor v0.1.0")
    print("轻量级Python代码编辑器")
    print("=" * 50)
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
