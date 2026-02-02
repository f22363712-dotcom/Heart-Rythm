# 🚀 快速部署指南 - 多平台选择

## 🎯 推荐部署平台对比

| 平台 | 免费额度 | 难度 | CLI支持 | 推荐指数 |
|------|---------|------|---------|----------|
| **Fly.io** | 免费小套餐 | ⭐⭐ 中等 | ✅ 完整 | ⭐⭐⭐⭐⭐ |
| **Vercel** | 有限免费 | ⭐⭐ 中等 | ✅ 完整 | ⭐⭐⭐⭐ |
| **Render** | 免费但慢 | ⭐ 简单 | ✅ 完整 | ⭐⭐⭐ |
| **Railway** | $5 免费额度 | ⭐ 简单 | ✅ 完整 | ⭐⭐⭐⭐ |

---

## ✨ 方案 1：Fly.io 部署（推荐）

### 优点：
- ✅ 完全免费（3 个小型 VM）
- ✅ 全球部署节点
- ✅ 自动 HTTPS
- ✅ 支持数据库
- ✅ CLI 完整支持

### 步骤 1：安装 Fly.io CLI

**Windows PowerShell**（管理员）：
```powershell
# 下载并安装
iwr https://fly.io/install.ps1 -useb | iex
```

或者下载安装包：
https://github.com/superfly/flyctl/releases

### 步骤 2：登录并部署

```bash
# 1. 登录（会打开浏览器）
flyctl auth login

# 2. 进入项目目录
cd "d:\Obsidian知识库\知识库\Heart-Rythm"

# 3. 创建应用（选择免费方案）
flyctl apps create heart-rythm --org personal

# 4. 部署
flyctl deploy
```

### 步骤 3：访问应用

部署完成后，Fly.io 会显示 URL：
```
https://heart-rythm.fly.dev
```

---

## 🌟 方案 2：Vercel 部署（最简单）

### 优点：
- ✅ 最简单的部署
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ GitHub 集成完美

### 步骤 1：访问 Vercel

打开：https://vercel.com/new

### 步骤 2：导入项目

1. 点击 **"Import Project"**
2. 选择 **Heart-Rythm** 仓库
3. 选择 **v2.1** 分支
4. 配置：
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### 步骤 3：部署

点击 **"Deploy"**，等待 2-3 分钟。

### 访问

Vercel 会提供 URL：
```
https://heart-rythm.vercel.app
```

---

## 🔥 方案 3：Render 部署（手动触发）

既然 Railway 没有自动部署，试试 Render：

### 访问：https://render.com

1. 删除现有的 Railway 服务（可选）
2. 在 Render 创建新服务
3. 配置：
   - **Branch**: v2.1
   - **Root Directory**: 留空
   - **Start Command**: `python app.py`

---

## 📱 方案 4：GitHub Actions + 自托管（高级）

如果你想要 GitHub 自动部署到任何平台：

### 1. 创建 GitHub Actions Workflow

文件：`.github/workflows/deploy.yml`

```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [v2.1]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### 2. 配置 Secrets

在 GitHub 仓库设置中添加：
- `FLY_API_TOKEN`: 从 Fly.io 获取

### 3. 自动部署

每次推送到 v2.1 分支会自动部署！

---

## 🎯 我的建议

**如果你赶时间**：使用 **Vercel**（网页操作，2 分钟完成）

**如果你想要完全免费**：使用 **Fly.io**（需要安装 CLI）

**如果你已经配置了 Railway**：在 Railway Dashboard 手动触发重新部署

---

## ❓ 常见问题

### Q: GitHub Pages 可以部署 Python 应用吗？
A: **不可以**。GitHub Pages 只支持静态网站（HTML/CSS/JS）。

### Q: 哪个平台最稳定？
A: **Vercel** 和 **Fly.io** 都很稳定。

### Q: 哪个平台完全免费？
A: **Fly.io** 提供 3 个免费小型 VM，**Render** 也有免费方案。

### Q: 可以自定义域名吗？
A: 所有平台都支持自定义域名。

---

**选择一个平台，我可以帮你完成配置！** 🚀
