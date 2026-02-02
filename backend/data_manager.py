"""
心动积分项目 - 数据管理模块
负责数据结构定义、文件存储和数据验证
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any


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
        self.couples: Dict[str, 'DataManager.Couple'] = {}
        self.rewards: List['DataManager.Reward'] = []
        self.exchange_records: List['DataManager.ExchangeRecord'] = []

    # ==================== 数据结构类 ====================

    class Couple:
        """情侣信息类"""

        def __init__(self, couple_id: str, name1: str, name2: str):
            self.couple_id = couple_id
            self.names = [name1, name2]
            self.points = 0
            self.history: List[Dict[str, Any]] = []
            self.created_time = datetime.now().isoformat()

        def to_dict(self) -> dict:
            return {
                "couple_id": self.couple_id,
                "names": self.names,
                "points": self.points,
                "history": self.history,
                "created_time": self.created_time
            }

        @classmethod
        def from_dict(cls, data: dict) -> 'DataManager.Couple':
            couple = cls(data["couple_id"], data["names"][0], data["names"][1])
            couple.points = data.get("points", 0)
            couple.history = data.get("history", [])
            couple.created_time = data.get("created_time", datetime.now().isoformat())
            return couple

    class Reward:
        """奖励商品类"""

        def __init__(self, reward_id: str, name: str, points_needed: int, 
                     stock: int, description: str = ""):
            self.reward_id = reward_id
            self.name = name
            self.points_needed = points_needed
            self.stock = stock
            self.description = description
            self.created_time = datetime.now().isoformat()

        def to_dict(self) -> dict:
            return {
                "reward_id": self.reward_id,
                "name": self.name,
                "points_needed": self.points_needed,
                "stock": self.stock,
                "description": self.description,
                "created_time": self.created_time
            }

        @classmethod
        def from_dict(cls, data: dict) -> 'DataManager.Reward':
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
            return {
                "record_id": self.record_id,
                "couple_id": self.couple_id,
                "reward_id": self.reward_id,
                "points_used": self.points_used,
                "exchange_time": self.exchange_time
            }

        @classmethod
        def from_dict(cls, data: dict) -> 'DataManager.ExchangeRecord':
            record = cls(
                data["record_id"],
                data["couple_id"],
                data["reward_id"],
                data["points_used"]
            )
            record.exchange_time = data.get("exchange_time", datetime.now().isoformat())
            return record

    # ==================== 数据验证方法 ====================

    def validate_couple_data(self, data: dict) -> bool:
        """验证情侣数据格式"""
        required_fields = ["couple_id", "names", "points"]
        for field in required_fields:
            if field not in data:
                return False
        if not isinstance(data.get("names"), list) or len(data.get("names", [])) != 2:
            return False
        if not isinstance(data.get("points"), (int, float)) or data.get("points", 0) < 0:
            return False
        return True

    def validate_reward_data(self, data: dict) -> bool:
        """验证奖励数据格式"""
        required_fields = ["reward_id", "name", "points_needed", "stock"]
        for field in required_fields:
            if field not in data:
                return False
        if not isinstance(data.get("points_needed"), int) or data.get("points_needed", 0) <= 0:
            return False
        if not isinstance(data.get("stock"), int) or data.get("stock", 0) < 0:
            return False
        return True

    # ==================== 数据操作方法 ====================

    def add_couple(self, couple_id: str, name1: str, name2: str) -> bool:
        """添加情侣"""
        if couple_id in self.couples:
            return False
        self.couples[couple_id] = self.Couple(couple_id, name1, name2)
        self.save_all_data()
        return True

    def get_couple(self, couple_id: str) -> Optional['DataManager.Couple']:
        """获取情侣信息"""
        return self.couples.get(couple_id)

    def get_all_couples(self) -> List['DataManager.Couple']:
        """获取所有情侣"""
        return list(self.couples.values())

    def add_reward(self, reward_id: str, name: str, points_needed: int, 
                   stock: int, description: str = "") -> bool:
        """添加奖励"""
        for reward in self.rewards:
            if reward.reward_id == reward_id:
                return False
        self.rewards.append(self.Reward(reward_id, name, points_needed, stock, description))
        self.save_all_data()
        return True

    def get_all_rewards(self) -> List['DataManager.Reward']:
        """获取所有奖励"""
        return self.rewards

    def add_points_history(self, couple_id: str, points_change: int, reason: str) -> bool:
        """添加积分变动记录"""
        couple = self.get_couple(couple_id)
        if not couple:
            return False
        
        couple.points += points_change
        couple.history.append({
            "timestamp": datetime.now().isoformat(),
            "points_change": points_change,
            "reason": reason,
            "new_balance": couple.points
        })
        self.save_all_data()
        return True

    def add_exchange_record(self, couple_id: str, reward_id: str, points_used: int) -> bool:
        """添加兑换记录"""
        record_id = f"EX{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.exchange_records.append(
            self.ExchangeRecord(record_id, couple_id, reward_id, points_used)
        )
        self.save_all_data()
        return True

    def get_all_exchange_records(self) -> List['DataManager.ExchangeRecord']:
        """获取所有兑换记录"""
        return self.exchange_records

    # ==================== 统计方法 ====================

    def get_stats(self) -> dict:
        """获取系统统计信息"""
        total_points = sum(c.points for c in self.couples.values())
        return {
            "total_couples": len(self.couples),
            "total_rewards": len(self.rewards),
            "total_exchanges": len(self.exchange_records),
            "total_points": total_points,
            "last_updated": datetime.now().isoformat()
        }

    # ==================== 数据持久化方法 ====================

    def save_all_data(self) -> bool:
        """保存所有数据到文件"""
        try:
            data = {
                "couples": {k: v.to_dict() for k, v in self.couples.items()},
                "rewards": [r.to_dict() for r in self.rewards],
                "exchange_records": [e.to_dict() for e in self.exchange_records],
                "last_updated": datetime.now().isoformat()
            }
            with open(self.main_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False

    def load_all_data(self) -> bool:
        """从文件加载所有数据"""
        if not os.path.exists(self.main_file):
            return True
        
        try:
            with open(self.main_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.couples = {}
            for k, v in data.get("couples", {}).items():
                self.couples[k] = self.Couple.from_dict(v)
            
            self.rewards = [self.Reward.from_dict(r) for r in data.get("rewards", [])]
            self.exchange_records = [
                self.ExchangeRecord.from_dict(e) for e in data.get("exchange_records", [])
            ]
            
            return True
        except Exception as e:
            print(f"加载数据失败: {e}")
            return False

    def create_backup(self) -> str:
        """创建数据备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
        
        try:
            data = {
                "couples": {k: v.to_dict() for k, v in self.couples.items()},
                "rewards": [r.to_dict() for r in self.rewards],
                "exchange_records": [e.to_dict() for e in self.exchange_records],
                "backup_time": datetime.now().isoformat()
            }
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self._cleanup_old_backups()
            return backup_file
        except Exception as e:
            print(f"创建备份失败: {e}")
            return ""

    def _cleanup_old_backups(self, max_backups: int = 10):
        """清理旧备份文件"""
        try:
            backups = sorted([
                f for f in os.listdir(self.backup_dir) 
                if f.startswith("backup_") and f.endswith(".json")
            ])
            while len(backups) > max_backups:
                oldest = backups.pop(0)
                os.remove(os.path.join(self.backup_dir, oldest))
        except Exception:
            pass

    def list_backups(self) -> List[str]:
        """列出所有备份文件"""
        try:
            backups = [
                os.path.join(self.backup_dir, f)
                for f in os.listdir(self.backup_dir)
                if f.startswith("backup_") and f.endswith(".json")
            ]
            return sorted(backups, reverse=True)
        except Exception:
            return []
