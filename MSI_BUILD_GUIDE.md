# Chango Editor MSI安装包打包指南 📦

**版本**: v1.3.4  
**更新日期**: 2025年10月6日

---

## 🎯 MSI安装包简介

MSI（Microsoft Installer）是Windows官方的安装包格式，具有以下优势：

- ✅ **企业级支持** - 支持组策略部署和静默安装
- ✅ **专业标准** - Windows官方推荐的安装包格式
- ✅ **卸载干净** - 自动管理注册表和文件清理
- ✅ **升级友好** - 支持原地升级，保留用户设置
- ✅ **数字签名** - 可添加数字证书，增强信任度

---

## 📋 方法一：使用 cx_Freeze（推荐）

这是最简单快速的方法，适合大多数情况。

### 步骤 1: 安装依赖

```bash
pip install cx_Freeze
```

### 步骤 2: 检查前提条件

确保已经构建了EXE文件：

```bash
# 如果还没有EXE，先构建
python build_exe.py
```

验证文件存在：
```bash
dir dist\ChangoEditor.exe
```

应该看到类似输出：
```
2025/10/06  ChangoEditor.exe  (约 36-40 MB)
```

### 步骤 3: 构建MSI安装包

```bash
python build_msi.py bdist_msi
```

**或者更简单地：**

```bash
python build_msi.py
```

脚本会自动添加 `bdist_msi` 参数。

### 步骤 4: 等待构建完成

构建过程大约需要 2-5 分钟，您会看到类似输出：

```
构建 Chango Editor MSI安装包
==================================================
✓ cx_Freeze 已安装
准备构建环境...
开始构建MSI安装包...
copying files to build\exe...
creating MSI installer...
building MSI installer...

==================================================
MSI构建完成！
安装包位置: dist/
文件: ChangoEditor-Setup-v1.3.4.msi (38.5 MB)
```

### 步骤 5: 找到安装包

MSI文件位于：
```
dist/ChangoEditor-Setup-v1.3.4.msi
```

---

## 📋 方法二：使用 WiX Toolset（高级）

这个方法可以创建更专业、更可定制的MSI安装包。

### 步骤 1: 安装 WiX Toolset

1. 访问 https://wixtoolset.org/
2. 下载并安装 WiX Toolset 3.x 或 4.x
3. 添加到系统PATH（通常会自动添加）

验证安装：
```bash
candle -?
light -?
```

### 步骤 2: 生成 WiX 源文件

```bash
python build_msi.py wix
```

这会创建：
```
installer/chango_editor.wxs
```

### 步骤 3: 编译 WiX 源文件

```bash
cd installer
candle chango_editor.wxs
```

生成 `chango_editor.wixobj`

### 步骤 4: 链接生成 MSI

```bash
light chango_editor.wixobj -out ChangoEditor-Setup-v1.3.4.msi
```

### 步骤 5: 添加图标（可选）

如果需要为MSI添加图标：

```bash
light chango_editor.wixobj ^
  -ext WixUIExtension ^
  -cultures:zh-CN ^
  -out ChangoEditor-Setup-v1.3.4.msi
```

---

## 🔧 常见问题解决

### 问题 1: "cx_Freeze 未安装"

**错误信息**:
```
✗ 缺少 cx_Freeze，请运行: pip install cx_freeze
```

**解决方法**:
```bash
pip install cx_Freeze
```

如果安装失败，尝试：
```bash
pip install --upgrade pip
pip install cx_Freeze --no-cache-dir
```

---

### 问题 2: "未找到 ChangoEditor.exe"

**错误信息**:
```
未找到 ChangoEditor.exe，正在构建...
```

**解决方法**:
先构建EXE文件：
```bash
python build_exe.py
```

---

### 问题 3: "模块导入错误"

**错误信息**:
```
ModuleNotFoundError: No module named 'PyQt6'
```

**解决方法**:
安装所有依赖：
```bash
pip install -r requirements.txt
```

---

### 问题 4: "权限不足"

**错误信息**:
```
PermissionError: [WinError 5] 拒绝访问
```

**解决方法**:
以管理员身份运行命令提示符或PowerShell：
1. 右键点击"命令提示符"或"PowerShell"
2. 选择"以管理员身份运行"
3. 切换到项目目录
4. 重新运行构建命令

---

### 问题 5: "WiX 命令未找到"

**错误信息**:
```
'candle' 不是内部或外部命令
```

**解决方法**:
1. 确认已安装 WiX Toolset
2. 添加到系统PATH：
   ```
   C:\Program Files (x86)\WiX Toolset v3.x\bin
   ```
3. 重启命令提示符

---

## 📊 构建参数说明

### cx_Freeze 参数

`build_msi.py` 支持以下参数：

```bash
# 标准构建
python build_msi.py bdist_msi

# 清理构建目录
python build_msi.py clean

# 生成WiX源文件
python build_msi.py wix
```

### 自定义选项

编辑 `build_msi.py` 可以自定义：

```python
# MSI选项
bdist_msi_options = {
    "add_to_path": False,  # 是否添加到PATH
    "initial_target_dir": f"[ProgramFilesFolder]\\{APP_NAME}",  # 安装目录
    "install_icon": get_icon_path() or "",  # 安装图标
    "target_name": f"ChangoEditor-Setup-v{APP_VERSION}.msi"  # 输出文件名
}
```

---

## 🎨 MSI安装包特性

### 安装选项

用户安装时可以选择：

1. **安装位置**
   - 默认：`C:\Program Files\Chango Editor`
   - 可自定义到任意位置

2. **快捷方式**
   - 桌面快捷方式
   - 开始菜单快捷方式

3. **文件关联**（如果配置）
   - 关联 .py, .txt 等文件类型

### 卸载功能

- Windows设置 → 应用 → Chango Editor → 卸载
- 或：控制面板 → 程序和功能 → Chango Editor → 卸载
- 自动清理所有文件和注册表项

### 升级支持

安装新版本时：
- 自动检测旧版本
- 提示是否升级
- 保留用户设置和主题

---

## 📦 完整构建流程示例

### 一键构建（从源码到MSI）

```bash
# 1. 清理旧文件
python build_msi.py clean

# 2. 安装/更新依赖
pip install -r requirements.txt
pip install cx_Freeze

# 3. 构建EXE（如果需要）
python build_exe.py

# 4. 构建MSI
python build_msi.py bdist_msi

# 5. 验证结果
dir dist\*.msi
```

### 分步构建（详细过程）

```bash
# 步骤1: 准备环境
echo "检查Python版本..."
python --version

echo "安装依赖..."
pip install cx_Freeze

# 步骤2: 构建主程序
echo "构建EXE..."
python build_exe.py

# 步骤3: 验证EXE
echo "测试EXE..."
dist\ChangoEditor.exe

# 步骤4: 构建MSI
echo "构建MSI安装包..."
python build_msi.py

# 步骤5: 测试安装
echo "MSI文件已生成，准备测试..."
```

---

## 🧪 测试 MSI 安装包

### 测试步骤

1. **双击MSI文件**
   ```
   dist\ChangoEditor-Setup-v1.3.4.msi
   ```

2. **跟随安装向导**
   - 欢迎页面
   - 许可协议
   - 选择安装位置
   - 确认安装

3. **验证安装**
   - 检查桌面快捷方式
   - 检查开始菜单
   - 运行程序
   - 测试所有功能

4. **测试卸载**
   - 控制面板 → 卸载程序
   - 卸载 Chango Editor
   - 验证文件已删除

### 静默安装测试

企业部署测试：

```bash
# 静默安装
msiexec /i ChangoEditor-Setup-v1.3.4.msi /quiet /norestart

# 静默卸载
msiexec /x ChangoEditor-Setup-v1.3.4.msi /quiet /norestart

# 安装到指定目录
msiexec /i ChangoEditor-Setup-v1.3.4.msi INSTALLDIR="D:\Apps\ChangoEditor" /quiet
```

---

## 📈 MSI vs EXE vs 便携版

### 对比表格

| 特性 | MSI安装包 | EXE单文件 | 便携版 |
|-----|----------|----------|--------|
| 文件大小 | 38-42 MB | 36-40 MB | 100-150 MB |
| 安装方式 | 安装向导 | 直接运行 | 解压即用 |
| 卸载 | Windows标准 | 无 | 删除文件夹 |
| 升级 | 原地升级 | 覆盖文件 | 重新解压 |
| 企业部署 | ✅ 支持 | ❌ 不支持 | ⚠️ 手动 |
| 数字签名 | ✅ 支持 | ✅ 支持 | ❌ 不适用 |
| 注册表 | ✅ 管理 | ❌ 不写入 | ❌ 不写入 |
| 多用户 | ✅ 支持 | ⚠️ 有限 | ⚠️ 有限 |
| 推荐场景 | 企业/正式发布 | 快速测试 | 临时使用 |

### 使用建议

**选择MSI当您需要**:
- 企业内部部署
- 正式软件发布
- 支持组策略管理
- 提供卸载功能
- 支持升级检测

**选择EXE当您需要**:
- 快速测试
- 个人使用
- 不希望安装
- 最小体积

**选择便携版当您需要**:
- U盘携带
- 不修改系统
- 多版本共存
- 开发测试

---

## 🔐 添加数字签名（可选）

### 为MSI添加数字签名

如果您有代码签名证书：

```bash
# 使用 signtool 签名
signtool sign /f "your_certificate.pfx" /p "password" /t "http://timestamp.digicert.com" ChangoEditor-Setup-v1.3.4.msi

# 验证签名
signtool verify /pa ChangoEditor-Setup-v1.3.4.msi
```

### 数字签名的好处

- ✅ 增强用户信任度
- ✅ 减少SmartScreen警告
- ✅ 验证软件来源
- ✅ 防止篡改

---

## 📋 打包检查清单

在发布MSI之前，请确认：

### 构建前检查
- [ ] 已更新版本号到 1.3.4
- [ ] 已更新 README.md
- [ ] 已更新"关于"对话框
- [ ] 已测试所有功能正常
- [ ] 已检查所有主题切换
- [ ] 已准备好图标文件

### 构建过程
- [ ] 已安装 cx_Freeze
- [ ] 已构建 EXE 文件
- [ ] MSI 构建成功
- [ ] 文件大小正常（38-42 MB）
- [ ] 无构建错误或警告

### 测试检查
- [ ] MSI 可以正常安装
- [ ] 程序启动无错误
- [ ] 所有功能正常工作
- [ ] 7个主题都能切换
- [ ] 快捷方式正确创建
- [ ] 可以正常卸载
- [ ] 卸载后文件清理干净

### 发布前检查
- [ ] 文件命名正确
- [ ] 版本号正确显示
- [ ] 添加到发布说明
- [ ] 准备更新日志
- [ ] 测试下载链接

---

## 🚀 快速开始（TL;DR）

如果您只想快速构建MSI，执行以下命令：

```bash
# 1. 安装依赖
pip install cx_Freeze

# 2. 构建MSI（一键完成）
python build_msi.py

# 3. 找到安装包
# 位置: dist\ChangoEditor-Setup-v1.3.4.msi
```

就这么简单！🎉

---

## 💡 高级技巧

### 1. 自动版本号

编辑 `build_msi.py`，从其他文件读取版本：

```python
# 从 main.py 读取版本
with open('src/main.py', 'r', encoding='utf-8') as f:
    for line in f:
        if 'setApplicationVersion' in line:
            APP_VERSION = line.split('"')[1]
            break
```

### 2. 多语言支持

在 `bdist_msi_options` 中添加：

```python
"languages": "2052;1033",  # 中文和英文
```

### 3. 自定义UI

使用 WiX 可以自定义安装界面：
- 添加欢迎页面图片
- 自定义许可协议
- 添加完成页面

---

## 📞 获取帮助

如果遇到问题：

1. **查看日志**
   ```bash
   # 详细日志模式
   python build_msi.py bdist_msi --verbose
   ```

2. **清理重试**
   ```bash
   python build_msi.py clean
   python build_msi.py bdist_msi
   ```

3. **检查依赖**
   ```bash
   pip list | findstr cx_Freeze
   pip list | findstr PyQt6
   ```

4. **社区支持**
   - GitHub Issues
   - Stack Overflow
   - cx_Freeze 文档

---

**祝您打包顺利！** 🎊  
**有任何问题随时联系！** 📧

---

*Chango Editor v1.3.4 - 专业MSI打包指南* 📦

