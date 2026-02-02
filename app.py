"""
云端部署完整启动脚本 v2.2
同时启动 API 和前端静态文件服务
更新时间: 2026-02-02
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入原始的 API app（供 Vercel 使用）
from backend.api.main import app as api_app

# 挂载为模块级别的 app 实例（Vercel 需要）
app = api_app

# 获取前端模板目录
frontend_templates_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "frontend", "templates"
)

# 挂载静态文件目录
frontend_static_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "frontend", "static"
)

if os.path.exists(frontend_static_dir):
    app.mount("/static", StaticFiles(directory=frontend_static_dir), name="static")

# 添加前端页面路由
@app.get("/")
def serve_index():
    """首页"""
    index_path = os.path.join(frontend_templates_dir, "index_new.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "前端模板未找到，请检查 frontend/templates 目录"}

@app.get("/login")
def serve_login():
    """登录页"""
    login_path = os.path.join(frontend_templates_dir, "login.html")
    if os.path.exists(login_path):
        return FileResponse(login_path)
    return {"message": "登录页面未找到"}

@app.get("/dashboard")
def serve_dashboard():
    """仪表板"""
    dashboard_path = os.path.join(frontend_templates_dir, "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"message": "仪表板页面未找到"}

@app.get("/rewards")
def serve_rewards():
    """奖励管理"""
    rewards_path = os.path.join(frontend_templates_dir, "rewards_new.html")
    if os.path.exists(rewards_path):
        return FileResponse(rewards_path)
    return {"message": "奖励页面未找到"}

@app.get("/admin")
def serve_admin():
    """管理员后台"""
    admin_path = os.path.join(frontend_templates_dir, "admin.html")
    if os.path.exists(admin_path):
        return FileResponse(admin_path)
    return {"message": "管理员页面未找到"}

# ==================== 启动函数 ====================

def start_backend():
    """启动后端服务（用于本地运行和 Railway 部署）"""
    print("🚀 启动完整应用（API + 前端）...")
    print(f"📂 当前目录: {os.getcwd()}")
    print(f"📂 Python路径: {sys.path[0]}")

    try:
        import uvicorn

        # 从环境变量获取端口，默认 8000
        port = int(os.environ.get('PORT', 8000))

        print(f"🌐 服务启动在端口: {port}")
        print(f"📄 前端页面: http://0.0.0.0:{port}/")
        print(f"📚 API文档: http://0.0.0.0:{port}/docs")

        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # 启动服务
    start_backend()
