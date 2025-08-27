"""
工具模块 - PyEditor Lite

包含各种工具和辅助功能：
- 语法高亮
- 文件监控
- 主题管理
- 设置管理
- Git工具
"""

# 为了避免循环导入，__init__.py 暂时为空
# 各模块请直接导入具体的类

__all__ = [
    'SyntaxHighlighter',
    'FileWatcher',
    'ThemeManager',
    'SettingsManager',
    'GitUtils'
]
