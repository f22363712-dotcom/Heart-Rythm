"""
API使用示例
供小组成员参考的完整API用法，使用实际的后端API
"""

import requests

# API基础URL
API_BASE_URL = "http://localhost:8000"

def send_request(method, endpoint, data=None):
    """发送HTTP请求的通用函数"""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError("不支持的HTTP方法")
        
        return response
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器，请确保后端服务正在运行")
        return None


def demonstrate_features():
    print("1. 🧑‍🤝‍🧑 添加情侣")
    # 添加第一个情侣
    response = send_request("POST", "couples/", {
        "couple_id": "002",
        "name1": "张三",
        "name2": "李四"
    })
    if response and response.ok:
        print(f"   ✅ {response.json()['message']}")
    else:
        print(f"   ❌ 操作失败: {response.json()['detail'] if response else '连接失败'}")
    
    # 添加第二个情侣
    response = send_request("POST", "couples/", {
        "couple_id": "003",
        "name1": "王五",
        "name2": "赵六"
    })
    if response and response.ok:
        print(f"   ✅ {response.json()['message']}")
    else:
        print(f"   ❌ 操作失败: {response.json()['detail'] if response else '连接失败'}")

    print("\n2. 🎁 添加奖励")
    # 添加第一个奖励
    response = send_request("POST", "rewards/", {
        "reward_id": "reward2",
        "name": "电影票",
        "points_needed": 50,
        "stock": 10,
        "description": "双人电影票一张"
    })
    if response and response.ok:
        print(f"   ✅ {response.json()['message']}")
    else:
        print(f"   ❌ 操作失败: {response.json()['detail'] if response else '连接失败'}")
    
    # 添加第二个奖励
    response = send_request("POST", "rewards/", {
        "reward_id": "reward3",
        "name": "周末旅行",
        "points_needed": 200,
        "stock": 2,
        "description": "短途旅行一次"
    })
    if response and response.ok:
        print(f"   ✅ {response.json()['message']}")
    else:
        print(f"   ❌ 操作失败: {response.json()['detail'] if response else '连接失败'}")

    print("\n3. ⭐ 积分变动")
    # 张三李四完成挑战任务，获得30积分
    response = send_request("POST", "points/", {
        "couple_id": "002",
        "points_change": 30,
        "reason": "完成挑战任务"
    })
    if response and response.ok:
        print(f"   ✅ {response.json()['message']}，新积分: {response.json()['new_points']}")
    else:
        print(f"   ❌ 操作失败: {response.json()['detail'] if response else '连接失败'}")
    
    # 张三李四兑换小礼物，扣除20积分
    response = send_request("POST", "points/", {
        "couple_id": "002",
        "points_change": -20,
        "reason": "兑换小礼物"
    })
    if response and response.ok:
        print(f"   ✅ {response.json()['message']}，新积分: {response.json()['new_points']}")
    else:
        print(f"   ❌ 操作失败: {response.json()['detail'] if response else '连接失败'}")
    
    # 王五赵六完成每周任务，获得100积分
    response = send_request("POST", "points/", {
        "couple_id": "003",
        "points_change": 100,
        "reason": "完成每周任务"
    })
    if response and response.ok:
        print(f"   ✅ {response.json()['message']}，新积分: {response.json()['new_points']}")
    else:
        print(f"   ❌ 操作失败: {response.json()['detail'] if response else '连接失败'}")

    print("\n4. 🔍 查询数据")
    # 查询张三李四的信息
    response = send_request("GET", "couples/002/")
    if response and response.ok:
        data = response.json()
        print(f"   ✅ 情侣: {data['names']}, 积分: {data['points']}")
        print(f"   历史记录: {data['history']}")
    else:
        print(f"   ❌ 查询失败: {response.json()['detail'] if response else '连接失败'}")

    print("\n5. 📈 系统统计")
    # 获取系统统计信息
    response = send_request("GET", "stats/")
    if response and response.ok:
        stats = response.json()
        for key, value in stats.items():
            print(f"   {key}: {value}")
    else:
        print(f"   ❌ 查询失败: {response.json()['detail'] if response else '连接失败'}")

    print("\n6. 💾 备份管理")
    # 列出所有备份
    response = send_request("GET", "backups/")
    if response and response.ok:
        backups = response.json()['backups']
        print(f"   ✅ 现有备份数量: {len(backups)}")
    else:
        print(f"   ❌ 查询失败: {response.json()['detail'] if response else '连接失败'}")


if __name__ == "__main__":
    print("=" * 60)
    print("API功能演示 - 使用实际的后端API")
    print("=" * 60)
    print("💡 提示: 请确保后端服务正在 http://localhost:8000 运行")
    print("   您可以通过主程序菜单启动后端服务\n")

    demonstrate_features()

    print("\n✅ 所有功能演示完成！")
