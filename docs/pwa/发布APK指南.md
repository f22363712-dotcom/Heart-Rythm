# 心动积分 - 发布 Android APK 指南

## 🎯 目标

将当前的 PWA 应用发布为 Android APK，实现：
- ✅ 不需要本地运行脚本
- ✅ 随时随地使用
- ✅ 像原生应用一样流畅

---

## 📋 方案对比

| 特性 | 当前 PWA | 方案A: APK+云服务器 | 方案B: 完整打包APK |
|------|----------|---------------------|-------------------|
| 需要本地脚本 | ✅ 需要 | ❌ 不需要 | ❌ 不需要 |
| 随时随地使用 | ❌ 仅局域网 | ✅ 任何地方 | ✅ 任何地方 |
| 多设备同步 | ✅ 支持 | ✅ 支持 | ❌ 不支持 |
| 开发成本 | 低 | 中 | 高 |
| 服务器成本 | 无 | ¥100-300/年 | 无 |
| 跨平台 | iOS+Android | iOS+Android | 仅Android |

**推荐：方案 A（APK + 云服务器）**

---

## 🚀 方案 A：APK + 云服务器（推荐）

### 第一步：部署后端到云服务器

#### 1.1 购买云服务器

**推荐配置：**
- **阿里云/腾讯云** 轻量应用服务器
- CPU: 1核
- 内存: 1GB
- 带宽: 1Mbps
- 系统: Ubuntu 20.04
- **价格**: ¥100-200/年

**购买链接：**
- 阿里云: https://www.aliyun.com/product/swas
- 腾讯云: https://cloud.tencent.com/product/lighthouse

#### 1.2 配置服务器环境

```bash
# 1. 连接服务器（使用 SSH）
ssh root@your-server-ip

# 2. 更新系统
apt update && apt upgrade -y

# 3. 安装 Python 3.9+
apt install python3 python3-pip python3-venv -y

# 4. 安装 Nginx（反向代理）
apt install nginx -y

# 5. 安装 Supervisor（进程管理）
apt install supervisor -y
```

#### 1.3 上传项目代码

```bash
# 在本地电脑上，打包项目
cd "d:\Obsidian知识库\知识库\10_Projects\Python心动积分"
tar -czf heart-rhythm.tar.gz backend/ frontend/ requirements.txt

# 上传到服务器（使用 SCP 或 FTP）
scp heart-rhythm.tar.gz root@your-server-ip:/root/

# 在服务器上解压
ssh root@your-server-ip
cd /root
tar -xzf heart-rhythm.tar.gz
```

#### 1.4 安装依赖

```bash
# 创建虚拟环境
cd /root
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn  # 生产环境 WSGI 服务器
```

#### 1.5 配置 Supervisor（自动启动）

创建配置文件：`/etc/supervisor/conf.d/heart-rhythm.conf`

```ini
[program:heart-rhythm-backend]
command=/root/venv/bin/uvicorn api.main:app --host 127.0.0.1 --port 8000
directory=/root/backend
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/heart-rhythm-backend.err.log
stdout_logfile=/var/log/heart-rhythm-backend.out.log

[program:heart-rhythm-frontend]
command=/root/venv/bin/gunicorn -w 2 -b 127.0.0.1:5000 main:app
directory=/root/frontend
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/heart-rhythm-frontend.err.log
stdout_logfile=/var/log/heart-rhythm-frontend.out.log
```

启动服务：
```bash
supervisorctl reread
supervisorctl update
supervisorctl start all
```

#### 1.6 配置 Nginx（反向代理 + HTTPS）

创建配置文件：`/etc/nginx/sites-available/heart-rhythm`

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    # 前端
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用配置：
```bash
ln -s /etc/nginx/sites-available/heart-rhythm /etc/nginx/sites-enabled/
nginx -t  # 测试配置
systemctl restart nginx
```

#### 1.7 配置 HTTPS（必须！PWA 需要）

```bash
# 安装 Certbot
apt install certbot python3-certbot-nginx -y

# 自动配置 HTTPS
certbot --nginx -d your-domain.com

# 自动续期
certbot renew --dry-run
```

#### 1.8 配置域名

1. 购买域名（阿里云/腾讯云，约 ¥50/年）
2. 添加 A 记录指向服务器 IP
3. 等待 DNS 生效（5-10 分钟）

---

### 第二步：修改前端 API 地址

修改 `frontend/main.py`:

```python
# 原来的配置
API_BASE_URL = "http://localhost:8000"

# 改为云服务器地址
API_BASE_URL = "https://your-domain.com/api"
```

修改 `frontend/templates/base_new.html`:

```javascript
// 原来的配置
const API_BASE_URL = '/api';

// 改为云服务器地址
const API_BASE_URL = 'https://your-domain.com/api';
```

---

### 第三步：将 PWA 打包为 APK

#### 方法 1：使用 PWA Builder（最简单）

1. **访问 PWA Builder**
   - 网址: https://www.pwabuilder.com/

2. **输入你的 PWA 地址**
   - 输入: `https://your-domain.com`
   - 点击"Start"

3. **检查 PWA 质量**
   - 确保所有检查项都通过
   - 特别是 Manifest 和 Service Worker

4. **生成 APK**
   - 点击"Package For Stores"
   - 选择"Android"
   - 选择"Google Play"或"Signed APK"
   - 下载生成的 APK

5. **签名 APK**
   - 使用 Android Studio 或 jarsigner 签名
   - 或使用 PWA Builder 的在线签名工具

#### 方法 2：使用 Capacitor（更灵活）

```bash
# 1. 安装 Capacitor CLI
npm install -g @capacitor/cli

# 2. 初始化项目
cd frontend
npx cap init "心动积分" "com.heartrhythm.app"

# 3. 添加 Android 平台
npx cap add android

# 4. 配置 capacitor.config.json
{
  "appId": "com.heartrhythm.app",
  "appName": "心动积分",
  "webDir": "static",
  "server": {
    "url": "https://your-domain.com",
    "cleartext": true
  }
}

# 5. 同步文件
npx cap sync

# 6. 打开 Android Studio
npx cap open android

# 7. 在 Android Studio 中构建 APK
# Build → Build Bundle(s) / APK(s) → Build APK(s)
```

#### 方法 3：使用 Cordova（传统方法）

```bash
# 1. 安装 Cordova
npm install -g cordova

# 2. 创建项目
cordova create HeartRhythm com.heartrhythm.app "心动积分"
cd HeartRhythm

# 3. 添加 Android 平台
cordova platform add android

# 4. 修改 config.xml
<content src="https://your-domain.com" />

# 5. 构建 APK
cordova build android --release

# 6. 签名 APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore my-release-key.keystore \
  platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk \
  alias_name
```

---

### 第四步：测试 APK

1. **安装到测试设备**
   ```bash
   adb install app-release.apk
   ```

2. **测试功能**
   - [ ] 应用启动正常
   - [ ] 登录功能正常
   - [ ] 数据加载正常
   - [ ] 添加积分功能正常
   - [ ] 兑换奖励功能正常
   - [ ] 离线缓存正常

3. **性能测试**
   - [ ] 启动速度 < 3 秒
   - [ ] 页面切换流畅
   - [ ] 网络请求正常

---

### 第五步：发布 APK

#### 选项 A：上架 Google Play（推荐）

**优势：**
- ✅ 官方渠道，用户信任度高
- ✅ 自动更新
- ✅ 统计数据完善

**步骤：**
1. 注册 Google Play 开发者账号（$25 一次性费用）
2. 创建应用
3. 上传 APK（或 AAB）
4. 填写应用信息（描述、截图等）
5. 提交审核（通常 1-3 天）

**注意事项：**
- 需要隐私政策页面
- 需要应用图标和截图
- 需要符合 Google Play 政策

#### 选项 B：自行分发

**方式：**
1. **直接分享 APK 文件**
   - 上传到网盘（百度网盘、阿里云盘）
   - 生成下载链接
   - 用户需要允许"未知来源"安装

2. **托管在自己的网站**
   - 在网站上提供下载链接
   - 添加安装说明

3. **使用第三方应用商店**
   - 豌豆荚、应用宝、华为应用市场等
   - 审核相对宽松

---

## 💰 成本估算

### 方案 A：APK + 云服务器

| 项目 | 费用 | 周期 |
|------|------|------|
| 云服务器 | ¥100-200 | 年 |
| 域名 | ¥50 | 年 |
| SSL 证书 | 免费（Let's Encrypt） | - |
| Google Play 开发者 | $25（¥180） | 一次性 |
| **总计** | **¥330-430** | **首年** |
| **续费** | **¥150-250** | **每年** |

### 方案 B：完整打包 APK

| 项目 | 费用 | 周期 |
|------|------|------|
| 开发成本 | 高（需要重写后端） | - |
| Google Play 开发者 | $25（¥180） | 一次性 |
| **总计** | **¥180 + 开发时间** | **首年** |

---

## 🎯 推荐方案总结

### 最佳方案：PWA Builder + 云服务器

**步骤：**
1. 部署后端到云服务器（1-2 小时）
2. 配置域名和 HTTPS（30 分钟）
3. 使用 PWA Builder 生成 APK（10 分钟）
4. 测试并发布（1 小时）

**总时间：** 约 3-4 小时
**总成本：** ¥330-430（首年）

**优势：**
- ✅ 开发成本低
- ✅ 维护简单
- ✅ 跨平台（iOS 也能用）
- ✅ 功能完整

---

## 📝 快速检查清单

### 部署前检查
- [ ] 云服务器已购买
- [ ] 域名已购买并解析
- [ ] Python 环境已安装
- [ ] 依赖已安装
- [ ] 数据库已初始化

### 部署后检查
- [ ] 后端 API 可访问
- [ ] 前端页面正常显示
- [ ] HTTPS 配置成功
- [ ] Service Worker 注册成功
- [ ] PWA 可以安装

### APK 打包检查
- [ ] API 地址已修改为云服务器
- [ ] Manifest 配置正确
- [ ] 图标和启动画面已设置
- [ ] APK 已签名
- [ ] 在真机上测试通过

### 发布前检查
- [ ] 应用信息完整
- [ ] 截图和描述已准备
- [ ] 隐私政策已发布
- [ ] 测试账号已准备
- [ ] 版本号已更新

---

## 🆘 常见问题

### Q1: 云服务器配置太低会不会卡？

**A:** 1核1GB 足够！
- 这个应用很轻量
- 预计同时在线用户 < 10 人
- 如果用户增多，可以随时升级

### Q2: 不会配置服务器怎么办？

**A:** 可以使用宝塔面板！
- 安装宝塔面板（免费）
- 图形化界面，操作简单
- 一键部署 Python 应用

### Q3: 没有域名可以吗？

**A:** 不行！
- PWA 必须使用 HTTPS
- HTTPS 需要域名
- 域名很便宜（¥50/年）

### Q4: 可以用免费服务器吗？

**A:** 不推荐！
- 免费服务器不稳定
- 可能随时关闭
- 性能差，用户体验不好

---

## 🎉 下一步

现在你有两个选择：

### 选择 1：继续使用 PWA（当前方案）
- 适合：仅自己或家人使用
- 优势：零成本
- 劣势：需要电脑运行脚本

### 选择 2：发布 APK（推荐）
- 适合：想随时随地使用
- 优势：专业、方便
- 劣势：需要一些成本（¥330/年）

**我的建议：**
- 先用 PWA 测试一段时间
- 确认功能稳定后再发布 APK
- 这样可以避免浪费

---

**文档版本：** v1.0
**更新日期：** 2025-01-23
