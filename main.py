"""
心动积分项目 - 主入口文件
集成后端和前端功能的统一入口
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def display_menu():
    """显示项目主菜单"""
    print("=" * 50)
    print("🎯 心动积分项目 - 主入口")
    print("=" * 50)
    print("1. 启动后端服务")
    print("2. 启动前端应用")
    print("3. 运行示例程序")
    print("4. 运行测试")
    print("0. 退出")
    print("=" * 50)

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    try:
        # 这里将在后续实现中替换为实际的后端启动代码
        print("📢 后端服务启动成功！")
        print("💡 提示：后端API将在后续开发中实现")
        return True
    except Exception as e:
        print(f"❌ 后端服务启动失败: {e}")
        return False

def start_frontend():
    """启动前端应用"""
    print("🎨 启动前端应用...")
    try:
        # 这里将在后续实现中替换为实际的前端启动代码
        print("📢 前端应用启动成功！")
        print("💡 提示：前端界面将在后续开发中实现")
        return True
    except Exception as e:
        print(f"❌ 前端应用启动失败: {e}")
        return False

def run_example():
    """运行示例程序"""
    print("📝 运行示例程序...")
    try:
        # 导入并运行docs目录中的示例程序
        example_path = os.path.join("docs", "example_usage.py")
        if os.path.exists(example_path):
            with open(example_path, 'r', encoding='utf-8') as f:
                exec(f.read())
            print("✅ 示例程序运行成功！")
        else:
            print("⚠️  示例文件不存在，请检查docs/example_usage.py")
        return True
    except Exception as e:
        print(f"❌ 示例程序运行失败: {e}")
        return False

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    try:
        # 这里将在后续实现中替换为实际的测试运行代码
        print("📢 测试运行成功！")
        print("💡 提示：测试套件将在后续开发中实现")
        return True
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False

def main():
    """主程序入口"""
    print("🎉 欢迎使用心动积分项目！")
    
    while True:
        display_menu()
        choice = input("请输入您的选择 [0-4]: ")
        
        if choice == "1":
            start_backend()
        elif choice == "2":
            start_frontend()
        elif choice == "3":
            run_example()
        elif choice == "4":
            run_tests()
        elif choice == "0":
            print("👋 感谢使用，再见！")
            break
        else:
            print("❓ 无效的选择，请重新输入")
        
        # 按任意键继续
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
