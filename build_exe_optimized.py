#!/usr/bin/env python3
"""
Chango Editor 优化版打包脚本
专注于最小体积和最快性能
更新时间: 2025年1月6日
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")

def verify_core_dependencies():
    """验证核心运行时依赖"""
    print("验证核心运行时依赖...")
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    # 核心运行时依赖
    core_dependencies = {
        'PyQt6': 'PyQt6',
        'Pygments': 'pygments'
    }
    
    # 可选运行时依赖
    optional_dependencies = {
        'chardet': 'chardet'  # 文件编码检测
    }
    
    for name, module in core_dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} (核心)")
        except ImportError:
            print(f"❌ {name} 未安装 (核心依赖)")
            print(f"请运行: pip install {name.lower()}")
            return False
    
    # 检查可选依赖
    for name, module in optional_dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} (可选)")
        except ImportError:
            print(f"⚠️  {name} 未安装 (可选，用于文件编码检测)")
    
    # 检查源文件
    required_files = [
        'src/main.py',
        'src/ui/main_window.py',
        'resources/themes/dark.json',
        'resources/themes/light.json'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ 缺少文件: {file_path}")
            return False
    
    return True

def build_optimized_exe():
    """构建优化的exe文件"""
    print("开始构建 Chango Editor 优化版可执行文件...")
    print("🎯 目标：最小体积 + 最快启动")
    print("="*60)
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    # 验证核心依赖
    if not verify_core_dependencies():
        print("❌ 核心依赖验证失败，无法继续构建")
        return False
    
    # 获取pyinstaller路径
    pyinstaller_path = 'Scripts/pyinstaller.exe' if os.path.exists('Scripts/pyinstaller.exe') else 'pyinstaller'
    
    # 优化的PyInstaller命令 - 专注于最小体积
    cmd = [
        pyinstaller_path,
        '--onefile',           # 单文件模式
        '--windowed',          # 无控制台模式
        '--name=ChangoEditor', # 可执行文件名
        '--clean',             # 清理临时文件
        '--noconfirm',         # 覆盖输出目录而不确认
        '--strip',             # 去除符号表（减少体积）
        '--noupx',             # 禁用UPX压缩（避免启动延迟）
        '--distpath=dist',     # 指定输出目录
        '--workpath=build',    # 指定工作目录
        
        # 优化：排除不必要的模块
        '--exclude-module=PIL',
        '--exclude-module=Pillow', 
        '--exclude-module=cairosvg',
        '--exclude-module=cairocffi',
        '--exclude-module=git',
        '--exclude-module=gitdb',
        '--exclude-module=GitPython',
        '--exclude-module=watchdog',
        '--exclude-module=pefile',
        '--exclude-module=altgraph',
        '--exclude-module=pywin32-ctypes',
        '--exclude-module=cffi',
        '--exclude-module=pycparser',
        '--exclude-module=defusedxml',
        '--exclude-module=packaging',
        '--exclude-module=smmap',
        '--exclude-module=tinycss2',
        '--exclude-module=webencodings',
        '--exclude-module=cssselect2',
        
        # 排除不必要的标准库模块
        '--exclude-module=tkinter',
        '--exclude-module=unittest',
        '--exclude-module=test',
        '--exclude-module=distutils',
        '--exclude-module=email',
        '--exclude-module=http',
        '--exclude-module=urllib3',
        '--exclude-module=xml.dom',
        '--exclude-module=xml.sax',
        '--exclude-module=xmlrpc',
        '--exclude-module=pydoc',
        '--exclude-module=doctest',
        '--exclude-module=multiprocessing',
        '--exclude-module=concurrent.futures',
        
        # 核心必需模块 - 精确指定
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=pygments.lexers.python',
        '--hidden-import=pygments.lexers.web',
        '--hidden-import=pygments.lexers.javascript',
        '--hidden-import=pygments.lexers.shell',
        '--hidden-import=pygments.lexers.data',
        '--hidden-import=pygments.formatters.other',
        
        # 文件编码检测（如果可用）
        '--hidden-import=chardet',
        
        # Chango Editor 核心模块
        '--hidden-import=src.ui.main_window',
        '--hidden-import=src.ui.tab_widget',
        '--hidden-import=src.ui.file_explorer',
        '--hidden-import=src.ui.search_dialog',
        '--hidden-import=src.ui.new_file_dialog',
        '--hidden-import=src.core.editor',
        '--hidden-import=src.utils.syntax',
        '--hidden-import=src.utils.themes',
        '--hidden-import=src.utils.settings',
        '--hidden-import=src.utils.file_templates',
        
        # 添加源码路径
        '--paths=src',
        
        # 主程序文件
        'src/main.py'
    ]
    
    # 只添加必需的资源文件
    essential_files = [
        'resources/themes/dark.json',
        'resources/themes/light.json'
    ]
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            cmd.extend(['--add-data', f'{file_path};resources/themes'])
            print(f"添加必需资源: {file_path}")
    
    # 只添加存在的图标文件（优先PNG）
    icon_files = [
        'resources/icons/chango_editor.png',
        'resources/icons/chango_editor.ico'
    ]
    
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            if icon_file.endswith('.ico'):
                cmd.extend(['--icon', icon_file])
                print(f"设置程序图标: {icon_file}")
            else:
                cmd.extend(['--add-data', f'{icon_file};resources/icons'])
                print(f"添加图标文件: {icon_file}")
            break  # 只使用第一个找到的图标
    
    print("\n执行优化打包命令...")
    print("🎯 优化重点：最小依赖 + 排除无用模块")
    print("="*60)
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, cwd=os.getcwd(), text=True)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("✅ 优化打包成功!")
            
            exe_path = 'dist/ChangoEditor.exe'
            if os.path.exists(exe_path):
                print(f"可执行文件位置: {os.path.abspath(exe_path)}")
                
                # 显示文件大小
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"优化后文件大小: {size_mb:.1f} MB")
                
                # 与之前的文件大小比较
                original_size = 45.7  # 之前的文件大小
                if size_mb < original_size:
                    reduction = original_size - size_mb
                    percentage = (reduction / original_size) * 100
                    print(f"🎉 体积减少: {reduction:.1f} MB ({percentage:.1f}%)")
                
                print("\n📝 优化特性:")
                print("- 排除了非必需的第三方库 (PIL, CairoSVG, Git等)")
                print("- 排除了未使用的标准库模块")
                print("- 精确指定必需的Pygments词法分析器")
                print("- 只包含运行时真正需要的依赖")
                print("- 启动速度更快，体积更小")
                
                # 快速测试
                print(f"\n🧪 快速测试: 双击 {exe_path} 验证是否正常启动")
                
            else:
                print("⚠️  exe文件未找到，构建可能未完全成功")
                return False
                
        else:
            print("\n" + "="*60)
            print("❌ 优化打包失败!")
            print("请检查上面的错误信息")
            return False
            
    except FileNotFoundError:
        print("❌ 找不到 pyinstaller 命令")
        print("请确保已安装 pyinstaller: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"❌ 打包过程出现异常: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """主函数"""
    print("Chango Editor 优化构建工具")
    print("目标：最小体积 + 最快启动")
    print("="*60)
    
    success = build_optimized_exe()
    
    if success:
        print("\n🎉 Chango Editor 优化版打包完成!")
        print("✨ 特点：精简依赖，快速启动，小体积")
        print("="*60)
    else:
        print("\n❌ 优化打包过程中出现错误")
        print("="*60)
        sys.exit(1)

if __name__ == '__main__':
    main()
