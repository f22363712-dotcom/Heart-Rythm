"""
前端功能测试脚本
测试登录、注册等功能
"""
import requests
import time

BASE_URL = "http://localhost:5000"
API_URL = "http://localhost:5000/api"

def test_frontend_pages():
    """测试前端页面是否可访问"""
    print("\n" + "="*60)
    print("测试前端页面访问")
    print("="*60)

    pages = [
        ("/", "首页"),
        ("/login", "登录页面"),
    ]

    for path, name in pages:
        try:
            response = requests.get(BASE_URL + path, timeout=5)
            if response.status_code == 200:
                print(f"✓ {name} ({path}): 正常")
            else:
                print(f"✗ {name} ({path}): 状态码 {response.status_code}")
        except Exception as e:
            print(f"✗ {name} ({path}): 错误 - {e}")

def test_login_flow():
    """测试登录流程"""
    print("\n" + "="*60)
    print("测试登录流程")
    print("="*60)

    # 测试登录
    login_data = {
        "username": "couple_test001",
        "password": "123456"
    }

    try:
        response = requests.post(f"{API_URL}/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 登录成功")
            print(f"  - 用户名: {data['user']['username']}")
            print(f"  - Token: {data['token'][:20]}...")
            if data.get('couple'):
                print(f"  - 情侣: {data['couple']['names'][0]} & {data['couple']['names'][1]}")
                print(f"  - 积分: {data['couple']['points']}")
            return data['token']
        else:
            print(f"✗ 登录失败: {response.json()}")
            return None
    except Exception as e:
        print(f"✗ 登录错误: {e}")
        return None

def test_authenticated_request(token):
    """测试需要认证的请求"""
    print("\n" + "="*60)
    print("测试认证请求")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # 获取当前用户信息
        response = requests.get(f"{API_URL}/auth/me", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 获取用户信息成功")
            print(f"  - 用户ID: {data['user_id']}")
            print(f"  - 用户名: {data['username']}")
        else:
            print(f"✗ 获取用户信息失败: {response.status_code}")

        # 获取情侣信息
        response = requests.get(f"{API_URL}/couples/me", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 获取情侣信息成功")
            print(f"  - 情侣ID: {data['couple_id']}")
            print(f"  - 名字: {data['names']}")
            print(f"  - 积分: {data['points']}")
        else:
            print(f"✗ 获取情侣信息失败: {response.status_code}")

    except Exception as e:
        print(f"✗ 请求错误: {e}")

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("心动积分系统 - 前端功能测试")
    print("="*60)

    # 等待服务启动
    print("\n等待服务启动...")
    time.sleep(2)

    # 测试前端页面
    test_frontend_pages()

    # 测试登录流程
    token = test_login_flow()

    if token:
        # 测试认证请求
        test_authenticated_request(token)

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
    print("\n提示: 请在浏览器中访问 http://localhost:5000 查看完整界面")

if __name__ == "__main__":
    main()
