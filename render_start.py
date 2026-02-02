#!/usr/bin/env python3
"""
Render 部署入口脚本
确保在正确的目录下启动服务
"""
import os
import sys
import subprocess

# 打印调试信息
print("=" * 50)
print("🔍 Render 部署诊断信息")
print("=" * 50)
print(f"当前工作目录: {os.getcwd()}")
print(f"脚本所在路径: {__file__}")
print(f"Python 路径: {sys.path}")
print("=" * 50)

# 查找项目根目录（包含 server.py 的目录）
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📂 项目根目录: {current_dir}")

# 切换到项目根目录
os.chdir(current_dir)
print(f"✅ 已切换到项目根目录")

# 检查必要文件
required_files = ['server.py', 'backend/api/main.py', 'requirements.txt']
missing_files = []
for f in required_files:
    if not os.path.exists(f):
        missing_files.append(f)
    else:
        print(f"✅ 找到文件: {f}")

if missing_files:
    print(f"❌ 缺少文件: {missing_files}")
    sys.exit(1)

print("=" * 50)
print("🚀 启动服务...")
print("=" * 50)

# 使用 subprocess 启动 server.py，确保在正确目录下运行
try:
    result = subprocess.run(
        [sys.executable, 'server.py'],
        cwd=current_dir,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"❌ 服务启动失败: {e}")
    sys.exit(e.returncode)
except Exception as e:
    print(f"❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
