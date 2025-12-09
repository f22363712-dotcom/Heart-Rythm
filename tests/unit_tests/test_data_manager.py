import unittest
import os
import tempfile
from backend.data_manager import DataManager


class TestDataManager(unittest.TestCase):
    """测试数据管理模块的单元测试"""
    
    def setUp(self):
        """在每个测试前设置临时数据目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.dm = DataManager(data_dir=self.temp_dir)
        self.dm.load_all_data()
    
    def tearDown(self):
        """在每个测试后清理临时文件"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_add_couple(self):
        """测试添加情侣功能"""
        result = self.dm.add_couple("test001", "张三", "李四")
        self.assertTrue(result)
        self.assertIn("test001", self.dm.couples)
    
    def test_add_duplicate_couple(self):
        """测试添加重复情侣ID"""
        self.dm.add_couple("test001", "张三", "李四")
        result = self.dm.add_couple("test001", "王五", "赵六")
        self.assertFalse(result)
    
    def test_get_couple(self):
        """测试获取情侣信息"""
        self.dm.add_couple("test001", "张三", "李四")
        couple = self.dm.get_couple("test001")
        self.assertIsNotNone(couple)
        self.assertEqual(couple.names, ["张三", "李四"])
    
    def test_get_nonexistent_couple(self):
        """测试获取不存在的情侣"""
        couple = self.dm.get_couple("nonexistent")
        self.assertIsNone(couple)
    
    def test_add_reward(self):
        """测试添加奖励功能"""
        result = self.dm.add_reward("reward001", "电影票", 50, 10, "双人电影票")
        self.assertTrue(result)
        self.assertEqual(len(self.dm.rewards), 1)
        self.assertEqual(self.dm.rewards[0].name, "电影票")
    
    def test_add_points_history(self):
        """测试积分变动功能"""
        self.dm.add_couple("test001", "张三", "李四")
        result = self.dm.add_points_history("test001", 100, "完成任务")
        self.assertTrue(result)
        couple = self.dm.get_couple("test001")
        self.assertEqual(couple.points, 100)
        self.assertEqual(len(couple.history), 1)
    
    def test_add_exchange_record(self):
        """测试添加兑换记录"""
        self.dm.add_couple("test001", "张三", "李四")
        self.dm.add_reward("reward001", "电影票", 50, 10)
        result = self.dm.add_exchange_record("test001", "reward001", 50)
        self.assertTrue(result)
        self.assertEqual(len(self.dm.exchange_records), 1)
    
    def test_validate_couple_data(self):
        """测试情侣数据验证"""
        # 有效的情侣数据
        valid_data = {
            "couple_id": "test001",
            "names": ["张三", "李四"],
            "points": 100
        }
        self.assertTrue(self.dm.validate_couple_data(valid_data))
        
        # 无效的情侣数据（缺少字段）
        invalid_data1 = {
            "couple_id": "test001",
            "names": ["张三", "李四"]
            # 缺少points字段
        }
        self.assertFalse(self.dm.validate_couple_data(invalid_data1))
        
        # 无效的情侣数据（积分为负数）
        invalid_data2 = {
            "couple_id": "test001",
            "names": ["张三", "李四"],
            "points": -100
        }
        self.assertFalse(self.dm.validate_couple_data(invalid_data2))
    
    def test_validate_reward_data(self):
        """测试奖励数据验证"""
        # 有效的奖励数据
        valid_data = {
            "reward_id": "reward001",
            "name": "电影票",
            "points_needed": 50,
            "stock": 10
        }
        self.assertTrue(self.dm.validate_reward_data(valid_data))
        
        # 无效的奖励数据（积分不足）
        invalid_data = {
            "reward_id": "reward001",
            "name": "电影票",
            "points_needed": -50,
            "stock": 10
        }
        self.assertFalse(self.dm.validate_reward_data(invalid_data))
    
    def test_get_system_stats(self):
        """测试系统统计功能"""
        self.dm.add_couple("test001", "张三", "李四")
        self.dm.add_couple("test002", "王五", "赵六")
        self.dm.add_reward("reward001", "电影票", 50, 10)
        self.dm.add_points_history("test001", 100, "完成任务")
        self.dm.add_points_history("test002", 200, "完成任务")
        
        stats = self.dm.get_system_stats()
        self.assertEqual(stats["total_couples"], 2)
        self.assertEqual(stats["total_rewards"], 1)
        self.assertEqual(stats["total_points"], 300)


if __name__ == "__main__":
    unittest.main()
