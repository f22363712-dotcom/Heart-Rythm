import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class DataManager:
    """数据处理管理器 - 负责数据结构、文件存储和数据验证"""

    def __init__(self, data_dir: str = "data"):
        """
        初始化数据管理器

        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.main_file = os.path.join(data_dir, "system_data.json")
        self.backup_dir = os.path.join(data_dir, "backups")

        # 创建必要的目录
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

        # 内存中的数据
        self.couples: Dict[str, 'Couple'] = {}
        self.rewards: List['Reward'] = []
        self.exchange_records: List['ExchangeRecord'] = []

    # ==================== 数据结构类 ====================

    class Couple:
        """情侣信息类"""

        def __init__(self, couple_id: str, name1: str, name2: str):
            self.couple_id = couple_id
            self.names = [name1, name2]
            self.points = 0
            self.history = []  # 积分变动记录
            self.created_time = datetime.now().isoformat()

        def to_dict(self) -> dict:
            """转换为字典，用于JSON序列化"""
            return {
                "couple_id": self.couple_id,
                "names": self.names,
                "points": self.points,
                "history": self.history,
                "created_time": self.created_time
            }

        @classmethod
        def from_dict(cls, data: dict) -> 'Couple':
            """从字典创建对象"""
            couple = cls(data["couple_id"], data["names"][0], data["names"][1])
            couple.points = data["points"]
            couple.history = data["history"]
            couple.created_time = data.get("created_time", datetime.now().isoformat())
            return couple

    class Reward:
        """奖励商品类"""

        def __init__(self, reward_id: str, name: str, points_needed: int, stock: int, description: str = ""):
            self.reward_id = reward_id
            self.name = name
            self.points_needed = points_needed
            self.stock = stock
            self.description = description
            self.created_time = datetime.now().isoformat()

        def to_dict(self) -> dict:
            """转换为字典，用于JSON序列化"""
            return {
                "reward_id": self.reward_id,
                "name": self.name,
                "points_needed": self.points_needed,
                "stock": self.stock,
                "description": self.description,
                "created_time": self.created_time
            }

        @classmethod
        def from_dict(cls, data: dict) -> 'Reward':
            """从字典创建对象"""
            reward = cls(
                data["reward_id"],
                data["name"],
                data["points_needed"],
                data["stock"],
                data.get("description", "")
            )
            reward.created_time = data.get("created_time", datetime.now().isoformat())
            return reward

    class ExchangeRecord:
        """兑换记录类"""

        def __init__(self, record_id: str, couple_id: str, reward_id: str, points_used: int):
            self.record_id = record_id
            self.couple_id = couple_id
            self.reward_id = reward_id
            self.points_used = points_used
            self.exchange_time = datetime.now().isoformat()

        def to_dict(self) -> dict:
            """转换为字典，用于JSON序列化"""
            return {
                "record_id": self.record_id,
                "couple_id": self.couple_id,
                "reward_id": self.reward_id,
                "points_used": self.points_used,
                "exchange_time": self.exchange_time
            }

        @classmethod
        def from_dict(cls, data: dict) -> 'ExchangeRecord':
            """从字典创建对象"""
            record = cls(
                data["record_id"],
                data["couple_id"],
                data["reward_id"],
                data["points_used"]
            )
            record.exchange_time = data.get("exchange_time", datetime.now().isoformat())
            return record

    # ==================== 数据验证方法 ====================

    def validate_couple_data(self, couple_data: dict) -> bool:
        """验证情侣数据"""
        required_fields = ["couple_id", "names", "points"]
        if not all(field in couple_data for field in required_fields):
            return False

        if not isinstance(couple_data["names"], list) or len(couple_data["names"]) != 2:
            return False

        if not isinstance(couple_data["points"], (int, float)) or couple_data["points"] < 0:
            return False

        return True

    def validate_reward_data(self, reward_data: dict) -> bool:
        """验证奖励数据"""
        required_fields = ["reward_id", "name", "points_needed", "stock"]
        if not all(field in reward_data for field in required_fields):
            return False

        if not isinstance(reward_data["points_needed"], int) or reward_data["points_needed"] < 0:
            return False

        if not isinstance(reward_data["stock"], int) or reward_data["stock"] < 0:
            return False

        return True

    def validate_exchange_record(self, record_data: dict) -> bool:
        """验证兑换记录数据"""
        required_fields = ["record_id", "couple_id", "reward_id", "points_used"]
        if not all(field in record_data for field in required_fields):
            return False

        if not isinstance(record_data["points_used"], int) or record_data["points_used"] < 0:
            return False

        return True

    # ==================== 文件存储方法 ====================

    def save_all_data(self) -> bool:
        """保存所有数据到文件"""
        try:
            data = {
                "couples": {cid: couple.to_dict() for cid, couple in self.couples.items()},
                "rewards": [reward.to_dict() for reward in self.rewards],
                "exchange_records": [record.to_dict() for record in self.exchange_records],
                "last_updated": datetime.now().isoformat()
            }

            # 自动备份当前数据
            self._create_backup()

            # 保存新数据
            with open(self.main_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"保存数据失败: {e}")
            return False

    def load_all_data(self) -> bool:
        """从文件加载所有数据"""
        try:
            if not os.path.exists(self.main_file):
                print("数据文件不存在，将创建新文件")
                return True

            with open(self.main_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 加载并验证情侣数据
            self.couples.clear()
            for cid, couple_data in data.get("couples", {}).items():
                if self.validate_couple_data(couple_data):
                    self.couples[cid] = self.Couple.from_dict(couple_data)
                else:
                    print(f"警告: 跳过无效的情侣数据: {cid}")

            # 加载并验证奖励数据
            self.rewards.clear()
            for reward_data in data.get("rewards", []):
                if self.validate_reward_data(reward_data):
                    self.rewards.append(self.Reward.from_dict(reward_data))
                else:
                    print(f"警告: 跳过无效的奖励数据: {reward_data.get('reward_id', 'unknown')}")

            # 加载并验证兑换记录
            self.exchange_records.clear()
            for record_data in data.get("exchange_records", []):
                if self.validate_exchange_record(record_data):
                    self.exchange_records.append(self.ExchangeRecord.from_dict(record_data))
                else:
                    print(f"警告: 跳过无效的兑换记录: {record_data.get('record_id', 'unknown')}")

            return True

        except Exception as e:
            print(f"加载数据失败: {e}")
            return False

    # ==================== 备份恢复方法 ====================

    def _create_backup(self) -> bool:
        """创建数据备份"""
        try:
            if os.path.exists(self.main_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")

                with open(self.main_file, 'r', encoding='utf-8') as source:
                    with open(backup_file, 'w', encoding='utf-8') as target:
                        target.write(source.read())

                # 清理过旧的备份（保留最近10个）
                self._cleanup_old_backups()
                return True

        except Exception as e:
            print(f"创建备份失败: {e}")

        return False

    def _cleanup_old_backups(self):
        """清理过旧的备份文件"""
        try:
            backup_files = []
            for file in os.listdir(self.backup_dir):
                if file.startswith("backup_") and file.endswith(".json"):
                    file_path = os.path.join(self.backup_dir, file)
                    backup_files.append((file_path, os.path.getctime(file_path)))

            # 按创建时间排序，删除最旧的
            backup_files.sort(key=lambda x: x[1])
            while len(backup_files) > 10:  # 保留最近10个备份
                old_file, _ = backup_files.pop(0)
                os.remove(old_file)

        except Exception as e:
            print(f"清理备份文件失败: {e}")

    def list_backups(self) -> List[str]:
        """列出所有可用的备份文件"""
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.startswith("backup_") and file.endswith(".json"):
                file_path = os.path.join(self.backup_dir, file)
                backups.append(file_path)
        return sorted(backups)

    def restore_from_backup(self, backup_file: str) -> bool:
        """从备份文件恢复数据"""
        try:
            if not os.path.exists(backup_file):
                print("备份文件不存在")
                return False

            # 创建当前状态的备份
            self._create_backup()

            # 恢复备份文件
            import shutil
            shutil.copy2(backup_file, self.main_file)

            # 重新加载数据
            return self.load_all_data()

        except Exception as e:
            print(f"恢复备份失败: {e}")
            return False

    # ==================== 数据操作方法 ====================

    def add_couple(self, couple_id: str, name1: str, name2: str) -> bool:
        """添加情侣"""
        if couple_id in self.couples:
            print(f"情侣ID已存在: {couple_id}")
            return False

        self.couples[couple_id] = self.Couple(couple_id, name1, name2)
        return self.save_all_data()

    def get_couple(self, couple_id: str) -> Optional[Couple]:
        """获取情侣信息"""
        return self.couples.get(couple_id)

    def add_reward(self, reward_id: str, name: str, points_needed: int, stock: int, description: str = "") -> bool:
        """添加奖励"""
        if any(reward.reward_id == reward_id for reward in self.rewards):
            print(f"奖励ID已存在: {reward_id}")
            return False

        self.rewards.append(self.Reward(reward_id, name, points_needed, stock, description))
        return self.save_all_data()

    def add_points_history(self, couple_id: str, points_change: int, reason: str) -> bool:
        """添加积分变动记录"""
        couple = self.get_couple(couple_id)
        if not couple:
            print(f"情侣不存在: {couple_id}")
            return False

        couple.points += points_change
        couple.history.append({
            "timestamp": datetime.now().isoformat(),
            "points_change": points_change,
            "reason": reason,
            "new_balance": couple.points
        })

        return self.save_all_data()

    def add_exchange_record(self, couple_id: str, reward_id: str, points_used: int) -> bool:
        """添加兑换记录"""
        record_id = f"EX{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.exchange_records.append(self.ExchangeRecord(record_id, couple_id, reward_id, points_used))
        return self.save_all_data()

    # ==================== 数据统计方法 ====================

    def get_system_stats(self) -> dict:
        """获取系统统计信息"""
        total_couples = len(self.couples)
        total_rewards = len(self.rewards)
        total_exchanges = len(self.exchange_records)
        total_points = sum(couple.points for couple in self.couples.values())

        return {
            "total_couples": total_couples,
            "total_rewards": total_rewards,
            "total_exchanges": total_exchanges,
            "total_points": total_points,
            "last_updated": datetime.now().isoformat()
        }


# ==================== 使用示例 ====================
def demo_usage():
    """演示如何使用数据管理器"""

    # 创建数据管理器实例
    dm = DataManager()

    # 加载现有数据
    if dm.load_all_data():
        print("数据加载成功！")
    else:
        print("数据加载失败或文件不存在")

    # 添加示例数据
    dm.add_couple("couple001", "小明", "小红")
    dm.add_reward("reward001", "浪漫晚餐", 100, 5, "双人浪漫晚餐一次")
    dm.add_points_history("couple001", 50, "完成每日任务")

    # 获取统计信息
    stats = dm.get_system_stats()
    print("系统统计:", stats)

    # 列出备份
    backups = dm.list_backups()
    print(f"可用备份: {len(backups)} 个")


if __name__ == "__main__":
    demo_usage()