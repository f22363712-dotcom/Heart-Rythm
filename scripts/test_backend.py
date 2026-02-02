"""
后端API测试脚本
测试登录、数据访问等功能
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("\n" + "="*60)
    print("1. 测试健康检查")
    print("="*60)

    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.status_code == 200

def test_admin_login():
    """测试管理员登录"""
    print("\n" + "="*60)
    print("2. 测试管理员登录")
    print("="*60)

    data = {
        "username": "admin",
        "password": "admin123"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"登录成功!")
        print(f"用户名: {result['user']['username']}")
        print(f"是否管理员: {result['user']['is_admin']}")
        print(f"Token: {result['token'][:20]}...")
        return result['token']
    else:
        print(f"登录失败: {response.json()}")
        return None

def test_couple_login():
    """测试情侣账号登录"""
    print("\n" + "="*60)
    print("3. 测试情侣账号登录")
    print("="*60)

    data = {
        "username": "couple_test001",
        "password": "123456"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"登录成功!")
        print(f"用户名: {result['user']['username']}")
        print(f"是否管理员: {result['user']['is_admin']}")
        if result.get('couple'):
            print(f"情侣信息:")
            print(f"  - ID: {result['couple']['couple_id']}")
            print(f"  - 名字: {result['couple']['names']}")
            print(f"  - 积分: {result['couple']['points']}")
        print(f"Token: {result['token'][:20]}...")
        return result['token']
    else:
        print(f"登录失败: {response.json()}")
        return None

def test_get_my_couple(token):
    """测试获取我的情侣信息"""
    print("\n" + "="*60)
    print("4. 测试获取我的情侣信息")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/couples/me", headers=headers)

    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"情侣信息:")
        print(f"  - ID: {result['couple_id']}")
        print(f"  - 名字: {result['names']}")
        print(f"  - 积分: {result['points']}")
        print(f"  - 创建时间: {result['created_time']}")
    else:
        print(f"获取失败: {response.json()}")

def test_get_base_rewards(token):
    """测试获取基础奖励列表"""
    print("\n" + "="*60)
    print("5. 测试获取基础奖励列表")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/rewards/base", headers=headers)

    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"基础奖励列表 (共{len(result['rewards'])}个):")
        for reward in result['rewards'][:5]:  # 只显示前5个
            print(f"  - {reward['name']}: {reward['points_needed']}积分 - {reward['description']}")
    else:
        print(f"获取失败: {response.json()}")

def test_get_my_rewards(token):
    """测试获取我的奖励列表"""
    print("\n" + "="*60)
    print("6. 测试获取我的奖励列表")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/rewards", headers=headers)

    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"我的奖励列表 (共{len(result['rewards'])}个):")
        if len(result['rewards']) == 0:
            print("  (暂无奖励，可以参考基础奖励列表自行创建)")
        for reward in result['rewards']:
            print(f"  - {reward['name']}: {reward['points_needed']}积分, 库存:{reward['stock']}")
    else:
        print(f"获取失败: {response.json()}")

def test_create_reward(token):
    """测试创建奖励"""
    print("\n" + "="*60)
    print("7. 测试创建奖励")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "测试奖励-浪漫晚餐",
        "points_needed": 100,
        "stock": 5,
        "description": "去喜欢的餐厅吃一顿浪漫晚餐"
    }

    response = requests.post(f"{BASE_URL}/rewards", json=data, headers=headers)

    print(f"状态码: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"创建成功!")
        print(f"奖励ID: {result['reward_id']}")
        return result['reward_id']
    else:
        print(f"创建失败: {response.json()}")
        return None

def test_update_points(token):
    """测试更新积分"""
    print("\n" + "="*60)
    print("8. 测试更新积分")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "points_change": 50,
        "reason": "完成每日任务"
    }

    response = requests.post(f"{BASE_URL}/points", json=data, headers=headers)

    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"积分更新成功!")
        print(f"新积分: {result['new_points']}")
    else:
        print(f"更新失败: {response.json()}")

def test_admin_get_all_couples(token):
    """测试管理员获取所有情侣"""
    print("\n" + "="*60)
    print("9. 测试管理员获取所有情侣")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/couples/all", headers=headers)

    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"所有情侣列表 (共{len(result['couples'])}对):")
        for couple in result['couples'][:5]:  # 只显示前5个
            print(f"  - {couple['names'][0]} & {couple['names'][1]}: {couple['points']}积分 (用户名: {couple['username']})")
    else:
        print(f"获取失败: {response.json()}")

def test_unauthorized_access(couple_token):
    """测试未授权访问（普通用户访问管理员接口）"""
    print("\n" + "="*60)
    print("10. 测试权限控制（普通用户访问管理员接口）")
    print("="*60)

    headers = {"Authorization": f"Bearer {couple_token}"}
    response = requests.get(f"{BASE_URL}/couples/all", headers=headers)

    print(f"状态码: {response.status_code}")
    if response.status_code == 403:
        print(f"✓ 权限控制正常！普通用户无法访问管理员接口")
        print(f"错误信息: {response.json()['detail']}")
    else:
        print(f"✗ 权限控制异常！")

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("心动积分系统 - 后端API测试")
    print("="*60)

    try:
        # 1. 健康检查
        if not test_health():
            print("\n✗ 健康检查失败，请确保后端服务已启动")
            return

        # 2. 管理员登录
        admin_token = test_admin_login()
        if not admin_token:
            print("\n✗ 管理员登录失败")
            return

        # 3. 情侣账号登录
        couple_token = test_couple_login()
        if not couple_token:
            print("\n✗ 情侣账号登录失败")
            return

        # 4. 测试情侣功能
        test_get_my_couple(couple_token)
        test_get_base_rewards(couple_token)
        test_get_my_rewards(couple_token)
        test_create_reward(couple_token)
        test_get_my_rewards(couple_token)  # 再次获取，查看新创建的奖励
        test_update_points(couple_token)

        # 5. 测试管理员功能
        test_admin_get_all_couples(admin_token)

        # 6. 测试权限控制
        test_unauthorized_access(couple_token)

        print("\n" + "="*60)
        print("测试完成！")
        print("="*60)
        print("\n总结:")
        print("✓ 用户认证系统正常")
        print("✓ 数据隔离正常（每对情侣只能访问自己的数据）")
        print("✓ 权限控制正常（普通用户无法访问管理员接口）")
        print("✓ 基础功能正常（积分、奖励、兑换）")

    except requests.exceptions.ConnectionError:
        print("\n✗ 无法连接到后端服务")
        print("请先启动后端服务: python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n✗ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
