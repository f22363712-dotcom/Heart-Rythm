# UI设计说明 - 玻璃态风格

## 🎨 设计理念

心动积分系统v2.0采用**玻璃态（Glassmorphism）**设计风格，营造温馨浪漫的氛围感。

---

## ✨ 核心设计元素

### 1. 玻璃态卡片 🪟

**特点**:
- 半透明背景：`rgba(255, 255, 255, 0.75)`
- 背景模糊：`backdrop-filter: blur(12px)`
- 柔和阴影：`0 8px 32px rgba(232, 74, 127, 0.1)`
- 圆角设计：`border-radius: 20px`

**效果**:
- 卡片像磨砂玻璃一样，能看到背后的渐变背景
- 悬停时上浮，增强交互感
- 视觉层次分明

### 2. 浮动爱心背景 💕

**特点**:
- 4个爱心emoji缓慢上浮
- 15秒完整动画循环
- 旋转720度
- 透明度0.15，不干扰内容

**效果**:
- 营造浪漫氛围
- 动态背景增加趣味性
- 不影响内容阅读

### 3. 胶囊按钮 💊

**特点**:
- 完全圆角：`border-radius: 50px`
- 渐变色彩：`linear-gradient(135deg, #ff6b8a 0%, #e84a7f 100%)`
- 悬停上浮：`transform: translateY(-2px)`
- 阴影增强：`box-shadow: 0 4px 15px`

**效果**:
- 更加柔和友好
- 视觉吸引力强
- 交互反馈明显

### 4. Ma Shan Zheng字体 ✍️

**应用范围**:
- 所有标题（h1-h5）
- 导航栏品牌名
- 页面大标题

**效果**:
- 手写风格，温馨可爱
- 增强情感表达
- 符合情侣主题

### 5. 粉色渐变主题 🌸

**配色方案**:
```css
--primary-pink: #ff6b8a    /* 主粉色 */
--primary-rose: #e84a7f    /* 玫瑰粉 */
--accent-coral: #ff8a80    /* 珊瑚粉 */
--bg-cream: #fff9f5        /* 奶油白 */
```

**渐变背景**:
```css
linear-gradient(135deg, #fff9f5 0%, #fff0f3 50%, #ffe4ec 100%)
```

---

## 🎯 组件样式指南

### 导航栏
- 半透明粉色：`rgba(255, 107, 138, 0.85)`
- 背景模糊：`backdrop-filter: blur(10px)`
- 固定顶部：`sticky-top`

### 卡片
- 玻璃态背景
- 悬停上浮5px
- 阴影增强效果

### 按钮
| 类型 | 颜色 | 用途 |
|------|------|------|
| primary | 粉色渐变 | 主要操作 |
| success | 绿色渐变 | 成功/兑换 |
| warning | 黄色渐变 | 警告/提醒 |
| danger | 红色渐变 | 删除/危险 |
| info | 蓝色渐变 | 信息/刷新 |

### 输入框
- 圆角12px
- 聚焦时粉色边框
- 光晕效果：`box-shadow: 0 0 0 4px rgba(255, 107, 138, 0.15)`

### 模态框
- 高度透明：`rgba(255, 255, 255, 0.95)`
- 强背景模糊：`backdrop-filter: blur(20px)`
- 大圆角：`border-radius: 24px`

### 列表
- 玻璃态背景
- 悬停右移5px
- 圆角12px

### 表格
- 玻璃态背景
- 表头粉色淡背景
- 悬停行高亮

---

## 🎭 动画效果

### 1. 浮动爱心
```css
@keyframes float-up {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
}
```

### 2. 卡片悬停
```css
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(232, 74, 127, 0.2);
}
```

### 3. 按钮悬停
```css
.btn:hover {
    transform: translateY(-2px);
}
```

### 4. 列表悬停
```css
.list-group-item:hover {
    transform: translateX(5px);
}
```

---

## 📱 响应式设计

### 断点
- **桌面**: > 992px
- **平板**: 768px - 992px
- **手机**: < 768px

### 适配策略
- 使用Bootstrap的栅格系统
- 卡片自动换行
- 导航栏折叠菜单
- 表格横向滚动

---

## 🎨 设计对比

### v1.0 vs v2.0

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 卡片背景 | 纯白色 | 半透明玻璃态 |
| 按钮形状 | 圆角矩形 | 胶囊形状 |
| 按钮颜色 | 纯色 | 渐变色 |
| 背景 | 静态渐变 | 渐变+浮动爱心 |
| 字体 | 标准字体 | Ma Shan Zheng |
| 阴影 | 标准阴影 | 柔和粉色阴影 |
| 动画 | 基础过渡 | 多种悬停动画 |

---

## 🛠️ 技术实现

### CSS变量系统
```css
:root {
    --primary-pink: #ff6b8a;
    --card-bg: rgba(255, 255, 255, 0.75);
    --glass-border: 1px solid rgba(255, 255, 255, 0.6);
    --shadow-soft: 0 8px 32px rgba(232, 74, 127, 0.1);
    --radius-large: 20px;
    --radius-pill: 50px;
}
```

### 关键CSS属性
- `backdrop-filter: blur()` - 背景模糊
- `rgba()` - 半透明颜色
- `linear-gradient()` - 渐变色
- `transform` - 变换动画
- `transition` - 平滑过渡

---

## 📝 使用建议

### 添加新组件时
1. 使用CSS变量保持一致性
2. 卡片使用`.card`类自动获得玻璃态
3. 按钮使用`.btn`类自动获得胶囊形状
4. 输入框使用`.form-control`自动获得圆角

### 自定义样式时
1. 优先使用`{% block extra_css %}`
2. 保持与主题一致的配色
3. 使用相同的圆角和阴影变量
4. 添加平滑的过渡动画

---

## 🎯 设计目标达成

✅ **视觉层次**: 通过透明度和模糊营造深度
✅ **氛围感**: 浮动爱心增加浪漫氛围
✅ **现代感**: 玻璃态是2024年流行设计趋势
✅ **一致性**: 所有页面统一设计语言
✅ **交互性**: 丰富的悬停和点击反馈
✅ **可读性**: 保持良好的文字对比度

---

## 🔄 回退方案

如需回退到旧版UI:

```bash
# 查看提交历史
git log --oneline

# 回退到UI升级前的版本
git checkout 0f6a305  # UI升级前的commit

# 或创建新分支保留旧版
git checkout -b v2-old-ui 0f6a305
```

---

## 📞 反馈

如对UI设计有建议，欢迎提出！

---

**设计师**: Claude Sonnet 4.5
**设计日期**: 2026年1月21日
**设计风格**: Glassmorphism (玻璃态)
