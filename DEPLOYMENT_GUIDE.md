# 心动积分项目 - 云端部署指南 🚀

本指南将帮助你将 Heart-Rythm（心动积分）项目部署到云端，让任何人都可以通过互联网访问使用。

## 📋 部署方案对比

我们提供多种部署方案，你可以根据自己的需求选择：

| 方案 | 价格 | 难度 | 推荐指数 | 特点 |
|------|------|------|----------|------|
| **Render** | 免费 | ⭐ 简单 | ⭐⭐⭐⭐⭐ | 完全免费、自动HTTPS、部署简单 |
| **Railway** | 免费额度 | ⭐⭐ 中等 | ⭐⭐⭐⭐ | 界面美观、功能强大 |
| **Vercel** | 免费 | ⭐⭐ 中等 | ⭐⭐⭐⭐ | 速度快、但需要改造代码 |
| **自建服务器** | 付费 | ⭐⭐⭐ 困难 | ⭐⭐ | 完全控制、需要维护 |

## 🎯 推荐方案：Render 部署（完全免费）

Render 提供免费的 Web 服务，包含：
- ✅ 512MB RAM
- ✅ 0.1 CPU
- ✅ 每月 750 小时运行时间
- ✅ 自动 HTTPS 证书
- ✅ 自动从 GitHub 部署

### 步骤 1：准备 GitHub 仓库

1. 确保你的代码已经推送到 GitHub：
   ```bash
   git add .
   git commit -m "准备部署"
   git push origin main
   ```

### 步骤 2：注册 Render 账号

1. 访问 [https://render.com](https://render.com)
2. 点击 "Sign Up" 注册账号
3. 使用 GitHub 账号登录（推荐）

### 步骤 3：创建新的 Web Service

1. 登录 Render 后，点击 **"New +"** 按钮
2. 选择 **"Web Service"**
3. 连接你的 GitHub 账号（如果还没连接）
4. 选择 **Heart-Rythm** 仓库
5. 填写配置信息：

   | 配置项 | 值 |
   |--------|-----|
   | **Name** | `heart-rhythm-backend` |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `python server.py` |
   | **Instance Type** | `Free` |

6. 点击 **"Create Web Service"**

### 步骤 4：等待部署完成

- Render 会自动从 GitHub 拉取代码
- 安装依赖（约 2-3 分钟）
- 启动服务（约 1-2 分钟）
- 部署完成后，你会看到一个 URL，例如：`https://heart-rhythm-backend.onrender.com`

### 步骤 5：访问应用

1. **后端 API 文档**：`https://你的服务名.onrender.com/docs`
2. **API 根路径**：`https://你的服务名.onrender.com/`

### 步骤 6：配置自动部署

Render 默认会监听你的 GitHub 仓库：
- 每次你 `git push` 到 main 分支
- Render 会自动重新部署
- 无需手动操作！

## 🔧 方案二：Railway 部署

### 步骤 1：注册 Railway

1. 访问 [https://railway.app](https://railway.app)
2. 使用 GitHub 账号登录

### 步骤 2：创建新项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择 **Heart-Rythm** 仓库

### 步骤 3：配置项目

Railway 会自动检测 Python 项目，但你需要手动调整：

1. 点击项目设置
2. 设置环境变量：
   ```bash
   PORT=8000
   PYTHON_VERSION=3.9
   ```
3. 修改 Root Directory 为空（或项目根目录）
4. 修改 Start Command 为：`python server.py`

### 步骤 4：部署

1. 点击 **"Deploy"**
2. 等待部署完成
3. Railway 会提供一个 URL，例如：`https://heart-rhythm.up.railway.app`

## 🌐 方案三：Vercel 部署

Vercel 主要用于前端，需要将后端改造为 API Routes。这里不做详细介绍。

## 🔐 配置环境变量（可选）

如果你的应用需要配置环境变量：

### 在 Render 中：

1. 进入你的 Web Service
2. 点击 **"Environment"** 标签
3. 添加环境变量，例如：
   - `SECRET_KEY`: 你的密钥
   - `DATABASE_URL`: 数据库连接（如果需要）

### 在 Railway 中：

1. 进入项目
2. 点击 **"Variables"** 标签
3. 添加环境变量

## 📊 监控和日志

### Render 监控：

1. 访问你的 Web Service
2. 点击 **"Logs"** 查看实时日志
3. 点击 **"Metrics"** 查看性能指标

### Railway 监控：

1. 访问你的项目
2. 点击 **"Logs"** 查看日志
3. 点击 **"Metrics"** 查看性能

## 🐛 常见问题

### 1. 部署失败

**问题**：Build 失败

**解决方案**：
- 检查 `requirements.txt` 是否包含所有依赖
- 查看 Build Logs 获取详细错误信息
- 确保所有 Python 文件没有语法错误

### 2. 服务启动失败

**问题**：服务无法启动

**解决方案**：
- 检查 `server.py` 是否存在且正确
- 查看 Logs 获取详细错误信息
- 确保端口号正确（默认 8000）

### 3. 服务无法访问

**问题**：部署成功但无法访问

**解决方案**：
- 检查服务是否在运行（查看 Dashboard）
- 等待 1-2 分钟让服务完全启动
- 检查防火墙设置

### 4. 服务休眠

**问题**：免费服务会自动休眠

**解决方案**：
- Render 免费版：15 分钟无请求会休眠，首次访问需要等待 30-60 秒
- Railway 免费版：类似休眠策略
- 解决方法：定时发送请求保持唤醒（可以使用 UptimeRobot）

### 5. 数据持久化

**问题**：免费服务重启后数据会丢失

**解决方案**：
- 使用外部数据库（如 Supabase、PlanetScale）
- 或定期备份数据到本地

## 🔄 更新应用

### 使用 Render：

```bash
# 本地修改代码
git add .
git commit -m "更新功能"
git push origin main

# Render 会自动检测并重新部署
```

### 使用 Railway：

```bash
# 同上
git add .
git commit -m "更新功能"
git push origin main

# Railway 会自动检测并重新部署
```

## 📈 性能优化

### 1. 减少启动时间

- 减少不必要的依赖
- 优化导入语句
- 使用缓存

### 2. 减少内存占用

- 使用流式处理大文件
- 及时释放不再使用的对象
- 避免内存泄漏

### 3. 提高响应速度

- 使用 CDN（如 CloudFlare）
- 启用 gzip 压缩
- 优化数据库查询

## 🔗 自定义域名

### Render：

1. 进入你的 Web Service
2. 点击 **"Custom Domains"**
3. 添加你的域名（如 `heart-rhythm.com`）
4. 按照提示配置 DNS

### Railway：

1. 进入项目设置
2. 点击 **"Domains"**
3. 添加你的域名
4. 配置 DNS

## 📝 总结

| 步骤 | Render | Railway |
|------|--------|---------|
| 注册 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 部署 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 速度 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 免费额度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**推荐选择**：如果你是第一次部署，推荐使用 **Render**，因为它最简单且完全免费。

## 🆘 需要帮助？

如果遇到问题，可以：
1. 查看项目的 [GitHub Issues](https://github.com/f22363712-dotcom/Heart-Rythm/issues)
2. 查看 [Render 文档](https://render.com/docs)
3. 查看 [Railway 文档](https://docs.railway.app)

---

**祝你部署成功！** 🎉
