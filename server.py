"""
云端部署启动脚本
启动 FastAPI 后端服务
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    print(f"📂 当前目录: {os.getcwd()}")
    print(f"📂 Python路径: {sys.path[0]}")

    try:
        import uvicorn
        from backend.api.main import app

        # 从环境变量获取端口，默认 8000
        port = int(os.environ.get('PORT', 8000))

        print(f"🌐 服务启动在端口: {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"❌ 后端服务启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # 启动后端服务
    start_backend()
