# 心动积分 PWA 快速参考卡片

## 🚀 快速启动

```bash
# Windows
start_pwa.bat

# 或手动启动
cd backend && python -m uvicorn api.main:app --reload
cd frontend && python main.py
```

**访问地址**: http://localhost:5000

---

## 📱 安装到手机

### Android (Chrome)
1. 访问应用
2. 点击"立即安装"横幅
3. 或菜单 → "添加到主屏幕"

### iOS (Safari)
1. 访问应用
2. 点击分享按钮 📤
3. "添加到主屏幕"

---

## 🔍 检查PWA状态

### Chrome DevTools (F12)
```
Application 标签:
├── Manifest ✓ 检查配置
├── Service Workers ✓ 查看状态
└── Cache Storage ✓ 查看缓存
```

### 验证脚本
```bash
python scripts/verify_pwa.py
```

---

## 📦 关键文件

```
frontend/static/
├── manifest.json    # PWA配置
├── sw.js            # Service Worker
└── icons/           # 应用图标

frontend/templates/
└── base_new.html    # PWA集成
```

---

## 🔄 更新PWA

1. 修改 `sw.js` 中的版本号:
   ```javascript
   const CACHE_VERSION = 'v2.1.2'; // 改这里
   ```

2. 用户访问时会自动提示更新

---

## 🎨 主题配置

```json
{
  "theme_color": "#e891a9",      // 状态栏颜色
  "background_color": "#faf5f7"  // 启动背景
}
```

---

## 📊 缓存策略

| 资源类型 | 策略 | 说明 |
|---------|------|------|
| 静态资源 | 缓存优先 | CSS/JS/字体 |
| 页面导航 | 网络优先 | HTML页面 |
| 图片字体 | 缓存优先 | 图片/字体文件 |
| API请求 | 仅网络 | 不缓存 |

---

## 🐛 常见问题

### Service Worker未注册
- 确保使用 HTTPS 或 localhost
- 检查浏览器控制台错误

### 图标不显示
```bash
python scripts/generate_pwa_icons.py
```

### 离线不工作
- 先在线访问一次
- 检查 Cache Storage

### iOS无法安装
- 必须使用 Safari 浏览器
- 手动添加到主屏幕

---

## 📱 支持的浏览器

| 浏览器 | 支持度 |
|--------|--------|
| Chrome (Android) | ✅ 完全支持 |
| Edge (Android) | ✅ 完全支持 |
| Safari (iOS) | ⚠️ 部分支持 |
| Chrome (Desktop) | ✅ 完全支持 |
| Firefox | ⚠️ 部分支持 |

---

## 🧪 测试清单

- [ ] Service Worker 注册成功
- [ ] Manifest 配置正确
- [ ] 图标显示正常
- [ ] 可以安装到主屏幕
- [ ] 离线访问正常
- [ ] 缓存策略有效
- [ ] 响应式布局适配
- [ ] Lighthouse PWA > 90

---

## 📚 文档链接

- [PWA部署指南](PWA_GUIDE.md)
- [测试清单](PWA_TEST_CHECKLIST.md)
- [完成总结](PWA_COMPLETION_SUMMARY.md)
- [使用说明](USAGE.md)

---

## 🔧 生产部署

### Nginx配置
```nginx
# Service Worker不缓存
location /static/sw.js {
    add_header Cache-Control "no-cache";
}

# 静态资源长期缓存
location /static/ {
    add_header Cache-Control "max-age=31536000";
}
```

### 必需条件
- ✅ HTTPS证书
- ✅ 正确的MIME类型
- ✅ CORS配置（如需要）

---

## 💡 性能指标

| 指标 | 目标值 |
|------|--------|
| 首次加载 | < 3秒 |
| 二次加载 | < 1秒 |
| PWA评分 | > 90 |
| 缓存命中率 | > 80% |

---

## 🎯 默认账号

**管理员**
- 用户名: `admin`
- 密码: `admin123`

**测试账号**
- 用户名: `couple_test001`
- 密码: `123456`

---

## 📞 获取帮助

1. 查看文档: [PWA_GUIDE.md](PWA_GUIDE.md)
2. 运行验证: `python scripts/verify_pwa.py`
3. 检查控制台错误信息
4. 查看测试清单: [PWA_TEST_CHECKLIST.md](PWA_TEST_CHECKLIST.md)

---

**💕 心动积分 v2.1 - PWA版**
**用爱记录每一刻**
