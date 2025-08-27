#!/usr/bin/env python3
"""
测试文件 - 用于验证PyEditor Lite的语法高亮功能
"""

import os
import sys
from typing import List, Dict, Optional

class TestClass:
    """测试类"""
    
    def __init__(self, name: str):
        self.name = name
        self.items = []
    
    @property
    def count(self) -> int:
        """获取项目数量"""
        return len(self.items)
    
    def add_item(self, item: str) -> None:
        """添加项目"""
        if item not in self.items:
            self.items.append(item)
            print(f"添加项目: {item}")
    
    def remove_item(self, item: str) -> bool:
        """删除项目"""
        try:
            self.items.remove(item)
            return True
        except ValueError:
            print(f"项目 '{item}' 不存在")
            return False

def main():
    """主函数"""
    # 创建测试实例
    test = TestClass("测试实例")
    
    # 添加一些项目
    items = ["项目1", "项目2", "项目3"]
    for item in items:
        test.add_item(item)
    
    # 显示统计信息
    print(f"总共有 {test.count} 个项目")
    
    # 测试数字和运算
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    average = total / len(numbers)
    
    print(f"数字列表: {numbers}")
    print(f"总和: {total}, 平均值: {average:.2f}")
    
    # 测试条件语句
    if test.count > 0:
        print("列表不为空")
    else:
        print("列表为空")
    
    # 测试循环
    for i, item in enumerate(test.items):
        print(f"{i + 1}. {item}")

if __name__ == "__main__":
    main()
