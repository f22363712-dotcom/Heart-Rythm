# Git使用指南

## 1. Git简介

Git是一个分布式版本控制系统，专为高效管理各种规模的项目而设计。它可以追踪代码的变更历史，支持多人协作开发，并且允许开发者在不同的分支上进行工作。

## 2. Git下载与安装

### 2.1 Windows系统

1. 访问官方网站：[https://git-scm.com/download/win](https://git-scm.com/download/win)
2. 下载最新版本的Git安装程序
3. 运行安装程序，按照默认选项一路点击"Next"即可完成安装
4. 安装完成后，可以通过右键点击桌面，选择"Git Bash Here"打开Git命令行窗口

### 2.2 macOS系统

1. 使用Homebrew安装（推荐）：
   ```bash
   brew install git
   ```
2. 或者从官方网站下载安装包：[https://git-scm.com/download/mac](https://git-scm.com/download/mac)

### 2.3 Linux系统

Ubuntu/Debian：
```bash
sudo apt update
sudo apt install git
```

CentOS/RHEL：
```bash
sudo yum install git
```

Fedora：
```bash
sudo dnf install git
```

## 3. 首次配置Git

安装完成后，需要配置用户信息，这将用于标识你的提交：

```bash
# 设置用户名
git config --global user.name "你的用户名"

# 设置邮箱
git config --global user.email "你的邮箱@example.com"

# 可选：设置默认分支名为main
git config --global init.defaultBranch main

# 可选：启用彩色输出
git config --global color.ui true
```

## 4. 心动积分项目Git工作流程

### 4.1 克隆项目仓库

在你的计算机上选择一个目录，打开Git Bash（Windows）或终端（macOS/Linux），执行以下命令：

```bash
# 克隆远程仓库（替换为实际的仓库URL）
git clone https://github.com/你的用户名/心动积分项目.git

# 进入项目目录
cd 心动积分项目
```

### 4.2 创建虚拟环境

请参考项目中的虚拟环境使用指南，在本地创建并激活虚拟环境：

```bash
# 创建虚拟环境
python -m venv .venv

# Windows PowerShell激活
.\.venv\Scripts\Activate.ps1

# Windows CMD激活
.venv\Scripts\activate.bat

# macOS/Linux激活
source .venv/bin/activate

# 安装项目依赖
pip install -r requirements.txt
```

### 4.3 日常开发流程

1. **更新本地代码**
   在开始工作前，先拉取远程仓库的最新代码：
   ```bash
   git pull origin main
   ```

2. **创建功能分支**（可选但推荐）
   ```bash
   git checkout -b feature/功能名称
   ```

3. **进行开发**
   修改或添加代码文件

4. **查看修改**
   ```bash
   # 查看哪些文件被修改
   git status
   
   # 查看具体修改内容
   git diff
   ```

5. **暂存更改**
   ```bash
   # 添加所有修改的文件
   git add .
   
   # 或者添加指定文件
   git add 文件名
   ```

6. **提交更改**
   ```bash
   git commit -m "提交信息：描述你的修改内容"
   ```

7. **推送更改到远程仓库**
   ```bash
   # 推送当前分支（如果是首次推送需要设置上游分支）
   git push -u origin 分支名称
   
   # 后续推送
   git push
   ```

## 5. 常见Git操作

### 5.1 查看历史记录

```bash
# 查看所有提交历史
git log

# 查看最近几条记录
git log -n 5

# 简洁显示
git log --oneline
```

### 5.2 分支管理

```bash
# 查看所有分支
git branch -a

# 切换分支
git checkout 分支名称

# 合并分支
git merge 被合并的分支
```

### 5.3 撤销操作

```bash
# 撤销工作目录中的修改
git checkout -- 文件名

# 撤销暂存区的修改
git reset HEAD 文件名

# 撤销最近一次提交（保留修改）
git reset --soft HEAD^1
```

### 5.4 冲突解决

当多人修改同一文件时可能会产生冲突：

1. 首先执行 `git pull` 获取最新代码
2. 编辑器会标记出冲突的部分，手动修改解决冲突
3. 解决后，使用 `git add` 标记冲突已解决
4. 最后执行 `git commit` 完成合并

## 6. 远程仓库管理

```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin 仓库URL

# 移除远程仓库
git remote remove origin
```

## 7. 注意事项

1. **不要提交敏感信息**：如密码、API密钥等
2. **提交前确认修改**：确保代码可以正常运行再提交
3. **编写有意义的提交信息**：清晰描述本次修改的内容和目的
4. **定期拉取更新**：避免长时间不更新导致大量冲突
5. **大型文件处理**：考虑使用Git LFS管理大型文件

## 8. Git客户端工具（可选）

除了命令行外，还可以使用图形化Git客户端：

- **GitHub Desktop**：[https://desktop.github.com/](https://desktop.github.com/)
- **GitKraken**：[https://www.gitkraken.com/](https://www.gitkraken.com/)
- **Sourcetree**：[https://www.sourcetreeapp.com/](https://www.sourcetreeapp.com/)

---

本指南由心动积分项目团队维护，如有问题请联系项目负责人。