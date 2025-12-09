"""
心动积分项目 - 主入口文件
集成后端和前端功能的统一入口
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

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
        import uvicorn
        from backend.api.main import app
        print("📢 后端服务正在启动...")
        print("🌐 API文档地址: http://localhost:8000/docs")
        print("🌐 重新加载: http://localhost:8000/reload")
        print("📝 按Ctrl+C停止服务")
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
        return True
    except Exception as e:
        print(f"❌ 后端服务启动失败: {e}")
        return False

def start_frontend():
    """启动前端应用"""
    print("🎨 启动前端应用...")
    try:
        import uvicorn
        from frontend.main import app as frontend_app
        print("📢 前端应用正在启动...")
        print("🌐 前端访问地址: http://localhost:5000")
        print("📝 按Ctrl+C停止服务")
        # 注意：Flask应用使用Flask自带的run方法，而不是uvicorn
        from frontend.main import app
        app.run(host="0.0.0.0", port=5000, debug=True)
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
        import pytest
        # 运行所有测试
        result = pytest.main(["-v"])
        if result == 0:
            print("📢 测试运行成功！")
            return True
        else:
            print(f"📢 测试运行完成，但有 {result} 个测试失败！")
            return False
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False

class TextRedirector:
    """将stdout重定向到Text组件"""
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
    
    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")
    
    def flush(self):
        pass

class HeartRhythmGUI(tk.Tk):
    """心动积分项目GUI界面"""
    
    def __init__(self):
        super().__init__()
        self.title("🎯 心动积分项目")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # 设置主题
        style = ttk.Style()
        style.theme_use("clam")
        
        # 创建主框架
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(main_frame, text="🎯 心动积分项目", font=('Arial', 18, 'bold'))
        title_label.pack(pady=10)
        
        # 创建描述
        desc_label = ttk.Label(main_frame, text="情侣积分管理系统 - 帮助情侣记录和管理彼此的积分")
        desc_label.pack(pady=5)
        
        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20, fill=tk.X)
        
        # 按钮样式
        style.configure("TButton", font=('Arial', 12), padding=15)
        
        # 功能按钮
        button_configs = [
            ("🚀 启动后端服务", self.start_backend_gui),
            ("🎨 启动前端应用", self.start_frontend_gui),
            ("📝 运行示例程序", self.run_example_gui),
            ("🧪 运行测试", self.run_tests_gui),
            ("❌ 退出", self.quit)
        ]
        
        for text, command in button_configs:
            ttk.Button(button_frame, text=text, command=command).pack(fill=tk.X, pady=5)
        
        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(status_frame, text="状态: ", font=('Arial', 10)).pack(side=tk.LEFT)
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=('Arial', 10, 'bold'), foreground="blue")
        status_label.pack(side=tk.LEFT)
        
        # 输出日志
        log_frame = ttk.LabelFrame(main_frame, text="输出日志")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, width=70, font=('Consolas', 10))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 重定向print到日志框
        sys.stdout = TextRedirector(self.log_text, "stdout")
    
    def start_backend_gui(self):
        """启动后端服务（GUI版本）"""
        self.status_var.set("启动后端服务中...")
        threading.Thread(target=self._run_with_status, args=(start_backend, "后端服务启动完成", "后端服务启动失败")).start()
    
    def start_frontend_gui(self):
        """启动前端应用（GUI版本）"""
        self.status_var.set("启动前端应用中...")
        threading.Thread(target=self._run_with_status, args=(start_frontend, "前端应用启动完成", "前端应用启动失败")).start()
    
    def run_example_gui(self):
        """运行示例程序（GUI版本）"""
        self.status_var.set("运行示例程序中...")
        threading.Thread(target=self._run_with_status, args=(run_example, "示例程序运行完成", "示例程序运行失败")).start()
    
    def run_tests_gui(self):
        """运行测试（GUI版本）"""
        self.status_var.set("运行测试中...")
        threading.Thread(target=self._run_with_status, args=(run_tests, "测试运行完成", "测试运行失败")).start()
    
    def _run_with_status(self, func, success_msg, error_msg):
        """在后台线程中运行函数并更新状态"""
        try:
            result = func()
            if result:
                self.status_var.set(success_msg)
            else:
                self.status_var.set(error_msg)
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"操作失败: {e}")
    
    def quit(self):
        """退出应用"""
        if messagebox.askokcancel("退出", "确定要退出心动积分项目吗？"):
            super().quit()

def main():
    """主程序入口"""
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        # 命令行模式
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
    else:
        # GUI模式
        app = HeartRhythmGUI()
        app.mainloop()

if __name__ == "__main__":
    main()
