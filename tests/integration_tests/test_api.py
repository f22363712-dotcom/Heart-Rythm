import unittest
import tempfile
import os
from fastapi.testclient import TestClient
from backend.api.main import app


class TestAPI(unittest.TestCase):
    """API集成测试"""
    
    def setUp(self):
        """设置测试客户端"""
        self.client = TestClient(app)
        
    def test_create_couple(self):
        """测试创建情侣API"""
        response = self.client.post(
            "/couples/",
            json={
                "couple_id": "test001",
                "name1": "张三",
                "name2": "李四"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("情侣创建成功", response.json()["message"])
    
    def test_get_couple(self):
        """测试获取情侣信息API"""
        # 先创建情侣
        self.client.post(
            "/couples/",
            json={
                "couple_id": "test001",
                "name1": "张三",
                "name2": "李四"
            }
        )
        
        # 然后获取情侣信息
        response = self.client.get("/couples/test001/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["names"], ["张三", "李四"])
    
    def test_get_nonexistent_couple(self):
        """测试获取不存在的情侣API"""
        response = self.client.get("/couples/nonexistent/")
        self.assertEqual(response.status_code, 404)
    
    def test_create_reward(self):
        """测试创建奖励API"""
        response = self.client.post(
            "/rewards/",
            json={
                "reward_id": "reward001",
                "name": "电影票",
                "points_needed": 50,
                "stock": 10,
                "description": "双人电影票"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("奖励创建成功", response.json()["message"])
    
    def test_update_points(self):
        """测试积分变动API"""
        # 先创建情侣
        self.client.post(
            "/couples/",
            json={
                "couple_id": "test001",
                "name1": "张三",
                "name2": "李四"
            }
        )
        
        # 然后进行积分变动
        response = self.client.post(
            "/points/",
            json={
                "couple_id": "test001",
                "points_change": 100,
                "reason": "完成任务"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("积分更新成功", response.json()["message"])
        self.assertEqual(response.json()["new_points"], 100)
    
    def test_create_exchange_record(self):
        """测试创建兑换记录API"""
        # 先创建情侣和奖励
        self.client.post(
            "/couples/",
            json={
                "couple_id": "test001",
                "name1": "张三",
                "name2": "李四"
            }
        )
        
        self.client.post(
            "/rewards/",
            json={
                "reward_id": "reward001",
                "name": "电影票",
                "points_needed": 50,
                "stock": 10
            }
        )
        
        # 然后创建兑换记录
        response = self.client.post(
            "/exchanges/",
            json={
                "couple_id": "test001",
                "reward_id": "reward001",
                "points_used": 50
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("兑换记录创建成功", response.json()["message"])
    
    def test_get_stats(self):
        """测试获取系统统计API"""
        response = self.client.get("/stats/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_couples", response.json())
        self.assertIn("total_rewards", response.json())
        self.assertIn("total_points", response.json())
        self.assertIn("total_exchanges", response.json())
    
    def test_list_backups(self):
        """测试列出备份API"""
        response = self.client.get("/backups/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("backups", response.json())
    
    def test_invalid_couple_data(self):
        """测试无效的情侣数据"""
        # 缺少必填字段
        response = self.client.post(
            "/couples/",
            json={
                "couple_id": "test001",
                "name1": "张三"
                # 缺少name2字段
            }
        )
        self.assertEqual(response.status_code, 422)  # 验证错误
    
    def test_invalid_reward_data(self):
        """测试无效的奖励数据"""
        # 积分不足
        response = self.client.post(
            "/rewards/",
            json={
                "reward_id": "reward001",
                "name": "电影票",
                "points_needed": -10,  # 无效的积分值
                "stock": 10
            }
        )
        self.assertEqual(response.status_code, 422)  # 验证错误


if __name__ == "__main__":
    unittest.main()
