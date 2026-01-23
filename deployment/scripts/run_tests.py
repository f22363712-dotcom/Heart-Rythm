#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
心动积分项目 - 测试运行脚本
使用全局 Python 环境，避免虚拟环境依赖问题
"""

import os
import sys
import subprocess

def main():
    """运行所有测试"""
    print("=" * 50)
    print("  心动积分项目 - 运行所有测试")
    print("=" * 50)
    print()

    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print(f"当前目录: {os.getcwd()}")
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}")
    print()

    # 强制使用全局 Python（忽略虚拟环境）
    # 设置环境变量，防止激活虚拟环境
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    # 清除 VIRTUAL_ENV 环境变量
    if 'VIRTUAL_ENV' in os.environ:
        del os.environ['VIRTUAL_ENV']

    # 检查tests目录是否存在
    if not os.path.exists("tests"):
        print("❌ 错误: tests目录不存在！")
        print(f"当前目录下的文件/文件夹:")
        for item in os.listdir("."):
            print(f"  - {item}")
        return 1

    print("✅ tests目录存在")
    print()
    print("开始运行测试...")
    print()

    # 直接使用当前 Python 运行 pytest
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            cwd=script_dir,
            capture_output=False,
            text=True,
            env=os.environ  # 使用修改后的环境变量
        )
        return result.returncode
    except KeyboardInterrupt:
        print("\n\n❌ 测试被用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 运行测试时出错: {e}")
        return 1

if __name__ == "__main__":
    print()
    exit_code = main()
    print()
    print("=" * 50)
    if exit_code == 0:
        print("✅ 所有测试通过！")
    else:
        print("❌ 测试失败")
    print("=" * 50)
    print()
    sys.exit(exit_code)
