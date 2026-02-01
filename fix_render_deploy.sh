#!/bin/bash
# Render 部署修复脚本
# 用于解决 Render 错误的 Root Directory 配置

echo "🔍 Render 部署诊断工具"
echo "=========================="

# 检查当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 当前分支: $CURRENT_BRANCH"

# 检查 server.py 是否存在
if [ -f "server.py" ]; then
    echo "✅ server.py 存在于根目录"
else
    echo "❌ server.py 不存在！"
    exit 1
fi

# 检查 backend/api/main.py
if [ -f "backend/api/main.py" ]; then
    echo "✅ backend/api/main.py 存在"
else
    echo "❌ backend/api/main.py 不存在！"
    exit 1
fi

echo ""
echo "📋 请按照以下步骤操作："
echo ""
echo "1️⃣  完全删除现有的 Render 服务"
echo "   - 登录 https://dashboard.render.com"
echo "   - 找到 heart-rhythm-backend 服务"
echo "   - 点击 Settings → Delete Service"
echo ""
echo "2️⃣  使用以下链接重新创建服务："
echo "   https://render.com/new/web-service"
echo ""
echo "3️⃣  配置服务（重要！）："
echo "   - GitHub Repository: Heart-Rythm"
echo "   - Branch: v2.1 ⚠️"
echo "   - Name: heart-rhythm-api"
echo "   - Environment: Python 3"
echo "   - Root Directory: 【留空！不要填写任何内容】⚠️"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python server.py"
echo ""
echo "4️⃣  如果 Root Directory 字段无法修改或显示为 src:"
echo "   - 先删除服务"
echo "   - 等待 1 分钟"
echo "   - 重新创建服务"
echo ""
echo "📌 如果问题仍然存在，请考虑使用 Railway："
echo "   https://railway.app/new"
echo "   Railway 会自动检测配置，更少问题"
