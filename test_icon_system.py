"""
测试新的图标系统
验证SVG图标能否正确渲染
"""

import sys
import os

# 设置UTF-8编码输出（Windows兼容）
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar
from PyQt6.QtCore import QSize, Qt
from src.utils.icon_provider import Icons, IconProvider


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图标系统测试 - v1.3.1")
        self.setGeometry(100, 100, 900, 200)
        
        # 初始化图标
        Icons.init_icons(color="#ffffff", size=18)
        
        # 创建工具栏
        toolbar = QToolBar("测试工具栏")
        self.addToolBar(toolbar)
        toolbar.setIconSize(QSize(18, 18))
        toolbar.setMovable(False)
        
        # 添加所有图标
        toolbar.addAction(Icons.FILE_NEW, "新建文件")
        toolbar.addAction(Icons.FOLDER_OPEN, "打开文件夹")
        toolbar.addAction(Icons.SAVE, "保存")
        toolbar.addSeparator()
        toolbar.addAction(Icons.TIMES_CIRCLE, "关闭")
        toolbar.addAction(Icons.FOLDER_TIMES, "关闭所有")
        toolbar.addSeparator()
        toolbar.addAction(Icons.UNDO, "撤销")
        toolbar.addAction(Icons.REDO, "重做")
        toolbar.addSeparator()
        toolbar.addAction(Icons.TRASH, "删除")
        toolbar.addAction(Icons.CHECK_CIRCLE, "全选")
        toolbar.addAction(Icons.COPY, "复制")
        toolbar.addAction(Icons.PASTE, "粘贴")
        toolbar.addSeparator()
        toolbar.addAction(Icons.SEARCH, "搜索")
        toolbar.addAction(Icons.EXCHANGE, "替换")
        toolbar.addSeparator()
        toolbar.addAction(Icons.SELECT_COPY, "全选并复制（彩色）")
        
        # 设置深色背景
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QToolBar {
                background-color: #3c3c3c;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: #505050;
            }
            QToolButton:pressed {
                background-color: #0078d4;
            }
        """)
        
        print("✓ 图标系统测试窗口已创建")
        print("✓ 所有图标已加载 (18x18像素)")
        print("✓ 使用Font Awesome风格的SVG图标")
        print("✓ 新增彩色'全选+复制'组合图标")


def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    
    print("\n" + "="*50)
    print("图标测试说明:")
    print("="*50)
    print("✓ 图标尺寸: 18x18 像素（适中清晰）")
    print("✓ 图标风格: Font Awesome SVG矢量图标")
    print("✓ 图标颜色: 白色 (#ffffff)")
    print("✓ 特色功能: 彩色'全选+复制'组合图标")
    print("✓ 图标质量: 矢量图标，任意缩放无损")
    print("✓ 现代化设计: 业界标准的专业图标库")
    print("="*50)
    print("\n将鼠标悬停在图标上查看工具提示")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

