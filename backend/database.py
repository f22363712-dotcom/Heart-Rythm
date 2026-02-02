"""
数据库模型和初始化
使用 SQLite 数据库存储用户、情侣、积分、奖励等数据
"""
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import hashlib
import secrets
from pathlib import Path


class Database:
    """数据库管理类"""

    def __init__(self, db_path: str = "data/heartbeat.db"):
        """初始化数据库连接"""
        self.db_path = db_path
        # 确保数据目录存在
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        return conn

    def init_database(self):
        """初始化数据库表结构"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                created_time TEXT NOT NULL
            )
        """)

        # 创建情侣表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS couples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                couple_id TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                name1 TEXT NOT NULL,
                name2 TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                created_time TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 创建积分历史表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS point_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                couple_id TEXT NOT NULL,
                points_change INTEGER NOT NULL,
                reason TEXT,
                created_time TEXT NOT NULL,
                FOREIGN KEY (couple_id) REFERENCES couples(couple_id) ON DELETE CASCADE
            )
        """)

        # 创建基础奖励表（供参考）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS base_rewards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                points_needed INTEGER NOT NULL,
                description TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)

        # 创建情侣奖励表（每对情侣自己设置）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS couple_rewards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reward_id TEXT UNIQUE NOT NULL,
                couple_id TEXT NOT NULL,
                name TEXT NOT NULL,
                points_needed INTEGER NOT NULL,
                stock INTEGER DEFAULT 1,
                description TEXT,
                created_time TEXT NOT NULL,
                FOREIGN KEY (couple_id) REFERENCES couples(couple_id) ON DELETE CASCADE
            )
        """)

        # 创建兑换记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT UNIQUE NOT NULL,
                couple_id TEXT NOT NULL,
                reward_id TEXT NOT NULL,
                points_used INTEGER NOT NULL,
                exchange_time TEXT NOT NULL,
                FOREIGN KEY (couple_id) REFERENCES couples(couple_id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        conn.close()

        # 初始化默认管理员账号和基础奖励
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据（管理员账号和基础奖励列表）"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 检查是否已有管理员账号
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:
            # 创建默认管理员账号: admin / admin123
            admin_password = self.hash_password("admin123")
            cursor.execute("""
                INSERT INTO users (username, password_hash, is_admin, created_time)
                VALUES (?, ?, 1, ?)
            """, ("admin", admin_password, datetime.now().isoformat()))
            print("已创建默认管理员账号: admin / admin123")

        # 检查是否已有基础奖励
        cursor.execute("SELECT COUNT(*) FROM base_rewards")
        reward_count = cursor.fetchone()[0]

        if reward_count == 0:
            # 添加一些基础奖励供参考
            base_rewards = [
                ("一起看电影", 50, "去电影院看一场电影"),
                ("浪漫晚餐", 100, "去喜欢的餐厅吃一顿浪漫晚餐"),
                ("周末旅行", 200, "周末一起去附近城市旅行"),
                ("送一束花", 30, "送对方一束鲜花"),
                ("做一顿大餐", 40, "亲手为对方做一顿丰盛的晚餐"),
                ("按摩服务", 60, "为对方提供30分钟按摩服务"),
                ("游乐园一日游", 150, "一起去游乐园玩一天"),
                ("买心仪的礼物", 120, "买一件对方心仪已久的礼物"),
                ("温泉之旅", 250, "一起去泡温泉放松"),
                ("演唱会门票", 300, "去看喜欢的歌手的演唱会"),
            ]

            for name, points, desc in base_rewards:
                cursor.execute("""
                    INSERT INTO base_rewards (name, points_needed, description)
                    VALUES (?, ?, ?)
                """, (name, points, desc))

            print(f"已添加 {len(base_rewards)} 个基础奖励供参考")

        conn.commit()
        conn.close()

    @staticmethod
    def hash_password(password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_id(prefix: str = "") -> str:
        """生成唯一ID"""
        return f"{prefix}{secrets.token_hex(8)}"

    # ==================== 用户相关方法 ====================

    def create_user(self, username: str, password: str, is_admin: bool = False) -> Optional[int]:
        """创建用户"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, password_hash, is_admin, created_time)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, 1 if is_admin else 0, datetime.now().isoformat()))

            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None  # 用户名已存在

    def verify_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """验证用户登录"""
        conn = self.get_connection()
        cursor = conn.cursor()

        password_hash = self.hash_password(password)
        cursor.execute("""
            SELECT id, username, is_admin FROM users
            WHERE username = ? AND password_hash = ?
        """, (username, password_hash))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row["id"],
                "username": row["username"],
                "is_admin": bool(row["is_admin"])
            }
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取用户信息"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, is_admin, created_time FROM users
            WHERE id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row["id"],
                "username": row["username"],
                "is_admin": bool(row["is_admin"]),
                "created_time": row["created_time"]
            }
        return None

    def get_all_users(self) -> List[Dict[str, Any]]:
        """获取所有用户（管理员功能）"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, is_admin, created_time FROM users
            ORDER BY created_time DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    # ==================== 情侣相关方法 ====================

    def create_couple(self, user_id: int, name1: str, name2: str) -> Optional[str]:
        """创建情侣对"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            couple_id = self.generate_id("couple_")
            cursor.execute("""
                INSERT INTO couples (couple_id, user_id, name1, name2, points, created_time)
                VALUES (?, ?, ?, ?, 0, ?)
            """, (couple_id, user_id, name1, name2, datetime.now().isoformat()))

            conn.commit()
            conn.close()
            return couple_id
        except Exception as e:
            print(f"创建情侣对失败: {e}")
            return None

    def get_couple_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据用户ID获取情侣信息"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM couples WHERE user_id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_couple_by_id(self, couple_id: str) -> Optional[Dict[str, Any]]:
        """根据couple_id获取情侣信息"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM couples WHERE couple_id = ?
        """, (couple_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_all_couples(self) -> List[Dict[str, Any]]:
        """获取所有情侣（管理员功能）"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.*, u.username
            FROM couples c
            LEFT JOIN users u ON c.user_id = u.id
            ORDER BY c.created_time DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def update_couple_points(self, couple_id: str, points_change: int, reason: str = "") -> bool:
        """更新情侣积分"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 更新积分
            cursor.execute("""
                UPDATE couples SET points = points + ?
                WHERE couple_id = ?
            """, (points_change, couple_id))

            # 记录历史
            cursor.execute("""
                INSERT INTO point_history (couple_id, points_change, reason, created_time)
                VALUES (?, ?, ?, ?)
            """, (couple_id, points_change, reason, datetime.now().isoformat()))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新积分失败: {e}")
            return False

    def get_point_history(self, couple_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """获取积分历史"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM point_history
            WHERE couple_id = ?
            ORDER BY created_time DESC
            LIMIT ?
        """, (couple_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    # ==================== 奖励相关方法 ====================

    def get_base_rewards(self) -> List[Dict[str, Any]]:
        """获取基础奖励列表"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM base_rewards
            WHERE is_active = 1
            ORDER BY points_needed ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def create_couple_reward(self, couple_id: str, name: str, points_needed: int,
                            stock: int = 1, description: str = "") -> Optional[str]:
        """创建情侣专属奖励"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            reward_id = self.generate_id("reward_")
            cursor.execute("""
                INSERT INTO couple_rewards (reward_id, couple_id, name, points_needed, stock, description, created_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (reward_id, couple_id, name, points_needed, stock, description, datetime.now().isoformat()))

            conn.commit()
            conn.close()
            return reward_id
        except Exception as e:
            print(f"创建奖励失败: {e}")
            return None

    def get_couple_rewards(self, couple_id: str) -> List[Dict[str, Any]]:
        """获取情侣的奖励列表"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM couple_rewards
            WHERE couple_id = ?
            ORDER BY points_needed ASC
        """, (couple_id,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def update_couple_reward(self, reward_id: str, name: str = None, points_needed: int = None,
                            stock: int = None, description: str = None) -> bool:
        """更新情侣奖励"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            updates = []
            params = []

            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if points_needed is not None:
                updates.append("points_needed = ?")
                params.append(points_needed)
            if stock is not None:
                updates.append("stock = ?")
                params.append(stock)
            if description is not None:
                updates.append("description = ?")
                params.append(description)

            if not updates:
                return False

            params.append(reward_id)
            query = f"UPDATE couple_rewards SET {', '.join(updates)} WHERE reward_id = ?"

            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新奖励失败: {e}")
            return False

    def delete_couple_reward(self, reward_id: str) -> bool:
        """删除情侣奖励"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM couple_rewards WHERE reward_id = ?", (reward_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除奖励失败: {e}")
            return False

    # ==================== 兑换相关方法 ====================

    def create_exchange_record(self, couple_id: str, reward_id: str, points_used: int) -> Optional[str]:
        """创建兑换记录"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 检查积分是否足够
            cursor.execute("SELECT points FROM couples WHERE couple_id = ?", (couple_id,))
            row = cursor.fetchone()
            if not row or row["points"] < points_used:
                return None

            # 检查库存
            cursor.execute("SELECT stock FROM couple_rewards WHERE reward_id = ?", (reward_id,))
            reward_row = cursor.fetchone()
            if not reward_row or reward_row["stock"] <= 0:
                return None

            # 创建兑换记录
            record_id = self.generate_id("exchange_")
            cursor.execute("""
                INSERT INTO exchange_records (record_id, couple_id, reward_id, points_used, exchange_time)
                VALUES (?, ?, ?, ?, ?)
            """, (record_id, couple_id, reward_id, points_used, datetime.now().isoformat()))

            # 扣除积分
            cursor.execute("""
                UPDATE couples SET points = points - ?
                WHERE couple_id = ?
            """, (points_used, couple_id))

            # 减少库存
            cursor.execute("""
                UPDATE couple_rewards SET stock = stock - 1
                WHERE reward_id = ?
            """, (reward_id,))

            # 记录积分历史
            cursor.execute("""
                INSERT INTO point_history (couple_id, points_change, reason, created_time)
                VALUES (?, ?, ?, ?)
            """, (couple_id, -points_used, f"兑换奖励: {reward_id}", datetime.now().isoformat()))

            conn.commit()
            conn.close()
            return record_id
        except Exception as e:
            print(f"创建兑换记录失败: {e}")
            return None

    def get_exchange_records(self, couple_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """获取兑换记录"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT e.*, r.name as reward_name
            FROM exchange_records e
            LEFT JOIN couple_rewards r ON e.reward_id = r.reward_id
            WHERE e.couple_id = ?
            ORDER BY e.exchange_time DESC
            LIMIT ?
        """, (couple_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_all_exchange_records(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取所有兑换记录（管理员功能）"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT e.*, r.name as reward_name, c.name1, c.name2
            FROM exchange_records e
            LEFT JOIN couple_rewards r ON e.reward_id = r.reward_id
            LEFT JOIN couples c ON e.couple_id = c.couple_id
            ORDER BY e.exchange_time DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
