#!/usr/bin/env python3
"""
Chango Editor 启动脚本

使用方法:
    python run.py [文件路径]
"""

import sys
import os

# 添加src目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# 导入并运行主程序
if __name__ == "__main__":
    from src.main import main
    main()
