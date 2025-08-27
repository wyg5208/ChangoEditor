#!/usr/bin/env python3
"""
Chango Editor PyInstaller 打包脚本
自动化打包成独立exe文件
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

def create_spec_file():
    """创建 PyInstaller spec 文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
project_root = os.path.dirname(os.path.abspath(SPECPATH))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

block_cipher = None

# 数据文件 - 包含主题、图标等资源
datas = [
    ('resources/themes/*.json', 'resources/themes'),
    ('resources/icons/*.svg', 'resources/icons'),
]

# 隐藏导入 - 确保所有模块都被包含
hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'pygments',
    'pygments.lexers',
    'pygments.formatters',
    'chardet',
    'watchdog',
    'watchdog.observers',
    'watchdog.events',
]

a = Analysis(
    ['src/main.py'],
    pathex=[src_path],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ChangoEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/chango_editor.ico'  # 如果有ico文件
)
'''
    
    with open('changoeditor.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("已创建 changoeditor.spec 文件")

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
            images[0].save(png_path, format='PNG')
            print(f"已生成PNG图标: {png_path}")
            
            # 保存为ICO文件，包含多种尺寸
            images[0].save(
                ico_path, 
                format='ICO', 
                sizes=[(img.width, img.height) for img in images]
            )
            print(f"已生成ICO图标: {ico_path}")
            
            return True
            
    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请运行: pip install pillow cairosvg")
    except Exception as e:
        print(f"图标转换失败: {e}")
        import traceback
        traceback.print_exc()
    
    return False

def build_exe():
    """构建exe文件"""
    print("开始构建 Chango Editor 可执行文件...")
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    # 创建spec文件
    create_spec_file()
    
    # 尝试转换图标
    convert_svg_to_ico()
    
    # 使用PyInstaller构建 - 分步添加数据文件以避免通配符问题
    cmd = [
        'pyinstaller',
        '--onefile',           # 单文件模式
        '--windowed',          # 无控制台模式
        '--name=ChangoEditor', # 可执行文件名
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=pygments',
        '--hidden-import=pygments.lexers',
        '--hidden-import=pygments.formatters',
        '--hidden-import=chardet',
        '--hidden-import=watchdog',
        '--hidden-import=watchdog.observers',
        '--hidden-import=watchdog.events',
        '--paths=src',         # 添加src目录到Python路径
        'src/main.py'
    ]
    
    # 添加主题文件
    theme_files = ['resources/themes/dark.json', 'resources/themes/light.json']
    for theme_file in theme_files:
        if os.path.exists(theme_file):
            cmd.extend(['--add-data', f'{theme_file};resources/themes'])
    
    # 添加图标文件 - 包含SVG、PNG、ICO格式
    icon_files = [
        'resources/icons/chango_editor.svg',
        'resources/icons/chango_editor.png', 
        'resources/icons/chango_editor.ico'
    ]
    
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            cmd.extend(['--add-data', f'{icon_file};resources/icons'])
            print(f"添加图标文件: {icon_file}")
    
    # 如果有ico文件，添加图标
    ico_path = 'resources/icons/chango_editor.ico'
    if os.path.exists(ico_path):
        cmd.extend(['--icon', ico_path])
    
    print("执行打包命令...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\\n✅ 打包成功!")
        print(f"可执行文件位置: {os.path.abspath('dist/ChangoEditor.exe')}")
        
        # 显示文件大小
        exe_path = 'dist/ChangoEditor.exe'
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"文件大小: {size_mb:.1f} MB")
        
        print("\\n📝 使用说明:")
        print("- 可执行文件是完全独立的，无需安装Python")
        print("- 可以直接分发给其他用户使用")
        print("- 首次运行可能需要一些时间来解压")
        
    else:
        print("❌ 打包失败!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False
    
    return True

if __name__ == '__main__':
    success = build_exe()
    if success:
        print("\\n🎉 Chango Editor 打包完成!")
    else:
        print("\\n❌ 打包过程中出现错误")
        sys.exit(1)
