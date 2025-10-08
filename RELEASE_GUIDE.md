# Chango Editor 发布指南

## 📦 如何发布新版本到 GitHub Releases

### 为什么使用 GitHub Releases？

✅ **推荐使用 GitHub Releases 发布 EXE 和 MSI 文件**，而不是直接提交到 Git 仓库：

1. **不占用仓库空间** - 二进制文件单独存储，不影响克隆速度
2. **版本管理清晰** - 每个版本的下载文件独立管理
3. **下载统计** - GitHub 提供下载次数统计
4. **CDN 加速** - GitHub 自动提供全球 CDN 下载加速
5. **自动生成下载链接** - 方便用户直接下载

---

## 🚀 发布步骤

### 步骤 1: 构建发布文件

```bash
# 1. 构建 EXE 文件
python build_exe.py

# 2. 构建 MSI 安装包
python build_msi.py

# 构建完成后，文件位置：
# - dist/ChangoEditor.exe  (约 36.4 MB)
# - installer/output/ChangoEditor-1.4.0.msi  (约 40 MB)
```

### 步骤 2: 创建 Git 标签

```bash
# 1. 确保所有更改已提交
git add .
git commit -m "Release v1.4.0 - 完整国际化支持"

# 2. 创建并推送标签
git tag -a v1.4.0 -m "v1.4.0 - 8种语言国际化支持"
git push origin v1.4.0

# 或者推送所有标签
git push --tags
```

### 步骤 3: 在 GitHub 创建 Release

#### 方法 1: 使用 GitHub 网页界面（推荐）

1. **访问仓库 Releases 页面**
   ```
   https://github.com/wyg5208/changoeditor/releases
   ```

2. **点击 "Create a new release"**

3. **填写 Release 信息**：
   - **Tag**: 选择刚创建的 `v1.4.0`（或创建新标签）
   - **Release title**: `Chango Editor v1.4.0 - 完整国际化支持`
   - **Description**: 复制 `CHANGELOG_v1.4.0.md` 的内容

4. **上传二进制文件**：
   - 拖拽或点击上传 `dist/ChangoEditor.exe`
   - 拖拽或点击上传 `installer/output/ChangoEditor-1.4.0.msi`

5. **发布选项**：
   - ✅ 勾选 "Set as the latest release"
   - ✅ 勾选 "Create a discussion for this release" (可选)

6. **点击 "Publish release"**

#### 方法 2: 使用 GitHub CLI（需要安装 gh）

```bash
# 安装 GitHub CLI (如果未安装)
# Windows: winget install GitHub.cli
# 或下载: https://cli.github.com/

# 登录 GitHub
gh auth login

# 创建 Release 并上传文件
gh release create v1.4.0 \
  --title "Chango Editor v1.4.0 - 完整国际化支持" \
  --notes-file CHANGELOG_v1.4.0.md \
  dist/ChangoEditor.exe \
  installer/output/ChangoEditor-1.4.0.msi

# 如果要设为最新版本
gh release create v1.4.0 \
  --title "Chango Editor v1.4.0 - 完整国际化支持" \
  --notes-file CHANGELOG_v1.4.0.md \
  --latest \
  dist/ChangoEditor.exe \
  installer/output/ChangoEditor-1.4.0.msi
```

---

## 📝 Release 描述模板

```markdown
# 🌍 Chango Editor v1.4.0 - 完整国际化支持

## 🎉 重大更新

v1.4.0 版本带来了完整的国际化支持，现在 Chango Editor 支持 8 种语言界面！

## 🌐 支持的语言

- 🇨🇳 简体中文 (zh_CN)
- 🇺🇸 English (en_US)
- 🇯🇵 日本語 (ja_JP)
- 🇲🇾 Bahasa Melayu (ms_MY)
- 🇰🇷 한국어 (ko_KR)
- 🇷🇺 Русский (ru_RU)
- 🇪🇸 Español (es_ES)
- 🇹🇼 繁體中文 (zh_TW)

## ✨ 新增功能

- ✅ 实时语言切换（无需重启）
- ✅ 智能系统语言检测
- ✅ 1160+ 翻译文本完整覆盖
- ✅ 状态栏 + 菜单栏双重切换入口

## 📦 下载选项

| 文件 | 大小 | 说明 |
|------|------|------|
| **ChangoEditor.exe** | ~36.4 MB | 独立可执行文件，解压即用 |
| **ChangoEditor-1.4.0.msi** | ~40 MB | Windows 安装包，完整安装体验 |

## 🔧 安装说明

### 使用 EXE 文件（绿色版）
1. 下载 `ChangoEditor.exe`
2. 双击运行，无需安装
3. 首次运行会自动检测系统语言

### 使用 MSI 安装包（推荐）
1. 下载 `ChangoEditor-1.4.0.msi`
2. 双击运行安装向导
3. 安装到指定目录
4. 自动创建开始菜单快捷方式

## 📋 系统要求

- Windows 10/11 (64位)
- 无需安装 Python 或其他依赖

## 🐛 已知问题

- 无

## 📖 完整更新日志

查看详细更新内容：[CHANGELOG_v1.4.0.md](https://github.com/wyg5208/changoeditor/blob/main/CHANGELOG_v1.4.0.md)

---

**⭐ 如果喜欢这个项目，请给我们一个 Star！**
```

---

## 🔄 更新现有 Release

如果需要更新已发布的 Release：

### 使用网页界面
1. 访问 Release 页面
2. 点击 Release 右侧的编辑按钮（铅笔图标）
3. 上传新文件或修改说明
4. 点击 "Update release"

### 使用 GitHub CLI
```bash
# 删除旧的文件资源
gh release delete-asset v1.4.0 ChangoEditor.exe --yes

# 上传新文件
gh release upload v1.4.0 dist/ChangoEditor.exe

# 或者先删除整个 release，再重新创建
gh release delete v1.4.0 --yes
gh release create v1.4.0 [参数...]
```

---

## 📊 查看下载统计

```bash
# 查看 Release 下载统计
gh release view v1.4.0

# 查看所有 Releases
gh release list
```

---

## ⚠️ 注意事项

1. **文件大小限制**: GitHub Release 单个文件最大 2GB
2. **命名规范**: 
   - 标签：`v1.4.0`（小写v + 版本号）
   - 文件：`ChangoEditor-1.4.0.msi`（带版本号）
3. **版本号规则**: 遵循 [语义化版本](https://semver.org/lang/zh-CN/)
   - 主版本号.次版本号.修订号 (MAJOR.MINOR.PATCH)
   - 例如：1.4.0 → 1.4.1（修复）或 1.5.0（新功能）

4. **不要直接提交二进制文件到 Git**:
   ```bash
   # .gitignore 应该包含：
   dist/
   *.exe
   *.msi
   ```

---

## 🎯 下载链接格式

发布后，用户可以通过以下链接下载：

```
# 最新版本（自动跳转）
https://github.com/wyg5208/changoeditor/releases/latest

# 特定版本
https://github.com/wyg5208/changoeditor/releases/tag/v1.4.0

# 直接下载文件
https://github.com/wyg5208/changoeditor/releases/download/v1.4.0/ChangoEditor.exe
https://github.com/wyg5208/changoeditor/releases/download/v1.4.0/ChangoEditor-1.4.0.msi
```

---

## 📚 更多资源

- [GitHub Releases 官方文档](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [GitHub CLI 文档](https://cli.github.com/manual/gh_release)
- [语义化版本规范](https://semver.org/lang/zh-CN/)

---

**祝发布顺利！** 🚀

