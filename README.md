# 心动积分项目 v2.1 - Heart Rhythm System

💕 专为情侣设计的积分管理系统，用爱记录每一刻

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/f22363712-dotcom/Heart-Rythm)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![PWA](https://img.shields.io/badge/PWA-enabled-success.svg)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Deployed](https://img.shields.io/badge/deployed-online-success.svg)](https://heart-rythm-production.up.railway.app)

## 🌐 在线访问

**云端部署地址**: https://heart-rythm-production.up.railway.app

- **API 文档**: https://heart-rythm-production.up.railway.app/docs
- **API 根路径**: https://heart-rythm-production.up.railway.app/
- **健康检查**: https://heart-rythm-production.up.railway.app/health/

> ✅ 部署在 Railway 云端，24/7 在线，HTTPS 安全连接

## 🎉 v2.1 PWA移动端化更新

### 新增功能
- 📱 **PWA支持**：可安装到手机主屏幕，像原生App一样使用
- 🚀 **离线访问**：Service Worker缓存，支持离线浏览
- ⚡ **快速加载**：智能缓存策略，秒开应用
- 📲 **安装提示**：自动提示用户安装到主屏幕
- 🎨 **移动端优化**：完整的响应式设计和触摸优化
- 🔄 **自动更新**：检测新版本并提示更新

### v2.0 核心功能
- ✅ **用户认证系统**：安全的登录注册机制
- ✅ **数据隔离**：每对情侣的数据完全独立
- ✅ **权限管理**：普通用户和管理员分级权限
- ✅ **SQLite数据库**：从JSON升级到关系型数据库
- ✅ **现代化UI**：基于Bootstrap 5的响应式设计
- ✅ **管理员后台**：系统统计和数据管理

### 安全特性
- 🔐 密码SHA256哈希加密
- 🔑 Token-based认证机制
- ⏰ 会话自动过期（24小时）
- 🛡️ API级别权限控制
- 🔒 HTTPS支持（生产环境必需）

## 环境要求

- Python 3.8或更高版本
- pip包管理器

## 获取项目

### 从GitHub克隆（推荐）

```bash
git clone https://github.com/f22363712-dotcom/Heart-Rythm.git
cd Heart-Rythm
```

### 或直接下载ZIP文件

1. 访问GitHub仓库：https://github.com/f22363712-dotcom/Heart-Rythm
2. 点击"Code"按钮，选择"Download ZIP"
3. 解压下载的ZIP文件
4. 进入解压后的目录

## 项目简介

心动积分是一个基于Python的Web应用，帮助情侣记录和管理彼此的心动积分，通过积分兑换系统增加感情互动和乐趣。

## 功能特性

### 用户功能
- **👤 用户认证**：注册、登录、登出
- **💑 情侣管理**：创建和管理情侣档案
- **⭐ 积分管理**：添加/减少积分，查看历史记录
- **🎁 奖励系统**：创建专属奖励，兑换奖励
- **📊 数据统计**：查看个人数据统计
- **🔒 数据隔离**：每对情侣数据完全独立

### 管理员功能
- **📈 系统统计**：查看全局数据统计
- **👥 用户管理**：查看所有情侣信息
- **📋 记录查看**：查看全局兑换记录
- **🔐 权限控制**：管理员专属权限

## 技术栈

### 后端
- **框架**：FastAPI 0.104+
- **数据库**：SQLite 3
- **认证**：Token-based (Bearer)
- **密码加密**：SHA256
- **API文档**：Swagger UI（自动生成）

### 前端
- **框架**：Flask 3.0+
- **UI库**：Bootstrap 5.3
- **图标**：Bootstrap Icons 1.11
- **模板引擎**：Jinja2
- **状态管理**：localStorage

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据迁移（首次使用或从v1.0升级）

```bash
python scripts/migrate_data.py
```

这将：
- 创建SQLite数据库
- 迁移现有JSON数据
- 为每对情侣创建账号
- 创建默认管理员账号

### 3. 启动服务

**方式一：使用PWA启动脚本（推荐）**
```bash
# Windows
start_pwa.bat

# 自动启动前后端服务并打开浏览器
```

**方式二：使用普通启动脚本**
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

**方式三：手动启动**
```bash
# 启动后端（端口8000）
cd backend
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# 启动前端（端口5000）
cd frontend
python main.py
```

### 4. 访问应用

- **前端界面**：http://localhost:5000
- **后端API**：http://localhost:8000
- **API文档**：http://localhost:8000/docs

### 5. 安装PWA到手机

#### Android设备
1. 使用Chrome浏览器访问 http://your-server:5000
2. 等待自动弹出"添加到主屏幕"提示
3. 点击"立即安装"
4. 应用图标将出现在主屏幕

#### iOS设备
1. 使用Safari浏览器访问应用
2. 点击底部分享按钮
3. 选择"添加到主屏幕"
4. 确认安装

> **注意**：PWA需要HTTPS环境（生产环境）或localhost（开发环境）

### 6. 默认账号

**管理员账号**
- 用户名：`admin`
- 密码：`admin123`

**情侣账号（示例）**
- 用户名：`couple_test001`
- 密码：`123456`

> 所有迁移的账号格式：`couple_{原ID}` / `123456`

## 项目结构

```
Python心动积分/
├── backend/
│   ├── api/
│   │   └── main.py          # API接口（v2.0）
│   ├── database.py          # 数据库模型（v2.0）
│   ├── auth.py              # 认证系统（v2.0）
│   └── data_manager.py      # 旧版数据管理（保留）
├── frontend/
│   ├── templates/
│   │   ├── base_new.html    # 基础模板（含PWA集成）
│   │   ├── login.html       # 登录页面
│   │   ├── index_new.html   # 首页
│   │   ├── dashboard.html   # 用户仪表板
│   │   ├── rewards_new.html # 奖励管理
│   │   └── admin.html       # 管理员后台
│   ├── static/
│   │   ├── manifest.json    # PWA配置文件
│   │   ├── sw.js            # Service Worker
│   │   └── icons/           # PWA图标
│   └── main.py              # 前端应用
├── data/
│   ├── heartbeat.db         # SQLite数据库（v2.0）
│   └── system_data.json.backup  # JSON备份
├── scripts/
│   ├── migrate_data.py      # 数据迁移脚本
│   ├── generate_pwa_icons.py # PWA图标生成脚本
│   ├── test_backend.py      # 后端测试
│   └── test_frontend.py     # 前端测试
├── start.bat                # 启动脚本（Windows）
├── start_pwa.bat            # PWA启动脚本（Windows）
├── requirements.txt         # 依赖列表
├── USAGE.md                 # 使用说明
├── PWA_GUIDE.md             # PWA部署指南
├── PROJECT_SUMMARY.md       # 项目总结
└── README.md                # 本文件
```

## 📖 文档

### 核心文档（推荐阅读）
- **[PWA使用说明](PWA使用说明.md)** - PWA 安装和使用完整指南（必读！）
- **[手机PWA安装指南](手机PWA安装指南.md)** - 手机端安装 PWA 的详细步骤和问题排查 ⭐ 新增
- **[快速测试PWA](快速测试PWA.md)** - PWA 功能测试清单和排查指南
- **[发布APK指南](发布APK指南.md)** - 将 PWA 发布为 Android APK 的完整教程

### 其他文档
- **[使用说明](USAGE.md)** - 详细的功能说明和使用指南
- **[PWA部署指南](PWA_GUIDE.md)** - PWA安装、部署和测试完整指南
- **[项目总结](PROJECT_SUMMARY.md)** - 完整的项目开发总结
- **[UI设计文档](UI_DESIGN.md)** - 界面设计理念和规范
- **[API文档](http://localhost:8000/docs)** - 在线API文档（需启动后端）

## 📱 PWA特性

### 离线功能
- 静态资源自动缓存（CSS、JS、字体）
- 页面内容智能缓存
- 离线时可访问已缓存页面
- API请求失败时友好提示

### 移动端优化
- 响应式布局适配所有屏幕尺寸
- 触摸优化（最小44px点击区域）
- 刘海屏和底部手势条适配
- 横屏模式优化
- 减少动画模式支持
- 高对比度模式支持

### 安装体验
- 自动显示安装提示横幅
- 支持Android、iOS、桌面浏览器
- 全屏体验（无浏览器地址栏）
- 自定义启动画面
- 应用快捷方式

### 性能优化
- Service Worker缓存策略
- 静态资源缓存优先
- 动态内容网络优先
- 图片和字体智能缓存
- 自动清理旧缓存

详细说明请查看 [PWA_GUIDE.md](PWA_GUIDE.md)

## 更新日志

### v2.1.0 (2026-01-23)

**PWA移动端化**
- 📱 实现完整的PWA支持
- 🚀 添加Service Worker离线缓存
- ⚡ 优化缓存策略（静态资源缓存优先，动态内容网络优先）
- 📲 实现自动安装提示功能
- 🎨 完善移动端响应式布局
- 🔄 添加自动更新检测
- 📱 支持刘海屏和底部手势条
- 👆 触摸优化（最小44px点击区域）
- 🌓 支持减少动画模式和高对比度模式
- 🎯 生成PWA图标（72px到512px全尺寸）
- 📝 创建PWA部署和使用文档

**技术改进**
- 优化Service Worker缓存管理
- 添加动态缓存大小限制
- 实现网络优先和缓存优先混合策略
- 添加PWA安装横幅UI
- 优化移动端CSS媒体查询

### v2.0.0 (2026-01-21)

**重大更新**
- ✨ 实现用户认证系统
- ✨ 添加数据隔离功能
- ✨ 升级到SQLite数据库
- ✨ 重构前端界面（Bootstrap 5）
- ✨ 添加管理员后台
- ✨ 实现权限控制系统
- 🔐 添加密码加密
- 🔑 实现Token认证
- 📝 完善文档和测试

**技术改进**
- 从JSON文件存储升级到SQLite
- 实现RESTful API标准
- 添加完整的错误处理
- 优化前端用户体验
- 添加响应式设计

### v1.0.0 (2025-12-18)

- 🚀 初始版本发布
- ✨ 基础功能实现
- 🎨 UI设计优化
- 💑 实现情侣管理功能
- ⭐ 实现积分变动功能
- 🎁 实现奖励兑换功能
- 📊 实现数据统计功能

## 使用说明

1. **注册情侣**：在情侣管理页面添加情侣信息
2. **记录积分**：通过API或前端界面记录积分变动
3. **设置奖励**：在奖励管理页面添加可兑换的奖励
4. **兑换奖励**：使用积分兑换喜欢的奖励
5. **查看统计**：在数据统计页面查看系统数据

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 概念缘由

[概念缘由.pdf](https://github.com/user-attachments/files/24053482/default.pdf)

