"""
数据迁移脚本
将现有的 JSON 数据迁移到 SQLite 数据库
"""
import json
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import Database


def migrate_data():
    """执行数据迁移"""
    print("=" * 60)
    print("开始数据迁移：JSON -> SQLite")
    print("=" * 60)

    # 读取 JSON 数据
    json_file = Path(__file__).parent.parent / "data" / "system_data.json"

    if not json_file.exists():
        print(f"警告: 未找到 JSON 数据文件: {json_file}")
        print("将创建空数据库")
        db = Database()
        print("\n✓ 数据库初始化完成")
        print(f"✓ 默认管理员账号: admin / admin123")
        return

    print(f"\n1. 读取 JSON 数据文件: {json_file}")
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    couples_data = data.get("couples", {})
    rewards_data = data.get("rewards", [])
    exchange_records_data = data.get("exchange_records", [])

    print(f"   - 情侣数据: {len(couples_data)} 条")
    print(f"   - 奖励数据: {len(rewards_data)} 条")
    print(f"   - 兑换记录: {len(exchange_records_data)} 条")

    # 初始化数据库
    print("\n2. 初始化数据库")
    db = Database()
    print("   ✓ 数据库表结构创建完成")
    print("   ✓ 默认管理员账号已创建: admin / admin123")
    print("   ✓ 基础奖励列表已创建")

    # 迁移情侣数据
    print("\n3. 迁移情侣数据")
    couple_id_to_user_id = {}  # 映射关系

    for couple_id, couple_info in couples_data.items():
        # 为每对情侣创建一个用户账号
        # 用户名格式: couple_{couple_id}
        # 默认密码: 123456
        username = f"couple_{couple_id}"
        password = "123456"

        user_id = db.create_user(username, password, is_admin=False)

        if user_id:
            # 创建情侣记录
            name1 = couple_info["names"][0]
            name2 = couple_info["names"][1]
            points = couple_info.get("points", 0)
            created_time = couple_info.get("created_time", "")

            # 直接插入数据库，保留原有的 couple_id
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO couples (couple_id, user_id, name1, name2, points, created_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (couple_id, user_id, name1, name2, points, created_time))
            conn.commit()
            conn.close()

            couple_id_to_user_id[couple_id] = user_id

            # 迁移积分历史
            history = couple_info.get("history", [])
            for record in history:
                points_change = record.get("points_change", 0)
                reason = record.get("reason", "")
                timestamp = record.get("timestamp", "")

                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO point_history (couple_id, points_change, reason, created_time)
                    VALUES (?, ?, ?, ?)
                """, (couple_id, points_change, reason, timestamp))
                conn.commit()
                conn.close()

            print(f"   ✓ {couple_id} ({name1} & {name2}) - 用户名: {username}, 密码: 123456")

    print(f"\n   共迁移 {len(couple_id_to_user_id)} 对情侣")

    # 迁移奖励数据
    print("\n4. 迁移奖励数据")
    print("   注意: 原有的全局奖励将被转换为各个情侣的专属奖励")

    # 由于原系统是全局奖励，现在需要为每对情侣创建专属奖励
    # 这里我们采取的策略是：不迁移旧的全局奖励，让用户自己设置
    # 如果需要迁移，可以为每对情侣复制一份奖励

    print("   跳过全局奖励迁移（用户可以参考基础奖励列表自行设置）")

    # 迁移兑换记录
    print("\n5. 迁移兑换记录")
    migrated_exchanges = 0

    for record in exchange_records_data:
        record_id = record.get("record_id", "")
        couple_id = record.get("couple_id", "")
        reward_id = record.get("reward_id", "")
        points_used = record.get("points_used", 0)
        exchange_time = record.get("exchange_time", "")

        # 检查 couple_id 是否存在
        if couple_id in couple_id_to_user_id:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO exchange_records (record_id, couple_id, reward_id, points_used, exchange_time)
                VALUES (?, ?, ?, ?, ?)
            """, (record_id, couple_id, reward_id, points_used, exchange_time))
            conn.commit()
            conn.close()
            migrated_exchanges += 1

    print(f"   ✓ 共迁移 {migrated_exchanges} 条兑换记录")

    # 备份原 JSON 文件
    print("\n6. 备份原 JSON 文件")
    backup_file = json_file.parent / "system_data.json.backup"
    import shutil
    shutil.copy(json_file, backup_file)
    print(f"   ✓ 已备份到: {backup_file}")

    print("\n" + "=" * 60)
    print("数据迁移完成！")
    print("=" * 60)
    print("\n重要信息:")
    print("1. 管理员账号: admin / admin123")
    print("2. 所有情侣账号:")
    print("   - 用户名格式: couple_{原couple_id}")
    print("   - 默认密码: 123456")
    print("   - 例如: couple_001 / 123456")
    print("\n3. 用户首次登录后，建议修改密码")
    print("4. 用户需要自行设置专属奖励（可参考基础奖励列表）")
    print("5. 原 JSON 文件已备份")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        migrate_data()
    except Exception as e:
        print(f"\n错误: 数据迁移失败")
        print(f"详细信息: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
