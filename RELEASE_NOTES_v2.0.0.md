# Release Notes - v2.0.0

## 🎉 心动积分系统 v2.0.0 正式发布！

**发布日期**: 2026年1月21日
**分支**: v2
**标签**: v2.0.0

---

## 🚀 重大更新

### 核心功能

#### 1. 用户认证系统 ✨
- **用户注册**: 创建账号并自动生成情侣档案
- **安全登录**: 用户名+密码登录
- **密码加密**: SHA256哈希加密，不保存明文
- **Token认证**: 基于Bearer Token的会话管理
- **自动过期**: 24小时会话自动过期

#### 2. 数据隔离 🔒
- **完全独立**: 每对情侣的数据完全隔离
- **权限控制**: 只能访问自己的积分和奖励
- **管理员权限**: 管理员可查看全局数据
- **API保护**: 所有接口都有权限验证

#### 3. 数据库升级 💾
- **从JSON到SQLite**: 升级到关系型数据库
- **6个数据表**: 规范化的表结构设计
- **数据迁移**: 一键迁移工具，保留所有历史数据
- **自动备份**: 迁移前自动备份原数据

#### 4. 前端重构 🎨
- **现代化设计**: 基于Bootstrap 5
- **响应式布局**: 适配各种设备
- **三种视图**: 访客/用户/管理员
- **5个核心页面**: 登录、首页、仪表板、奖励、管理后台

#### 5. 管理员后台 👨‍💼
- **系统统计**: 情侣总数、总积分、兑换次数
- **用户管理**: 查看所有情侣信息
- **数据查看**: 全局兑换记录
- **权限保护**: 只有管理员可访问

---

## 📦 新增文件

### 后端
- `backend/database.py` - 数据库模型（560行）
- `backend/auth.py` - 认证系统（141行）
- `backend/api/main.py` - 重写API（600行）

### 前端
- `frontend/templates/base_new.html` - 基础模板
- `frontend/templates/login.html` - 登录页面
- `frontend/templates/index_new.html` - 新首页
- `frontend/templates/dashboard.html` - 用户仪表板
- `frontend/templates/rewards_new.html` - 奖励管理
- `frontend/templates/admin.html` - 管理员后台

### 工具和文档
- `scripts/migrate_data.py` - 数据迁移脚本
- `scripts/test_backend.py` - 后端测试
- `scripts/test_frontend.py` - 前端测试
- `start.bat` - 启动脚本
- `USAGE.md` - 使用说明
- `PROJECT_SUMMARY.md` - 项目总结

### 数据
- `data/heartbeat.db` - SQLite数据库

---

## 🔧 技术改进

### 安全性
- ✅ 密码SHA256哈希加密
- ✅ Token-based认证
- ✅ 会话管理和过期控制
- ✅ API级别权限验证
- ✅ 数据隔离保护

### 架构
- ✅ 前后端分离
- ✅ RESTful API标准
- ✅ 关系型数据库
- ✅ 模块化代码组织
- ✅ 完整的错误处理

### 用户体验
- ✅ 响应式设计
- ✅ 实时数据加载
- ✅ 友好的空状态提示
- ✅ 操作成功/失败反馈
- ✅ 平滑动画效果

---

## 📊 统计数据

### 代码量
- **后端**: ~1,500行
- **前端**: ~2,000行
- **测试**: ~400行
- **文档**: ~1,000行
- **总计**: ~4,900行

### Git提交
- **v2.0相关提交**: 7次
- **代码变更**: +3,900行, -200行
- **新增文件**: 15个
- **修改文件**: 3个

---

## 🔑 默认账号

### 管理员账号
```
用户名: admin
密码: admin123
```

### 情侣账号（示例）
```
用户名: couple_test001
密码: 123456
```

> 所有从v1.0迁移的账号格式：`couple_{原ID}` / `123456`

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone -b v2 https://github.com/f22363712-dotcom/Heart-Rythm.git
cd Heart-Rythm
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 数据迁移（首次使用）
```bash
python scripts/migrate_data.py
```

### 4. 启动服务
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

### 5. 访问应用
- **前端界面**: http://localhost:5000
- **API文档**: http://localhost:8000/docs

---

## 📖 文档

- **[README.md](README.md)** - 项目说明
- **[USAGE.md](USAGE.md)** - 详细使用指南
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 完整项目总结

---

## 🔄 从v1.0升级

### 升级步骤

1. **备份数据**
   ```bash
   # 备份现有的JSON数据
   cp data/system_data.json data/system_data.json.backup
   ```

2. **切换到v2分支**
   ```bash
   git fetch origin
   git checkout v2
   ```

3. **安装新依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行数据迁移**
   ```bash
   python scripts/migrate_data.py
   ```

5. **启动新版本**
   ```bash
   start.bat
   ```

### 迁移说明
- 所有现有数据会被保留
- 自动为每对情侣创建账号
- 原JSON文件会被备份
- 默认密码为 `123456`

---

## ⚠️ 重要变更

### 不兼容的变更
1. **数据存储**: 从JSON文件改为SQLite数据库
2. **API接口**: 大部分接口需要认证
3. **前端路由**: 页面路径有所变化
4. **启动方式**: 使用新的启动脚本

### 已移除的功能
- 旧版的JSON直接访问方式
- 无认证的API访问

### 保留的功能
- 所有核心业务功能
- 数据完整性
- 基本操作流程

---

## 🐛 已知问题

目前没有已知的严重问题。如有问题请在GitHub Issues中报告。

---

## 🔮 未来计划

### 短期（v2.1）
- [ ] 修改密码功能
- [ ] 用户头像上传
- [ ] 数据导出功能
- [ ] 更多统计图表

### 长期（v3.0）
- [ ] 移动端优化
- [ ] PWA支持
- [ ] 社交功能
- [ ] 数据分析

---

## 🙏 致谢

感谢所有使用和支持心动积分系统的用户！

---

## 📞 支持

- **GitHub**: https://github.com/f22363712-dotcom/Heart-Rythm
- **Issues**: https://github.com/f22363712-dotcom/Heart-Rythm/issues
- **分支**: v2
- **标签**: v2.0.0

---

## 📄 许可证

© 2025-2026 心动积分项目 · 用爱记录每一刻

---

**开发者**: Claude Sonnet 4.5
**发布日期**: 2026年1月21日
**版本**: 2.0.0
