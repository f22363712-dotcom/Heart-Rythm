"""
云端部署启动脚本
同时启动后端和前端服务，使用 gunicorn 作为生产服务器
"""

import os
import sys
import subprocess
import threading
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_backend():
    """启动后端服务 - 使用 gunicorn"""
    print("🚀 启动后端服务...")
    try:
        # 在生产环境使用 gunicorn
        if os.environ.get('RENDER') or os.environ.get('VERCEL') or os.environ.get('RAILWAY'):
            # 云端环境：直接运行 uvicorn
            import uvicorn
            from backend.api.main import app
            uvicorn.run(app, host="0.0.0.0", port=8000)
        else:
            # 本地环境：使用 gunicorn
            subprocess.run([
                "gunicorn",
                "backend.api.main:app",
                "--workers", "1",
                "--worker-class", "uvicorn.workers.UvicornWorker",
                "--bind", "0.0.0.0:8000",
                "--timeout", "120"
            ])
    except ImportError:
        # 如果没有 gunicorn，回退到 uvicorn
        print("⚠️  gunicorn 未安装，使用 uvicorn...")
        import uvicorn
        from backend.api.main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"❌ 后端服务启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 启动后端服务
    start_backend()
