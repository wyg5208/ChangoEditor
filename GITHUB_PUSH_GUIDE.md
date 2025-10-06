# Chango Editor - GitHub推送完整指南

## 准备工作

### 1. 安装Git (如果尚未安装)
```bash
# 下载并安装Git for Windows
# 访问: https://git-scm.com/download/win
# 安装后重启终端
```

### 2. 验证Git安装
```bash
git --version
# 应该显示: git version 2.x.x.windows.x
```

## 步骤一：配置Git用户信息

```bash
# 配置全局用户名和邮箱 (只需配置一次)
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"

# 验证配置
git config --global user.name
git config --global user.email
```

## 步骤二：初始化Git仓库并添加文件

```bash
# 1. 确认当前在项目根目录
pwd
# 应该显示: D:\python_projects\changoeditor

# 2. 检查Git仓库状态
git status

# 3. 添加所有文件到暂存区
git add .

# 4. 检查哪些文件被添加 (查看.gitignore是否生效)
git status

# 5. 创建初始提交
git commit -m "Initial commit: Add Chango Editor v1.2.0

- Complete code editor with PyQt6
- Support for 20+ programming languages
- Dark/Light theme system
- File browser with tree view
- Find/Replace with regex support
- Toolbar with icons and tooltips
- Complete user guide and documentation"
```

## 步骤三：在GitHub上创建仓库

1. **登录GitHub**: https://github.com
2. **创建新仓库**:
   - 点击右上角 "+" → "New repository"
   - Repository name: `chango-editor` (推荐名称)
   - Description: `A powerful code editor similar to Sublime Text, built with Python and PyQt6`
   - 设置为 Public (开源项目)
   - **不要** 勾选 "Add a README file" (我们已经有了)
   - **不要** 勾选 "Add .gitignore" (我们已经配置了)
   - 选择 "MIT License" (如果需要)
3. **创建仓库**

## 步骤四：连接远程仓库并推送

GitHub会显示命令，类似于：

```bash
# 1. 添加远程仓库 (替换成你的用户名)
git remote add origin https://github.com/你的用户名/chango-editor.git

# 2. 验证远程仓库配置
git remote -v

# 3. 推送到主分支 (首次推送)
git push -u origin main

# 如果提示分支名称问题，可能需要重命名分支
git branch -M main
git push -u origin main
```

## 步骤五：身份验证

GitHub推送时需要身份验证，有两种方式：

### 方式A: Personal Access Token (推荐)
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → 勾选 "repo" 权限
3. 复制生成的token
4. 推送时用户名输入GitHub用户名，密码输入token

### 方式B: SSH密钥 (更安全)
```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 添加SSH密钥到GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出内容到 GitHub → Settings → SSH and GPG keys → New SSH key

# 使用SSH URL添加远程仓库
git remote set-url origin git@github.com:你的用户名/chango-editor.git
```

## 完整命令序列总结

假设您的GitHub用户名是 `yourname`：

```bash
# 1. 配置Git (首次使用)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. 初始化和提交
git add .
git commit -m "Initial commit: Add Chango Editor v1.2.0"

# 3. 连接GitHub仓库
git remote add origin https://github.com/yourname/chango-editor.git

# 4. 推送代码
git branch -M main
git push -u origin main
```

## 项目文件结构确认

推送后，GitHub上应该包含以下核心文件：
```
chango-editor/
├── src/                    # 源代码
├── resources/              # 资源文件  
├── test_files/             # 测试文件(示例)
├── tests/                  # 测试脚本
├── installer/              # 安装器配置
├── .gitignore             # Git忽略规则
├── README.md              # 项目说明
├── requirements.txt       # Python依赖
├── setup.py               # 安装脚本
├── run.py                 # 启动脚本
├── changoeditor.spec      # PyInstaller配置
├── build_exe.py           # 构建脚本
└── LICENSE                # 开源协议
```

## 后续操作

推送成功后，您可以：

1. **设置仓库描述和标签**
2. **创建Release版本**：上传编译好的exe文件
3. **添加项目截图**：更新README中的图片链接
4. **设置GitHub Pages**：如果有文档网站需求

## 常见问题

### 问题1: 推送失败 - 认证错误
**解决**: 使用Personal Access Token而不是密码

### 问题2: 文件太大
**解决**: 检查.gitignore是否正确忽略了build/dist目录

### 问题3: 仓库已存在
**解决**: 
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### 问题4: 分支名称问题
**解决**:
```bash
git branch -M main
git push -u origin main
```

完成推送后，您的Chango Editor项目就可以在GitHub上公开访问了！
