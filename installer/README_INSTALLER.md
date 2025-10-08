# Chango Editor 安装包构建指南

本目录包含为 Chango Editor 创建 Windows 安装包的各种脚本和配置文件。

## 🛠️ 支持的安装包格式

### 1. Inno Setup (推荐) ⭐
- **文件**: `chango_editor_setup.iss`
- **优点**: 功能强大、免费、易于定制
- **特性**: 中文界面、文件关联、自动卸载旧版本
- **工具**: [Inno Setup](https://jrsoftware.org/isinfo.php)

### 2. NSIS (轻量级)
- **文件**: `chango_editor_nsis.nsi`
- **优点**: 轻量级、开源、高度可定制
- **特性**: 现代UI、组件选择、多语言支持
- **工具**: [NSIS](https://nsis.sourceforge.io/)

### 3. MSI (企业级)
- **文件**: `build_msi.py`、`chango_editor.wxs`
- **优点**: Windows原生、企业部署友好
- **特性**: Group Policy支持、无人值守安装
- **工具**: [cx_Freeze](https://pypi.org/project/cx-freeze/) 或 [WiX Toolset](https://wixtoolset.org/)

## 🚀 快速开始

### 推荐方式：使用自动化脚本
```bash
# 一键构建 EXE + MSI
python quick_release.py

# 或单独构建
python build_exe.py    # 便携版 EXE
python build_msi.py    # MSI 安装包
```

### 手动构建

#### Inno Setup
1. 下载安装 [Inno Setup](https://jrsoftware.org/isinfo.php)
2. 右键点击 `chango_editor_setup.iss` → "Compile"
3. 或命令行: `"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" chango_editor_setup.iss`

#### NSIS
1. 下载安装 [NSIS](https://nsis.sourceforge.io/)
2. 右键点击 `chango_editor_nsis.nsi` → "Compile NSIS Script"
3. 或命令行: `"C:\Program Files (x86)\NSIS\makensis.exe" chango_editor_nsis.nsi`

#### MSI
1. 安装依赖: `pip install cx_freeze`
2. 运行: `python build_msi.py bdist_msi`
3. 或使用 WiX: `python build_msi.py wix`

## 📁 文件说明

### 脚本文件
- `../build_exe.py` - 便携版 EXE 构建脚本 (PyInstaller)
- `../build_msi.py` - MSI 安装包构建脚本 (cx_Freeze)
- `../quick_release.py` - 自动化发布脚本 (推荐使用)
- `chango_editor_setup.iss` - Inno Setup 安装脚本 (可选)
- `chango_editor_nsis.nsi` - NSIS 安装脚本 (可选)

### 辅助文件
- `install_info.txt` - 安装前信息页面
- `install_complete.txt` - 安装完成页面
- `wizard_image.bmp` - 安装向导大图 (可选)
- `wizard_small.bmp` - 安装向导小图 (可选)

## ✨ 安装包特性

### 共同特性
- ✅ 一键安装/卸载
- ✅ 自定义安装路径
- ✅ 桌面和开始菜单快捷方式
- ✅ 文件关联 (.py, .js 等)
- ✅ 卸载时完全清理
- ✅ 中文安装界面

### Inno Setup 特色
- 📋 许可协议展示
- 🔄 自动检测并卸载旧版本
- 📊 安装前后信息页面
- 🎨 现代化安装界面
- 🗂️ 组件选择 (示例文件、文件关联等)

### NSIS 特色
- 🏗️ 安装类型选择 (完整/最小)
- 📝 详细的组件描述
- 🎯 精确的注册表操作
- 💾 安装大小估算

### MSI 特色
- 🏢 企业部署支持
- 📋 Group Policy 兼容
- 🔧 Windows Installer 标准
- 🛡️ 数字签名支持 (需配置)

## 📋 系统要求

### 运行要求
- Windows 7 SP1 或更高版本
- 64位操作系统
- 至少 100MB 可用磁盘空间

### 构建要求
- Python 3.8+
- 已构建的 ChangoEditor.exe
- 相应的构建工具 (Inno Setup/NSIS/WiX)

## 🔧 自定义配置

### 修改应用信息
编辑各脚本文件的头部变量:
- 应用名称、版本号
- 发布者信息
- 许可证文件路径
- 图标文件路径

### 添加文件关联
在注册表部分添加新的文件类型:
```iss
; 示例：关联 .html 文件
Root: HKCU; Subkey: "SOFTWARE\Classes\.html\OpenWithProgids"; ValueType: string; ValueName: "ChangoEditor.html"; ValueData: "";
```

### 自定义界面
- 替换 `wizard_image.bmp` (164x314 像素)
- 替换 `wizard_small.bmp` (55x58 像素)
- 修改 `install_info.txt` 和 `install_complete.txt`

## 🐛 故障排除

### 常见问题

**Q: 构建时提示找不到 ChangoEditor.exe**
A: 先运行 `python build_exe.py` 构建主程序

**Q: Inno Setup 报编码错误**
A: 确保 .iss 文件保存为 UTF-8 编码

**Q: MSI 构建失败**
A: 检查是否安装了 cx_freeze: `pip install cx_freeze`

**Q: 安装包无法运行**
A: 检查目标系统是否满足运行要求，尝试"以管理员身份运行"

### 调试技巧
1. 查看构建日志中的错误信息
2. 使用 `/LOG` 参数获取详细安装日志
3. 检查文件路径是否正确
4. 验证所有依赖文件是否存在

## 📞 获取帮助

- **项目主页**: https://github.com/aweng1977/chango/chango-editor
- **问题报告**: https://github.com/aweng1977/chango/chango-editor/issues
- **工具文档**: 
  - [Inno Setup 文档](https://jrsoftware.org/ishelp/)
  - [NSIS 文档](https://nsis.sourceforge.io/Docs/)
  - [WiX 文档](https://wixtoolset.org/documentation/)

## 📄 许可证

本安装包构建脚本与 Chango Editor 使用相同的 MIT 许可证。
