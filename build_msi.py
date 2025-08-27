#!/usr/bin/env python3
"""
Chango Editor MSI安装包构建脚本
支持使用cx_Freeze创建MSI安装包

使用方法：
1. 安装依赖：pip install cx_freeze
2. 运行脚本：python build_msi.py bdist_msi

注意：需要在Windows环境下运行
"""

import os
import sys
import shutil
import subprocess
from cx_Freeze import setup, Executable

# 应用信息
APP_NAME = "Chango Editor"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "功能强大的代码编辑器"
APP_AUTHOR = "Chango Team"
APP_URL = "https://github.com/aweng1977/chango/chango-editor"

def get_icon_path():
    """获取图标文件路径"""
    icon_paths = [
        'resources/icons/chango_editor.ico',
        'resources/icons/chango_editor.png',
        'resources/icons/chango_editor.svg'
    ]
    
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            return icon_path
    return None

def clean_build():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")

def prepare_build():
    """准备构建环境"""
    print("准备构建环境...")
    
    # 确保有可执行文件
    exe_path = "dist/ChangoEditor.exe"
    if not os.path.exists(exe_path):
        print("未找到 ChangoEditor.exe，正在构建...")
        result = subprocess.run([sys.executable, "build_exe.py"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"构建exe失败: {result.stderr}")
            return False
        print("exe构建完成")
    
    return True

# 包含的文件和目录
include_files = [
    # 主程序（如果存在预构建的exe）
    ("dist/ChangoEditor.exe", "ChangoEditor.exe"),
    # 许可证和说明文件
    ("LICENSE", "LICENSE.txt"),
    ("README.md", "README.txt"),
    # 示例文件
    ("test_files", "examples"),
    # 图标文件
]

# 添加图标文件（如果存在）
icon_file = get_icon_path()
if icon_file:
    include_files.append((icon_file, f"icons/{os.path.basename(icon_file)}"))

# 构建选项
build_exe_options = {
    "packages": ["PyQt6", "pygments", "watchdog", "chardet"],
    "excludes": ["tkinter", "unittest", "email", "html", "http", "json", "urllib", "xml"],
    "include_files": include_files,
    "build_exe": "build/exe",
    "optimize": 2,
    "include_msvcrt": True,
}

# MSI选项
bdist_msi_options = {
    "add_to_path": False,
    "initial_target_dir": f"[ProgramFilesFolder]\\{APP_NAME}",
    "install_icon": get_icon_path() or "",
    "summary_data": {
        "author": APP_AUTHOR,
        "comments": APP_DESCRIPTION,
        "keywords": "代码编辑器;编程;开发工具"
    },
    "target_name": f"ChangoEditor-Setup-v{APP_VERSION}.msi"
}

# 可执行文件定义
executables = [
    Executable(
        script="src/main.py",
        base="Win32GUI",  # Windows GUI应用
        target_name="ChangoEditor.exe",
        icon=get_icon_path(),
        shortcut_name=APP_NAME,
        shortcut_dir="DesktopFolder",
    )
]

def build_msi():
    """构建MSI安装包"""
    if not prepare_build():
        return False
    
    print("开始构建MSI安装包...")
    
    # 运行cx_Freeze构建
    setup(
        name=APP_NAME,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        author=APP_AUTHOR,
        url=APP_URL,
        options={
            "build_exe": build_exe_options,
            "bdist_msi": bdist_msi_options
        },
        executables=executables
    )

def create_advanced_msi():
    """创建高级MSI安装包（使用WiX工具链）"""
    print("创建高级MSI安装包...")
    
    # WiX源文件
    wxs_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" 
           Name="{APP_NAME}" 
           Language="2052" 
           Version="{APP_VERSION}" 
           Manufacturer="{APP_AUTHOR}" 
           UpgradeCode="{{12345678-1234-1234-1234-123456789012}}">
    
    <Package InstallerVersion="200" 
             Compressed="yes" 
             InstallScope="perUser" 
             Description="{APP_DESCRIPTION}" />
    
    <MajorUpgrade DowngradeErrorMessage="已安装更新版本的 {APP_NAME}。" />
    
    <MediaTemplate EmbedCab="yes" />
    
    <Feature Id="ProductFeature" Title="{APP_NAME}" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
      <ComponentRef Id="DesktopShortcut" />
      <ComponentRef Id="StartMenuShortcut" />
    </Feature>
    
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="LocalAppDataFolder">
        <Directory Id="INSTALLFOLDER" Name="{APP_NAME}" />
      </Directory>
      
      <Directory Id="DesktopFolder" Name="Desktop" />
      
      <Directory Id="ProgramMenuFolder" Name="Programs">
        <Directory Id="ApplicationProgramsFolder" Name="{APP_NAME}" />
      </Directory>
    </Directory>
    
    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <Component Id="MainExecutable" Guid="*">
        <File Id="ChangoEditorExe" 
              Source="dist\\ChangoEditor.exe" 
              KeyPath="yes" />
      </Component>
      
      <Component Id="LicenseFile" Guid="*">
        <File Id="LicenseFile" 
              Source="LICENSE" 
              Name="LICENSE.txt" 
              KeyPath="yes" />
      </Component>
      
      <Component Id="ReadmeFile" Guid="*">
        <File Id="ReadmeFile" 
              Source="README.md" 
              Name="README.txt" 
              KeyPath="yes" />
      </Component>
    </ComponentGroup>
    
    <Component Id="DesktopShortcut" Directory="DesktopFolder" Guid="*">
      <Shortcut Id="DesktopShortcut" 
                Name="{APP_NAME}" 
                Target="[INSTALLFOLDER]ChangoEditor.exe" 
                WorkingDirectory="INSTALLFOLDER" />
      <RemoveFolder Id="DesktopFolder" On="uninstall" />
      <RegistryValue Root="HKCU" 
                     Key="Software\\{APP_AUTHOR}\\{APP_NAME}" 
                     Name="installed" 
                     Type="integer" 
                     Value="1" 
                     KeyPath="yes" />
    </Component>
    
    <Component Id="StartMenuShortcut" Directory="ApplicationProgramsFolder" Guid="*">
      <Shortcut Id="StartMenuShortcut" 
                Name="{APP_NAME}" 
                Target="[INSTALLFOLDER]ChangoEditor.exe" 
                WorkingDirectory="INSTALLFOLDER" />
      <RemoveFolder Id="ApplicationProgramsFolder" On="uninstall" />
      <RegistryValue Root="HKCU" 
                     Key="Software\\{APP_AUTHOR}\\{APP_NAME}" 
                     Name="installed" 
                     Type="integer" 
                     Value="1" 
                     KeyPath="yes" />
    </Component>
    
  </Product>
</Wix>'''
    
    # 保存WiX源文件
    with open('installer/chango_editor.wxs', 'w', encoding='utf-8') as f:
        f.write(wxs_content)
    
    print("WiX源文件已创建: installer/chango_editor.wxs")
    print("要构建MSI，请使用WiX工具链:")
    print("1. 安装 WiX Toolset")
    print("2. 运行: candle installer/chango_editor.wxs")
    print("3. 运行: light chango_editor.wixobj -out ChangoEditor-Setup.msi")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
    elif len(sys.argv) > 1 and sys.argv[1] == "wix":
        create_advanced_msi()
    else:
        print(f"构建 {APP_NAME} MSI安装包")
        print("=" * 50)
        
        # 检查依赖
        try:
            import cx_Freeze
            print("✓ cx_Freeze 已安装")
        except ImportError:
            print("✗ 缺少 cx_Freeze，请运行: pip install cx_freeze")
            sys.exit(1)
        
        # 构建MSI
        if "bdist_msi" not in sys.argv:
            sys.argv.append("bdist_msi")
        
        build_msi()
        
        print("\n" + "=" * 50)
        print("MSI构建完成！")
        print("安装包位置: dist/")
        
        # 显示构建结果
        dist_files = os.listdir("dist") if os.path.exists("dist") else []
        msi_files = [f for f in dist_files if f.endswith('.msi')]
        if msi_files:
            for msi_file in msi_files:
                size = os.path.getsize(f"dist/{msi_file}") / (1024*1024)
                print(f"文件: {msi_file} ({size:.1f} MB)")
        else:
            print("未找到MSI文件，请检查构建日志")

