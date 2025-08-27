#!/usr/bin/env python3
"""
Chango Editor 统一安装包构建脚本
支持多种安装包格式：Inno Setup (ISS)、NSIS、WiX MSI

使用方法：
python build_installer.py [inno|nsis|msi|all]

依赖工具：
- Inno Setup: https://jrsoftware.org/isinfo.php
- NSIS: https://nsis.sourceforge.io/
- WiX Toolset: https://wixtoolset.org/
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

class InstallerBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.installer_dir = self.project_root / "installer"
        self.installer_output_dir = self.dist_dir / "installer"
        
        # 确保目录存在
        self.installer_dir.mkdir(exist_ok=True)
        self.installer_output_dir.mkdir(parents=True, exist_ok=True)
    
    def check_exe_exists(self):
        """检查主程序exe是否存在"""
        exe_path = self.dist_dir / "ChangoEditor.exe"
        if not exe_path.exists():
            print("❌ 未找到 ChangoEditor.exe")
            print("请先运行: python build_exe.py")
            return False
        
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ 找到主程序: {exe_path} ({size_mb:.1f} MB)")
        return True
    
    def find_tool(self, tool_name, possible_paths):
        """查找构建工具"""
        for path in possible_paths:
            full_path = Path(path)
            if full_path.exists():
                print(f"✓ 找到 {tool_name}: {full_path}")
                return str(full_path)
        
        print(f"❌ 未找到 {tool_name}")
        return None
    
    def build_inno_setup(self):
        """构建 Inno Setup 安装包"""
        print("\n📦 构建 Inno Setup 安装包...")
        
        # 查找 Inno Setup 编译器
        inno_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe",
            r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
            r"C:\Program Files\Inno Setup 5\ISCC.exe",
        ]
        
        iscc_path = self.find_tool("Inno Setup", inno_paths)
        if not iscc_path:
            print("请下载安装 Inno Setup: https://jrsoftware.org/isinfo.php")
            return False
        
        # 构建命令
        iss_file = self.installer_dir / "chango_editor_setup.iss"
        if not iss_file.exists():
            print(f"❌ 未找到脚本文件: {iss_file}")
            return False
        
        cmd = [iscc_path, str(iss_file)]
        
        try:
            print(f"执行: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=str(self.project_root), 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Inno Setup 构建成功!")
                return True
            else:
                print(f"❌ 构建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 执行失败: {e}")
            return False
    
    def build_nsis(self):
        """构建 NSIS 安装包"""
        print("\n📦 构建 NSIS 安装包...")
        
        # 查找 NSIS 编译器
        nsis_paths = [
            r"C:\Program Files (x86)\NSIS\makensis.exe",
            r"C:\Program Files\NSIS\makensis.exe",
        ]
        
        makensis_path = self.find_tool("NSIS", nsis_paths)
        if not makensis_path:
            print("请下载安装 NSIS: https://nsis.sourceforge.io/")
            return False
        
        # 构建命令
        nsi_file = self.installer_dir / "chango_editor_nsis.nsi"
        if not nsi_file.exists():
            print(f"❌ 未找到脚本文件: {nsi_file}")
            return False
        
        cmd = [makensis_path, str(nsi_file)]
        
        try:
            print(f"执行: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=str(self.project_root),
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ NSIS 构建成功!")
                return True
            else:
                print(f"❌ 构建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 执行失败: {e}")
            return False
    
    def build_msi(self):
        """构建 MSI 安装包"""
        print("\n📦 构建 MSI 安装包...")
        
        try:
            # 方法1: 使用 cx_Freeze
            print("尝试使用 cx_Freeze...")
            result = subprocess.run([sys.executable, "build_msi.py", "bdist_msi"], 
                                  cwd=str(self.project_root),
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ cx_Freeze MSI 构建成功!")
                return True
            else:
                print(f"cx_Freeze 构建失败: {result.stderr}")
                
        except Exception as e:
            print(f"cx_Freeze 执行失败: {e}")
        
        # 方法2: 生成 WiX 源文件
        print("生成 WiX 源文件...")
        try:
            result = subprocess.run([sys.executable, "build_msi.py", "wix"],
                                  cwd=str(self.project_root),
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ WiX 源文件生成成功!")
                print("要完成MSI构建，请:")
                print("1. 安装 WiX Toolset: https://wixtoolset.org/")
                print("2. 运行: candle installer/chango_editor.wxs")
                print("3. 运行: light chango_editor.wixobj -out ChangoEditor-Setup.msi")
                return True
            else:
                print(f"WiX 源文件生成失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"WiX 生成失败: {e}")
            return False
    
    def show_results(self):
        """显示构建结果"""
        print("\n" + "="*60)
        print("📋 构建结果总结")
        print("="*60)
        
        output_dir = self.installer_output_dir
        if output_dir.exists():
            files = list(output_dir.glob("*"))
            if files:
                print(f"📁 安装包位置: {output_dir}")
                for file in files:
                    if file.is_file():
                        size_mb = file.stat().st_size / (1024 * 1024)
                        print(f"  📦 {file.name} ({size_mb:.1f} MB)")
            else:
                print("❌ 未找到生成的安装包文件")
        else:
            print("❌ 输出目录不存在")
        
        print("\n💡 使用提示:")
        print("• 安装包可以直接分发给用户")
        print("• 用户无需安装Python或其他依赖")
        print("• 支持自定义安装路径和组件选择")
        print("• 包含卸载程序，可完全清理")

def main():
    parser = argparse.ArgumentParser(description="Chango Editor 安装包构建工具")
    parser.add_argument("type", nargs="?", default="all",
                       choices=["inno", "nsis", "msi", "all"],
                       help="安装包类型 (default: all)")
    parser.add_argument("--clean", action="store_true",
                       help="清理构建目录")
    
    args = parser.parse_args()
    
    builder = InstallerBuilder()
    
    if args.clean:
        print("🧹 清理构建目录...")
        if builder.installer_output_dir.exists():
            shutil.rmtree(builder.installer_output_dir)
            print(f"已清理: {builder.installer_output_dir}")
        return
    
    print("🚀 Chango Editor 安装包构建工具")
    print("="*60)
    
    # 检查前提条件
    if not builder.check_exe_exists():
        return
    
    # 构建安装包
    success_count = 0
    total_count = 0
    
    if args.type in ["inno", "all"]:
        total_count += 1
        if builder.build_inno_setup():
            success_count += 1
    
    if args.type in ["nsis", "all"]:
        total_count += 1
        if builder.build_nsis():
            success_count += 1
    
    if args.type in ["msi", "all"]:
        total_count += 1
        if builder.build_msi():
            success_count += 1
    
    # 显示结果
    builder.show_results()
    
    print(f"\n🎉 构建完成: {success_count}/{total_count} 成功")
    
    if success_count == 0:
        print("\n❌ 所有构建都失败了，请检查:")
        print("• 是否安装了相应的构建工具")
        print("• 是否存在必要的源文件")
        print("• 查看上面的错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()

