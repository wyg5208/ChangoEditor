# Chango Editor 🚀

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.9+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/yourusername/chango-editor)
[![Version](https://img.shields.io/badge/Version-1.3.4-brightgreen.svg)](https://github.com/yourusername/chango-editor/releases)

一个强大的类似于 Sublime Text 的代码编辑器，基于 Python 和 PyQt6 构建，提供完整的代码编辑体验。

## 🎨 v1.3.4 主题系统扩展 (最新)
- 🌈 **5个新主题** - Deep Blue、Light Yellow、Ocean、Forest、Monokai
- 📁 **零代码配置** - 只需添加JSON文件即可创建新主题
- 🎯 **场景化配色** - 专业开发、护眼阅读、创意设计等多场景覆盖
- 🔧 **完整文档** - 详细的主题创建和使用指南
- 🚀 **实时切换** - 菜单即时切换，无需重启

## 📁 v1.3.3 打开文件夹功能
- 📂 **打开文件夹功能** - 新增"打开文件夹"到文件浏览器，快捷键Ctrl+Shift+O
- 📏 **路径区优化** - 路径显示高度增加50%，避免滚动条遮挡文字
- 🎨 **工具栏新增** - 添加文件夹图标按钮，与打开文件功能并列
- ⚡ **快速切换** - 一键切换工作目录，提升浏览效率

## 🗂️ v1.3.2 文件浏览器改进
- 🎨 **图标风格统一** - 4个按钮全部改用SVG矢量图标，与工具栏风格一致
- 📁 **路径完整显示** - 添加横向滚动条，完整显示文件路径无截断
- 🖱️ **路径可复制** - 路径文本可选择和复制，方便使用
- 🎯 **专业美观** - 整体视觉风格统一，提升专业度

## 🎨 v1.3.1 图标系统优化
- 📏 **尺寸优化** - 图标尺寸调整为18×18像素，界面更紧凑
- 🌈 **彩色快捷图标** - 新增"全选+复制"彩色组合图标，一键完成两步操作
- 🎯 **视觉层次** - 彩色图标突出重要快捷功能，易于识别
- ⚡ **效率提升** - Ctrl+Shift+C快速全选并复制所有内容

## 🚀 v1.3.0 图标系统全面升级
- 🎨 **专业图标库** - 采用Font Awesome风格SVG矢量图标
- 📐 **矢量图标** - 任意缩放无损，支持HiDPI/Retina显示器
- 🎭 **主题适配** - 图标颜色自动匹配主题，无缝切换
- 🔧 **易于扩展** - 模块化设计，方便添加自定义图标

## 🎯 v1.2.0 UI现代化升级 
- 🎨 **工具栏全面图标化** - 中文文字改为直观图标，支持工具提示显示快捷键
- 📁 **文件浏览器增强** - 新增展开/收起全部功能，一键管理文件夹视图
- 💡 **智能工具提示系统** - 所有按钮悬停显示功能名称和快捷键说明
- 🌍 **界面国际化升级** - 现代化专业设计，符合国际软件标准
- 📖 **完整使用指南** - 帮助菜单新增使用说明，详细的HTML格式用户手册

## 🔄 v1.1.8 手动刷新功能
- 🔲 **手动刷新按钮** - 在文件浏览区添加"刷新"按钮，解决首次保存后未刷新的问题

## 📚 历史版本亮点
- **v1.1.7** 🔄 智能文件浏览区刷新 + 💾 文件类型记忆功能
- **v1.1.6** 🔧 路径更新BUG修复
- **v1.1.5** 📝 文件名实时同步 + 💾 智能保存传递
- **v1.1.4** ⚡ 综合功能增强（TAB名称、路径提示等）
- **v1.1.3** 🔧 精细化修复（对话框布局、保存同步）
- **v1.1.2** 🎨 界面优化（全局主题一致性）
- **v1.1.1** 🔧 重要修复（文件树导航、撤销功能）
- **v1.1.0** 🎉 新功能（树形浏览器、文件拖拽、工具栏增强）

![Chango Editor Screenshot](docs/screenshot.png)

## ✨ 主要功能

### 🎨 **智能主题系统**
- 深色/明亮主题无缝切换
- 实时主题应用，无需重启
- 自定义主题配置

### 📝 **强大的编辑功能**
- 支持 20+ 种编程语言的语法高亮
- 智能代码缩进和自动补全
- 多标签页管理，支持拖拽排序
- 撤销/重做系统

### 🔍 **高级搜索替换**
- 正则表达式支持
- 大小写敏感/全词匹配
- 统计搜索结果和当前位置
- 循环搜索提示

### 📁 **文件管理**
- 🆕 树形文件浏览器（支持展开/折叠）
- 🆕 文件拖拽打开（支持批量操作）
- 智能文件编码检测
- 文件模板系统
- 自动保存和恢复

### ⚡ **快捷操作**
- 🎯 **图标化工具栏** - 直观的图标界面，支持工具提示和快捷键显示
- ⌨️ **完整快捷键支持** - 所有功能都有对应的快捷键
- 📁 **智能文件管理** - 一键展开/收起全部文件夹，快速导航
- 📊 **实时状态反馈** - 状态栏显示操作结果和文件信息
- 🖱️ **右键上下文菜单** - 文件和标签页的快捷操作菜单

## 🚀 快速开始

### 方式1: 下载可执行文件 (推荐)

1. 前往 [Releases](https://github.com/yourusername/chango-editor/releases) 页面
2. 下载最新版本的 `ChangoEditor.exe` (36.4 MB)
3. 双击运行，无需安装任何依赖

### 方式2: 源码运行

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/chango-editor.git
cd chango-editor
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **运行编辑器**
```bash
python run.py
```

## 📋 系统要求

### EXE 版本 (推荐)
- Windows 10/11
- 无其他依赖

### 源码版本
- Python 3.11+
- PyQt6 6.9+
- Windows/Linux/macOS

## 🎮 使用指南

### 快捷键参考

| 功能 | 快捷键 | 描述 |
|------|--------|------|
| 新建文件 | `Ctrl+N` | 创建新的空白文件 |
| 打开文件 | `Ctrl+O` | 打开现有文件 |
| 保存文件 | `Ctrl+S` | 保存当前文件 |
| 另存为 | `Ctrl+Shift+S` | 另存为新文件 |
| 关闭当前文件 | `Ctrl+W` | 关闭当前标签页 |
| 关闭所有文件 | `Ctrl+Shift+W` | 关闭所有标签页 |
| 撤销 | `Ctrl+Z` | 撤销上一操作 |
| 重做 | `Ctrl+Y` | 重做操作 |
| 查找 | `Ctrl+F` | 在当前文件中查找 |
| 替换 | `Ctrl+H` | 查找并替换 |
| 全选 | `Ctrl+A` | 选择全部内容 |
| 清除 | `Ctrl+Delete` | 清除当前编辑器所有内容 |

### 使用指南
- 菜单栏 → **帮助** → **使用说明** 查看详细用户手册
- 完整的HTML格式指南，包含所有功能介绍和操作技巧
- 在默认浏览器中打开，便于阅读和收藏

### 主题切换
- 菜单栏 → **主题** → 选择 "深色主题" 或 "明亮主题"
- 支持实时切换，立即生效

### 工具栏功能
- 🎯 **图标化设计** - 所有按钮使用直观图标，鼠标悬停显示功能和快捷键
- 📄📂💾 **文件操作** - 新建、打开、保存等基础功能
- ↶↷🗑️ **编辑操作** - 撤销、重做、清除等编辑功能
- 📋📰🔘 **文本操作** - 复制、粘贴、全选等文本处理
- 🔍🔄 **查找替换** - 强大的搜索和替换功能

### 文件浏览器
- ⬆️ **上级目录** - 快速返回上一级目录
- 🔄 **手动刷新** - 刷新文件列表，检测外部变更
- ⬇️ **展开全部** - 一键展开所有文件夹
- ⬆️ **收起全部** - 一键收起所有文件夹，保持界面整洁

### 语法高亮支持
Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, PHP, Ruby, Shell, SQL, HTML, CSS, XML, JSON, YAML, Markdown, 等20+种语言

## 🛠️ 开发与构建

### 项目结构
```
changoeditor/
├── src/                    # 源代码
│   ├── core/              # 核心功能模块
│   │   ├── editor.py      # 文本编辑器核心
│   │   ├── document.py    # 文档管理
│   │   └── ...
│   ├── ui/                # 用户界面模块
│   │   ├── main_window.py # 主窗口
│   │   ├── tab_widget.py  # 标签页管理
│   │   └── ...
│   ├── utils/             # 工具模块
│   │   ├── syntax.py      # 语法高亮
│   │   ├── themes.py      # 主题管理
│   │   └── ...
│   └── main.py            # 程序入口
├── resources/             # 资源文件
│   ├── themes/           # 主题配置
│   └── icons/            # 图标文件
├── test_files/           # 测试文件
├── docs/                 # 项目文档
├── dist/                 # 打包输出目录
├── requirements.txt      # Python 依赖
├── setup.py             # 安装脚本
├── build_exe.py         # EXE 打包脚本
└── run.py               # 启动脚本
```

### 开发状态

- ✅ **核心架构**: 完整的编辑器框架
- ✅ **文本编辑**: 语法高亮、撤销重做
- ✅ **文件管理**: 多标签页、树形文件浏览器
- ✅ **搜索替换**: 正则表达式、统计功能
- ✅ **主题系统**: 深色/明亮主题切换
- ✅ **图标化界面**: 现代化工具栏设计
- ✅ **智能文件操作**: 拖拽、展开/收起、刷新
- ✅ **用户指南**: 完整的HTML使用手册
- ✅ **EXE 打包**: 独立可执行文件

### 构建 EXE 文件

```bash
# 安装打包依赖
pip install pyinstaller

# 运行打包脚本
python build_exe.py

# 输出文件: dist/ChangoEditor.exe
```

## 🐛 问题反馈

如果您遇到任何问题或有功能建议，请：

1. 查看 [已知问题](https://github.com/wyg5208/ChangoEditor/issues)
2. 提交新的 [Issue](https://github.com/wyg5208/ChangoEditor/issues/new)
3. 提供详细的错误信息和重现步骤

## 🤝 参与贡献

我们欢迎所有形式的贡献！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 🌟 致谢

- [PyQt6](https://pypi.org/project/PyQt6/) - 强大的 GUI 框架
- [Pygments](https://pygments.org/) - 语法高亮引擎
- [Sublime Text](https://www.sublimetext.com/) - 设计灵感来源

## 📧 联系方式

- **项目主页**: https://github.com/wyg5208/ChangoEditor
- **问题反馈**: https://github.com/wyg5208/ChangoEditor/issues
- **版本发布**: https://github.com/wyg5208/ChangoEditor/releases

---

**⭐ 如果这个项目对您有帮助，请考虑给一个 Star！**
