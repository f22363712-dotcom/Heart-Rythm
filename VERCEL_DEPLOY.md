# Vercel 部署详细指南 - v2.1 分支

## 🚀 快速部署步骤

### 步骤 1：使用直接链接（最简单）

**复制并打开这个链接**（自动选择 v2.1 分支）：
```
https://vercel.com/new?clone=&repository.name=heart-rythm&repository.url=https%3A%2F%2Fgithub.com%2Ff22363712-dotcom%2FHeart-Rythm&repository.branch=v2.1
```

### 步骤 2：手动配置（如果上述链接不工作）

1. **登录 Vercel**
   - 访问 https://vercel.com
   - 点击 "Sign Up" 或 "Login"
   - 使用 **Continue with GitHub**

2. **点击 "Add New..." → "Project"**

3. **导入 GitHub 仓库**
   - 找到 **Heart-Rythm** 仓库
   - 点击 **"Import"** 按钮

4. **配置项目**（重要！）

   在 "Configure Project" 页面：

   | 配置项 | 值 | 位置 |
   |--------|-----|------|
   | **Project Name** | `heart-rythm` | 顶部 |
   | **Framework Preset** | `Other` | 下拉菜单 |
   | **Root Directory** | `./` | 留空 |
   | **Build Command** | `pip install -r requirements.txt` | 输入框 |
   | **Start Command** | `python app.py` | 输入框 |
   | **Branch** | **v2.1** ⚠️ | 下拉菜单 |

   **注意**：Branch 选项通常在页面的 **"Environment Variables"** 下方

5. **点击 "Deploy"**

6. **等待部署完成**（约 2-3 分钟）

---

## 🔧 如果找不到 Branch 选项

### 方法 A：导入后修改

1. 先导入项目（使用默认分支）
2. 进入项目 → **Settings** → **Git**
3. 修改 **"Production Branch"** 为 `v2.1`
4. 保存后点击 **"Redeploy"**

### 方法 B：删除重建

1. 在 Vercel Dashboard 删除刚创建的项目
2. 重新导入，这次在导入界面仔细查找 Branch 下拉菜单
3. Branch 选项通常在：
   - "Configure Project" 部分的底部
   - 或者点击 "Show Advanced" 后显示

---

## 📱 部署成功后

你会得到一个 URL：
```
https://heart-rythm.vercel.app
```

或
```
https://heart-rythm-你的用户名.vercel.app
```

访问这个 URL，你应该看到：
- ✅ 完整的登录页面
- ✅ 网页界面（不是 JSON）

---

## ❓ 常见问题

### Q: 我完全找不到 Branch 选项

**A**: Vercel 新版本可能隐藏了这个选项。尝试：
1. 导入后在项目设置中修改
2. 或使用上面的直接链接

### Q: 部署后还是显示 JSON

**A**: 检查以下几点：
1. 确认使用的是 `v2.1` 分支
2. 确认 Start Command 是 `python app.py`
3. 查看部署日志，确认 `app.py` 被执行

### Q: 部署失败怎么办

**A**: 查看 Vercel 的部署日志：
1. 进入项目 → **Deployments**
2. 点击最新的部署
3. 查看 **Build Logs** 找到错误信息

---

## 🎯 一键部署链接总结

**复制以下任一链接到浏览器打开**：

### 链接 1（推荐）
```
https://vercel.com/new?clone=&repository.name=heart-rythm&repository.url=https%3A%2F%2Fgithub.com%2Ff22363712-dotcom%2FHeart-Rythm&repository.branch=v2.1
```

### 链接 2（备用）
```
https://vercel.com/new/clone?repository-url=https://github.com/f22363712-dotcom/Heart-Rythm.git&branch=v2.1
```

打开链接后，只需：
1. 登录 GitHub
2. 点击 "Deploy"
3. 等待完成！

---

## ✅ 部署验证清单

部署完成后，检查：

- [ ] 访问域名能看到登录页面（不是 JSON）
- [ ] 能访问 /docs 查看 API 文档
- [ ] 能访问 /dashboard 进入仪表板
- [ ] 没有控制台错误（F12 查看）

全部通过？恭喜你部署成功了！🎉
