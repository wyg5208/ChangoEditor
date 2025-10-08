#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chango Editor PyInstaller 打包脚本
自动化打包成独立exe文件

更新历史:
- 2025年10月8日: v1.4.0 - 版本自动识别，支持8种语言国际化
- 2025年10月6日: 更新主题文件打包配置，支持7个主题
- 2025年1月6日: 初始版本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 设置 UTF-8 编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 从统一版本配置文件导入版本信息
try:
    from version import (
        __version__ as APP_VERSION,
        APP_NAME,
        APP_DISPLAY_NAME,
        APP_DESCRIPTION
    )
    print(f"✅ 版本信息加载成功: v{APP_VERSION}")
except ImportError:
    # 降级方案：如果version.py不存在，使用默认值
    print("⚠️  警告: 未找到 version.py，使用默认版本信息")
    APP_VERSION = "1.4.0"
    APP_NAME = "ChangoEditor"
    APP_DISPLAY_NAME = "Chango Editor"
    APP_DESCRIPTION = "功能强大的代码编辑器"

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")

def verify_dependencies():
    """验证构建依赖"""
    print("验证构建依赖...")
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    # 检查主要依赖
    dependencies = {
        'PyQt6': 'PyQt6',
        'Pygments': 'pygments', 
        'Pillow': 'PIL',
        'CairoSVG': 'cairosvg',
        'chardet': 'chardet',
        'watchdog': 'watchdog'
    }
    
    # 可选依赖 - GitPython (不是必需的)
    optional_dependencies = {
        'GitPython': 'git'
    }
    
    for name, module in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} 未安装")
            print(f"请运行: pip install {name.lower()}")
            return False
    
    # 检查可选依赖
    for name, module in optional_dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} (可选)")
        except ImportError:
            print(f"⚠️  {name} 未安装 (可选，用于Git功能)")
    
    # 检查源文件
    required_files = [
        'src/main.py',
        'src/ui/main_window.py',
        'src/core/i18n.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ 缺少文件: {file_path}")
            return False
    
    # 检查主题文件（自动扫描）
    theme_dir = Path('resources/themes')
    if theme_dir.exists():
        theme_count = len(list(theme_dir.glob('*.json')))
        print(f"✅ 主题文件: {theme_count} 个")
    else:
        print("⚠️  警告: resources/themes 目录不存在")
    
    # 检查国际化语言文件（自动扫描）
    i18n_dir = Path('resources/i18n/locales')
    if i18n_dir.exists():
        locale_count = len(list(i18n_dir.glob('*.json')))
        print(f"✅ 语言文件: {locale_count} 个")
    else:
        print("⚠️  警告: resources/i18n/locales 目录不存在")
    
    return True

def convert_svg_to_ico():
    """将SVG图标转换为ICO和PNG格式"""
    try:
        from PIL import Image
        import cairosvg
        import io
        
        svg_path = 'resources/icons/chango_editor.svg'
        ico_path = 'resources/icons/chango_editor.ico'
        png_path = 'resources/icons/chango_editor.png'
        
        if os.path.exists(svg_path):
            print(f"开始转换SVG图标: {svg_path}")
            
            # 转换SVG到PNG (多种尺寸)
            sizes = [256, 128, 64, 48, 32, 16]
            images = []
            
            for size in sizes:
                png_data = cairosvg.svg2png(
                    url=svg_path, 
                    output_width=size, 
                    output_height=size
                )
                img = Image.open(io.BytesIO(png_data))
                # 确保是RGBA模式，支持透明度
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                images.append(img)
            
            # 保存最大尺寸为PNG文件
            if not os.path.exists(png_path):
                images[0].save(png_path, format='PNG')
                print(f"已生成PNG图标: {png_path}")
            
            # 保存为ICO文件，包含多种尺寸
            if not os.path.exists(ico_path):
                images[0].save(
                    ico_path, 
                    format='ICO', 
                    sizes=[(img.width, img.height) for img in images]
                )
                print(f"已生成ICO图标: {ico_path}")
            
            return True
            
    except ImportError as e:
        print(f"图标转换跳过 - 缺少依赖库: {e}")
        print("如需图标转换，请运行: pip install pillow cairosvg")
    except Exception as e:
        print(f"图标转换失败: {e}")
        import traceback
        traceback.print_exc()
    
    return False

def build_exe():
    """构建exe文件"""
    print("开始构建 Chango Editor 可执行文件...")
    print("="*60)
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    # 验证依赖
    if not verify_dependencies():
        print("❌ 依赖验证失败，无法继续构建")
        return False
    
    # 尝试转换图标
    convert_svg_to_ico()
    
    # 获取pyinstaller路径
    pyinstaller_path = 'Scripts/pyinstaller.exe' if os.path.exists('Scripts/pyinstaller.exe') else 'pyinstaller'
    
    # 构建PyInstaller命令
    exe_name = f"{APP_NAME}-v{APP_VERSION}" if APP_VERSION else APP_NAME
    
    cmd = [
        pyinstaller_path,
        '--onefile',           # 单文件模式
        '--windowed',          # 无控制台模式
        f'--name={exe_name}',  # 可执行文件名（带版本号）
        '--clean',             # 清理临时文件
        '--noconfirm',         # 覆盖输出目录而不确认
        '--distpath=dist',     # 指定输出目录
        '--workpath=build',    # 指定工作目录
        
        # PyQt6 相关模块
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtPrintSupport',
        
        # 语法高亮相关
        '--hidden-import=pygments',
        '--hidden-import=pygments.lexers',
        '--hidden-import=pygments.formatters',
        '--hidden-import=pygments.lexers.python',
        '--hidden-import=pygments.lexers.web',
        '--hidden-import=pygments.lexers.shell',
        '--hidden-import=pygments.lexers.data',
        
        # 文件编码检测
        '--hidden-import=chardet',
        
        # 文件监控
        '--hidden-import=watchdog',
        '--hidden-import=watchdog.observers',
        '--hidden-import=watchdog.events',
        
        # Git 支持（可选）
        '--hidden-import=git',
        '--hidden-import=gitdb',
        '--hidden-import=smmap',
        
        # Chango Editor 核心模块
        '--hidden-import=src',
        '--hidden-import=src.ui',
        '--hidden-import=src.ui.main_window',
        '--hidden-import=src.ui.tab_widget',
        '--hidden-import=src.ui.file_explorer',
        '--hidden-import=src.ui.search_dialog',
        '--hidden-import=src.ui.new_file_dialog',
        '--hidden-import=src.ui.split_view',
        '--hidden-import=src.ui.language_selector',  # 国际化 UI
        '--hidden-import=src.core',
        '--hidden-import=src.core.editor',
        '--hidden-import=src.core.document',
        '--hidden-import=src.core.selection',
        '--hidden-import=src.core.undo_redo',
        '--hidden-import=src.core.i18n',  # 国际化核心模块
        '--hidden-import=src.utils',
        '--hidden-import=src.utils.syntax',
        '--hidden-import=src.utils.themes',
        '--hidden-import=src.utils.settings',
        '--hidden-import=src.utils.file_templates',
        '--hidden-import=src.utils.file_watcher',
        '--hidden-import=src.utils.git_utils',
        
        # 添加源码路径
        '--paths=src',
        
        # 主程序文件
        'src/main.py'
    ]
    
    print(f"\n📦 构建 {APP_DISPLAY_NAME} v{APP_VERSION}")
    print(f"📋 EXE文件名: {exe_name}.exe")
    
    # 自动添加所有主题文件
    theme_dir = Path('resources/themes')
    if theme_dir.exists():
        theme_files = list(theme_dir.glob('*.json'))
        for theme_file in theme_files:
            cmd.extend(['--add-data', f'{theme_file};resources/themes'])
            print(f"✅ 添加主题: {theme_file.name}")
        print(f"📦 总计 {len(theme_files)} 个主题文件")
    else:
        print("⚠️  警告: resources/themes 目录不存在")
    
    # 自动添加所有国际化语言文件（新增）
    i18n_dir = Path('resources/i18n/locales')
    if i18n_dir.exists():
        locale_files = list(i18n_dir.glob('*.json'))
        for locale_file in locale_files:
            cmd.extend(['--add-data', f'{locale_file};resources/i18n/locales'])
            print(f"✅ 添加语言: {locale_file.stem}")
        print(f"🌍 总计 {len(locale_files)} 个语言文件")
    else:
        print("⚠️  警告: resources/i18n/locales 目录不存在")
    
    # 添加图标文件
    icon_files = [
        'resources/icons/chango_editor.svg',
        'resources/icons/chango_editor.png', 
        'resources/icons/chango_editor.ico'
    ]
    
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            cmd.extend(['--add-data', f'{icon_file};resources/icons'])
            print(f"添加图标文件: {icon_file}")
    
    # 如果有ico文件，设置为程序图标
    ico_path = 'resources/icons/chango_editor.ico'
    if os.path.exists(ico_path):
        cmd.extend(['--icon', ico_path])
        print(f"设置程序图标: {ico_path}")
    
    print("\n执行打包命令...")
    print("="*60)
    print(f"命令预览: pyinstaller --onefile --windowed --name={exe_name} ...")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, cwd=os.getcwd(), text=True)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("✅ 打包成功!")
            
            exe_path = f'dist/{exe_name}.exe'
            if os.path.exists(exe_path):
                print(f"📁 可执行文件位置: {os.path.abspath(exe_path)}")
                print(f"📋 文件名: {exe_name}.exe")
                print(f"🔖 版本号: v{APP_VERSION}")
                
                # 显示文件大小
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"📊 文件大小: {size_mb:.1f} MB")
                
                print("\n📝 使用说明:")
                print("- ✅ 完全独立的可执行文件，无需安装Python")
                print("- ✅ 支持8种语言界面（简中、英、日、马来、韩、俄、西、繁中）")
                print("- ✅ 包含7个精美主题")
                print("- ✅ 可以直接分发给其他用户使用")  
                print("- ✅ 首次运行可能需要一些时间来解压")
                print("- ✅ 支持拖拽文件到编辑器窗口打开")
                print(f"- ✅ 支持命令行参数: {exe_name}.exe [文件路径]")
                
                # 快速测试
                print(f"\n🧪 快速测试: 双击 {exe_path} 验证是否正常启动")
                
            else:
                print("⚠️  exe文件未找到，构建可能未完全成功")
                return False
                
        else:
            print("\n" + "="*60)
            print("❌ 打包失败!")
            print("请检查上面的错误信息或运行以下命令获取详细日志:")
            print(f"pyinstaller {' '.join(cmd[1:])}")
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
    print(f"{APP_DISPLAY_NAME} v{APP_VERSION} 构建工具")
    print("="*60)
    
    success = build_exe()
    
    if success:
        print(f"\n🎉 {APP_DISPLAY_NAME} v{APP_VERSION} 打包完成!")
        print("="*60)
        print("\n📦 生成的文件包含:")
        print(f"  • {APP_NAME}-v{APP_VERSION}.exe (便携版)")
        print("  • 7个精美主题")
        print("  • 8种语言界面")
        print("  • 完整功能支持")
        print("\n💡 提示:")
        print(f"  • 要更新版本号，请修改 version.py 文件")
        print(f"  • 当前版本会自动从 version.py 读取")
    else:
        print(f"\n❌ {APP_DISPLAY_NAME} 打包过程中出现错误")
        print("="*60)
        sys.exit(1)

if __name__ == '__main__':
    main()