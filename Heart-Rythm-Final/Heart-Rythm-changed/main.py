"""
心动积分项目 - 主入口文件
统一管理后端和前端服务的启动
"""

import os
import sys
import subprocess
import threading
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def display_banner():
    """显示欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        💕 心动积分项目 - Heart Rhythm System 💕          ║
║                                                          ║
║        专为情侣设计的积分管理系统                         ║
║        用爱记录每一刻                                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_menu():
    """显示主菜单"""
    print("\n" + "=" * 50)
    print("🎯 请选择操作:")
    print("=" * 50)
    print("  [1] 🚀 启动后端服务 (端口: 8000)")
    print("  [2] 🎨 启动前端应用 (端口: 5000)")
    print("  [3] 🔥 同时启动后端和前端")
    print("  [4] 📝 运行示例程序")
    print("  [5] 🧪 运行测试")
    print("  [0] 👋 退出")
    print("=" * 50)


def start_backend():
    """启动后端服务"""
    print("\n🚀 正在启动后端服务...")
    print("📍 API地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("💡 按 Ctrl+C 停止服务\n")
    
    try:
        import uvicorn
        from backend.api.main import app
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n✅ 后端服务已停止")
    except Exception as e:
        print(f"\n❌ 启动后端失败: {e}")


def start_frontend():
    """启动前端应用"""
    print("\n🎨 正在启动前端应用...")
    print("📍 前端地址: http://localhost:5000")
    print("💡 按 Ctrl+C 停止服务\n")
    
    try:
        from frontend.main import app
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n✅ 前端应用已停止")
    except Exception as e:
        print(f"\n❌ 启动前端失败: {e}")


def start_both():
    """同时启动后端和前端"""
    print("\n🔥 正在同时启动后端和前端...")
    print("=" * 50)
    print("📍 后端API: http://localhost:8000")
    print("📍 前端界面: http://localhost:5000")
    print("📚 API文档: http://localhost:8000/docs")
    print("=" * 50)
    print("💡 按 Ctrl+C 停止所有服务\n")
    
    # 在后台线程启动后端
    backend_thread = threading.Thread(target=lambda: subprocess.run(
        [sys.executable, "-m", "uvicorn", "backend.api.main:app", 
         "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    ), daemon=True)
    backend_thread.start()
    
    # 等待后端启动并检查健康状态
    print("🔍 正在检查后端服务健康状态...")
    backend_ready = False
    import requests
    for _ in range(30):  # 最多等待30秒
        try:
            response = requests.get("http://localhost:8000/health/", timeout=1)
            if response.status_code == 200:
                backend_ready = True
                break
        except:
            pass
        time.sleep(1)
        print(".", end="", flush=True)
    
    if not backend_ready:
        print("\n❌ 后端服务启动失败或超时，请检查日志")
        return
    
    print("\n✅ 后端服务已成功启动")
    
    # 启动前端
    try:
        from frontend.main import app
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n✅ 所有服务已停止")


def run_example():
    """运行示例程序"""
    print("\n📝 运行示例程序...")
    example_path = os.path.join("docs", "example_usage.py")
    
    if os.path.exists(example_path):
        try:
            subprocess.run([sys.executable, example_path])
        except Exception as e:
            print(f"❌ 运行示例失败: {e}")
    else:
        print("⚠️  示例文件不存在")


def run_tests():
    """运行测试"""
    print("\n🧪 运行测试...")
    try:
        import pytest
        pytest.main(["-v", "tests/"])
    except ImportError:
        print("❌ pytest 未安装，请先运行: pip install pytest")
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")


def main():
    """主函数"""
    display_banner()
    
    while True:
        display_menu()
        
        try:
            choice = input("\n请输入选择 [0-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 再见！")
            break
        
        if choice == "1":
            start_backend()
        elif choice == "2":
            start_frontend()
        elif choice == "3":
            start_both()
        elif choice == "4":
            run_example()
        elif choice == "5":
            run_tests()
        elif choice == "0":
            print("\n👋 再见！祝您和爱人幸福美满！💕")
            break
        else:
            print("\n⚠️  无效选择，请重新输入")


if __name__ == "__main__":
    main()
