#!/usr/bin/env python3
"""
UI优化测试脚本 - Chango Editor
测试工具栏图标化、文件浏览器按钮图标化和展开/收起全部功能
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_window import MainWindow

def test_ui_optimizations():
    """测试UI优化功能"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 创建一个定时器来自动测试展开/收起功能
    def test_expand_collapse():
        if hasattr(window, 'file_explorer'):
            print("=== 测试展开/收起全部功能 ===")
            print("3秒后展开全部...")
            QTimer.singleShot(3000, lambda: window.file_explorer.expand_all())
            print("6秒后收起全部...")
            QTimer.singleShot(6000, lambda: window.file_explorer.collapse_all())
    
    # 启动测试
    QTimer.singleShot(1000, test_expand_collapse)
    
    print("=== UI优化测试说明 ===")
    print("1. 工具栏按钮现在应该显示为图标")
    print("2. 将鼠标悬停在工具栏按钮上查看工具提示")
    print("3. 左侧文件浏览器顶部应该有5个图标按钮:")
    print("   - ⬆️ (上级目录)")
    print("   - 🔄 (刷新)")
    print("   - 📂 (展开全部)")
    print("   - 📁 (收起全部)")
    print("4. 点击展开/收起按钮测试功能")
    print("=== 测试开始 ===")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_ui_optimizations()
