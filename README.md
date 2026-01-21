# 心动积分项目 v2.0 - Heart Rhythm System

💕 专为情侣设计的积分管理系统，用爱记录每一刻

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/f22363712-dotcom/Heart-Rythm)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

## 🎉 v2.0 重大更新

### 新增功能
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

**方式一：使用启动脚本（推荐）**
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

**方式二：手动启动**
```bash
# 启动后端（端口8000）
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload

# 启动前端（端口5000）
python frontend/main.py
```

### 4. 访问应用

- **前端界面**：http://localhost:5000
- **后端API**：http://localhost:8000
- **API文档**：http://localhost:8000/docs

### 5. 默认账号

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
│   │   ├── base_new.html    # 基础模板
│   │   ├── login.html       # 登录页面
│   │   ├── index_new.html   # 首页
│   │   ├── dashboard.html   # 用户仪表板
│   │   ├── rewards_new.html # 奖励管理
│   │   └── admin.html       # 管理员后台
│   └── main.py              # 前端应用
├── data/
│   ├── heartbeat.db         # SQLite数据库（v2.0）
│   └── system_data.json.backup  # JSON备份
├── scripts/
│   ├── migrate_data.py      # 数据迁移脚本
│   ├── test_backend.py      # 后端测试
│   └── test_frontend.py     # 前端测试
├── start.bat                # 启动脚本（Windows）
├── requirements.txt         # 依赖列表
├── USAGE.md                 # 使用说明
├── PROJECT_SUMMARY.md       # 项目总结
└── README.md                # 本文件
```

## 📖 文档

- **[使用说明](USAGE.md)** - 详细的功能说明和使用指南
- **[项目总结](PROJECT_SUMMARY.md)** - 完整的项目开发总结
- **[API文档](http://localhost:8000/docs)** - 在线API文档（需启动后端）

## 更新日志

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

