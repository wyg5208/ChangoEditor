#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chango Editor 快速发布脚本
自动构建 EXE 和 MSI，并准备 GitHub Release
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

# 设置 UTF-8 编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 版本配置
VERSION = "1.4.0"
TAG = f"v{VERSION}"
RELEASE_TITLE = f"Chango Editor v{VERSION} - 完整国际化支持"

# 文件路径
EXE_FILE = Path("dist/ChangoEditor.exe")
MSI_FILE = Path(f"installer/output/ChangoEditor-{VERSION}.msi")
CHANGELOG_FILE = Path("CHANGELOG_v1.4.0.md")

def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{'='*70}")
    print(f"步骤 {step}: {message}")
    print('='*70)

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n🔧 {description}...")
    print(f"命令: {cmd}")
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        text=True,
        encoding='utf-8',
        errors='ignore'  # 忽略无法解码的字符
    )
    
    if result.returncode != 0:
        print(f"❌ 失败: {result.stderr}")
        return False
    else:
        print(f"✅ 成功")
        if result.stdout:
            print(result.stdout)
    return True

def check_files():
    """检查必要文件是否存在"""
    print_step(1, "检查文件")
    
    files_to_check = {
        "build_exe.py": "EXE构建脚本",
        "build_msi.py": "MSI构建脚本",
        "CHANGELOG_v1.4.0.md": "更新日志"
    }
    
    all_exist = True
    for file, desc in files_to_check.items():
        if Path(file).exists():
            print(f"  ✅ {desc}: {file}")
        else:
            print(f"  ❌ {desc}缺失: {file}")
            all_exist = False
    
    return all_exist

def build_exe():
    """构建 EXE 文件"""
    print_step(2, "构建 EXE 文件")
    
    if not run_command("python build_exe.py", "构建 EXE"):
        return False
    
    if EXE_FILE.exists():
        size_mb = EXE_FILE.stat().st_size / (1024 * 1024)
        print(f"\n✅ EXE 文件已创建: {EXE_FILE}")
        print(f"   大小: {size_mb:.1f} MB")
        return True
    else:
        print(f"\n❌ EXE 文件未找到: {EXE_FILE}")
        return False

def build_msi():
    """构建 MSI 安装包"""
    print_step(3, "构建 MSI 安装包")
    
    if not run_command("python build_msi.py", "构建 MSI"):
        return False
    
    if MSI_FILE.exists():
        size_mb = MSI_FILE.stat().st_size / (1024 * 1024)
        print(f"\n✅ MSI 文件已创建: {MSI_FILE}")
        print(f"   大小: {size_mb:.1f} MB")
        return True
    else:
        print(f"\n❌ MSI 文件未找到: {MSI_FILE}")
        return False

def prepare_release_package():
    """准备发布包"""
    print_step(4, "准备发布包")
    
    # 创建 release 目录
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # 复制文件
    files_to_copy = []
    
    if EXE_FILE.exists():
        dest = release_dir / EXE_FILE.name
        shutil.copy2(EXE_FILE, dest)
        print(f"  ✅ 复制: {EXE_FILE.name}")
        files_to_copy.append(dest)
    
    if MSI_FILE.exists():
        dest = release_dir / MSI_FILE.name
        shutil.copy2(MSI_FILE, dest)
        print(f"  ✅ 复制: {MSI_FILE.name}")
        files_to_copy.append(dest)
    
    if CHANGELOG_FILE.exists():
        dest = release_dir / CHANGELOG_FILE.name
        shutil.copy2(CHANGELOG_FILE, dest)
        print(f"  ✅ 复制: {CHANGELOG_FILE.name}")
    
    print(f"\n📦 发布包已准备在: {release_dir.absolute()}")
    return files_to_copy

def show_github_instructions(files):
    """显示 GitHub Release 说明"""
    print_step(5, "GitHub Release 发布说明")
    
    print("""
📋 使用 GitHub 网页界面发布（推荐）:

1. 访问仓库 Releases 页面:
   https://github.com/wyg5208/changoeditor/releases

2. 点击 "Create a new release"

3. 填写信息:
   - Tag: v1.4.0
   - Title: Chango Editor v1.4.0 - 完整国际化支持
   - Description: 复制 CHANGELOG_v1.4.0.md 的内容

4. 上传文件（拖拽到 "Attach binaries" 区域）:
""")
    
    for file in files:
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"   - {file.name} ({size_mb:.1f} MB)")
    
    print("""
5. 勾选 "Set as the latest release"

6. 点击 "Publish release"

---

🔧 或使用 GitHub CLI 发布:

   gh release create v1.4.0 \\
     --title "Chango Editor v1.4.0 - 完整国际化支持" \\
     --notes-file CHANGELOG_v1.4.0.md \\
     --latest \\
     release/ChangoEditor.exe \\
     release/ChangoEditor-1.4.0.msi

---

📥 发布后的下载链接:

   最新版本: https://github.com/wyg5208/changoeditor/releases/latest
   特定版本: https://github.com/wyg5208/changoeditor/releases/tag/v1.4.0
   
   直接下载:
   - EXE: https://github.com/wyg5208/changoeditor/releases/download/v1.4.0/ChangoEditor.exe
   - MSI: https://github.com/wyg5208/changoeditor/releases/download/v1.4.0/ChangoEditor-1.4.0.msi
""")

def main():
    """主函数"""
    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           Chango Editor v{VERSION} 快速发布脚本                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    try:
        # 检查文件
        if not check_files():
            print("\n❌ 缺少必要文件，请检查！")
            return 1
        
        # 询问是否继续
        print("\n⚠️  准备构建 EXE 和 MSI 文件...")
        response = input("继续吗? (y/n): ").strip().lower()
        if response != 'y':
            print("已取消")
            return 0
        
        # 构建 EXE
        if not build_exe():
            print("\n❌ EXE 构建失败")
            return 1
        
        # 构建 MSI
        if not build_msi():
            print("\n❌ MSI 构建失败")
            return 1
        
        # 准备发布包
        files = prepare_release_package()
        
        # 显示说明
        show_github_instructions(files)
        
        print(f"\n{'='*70}")
        print("✅ 所有构建步骤完成！")
        print("📦 请按照上述说明在 GitHub 上创建 Release")
        print('='*70)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        return 1
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

