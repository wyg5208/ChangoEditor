"""
核心模块 - PyEditor Lite

包含编辑器的核心功能：
- 文本编辑器
- 文档管理
- 选择管理
- 撤销/重做系统
"""

# 为了避免循环导入，__init__.py 暂时为空
# 各模块请直接导入具体的类

__all__ = [
    'TextEditor',
    'DocumentManager', 
    'SelectionManager',
    'UndoRedoSystem'
]
