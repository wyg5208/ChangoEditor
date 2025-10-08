#!/usr/bin/env python3
"""
Chango Editor 自动部署到 Madechango 网站
自动同步静态文件和可执行文件到生产环境

使用方法：
1. 在 changoeditor 项目根目录运行
2. python deploy_to_madechango.py

功能：
- 自动将 docs/user_guide.html 部署到 madechango 静态目录
- 自动创建并部署 index.html 下载页面
- 自动同步 dist/ChangoEditor.exe 到下载目录
- 自动备份原有文件
- 详细的日志输出

更新时间: 2025年10月6日
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

# 配置区域
CONFIG = {
    # Chango Editor 项目路径
    'changoeditor_root': r'D:\python_projects\changoeditor',
    
    # Madechango 项目路径
    'madechango_root': r'D:\python_projects\madechango',
    
    # 目标路径
    'target_static': r'D:\python_projects\madechango\app\static\changoeditor',
    'target_download': r'D:\python_projects\madechango\app\static\changoeditor\download',
    
    # 版本信息（从 README.md 读取）
    'version': '1.3.5',  # 最新版本
    
    # 备份目录
    'backup_dir': r'D:\python_projects\changoeditor\backups'
}

class DeployManager:
    """部署管理器"""
    
    def __init__(self):
        self.config = CONFIG
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def log(self, message, level='INFO'):
        """输出日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        prefix = {
            'INFO': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'SUCCESS': '🎉'
        }.get(level, 'ℹ️')
        print(f"[{timestamp}] {prefix} {message}")
    
    def ensure_dir(self, path):
        """确保目录存在"""
        Path(path).mkdir(parents=True, exist_ok=True)
        self.log(f"确保目录存在: {path}")
    
    def backup_file(self, file_path):
        """备份文件"""
        if not os.path.exists(file_path):
            return None
            
        backup_dir = os.path.join(self.config['backup_dir'], self.timestamp)
        self.ensure_dir(backup_dir)
        
        filename = os.path.basename(file_path)
        backup_path = os.path.join(backup_dir, filename)
        
        shutil.copy2(file_path, backup_path)
        self.log(f"备份文件: {filename} -> {backup_path}", 'INFO')
        return backup_path
    
    def get_file_hash(self, file_path):
        """计算文件MD5哈希值"""
        if not os.path.exists(file_path):
            return None
            
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()
    
    def get_file_size_mb(self, file_path):
        """获取文件大小（MB）"""
        if not os.path.exists(file_path):
            return 0
        return os.path.getsize(file_path) / (1024 * 1024)
    
    def read_version_from_readme(self):
        """从 README.md 读取版本号"""
        readme_path = os.path.join(self.config['changoeditor_root'], 'README.md')
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if 'Version' in line and 'badge' in line:
                        # 匹配 [![Version](https://img.shields.io/badge/Version-1.3.4-brightgreen.svg)]
                        import re
                        match = re.search(r'Version-(\d+\.\d+\.\d+)', line)
                        if match:
                            return match.group(1)
        except Exception as e:
            self.log(f"读取版本号失败: {e}", 'WARNING')
        return self.config['version']
    
    def create_index_html(self):
        """创建下载页面 index.html"""
        version = self.read_version_from_readme()
        
        # 读取 README.md 获取更新内容
        readme_path = os.path.join(self.config['changoeditor_root'], 'README.md')
        update_notes = []
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取最新版本的更新内容
                lines = content.split('\n')
                in_latest = False
                for line in lines:
                    if f'v{version}' in line or 'v1.3.5' in line:
                        in_latest = True
                    elif in_latest:
                        if line.startswith('##') and 'v1.3' not in line:
                            break
                        if line.startswith('-'):
                            update_notes.append(line)
        except Exception as e:
            self.log(f"读取更新说明失败: {e}", 'WARNING')
        
        # 生成 HTML 内容
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chango Editor - 强大的代码编辑器</title>
    <meta name="description" content="Chango Editor 是一个功能强大的类似于 Sublime Text 的代码编辑器，支持20+种编程语言，7个精美主题，完全免费开源。">
    <meta name="keywords" content="代码编辑器,文本编辑器,Chango Editor,免费编辑器,开源编辑器,Python编辑器">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .version {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .header .tagline {{
            font-size: 1.3em;
            opacity: 0.95;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .download-section {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            text-align: center;
            color: white;
        }}
        
        .download-button {{
            display: inline-block;
            background: white;
            color: #f5576c;
            padding: 18px 50px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.3em;
            font-weight: bold;
            margin: 20px 10px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .download-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        
        .download-button.secondary {{
            background: transparent;
            color: white;
            border: 2px solid white;
        }}
        
        .file-info {{
            margin-top: 20px;
            font-size: 0.95em;
            opacity: 0.9;
        }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        
        .feature-card {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .feature-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        .feature-card ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .feature-card li {{
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .feature-card li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
        }}
        
        .update-notes {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
        }}
        
        .update-notes h3 {{
            color: #856404;
            margin-bottom: 15px;
        }}
        
        .update-notes ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .update-notes li {{
            padding: 8px 0;
            color: #856404;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        .badges {{
            margin: 20px 0;
        }}
        
        .badges img {{
            margin: 5px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .download-button {{
                display: block;
                margin: 10px 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Chango Editor</h1>
            <div class="version">v{version}</div>
            <div class="tagline">功能强大的代码编辑器 · 支持20+语言 · 7个精美主题</div>
            <div class="badges">
                <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
                <img src="https://img.shields.io/badge/PyQt6-6.9+-green.svg" alt="PyQt6">
                <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
                <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Platform">
            </div>
        </div>
        
        <div class="content">
            <div class="download-section">
                <h2>📥 立即下载</h2>
                <p>完全免费 · 无需安装Python · 开箱即用</p>
                
                <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin: 20px 0;">
                    <a href="download/ChangoEditor.exe" class="download-button" download>
                        🚀 便携版 (EXE)
                    </a>
                    <a href="download/ChangoEditor-Setup-v{version}.msi" class="download-button" download>
                        💾 安装包 (MSI)
                    </a>
                </div>
                
                <a href="user-guide.html" class="download-button secondary" style="margin-top: 10px;">
                    📖 查看使用指南
                </a>
                
                <div class="file-info" style="margin-top: 30px;">
                    <div style="text-align: left; max-width: 600px; margin: 0 auto;">
                        <h4 style="margin-bottom: 15px; color: white;">💡 版本说明</h4>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                            <strong>🚀 便携版 (EXE)</strong>
                            <ul style="margin: 8px 0 0 20px; text-align: left;">
                                <li>大小: ~36 MB</li>
                                <li>无需安装，双击即用</li>
                                <li>适合临时使用或U盘携带</li>
                                <li>首次启动需要解压（几秒钟）</li>
                            </ul>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                            <strong>💾 安装包 (MSI)</strong>
                            <ul style="margin: 8px 0 0 20px; text-align: left;">
                                <li>大小: ~40 MB</li>
                                <li>标准Windows安装程序</li>
                                <li>自动创建桌面快捷方式</li>
                                <li>支持完全卸载，推荐长期使用</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="file-info" style="margin-top: 20px;">
                    <div>🖥️ 系统要求: Windows 10/11</div>
                    <div>🔄 更新时间: {datetime.now().year}年{datetime.now().month}月{datetime.now().day}日</div>
                </div>
            </div>
            
            {'<div class="update-notes"><h3>🎉 最新更新 (v' + version + ')</h3><ul>' + ''.join(f'<li>{note}</li>' for note in update_notes[:10]) + '</ul></div>' if update_notes else ''}
            
            <h2 style="margin: 40px 0 20px 0; color: #333;">✨ 主要特性</h2>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🎨 智能主题系统</h3>
                    <ul>
                        <li>7个精美主题</li>
                        <li>深色/明亮模式</li>
                        <li>实时切换</li>
                        <li>自定义配置</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>📝 强大编辑功能</h3>
                    <ul>
                        <li>20+语言语法高亮</li>
                        <li>智能代码缩进</li>
                        <li>多标签页管理</li>
                        <li>撤销/重做系统</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>🔍 高级搜索替换</h3>
                    <ul>
                        <li>正则表达式支持</li>
                        <li>大小写敏感</li>
                        <li>全词匹配</li>
                        <li>循环搜索</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>📁 文件管理</h3>
                    <ul>
                        <li>树形文件浏览器</li>
                        <li>文件拖拽打开</li>
                        <li>智能编码检测</li>
                        <li>文件模板系统</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #e7f3ff; padding: 25px; border-radius: 10px; margin-top: 40px;">
                <h3 style="color: #0066cc; margin-bottom: 15px;">⚡ 快速开始</h3>
                <ol style="padding-left: 20px; color: #333;">
                    <li style="margin: 10px 0;">下载 <code style="background: white; padding: 2px 8px; border-radius: 3px;">ChangoEditor.exe</code></li>
                    <li style="margin: 10px 0;">双击运行（首次启动可能需要几秒钟）</li>
                    <li style="margin: 10px 0;">开始编写代码！无需任何配置</li>
                </ol>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Chango Editor</strong> - 开源免费的代码编辑器</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/wyg5208/ChangoEditor" target="_blank">GitHub 项目主页</a> · 
                <a href="https://github.com/wyg5208/ChangoEditor/issues" target="_blank">问题反馈</a> · 
                <a href="user-guide.html">使用指南</a>
            </p>
            <p style="margin-top: 15px; font-size: 0.9em;">
                © 2025 Chango Editor · MIT License
            </p>
        </div>
    </div>
</body>
</html>'''
        
        return html_content
    
    def deploy(self):
        """执行部署"""
        self.log("="*60)
        self.log("开始部署 Chango Editor 到 Madechango 网站", 'INFO')
        self.log("="*60)
        
        # 1. 确保目标目录存在
        self.ensure_dir(self.config['target_static'])
        self.ensure_dir(self.config['target_download'])
        
        # 2. 部署 user_guide.html
        source_guide = os.path.join(self.config['changoeditor_root'], 'docs', 'user_guide.html')
        target_guide = os.path.join(self.config['target_static'], 'user-guide.html')
        
        if os.path.exists(source_guide):
            self.backup_file(target_guide)
            shutil.copy2(source_guide, target_guide)
            self.log(f"✅ 部署使用指南: user-guide.html", 'SUCCESS')
        else:
            self.log(f"源文件不存在: {source_guide}", 'ERROR')
        
        # 3. 创建并部署 index.html
        index_content = self.create_index_html()
        target_index = os.path.join(self.config['target_static'], 'index.html')
        
        self.backup_file(target_index)
        with open(target_index, 'w', encoding='utf-8') as f:
            f.write(index_content)
        self.log(f"✅ 创建下载页面: index.html", 'SUCCESS')
        
        # 4. 部署 ChangoEditor.exe
        source_exe = os.path.join(self.config['changoeditor_root'], 'dist', 'ChangoEditor.exe')
        target_exe = os.path.join(self.config['target_download'], 'ChangoEditor.exe')
        
        if os.path.exists(source_exe):
            # 检查文件是否有变化
            source_hash = self.get_file_hash(source_exe)
            target_hash = self.get_file_hash(target_exe)
            
            if source_hash != target_hash:
                self.backup_file(target_exe)
                shutil.copy2(source_exe, target_exe)
                size_mb = self.get_file_size_mb(target_exe)
                self.log(f"✅ 部署可执行文件: ChangoEditor.exe ({size_mb:.1f} MB)", 'SUCCESS')
                self.log(f"   MD5: {source_hash}", 'INFO')
            else:
                self.log(f"⏭️  可执行文件未变化，跳过部署", 'INFO')
        else:
            self.log(f"源文件不存在: {source_exe}", 'ERROR')
            self.log(f"请先运行 build_exe.py 构建可执行文件", 'WARNING')
        
        # 5. 部署 MSI 安装包
        version = self.read_version_from_readme()
        source_msi = os.path.join(self.config['changoeditor_root'], 'dist', f'ChangoEditor-Setup-v{version}.msi')
        target_msi = os.path.join(self.config['target_download'], f'ChangoEditor-Setup-v{version}.msi')
        
        if os.path.exists(source_msi):
            # 检查文件是否有变化
            source_hash = self.get_file_hash(source_msi)
            target_hash = self.get_file_hash(target_msi)
            
            if source_hash != target_hash:
                self.backup_file(target_msi)
                shutil.copy2(source_msi, target_msi)
                size_mb = self.get_file_size_mb(target_msi)
                self.log(f"✅ 部署MSI安装包: ChangoEditor-Setup-v{version}.msi ({size_mb:.1f} MB)", 'SUCCESS')
                self.log(f"   MD5: {source_hash}", 'INFO')
            else:
                self.log(f"⏭️  MSI安装包未变化，跳过部署", 'INFO')
        else:
            self.log(f"⚠️  MSI文件不存在: {source_msi}", 'WARNING')
            self.log(f"   如需MSI安装包，请运行: python build_msi.py", 'INFO')
        
        # 6. 生成部署报告
        self.generate_report()
        
        self.log("="*60)
        self.log("部署完成！", 'SUCCESS')
        self.log("="*60)
        
        # 7. 显示访问地址
        version = self.read_version_from_readme()
        self.log("\n📍 访问地址:", 'INFO')
        self.log("   本地: http://madechango.com/static/changoeditor/", 'INFO')
        self.log("   线上: https://madechango.com/static/changoeditor/", 'INFO')
        self.log("\n📖 使用指南:", 'INFO')
        self.log("   http://madechango.com/static/changoeditor/user-guide.html", 'INFO')
        self.log("\n📥 下载地址:", 'INFO')
        self.log("   EXE便携版: http://madechango.com/static/changoeditor/download/ChangoEditor.exe", 'INFO')
        self.log(f"   MSI安装包: http://madechango.com/static/changoeditor/download/ChangoEditor-Setup-v{version}.msi", 'INFO')
    
    def generate_report(self):
        """生成部署报告"""
        report_path = os.path.join(self.config['changoeditor_root'], 'DEPLOYMENT_REPORT.md')
        
        version = self.read_version_from_readme()
        
        now = datetime.now()
        report_content = f"""# Chango Editor 部署报告

**部署时间**: {now.year}年{now.month}月{now.day}日 {now.hour:02d}:{now.minute:02d}:{now.second:02d}  
**版本号**: v{version}

## 部署内容

### 1. 静态文件
- ✅ index.html - 下载页面
- ✅ user-guide.html - 使用指南

**目标目录**: `{self.config['target_static']}`

### 2. 可执行文件
- ✅ ChangoEditor.exe（便携版）
- ✅ ChangoEditor-Setup-v{version}.msi（安装包）

**目标目录**: `{self.config['target_download']}`

## 访问地址

### 生产环境
- **主页**: https://madechango.com/static/changoeditor/
- **使用指南**: https://madechango.com/static/changoeditor/user-guide.html
- **EXE便携版**: https://madechango.com/static/changoeditor/download/ChangoEditor.exe
- **MSI安装包**: https://madechango.com/static/changoeditor/download/ChangoEditor-Setup-v{version}.msi

### 测试环境
- **主页**: http://madechango.com/static/changoeditor/
- **使用指南**: http://madechango.com/static/changoeditor/user-guide.html
- **EXE便携版**: http://madechango.com/static/changoeditor/download/ChangoEditor.exe
- **MSI安装包**: http://madechango.com/static/changoeditor/download/ChangoEditor-Setup-v{version}.msi

## 文件清单

| 文件 | 大小 | 说明 |
|------|------|------|
| index.html | ~15 KB | 下载页面 |
| user-guide.html | ~50 KB | 使用指南 |
| ChangoEditor.exe | ~36 MB | EXE便携版 |
| ChangoEditor-Setup-v{version}.msi | ~40 MB | MSI安装包 |

## Nginx 配置

当前 nginx.conf 已正确配置静态文件服务，无需修改。

```nginx
location /static/ {{
    alias D:/python_projects/madechango/app/static/;
    expires 30d;
    add_header Cache-Control "public";
}}
```

访问规则：
- `/static/changoeditor/` → `D:/python_projects/madechango/app/static/changoeditor/`
- 自动提供目录索引（如果启用）
- 缓存时间：30天

## 下次部署

只需在 changoeditor 项目目录运行：

```bash
python deploy_to_madechango.py
```

脚本会自动：
1. 检查文件变化
2. 备份原有文件
3. 同步最新文件
4. 生成部署报告

## 备份位置

备份目录: `{self.config['backup_dir']}/{self.timestamp}/`

---

**注意**: 此报告由自动部署脚本生成
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.log(f"\n📄 部署报告已生成: {report_path}", 'INFO')

def main():
    """主函数"""
    try:
        manager = DeployManager()
        manager.deploy()
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  部署已取消")
        return 1
    except Exception as e:
        print(f"\n❌ 部署失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

