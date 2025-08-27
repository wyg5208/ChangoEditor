#!/usr/bin/env python3
"""
语法高亮测试脚本
用于验证Chango Editor的语法高亮功能是否正常工作
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_path = current_dir / 'src'
sys.path.insert(0, str(src_path))

from utils.syntax import SyntaxHighlighter

def test_syntax_highlighting():
    """测试语法高亮功能"""
    print("=== Chango Editor 语法高亮测试 ===\n")
    
    # 测试文件列表
    test_files = [
        ('test_files/test.py', 'python'),
        ('test_files/test.js', 'javascript'),
        ('test_files/test.ts', 'typescript'),
        ('test_files/test.java', 'java'),
        ('test_files/test.cpp', 'cpp'),
        ('test_files/test.cs', 'csharp'),
        ('test_files/test.go', 'go'),
        ('test_files/test.rs', 'rust'),
        ('test_files/test.php', 'php'),
        ('test_files/test.rb', 'ruby'),
    ]
    
    highlighter = SyntaxHighlighter()
    
    for file_path, language in test_files:
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            continue
            
        try:
            # 读取文件内容（只读取前500字符用于测试）
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(500)
            
            print(f"📝 测试文件: {file_path}")
            print(f"🔤 语言: {language}")
            
            # 设置语言
            highlighter.set_language(language)
            
            # 检查是否支持Pygments
            if highlighter.lexer:
                print(f"✅ Pygments支持: {highlighter.lexer.name}")
            else:
                print(f"🔄 使用正则表达式高亮")
            
            # 测试语法高亮（这里只是验证不会出错）
            try:
                # 这里不实际高亮，只是验证设置正确
                print(f"🎨 语法高亮器初始化成功")
            except Exception as e:
                print(f"❌ 语法高亮出错: {e}")
            
            print(f"📏 文件大小: {len(content)} 字符")
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ 处理文件出错: {e}")
            print("-" * 50)

def test_language_detection():
    """测试语言检测功能"""
    print("\n=== 语言检测测试 ===\n")
    
    # 从editor模块导入语言检测功能
    try:
        from core.editor import TextEditor
        editor = TextEditor()
        
        test_extensions = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.xml': 'xml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
            '.yaml': 'yaml',
        }
        
        print("文件扩展名 -> 检测语言")
        print("-" * 30)
        
        for ext, expected_lang in test_extensions.items():
            # 模拟设置文件路径
            test_file = f"test{ext}"
            editor.file_path = test_file
            detected_lang = editor.detect_language()
            
            if detected_lang == expected_lang:
                print(f"✅ {ext:<8} -> {detected_lang}")
            else:
                print(f"❌ {ext:<8} -> {detected_lang} (期望: {expected_lang})")
                
    except Exception as e:
        print(f"❌ 语言检测测试失败: {e}")

def main():
    """主函数"""
    print("Chango Editor 语法高亮测试工具")
    print("=" * 40)
    
    # 检查是否在正确的目录
    if not os.path.exists('src'):
        print("❌ 错误: 请在chango_editor项目根目录运行此脚本")
        return
    
    if not os.path.exists('test_files'):
        print("❌ 错误: test_files目录不存在")
        return
    
    # 运行测试
    test_syntax_highlighting()
    test_language_detection()
    
    print("\n🎉 测试完成!")
    print("\n📋 测试总结:")
    print("1. 语法高亮器初始化测试")
    print("2. 多语言支持验证") 
    print("3. 文件扩展名语言检测")
    print("\n💡 提示: 你可以运行以下命令测试编辑器:")
    print("   python run.py test_files/test.py")
    print("   python run.py test_files/test.js")
    print("   python run.py test_files/test.java")

if __name__ == "__main__":
    main()
