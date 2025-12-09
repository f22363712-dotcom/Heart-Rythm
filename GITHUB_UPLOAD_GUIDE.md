# GitHub代码上传指南

本指南详细说明如何将本地代码上传到GitHub仓库，适用于Windows、macOS和Linux系统。

## 一、准备工作

### 1. 安装Git

- **Windows**：从 [Git官网](https://git-scm.com/download/win) 下载安装程序，按照默认选项安装即可。
- **macOS**：使用Homebrew安装：`brew install git`，或从 [Git官网](https://git-scm.com/download/mac) 下载安装包。
- **Linux**：使用包管理器安装，如Ubuntu/Debian：`sudo apt-get install git`，CentOS/RHEL：`sudo yum install git`。

### 2. 创建GitHub账号

如果还没有GitHub账号，访问 [GitHub官网](https://github.com/) 注册一个。

### 3. 创建GitHub仓库

1. 登录GitHub后，点击右上角的「+」按钮，选择「New repository」。
2. 填写仓库信息：
   - **Repository name**：输入仓库名称（如：Heart-Rythm）
   - **Description**：（可选）输入仓库描述
   - **Visibility**：选择「Public」（公开）或「Private」（私有）
   - 不要勾选「Initialize this repository with a README」（我们将手动添加）
3. 点击「Create repository」按钮创建仓库。

## 二、本地操作

### 1. 初始化Git仓库

在本地项目目录中打开命令行终端，执行以下命令：

```bash
git init
```

这将在当前目录创建一个 `.git` 隐藏目录，用于跟踪版本控制。

### 2. 配置Git用户信息

执行以下命令配置你的Git用户名和邮箱（使用你GitHub账号的用户名和邮箱）：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

### 3. 创建.gitignore文件

`.gitignore` 文件用于指定Git应忽略的文件和目录，避免将不必要的文件上传到GitHub。

在项目根目录创建 `.gitignore` 文件，添加以下内容（根据项目需要调整）：

```gitignore
# 依赖目录
__pycache__/
*.py[cod]
*$py.class

# 构建和打包目录
build/
dist/
*.spec

# PyInstaller相关文件
*.manifest
*.toc

# 数据目录（根据需要调整）
data/

# IDE相关
.idea/
.vscode/
*.swp
*.swo
*~

# 操作系统文件
.DS_Store
Thumbs.db

# 日志文件
*.log

# 临时文件
*.tmp
*.temp

# 虚拟环境
venv/
*.venv/
env/
.env/

# 敏感信息
.env
*.key
*.pem

# 测试覆盖率
.coverage
coverage.xml
htmlcov/
```

### 4. 添加文件到暂存区

执行以下命令将所有文件添加到Git暂存区：

```bash
git add .
```

如果只想添加特定文件，可以使用：

```bash
git add 文件名
```

### 5. 提交代码

执行以下命令提交代码到本地仓库，同时添加提交信息：

```bash
git commit -m "提交信息"
```

提交信息应简洁明了，描述本次提交的主要内容，如：

```bash
git commit -m "完成核心功能开发，添加文档和GUI支持"
```

## 三、连接GitHub仓库

### 1. 获取GitHub仓库URL

在GitHub仓库页面，点击「Code」按钮，复制仓库的HTTPS或SSH URL。

- HTTPS URL示例：`https://github.com/用户名/仓库名.git`
- SSH URL示例：`git@github.com:用户名/仓库名.git`

### 2. 添加远程仓库

执行以下命令将本地仓库与GitHub远程仓库关联：

```bash
git remote add origin 你的GitHub仓库URL
```

例如：

```bash
git remote add origin https://github.com/f22363712-dotcom/Heart-Rythm.git
```

### 3. 推送到GitHub

执行以下命令将本地代码推送到GitHub远程仓库的main分支：

```bash
git push -u origin main
```

第一次推送时需要输入GitHub账号的用户名和密码（或个人访问令牌）。

## 四、后续操作

### 1. 更新本地代码后推送到GitHub

当你修改了本地代码后，执行以下命令更新GitHub仓库：

```bash
git add .
git commit -m "更新描述"
git push origin main
```

### 2. 从GitHub拉取最新代码

如果其他成员更新了GitHub仓库，执行以下命令拉取最新代码：

```bash
git pull origin main
```

### 3. 查看Git状态

执行以下命令查看当前Git仓库的状态：

```bash
git status
```

### 4. 查看提交历史

执行以下命令查看提交历史：

```bash
git log
```

## 五、常见问题及解决方案

### 1. 推送时出现权限错误

**问题**：`remote: Permission to 用户名/仓库名.git denied to 旧用户名.`

**解决方案**：
- 检查Git用户配置是否正确
- 重新输入GitHub账号的用户名和密码（或个人访问令牌）
- 如果使用SSH URL，检查SSH密钥是否正确配置

### 2. 推送时出现冲突

**问题**：`error: failed to push some refs to 'https://github.com/用户名/仓库名.git'`

**解决方案**：
- 先拉取最新代码：`git pull origin main`
- 解决冲突（IDE会提示冲突文件，手动修改）
- 再次提交并推送：`git add . && git commit -m "解决冲突" && git push origin main`

### 3. 忘记添加.gitignore文件

**解决方案**：
- 创建.gitignore文件
- 执行以下命令更新：
  ```bash
  git rm -r --cached .
  git add .
  git commit -m "添加.gitignore文件"
  git push origin main
  ```

## 六、最佳实践

1. **定期提交**：每次完成一个功能或修复一个bug后，及时提交代码
2. **编写清晰的提交信息**：提交信息应简洁明了，描述本次提交的主要内容
3. **使用.gitignore文件**：避免将不必要的文件上传到GitHub
4. **分支管理**：使用分支开发新功能，完成后合并到主分支
5. **定期拉取代码**：避免与其他成员的代码冲突

## 七、GitHub Desktop（可选）

如果你不喜欢使用命令行，可以使用GitHub Desktop客户端，这是一个可视化的Git管理工具：

1. 下载并安装 [GitHub Desktop](https://desktop.github.com/)
2. 登录GitHub账号
3. 克隆仓库或添加本地仓库
4. 使用可视化界面进行提交、推送等操作

## 八、参考资源

- [Git官方文档](https://git-scm.com/doc)
- [GitHub官方指南](https://docs.github.com/en/get-started)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**作者**：Heart-Rythm项目组  
**更新日期**：2025-12-09  
**版本**：1.0