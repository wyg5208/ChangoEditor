#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chango Editor 统一版本配置文件
所有构建脚本都从这里读取版本信息，确保版本号一致性

更新说明：
- 修改此文件后，所有构建脚本会自动使用新版本号
- 无需手动更新多个文件
"""

# 版本信息
__version__ = "1.4.0"
__version_info__ = (1, 4, 0)

# 应用信息
APP_NAME = "ChangoEditor"
APP_DISPLAY_NAME = "Chango Editor"
APP_DESCRIPTION = "功能强大的代码编辑器 - 支持20+语言、8种界面语言、7个精美主题"
APP_AUTHOR = "Chango Team"
APP_URL = "https://github.com/wyg5208/changoeditor"
APP_LICENSE = "MIT"

# 发布信息
RELEASE_TITLE = f"{APP_DISPLAY_NAME} v{__version__} - 完整国际化支持"
RELEASE_TAG = f"v{__version__}"

# 版本历史
VERSION_HISTORY = {
    "1.4.0": {
        "date": "2025-10-08",
        "title": "完整国际化支持",
        "highlights": [
            "8种语言界面支持",
            "实时语言切换",
            "智能语言检测",
            "完整翻译覆盖"
        ]
    },
    "1.3.4": {
        "date": "2025-10-06",
        "title": "主题系统扩展",
        "highlights": [
            "5个新主题",
            "零代码配置",
            "场景化配色"
        ]
    },
    "1.3.3": {
        "date": "2025-10-06",
        "title": "打开文件夹功能",
        "highlights": [
            "文件夹浏览",
            "路径区优化"
        ]
    }
}

def get_version():
    """获取版本号字符串"""
    return __version__

def get_version_info():
    """获取版本号元组"""
    return __version_info__

def get_full_version_string():
    """获取完整版本字符串"""
    return f"{APP_DISPLAY_NAME} v{__version__}"

def get_latest_changes():
    """获取最新版本的更新内容"""
    if __version__ in VERSION_HISTORY:
        info = VERSION_HISTORY[__version__]
        changes = f"{info['title']} ({info['date']})\n"
        for highlight in info['highlights']:
            changes += f"  • {highlight}\n"
        return changes
    return "版本信息未找到"

if __name__ == "__main__":
    # 当直接运行此文件时，显示版本信息
    print("=" * 60)
    print(f"{APP_DISPLAY_NAME} 版本信息")
    print("=" * 60)
    print(f"版本号: {__version__}")
    print(f"版本元组: {__version_info__}")
    print(f"应用名称: {APP_NAME}")
    print(f"显示名称: {APP_DISPLAY_NAME}")
    print(f"描述: {APP_DESCRIPTION}")
    print(f"作者: {APP_AUTHOR}")
    print(f"网址: {APP_URL}")
    print(f"许可证: {APP_LICENSE}")
    print(f"发布标签: {RELEASE_TAG}")
    print(f"发布标题: {RELEASE_TITLE}")
    print("\n最新更新:")
    print(get_latest_changes())
    print("=" * 60)

