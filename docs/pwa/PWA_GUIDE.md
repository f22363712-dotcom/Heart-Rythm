# 心动积分 PWA 移动端化指南

## 📱 什么是 PWA？

PWA (Progressive Web App) 是一种可以像原生应用一样安装到手机主屏幕的网页应用。心动积分系统已完成PWA移动端化，支持：

- ✅ 添加到主屏幕，像原生App一样使用
- ✅ 离线访问（缓存静态资源）
- ✅ 快速加载（Service Worker缓存）
- ✅ 全屏体验（无浏览器地址栏）
- ✅ 推送通知（可选功能）
- ✅ 自动更新检测

---

## 🎯 PWA 功能特性

### 1. 安装到主屏幕

用户可以将心动积分添加到手机主屏幕，获得类似原生应用的体验：

- **Android**: 浏览器会自动显示"添加到主屏幕"提示
- **iOS**: 点击分享按钮 → "添加到主屏幕"
- **桌面浏览器**: 地址栏会显示安装图标

### 2. 离线功能

- 静态资源（CSS、JS、字体）自动缓存
- 页面内容智能缓存
- 离线时可访问已缓存的页面
- API请求失败时显示友好提示

### 3. 快速加载

- Service Worker 缓存策略优化
- 静态资源缓存优先
- 动态内容网络优先
- 图片和字体智能缓存

### 4. 移动端优化

- 响应式布局适配各种屏幕
- 触摸优化（最小44px点击区域）
- 刘海屏和底部手势条适配
- 横屏模式优化
- 减少动画模式支持
- 高对比度模式支持

---

## 🚀 部署指南

### 前置要求

1. **HTTPS 支持**（必需）
   - PWA 必须在 HTTPS 环境下运行
   - 本地开发可以使用 `localhost`
   - 生产环境必须配置 SSL 证书

2. **Web 服务器配置**
   - 确保 `manifest.json` 和 `sw.js` 可访问
   - 设置正确的 MIME 类型

### 部署步骤

#### 1. 启动后端服务

```bash
cd backend
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. 启动前端服务

```bash
cd frontend
python main.py
```

前端服务默认运行在 `http://127.0.0.1:5000`

#### 3. 配置 HTTPS（生产环境）

**使用 Nginx 反向代理：**

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 前端
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Service Worker 和 Manifest
    location /static/ {
        proxy_pass http://127.0.0.1:5000/static/;
        add_header Cache-Control "public, max-age=31536000";
    }

    # Service Worker 不缓存
    location /static/sw.js {
        proxy_pass http://127.0.0.1:5000/static/sw.js;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
}
```

#### 4. 验证 PWA 配置

使用 Chrome DevTools 检查：

1. 打开 Chrome 开发者工具（F12）
2. 切换到 "Application" 标签
3. 检查以下项目：
   - **Manifest**: 确认 manifest.json 加载成功
   - **Service Workers**: 确认 sw.js 注册成功
   - **Cache Storage**: 查看缓存的资源

---

## 📲 用户安装指南

### Android 设备

1. 使用 Chrome 浏览器访问网站
2. 等待自动弹出"添加到主屏幕"提示
3. 或点击右上角菜单 → "添加到主屏幕"
4. 确认安装

### iOS 设备

1. 使用 Safari 浏览器访问网站
2. 点击底部分享按钮（方框+箭头）
3. 滚动找到"添加到主屏幕"
4. 输入名称（默认"心动积分"）
5. 点击"添加"

### 桌面浏览器

1. 访问网站
2. 地址栏右侧会显示安装图标（+）
3. 点击图标并确认安装
4. 应用会添加到应用列表

---

## 🔧 开发指南

### 文件结构

```
frontend/
├── static/
│   ├── manifest.json          # PWA 配置文件
│   ├── sw.js                   # Service Worker
│   └── icons/                  # PWA 图标
│       ├── icon-72x72.png
│       ├── icon-96x96.png
│       ├── icon-128x128.png
│       ├── icon-144x144.png
│       ├── icon-152x152.png
│       ├── icon-192x192.png
│       ├── icon-384x384.png
│       ├── icon-512x512.png
│       ├── shortcut-record.png
│       ├── shortcut-reward.png
│       └── badge-72x72.png
└── templates/
    └── base_new.html           # 集成了 PWA 功能的基础模板
```

### 修改 Manifest

编辑 `frontend/static/manifest.json`：

```json
{
  "name": "心动积分 - 爱的印记本",
  "short_name": "心动积分",
  "description": "用积分记录爱，用兑换传递心意",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#faf5f7",
  "theme_color": "#e891a9",
  "orientation": "portrait"
}
```

### 更新 Service Worker

修改 `frontend/static/sw.js` 后，记得更新版本号：

```javascript
const CACHE_VERSION = 'v2.1.2'; // 修改版本号
```

版本号变化会触发 Service Worker 更新。

### 添加新的缓存资源

在 `sw.js` 中添加需要缓存的资源：

```javascript
const STATIC_CACHE_URLS = [
  '/',
  '/login',
  '/dashboard',  // 新增页面
  '/static/manifest.json',
  // ... 其他资源
];
```

### 生成新图标

如果需要重新生成图标：

```bash
python scripts/generate_pwa_icons.py
```

或使用在线工具：
- [RealFaviconGenerator](https://realfavicongenerator.net/)
- [PWA Builder](https://www.pwabuilder.com/imageGenerator)

---

## 🧪 测试指南

### 本地测试

1. **启动服务**
   ```bash
   # 终端1：启动后端
   cd backend && python -m uvicorn api.main:app --reload

   # 终端2：启动前端
   cd frontend && python main.py
   ```

2. **访问应用**
   - 打开 Chrome 浏览器
   - 访问 `http://localhost:5000`

3. **测试 PWA 功能**
   - 打开 DevTools → Application
   - 检查 Manifest 和 Service Worker
   - 尝试离线模式（DevTools → Network → Offline）

### 移动端测试

#### 方法1：使用 Chrome 远程调试

1. 手机开启 USB 调试
2. 连接电脑
3. Chrome 访问 `chrome://inspect`
4. 在手机上打开应用
5. 点击 "inspect" 进行调试

#### 方法2：使用 ngrok 内网穿透

```bash
# 安装 ngrok
npm install -g ngrok

# 启动内网穿透
ngrok http 5000
```

使用 ngrok 提供的 HTTPS 地址在手机上访问。

### PWA 审计

使用 Lighthouse 进行 PWA 审计：

1. 打开 Chrome DevTools
2. 切换到 "Lighthouse" 标签
3. 选择 "Progressive Web App"
4. 点击 "Generate report"
5. 查看评分和建议

---

## 🐛 常见问题

### 1. Service Worker 未注册

**症状**: 控制台显示 "Service Worker 注册失败"

**解决方案**:
- 确保使用 HTTPS 或 localhost
- 检查 `sw.js` 文件路径是否正确
- 查看浏览器控制台的详细错误信息

### 2. 图标不显示

**症状**: 安装后图标显示为默认图标

**解决方案**:
- 检查图标文件是否存在于 `frontend/static/icons/`
- 确认 manifest.json 中的图标路径正确
- 清除浏览器缓存后重试

### 3. 离线功能不工作

**症状**: 断网后无法访问应用

**解决方案**:
- 确认 Service Worker 已激活
- 检查缓存策略配置
- 查看 Cache Storage 中是否有缓存内容

### 4. iOS 安装后无法打开

**症状**: 点击图标后白屏或闪退

**解决方案**:
- 确保 `start_url` 配置正确
- 检查是否有 JavaScript 错误
- 确认所有资源都使用 HTTPS

### 5. 更新不生效

**症状**: 修改代码后，用户看到的还是旧版本

**解决方案**:
- 更新 Service Worker 版本号
- 清除浏览器缓存
- 在 DevTools → Application → Service Workers 中点击 "Update"

---

## 📊 性能优化建议

### 1. 减小资源体积

- 压缩图片（使用 WebP 格式）
- 压缩 CSS 和 JavaScript
- 使用 CDN 加速静态资源

### 2. 优化缓存策略

- 静态资源使用长期缓存
- 动态内容使用短期缓存
- API 请求不缓存

### 3. 预缓存关键资源

在 Service Worker 安装时预缓存：
- 首页
- 登录页
- 核心 CSS/JS
- 常用图标

### 4. 懒加载非关键资源

- 图片懒加载
- 路由懒加载
- 按需加载组件

---

## 🔐 安全注意事项

### 1. HTTPS 必需

- 生产环境必须使用 HTTPS
- 使用有效的 SSL 证书
- 配置 HSTS 头

### 2. Content Security Policy

在 HTML 中添加 CSP 头：

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
               font-src 'self' https://fonts.gstatic.com;">
```

### 3. Service Worker 安全

- Service Worker 文件不要缓存
- 定期更新 Service Worker
- 验证缓存的资源完整性

---

## 📈 监控和分析

### 1. 安装率监控

在 Service Worker 中添加：

```javascript
self.addEventListener('appinstalled', (event) => {
  // 发送安装事件到分析服务
  console.log('PWA 已安装');
});
```

### 2. 离线使用监控

```javascript
self.addEventListener('fetch', (event) => {
  if (!navigator.onLine) {
    // 记录离线使用情况
    console.log('离线访问:', event.request.url);
  }
});
```

### 3. 性能监控

使用 Performance API 监控加载性能：

```javascript
window.addEventListener('load', () => {
  const perfData = performance.getEntriesByType('navigation')[0];
  console.log('页面加载时间:', perfData.loadEventEnd - perfData.fetchStart);
});
```

---

## 🎨 自定义主题

### 修改主题色

编辑 `manifest.json`：

```json
{
  "theme_color": "#e891a9",        // 状态栏颜色
  "background_color": "#faf5f7"    // 启动画面背景色
}
```

同时修改 HTML 中的 meta 标签：

```html
<meta name="theme-color" content="#e891a9">
```

### 添加启动画面

创建 `frontend/static/splash.html`：

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      background: linear-gradient(135deg, #faf5f7 0%, #f8e8ed 100%);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .logo {
      font-size: 4rem;
      animation: heartbeat 1.5s infinite;
    }
    @keyframes heartbeat {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.1); }
    }
  </style>
</head>
<body>
  <div class="logo">💕</div>
</body>
</html>
```

---

## 📚 参考资源

### 官方文档

- [MDN - Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Google - PWA 指南](https://web.dev/progressive-web-apps/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)

### 工具和库

- [Workbox](https://developers.google.com/web/tools/workbox) - Google 的 Service Worker 库
- [PWA Builder](https://www.pwabuilder.com/) - PWA 构建工具
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - PWA 审计工具

### 测试工具

- [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools)
- [PWA Testing Tool](https://www.pwatester.com/)
- [Manifest Validator](https://manifest-validator.appspot.com/)

---

## 🎉 更新日志

### v2.1.1 (2025-01-23)

- ✅ 完成 PWA 基础功能
- ✅ 添加 Service Worker 缓存策略
- ✅ 实现离线访问功能
- ✅ 优化移动端响应式布局
- ✅ 添加安装提示功能
- ✅ 支持刘海屏和底部手势条
- ✅ 添加触摸优化
- ✅ 支持减少动画模式
- ✅ 支持高对比度模式

### 计划中的功能

- 🔲 推送通知功能
- 🔲 后台同步功能
- 🔲 分享目标 API
- 🔲 快捷方式功能
- 🔲 暗色模式支持

---

## 💬 反馈和支持

如有问题或建议，请：

1. 查看本文档的常见问题部分
2. 在 GitHub 提交 Issue
3. 联系开发团队

---

**💕 用爱记录每一刻**
