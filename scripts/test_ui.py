"""
UI测试脚本 - 验证玻璃态设计
"""
import requests
import time

BASE_URL = "http://localhost:5000"

def test_pages():
    """测试所有页面是否可访问"""
    print("\n" + "="*60)
    print("测试玻璃态UI页面")
    print("="*60)

    pages = [
        ("/", "首页"),
        ("/login", "登录页面"),
        ("/dashboard", "用户仪表板"),
        ("/rewards", "奖励管理"),
        ("/admin", "管理员后台"),
    ]

    print("\n页面访问测试:")
    for path, name in pages:
        try:
            response = requests.get(BASE_URL + path, timeout=5)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"{status} {name} ({path}): 状态码 {response.status_code}")
        except Exception as e:
            print(f"❌ {name} ({path}): 错误 - {e}")

def check_glass_effect():
    """检查玻璃态效果关键词"""
    print("\n" + "="*60)
    print("检查玻璃态设计元素")
    print("="*60)

    try:
        response = requests.get(BASE_URL, timeout=5)
        html = response.text

        checks = [
            ("backdrop-filter", "背景模糊效果"),
            ("rgba(255, 255, 255, 0.75)", "半透明卡片"),
            ("Ma Shan Zheng", "可爱字体"),
            ("floating-hearts", "浮动爱心"),
            ("border-radius: var(--radius-pill)", "胶囊按钮"),
            ("linear-gradient", "渐变色彩"),
        ]

        print("\n设计元素检查:")
        for keyword, description in checks:
            if keyword in html:
                print(f"✅ {description}: 已应用")
            else:
                print(f"❌ {description}: 未找到")

    except Exception as e:
        print(f"❌ 检查失败: {e}")

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("心动积分系统 - 玻璃态UI测试")
    print("="*60)

    print("\n提示: 请确保前端服务已启动 (http://localhost:5000)")
    print("等待服务启动...")
    time.sleep(2)

    # 测试页面访问
    test_pages()

    # 检查玻璃态效果
    check_glass_effect()

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
    print("\n💡 建议:")
    print("1. 在浏览器中访问 http://localhost:5000 查看实际效果")
    print("2. 检查以下特性:")
    print("   - 卡片是否有半透明玻璃效果")
    print("   - 按钮是否为胶囊形状")
    print("   - 背景是否有浮动爱心")
    print("   - 标题是否使用可爱字体")
    print("   - 悬停时是否有平滑动画")

if __name__ == "__main__":
    main()
