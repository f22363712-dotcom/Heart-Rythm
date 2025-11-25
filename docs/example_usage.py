"""
数据处理模块使用示例
供小组成员参考的完整API用法
"""

from data_manager import DataManager


def demonstrate_features():
    dm = DataManager()
    dm.load_all_data()

    print("1. 🧑‍🤝‍🧑 添加情侣")
    dm.add_couple("002", "张三", "李四")
    dm.add_couple("003", "王五", "赵六")

    print("2. 🎁 添加奖励")
    dm.add_reward("reward2", "电影票", 50, 10, "双人电影票一张")
    dm.add_reward("reward3", "周末旅行", 200, 2, "短途旅行一次")

    print("3. ⭐ 积分变动")
    dm.add_points_history("002", 30, "完成挑战任务")
    dm.add_points_history("002", -20, "兑换小礼物")
    dm.add_points_history("003", 100, "完成每周任务")

    print("4. 🔍 查询数据")
    couple = dm.get_couple("002")
    if couple:
        print(f"   情侣: {couple.names}, 积分: {couple.points}")
        print(f"   历史记录: {couple.history}")

    print("5. 💾 备份功能")
    backups = dm.list_backups()
    print(f"   现有备份数量: {len(backups)}")

    print("6. 📈 系统统计")
    stats = dm.get_system_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")


def test_data_validation():
    """测试数据验证功能"""
    print("\n🧪 测试数据验证:")
    dm = DataManager()

    # 测试无效数据
    invalid_couple = {"couple_id": "test", "names": "不是列表", "points": -10}
    is_valid = dm.validate_couple_data(invalid_couple)
    print(f"   无效情侣数据验证结果: {is_valid} (应该为False)")

    valid_couple = {"couple_id": "test", "names": ["A", "B"], "points": 100}
    is_valid = dm.validate_couple_data(valid_couple)
    print(f"   有效情侣数据验证结果: {is_valid} (应该为True)")


if __name__ == "__main__":
    print("=" * 60)
    print("数据处理模块 - 完整功能演示")
    print("=" * 60)

    demonstrate_features()
    test_data_validation()

    print("\n✅ 所有功能演示完成！")