"""
心动积分项目 - 后端API服务
使用FastAPI构建RESTful API
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.data_manager import DataManager

app = FastAPI(
    title="心动积分项目 API",
    description="💕 情侣积分管理系统的后端API服务",
    version="1.0.0"
)

# 添加CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据管理器
dm = DataManager()
dm.load_all_data()

# ==================== Pydantic模型定义 ====================

class CoupleBase(BaseModel):
    name1: str = Field(..., min_length=1, description="第一个人的名字")
    name2: str = Field(..., min_length=1, description="第二个人的名字")

class CoupleCreate(CoupleBase):
    couple_id: str = Field(..., min_length=1, description="情侣唯一标识符")

class RewardBase(BaseModel):
    name: str = Field(..., min_length=1, description="奖励名称")
    points_needed: int = Field(..., gt=0, description="兑换所需积分")
    stock: int = Field(..., ge=0, description="奖励库存")
    description: str = Field("", max_length=200, description="奖励描述")

class RewardCreate(RewardBase):
    reward_id: str = Field(..., min_length=1, description="奖励唯一标识符")

class PointsChange(BaseModel):
    couple_id: str = Field(..., min_length=1, description="情侣ID")
    points_change: int = Field(..., description="积分变动值（正数增加，负数减少）")
    reason: str = Field(..., min_length=1, max_length=100, description="积分变动原因")

class ExchangeRecord(BaseModel):
    couple_id: str = Field(..., min_length=1, description="情侣ID")
    reward_id: str = Field(..., min_length=1, description="奖励ID")
    points_used: int = Field(..., gt=0, description="使用的积分")

# ==================== 情侣管理API ====================

@app.post("/couples/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_couple(couple: CoupleCreate):
    """创建新情侣"""
    success = dm.add_couple(couple.couple_id, couple.name1, couple.name2)
    if success:
        return {"message": "情侣创建成功", "couple_id": couple.couple_id}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="情侣创建失败，ID可能已存在"
    )

@app.get("/couples/{couple_id}/", response_model=dict, status_code=status.HTTP_200_OK)
def get_couple(couple_id: str):
    """获取指定情侣信息"""
    couple = dm.get_couple(couple_id)
    if couple:
        return {
            "couple_id": couple.couple_id,
            "names": couple.names,
            "points": couple.points,
            "history": couple.history,
            "created_time": couple.created_time
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="情侣不存在"
    )

@app.get("/couples/", response_model=dict, status_code=status.HTTP_200_OK)
def get_all_couples():
    """获取所有情侣列表"""
    couples = dm.get_all_couples()
    return {
        "couples": [
            {
                "couple_id": c.couple_id,
                "names": c.names,
                "points": c.points
            }
            for c in couples
        ]
    }

# ==================== 奖励管理API ====================

@app.post("/rewards/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_reward(reward: RewardCreate):
    """创建新奖励"""
    success = dm.add_reward(
        reward.reward_id,
        reward.name,
        reward.points_needed,
        reward.stock,
        reward.description
    )
    if success:
        return {"message": "奖励创建成功", "reward_id": reward.reward_id}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="奖励创建失败，ID可能已存在"
    )

@app.get("/rewards/", response_model=dict, status_code=status.HTTP_200_OK)
def get_all_rewards():
    """获取所有奖励列表"""
    rewards = dm.get_all_rewards()
    return {
        "rewards": [
            {
                "reward_id": r.reward_id,
                "name": r.name,
                "points_needed": r.points_needed,
                "stock": r.stock,
                "description": r.description
            }
            for r in rewards
        ]
    }

# ==================== 积分变动API ====================

@app.post("/points/", response_model=dict, status_code=status.HTTP_200_OK)
def update_points(points_data: PointsChange):
    """更新情侣积分"""
    couple = dm.get_couple(points_data.couple_id)
    if not couple:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣不存在"
        )
    
    success = dm.add_points_history(
        points_data.couple_id,
        points_data.points_change,
        points_data.reason
    )
    if success:
        updated_couple = dm.get_couple(points_data.couple_id)
        return {
            "message": "积分更新成功",
            "couple_id": points_data.couple_id,
            "new_points": updated_couple.points
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="积分更新失败"
    )

# ==================== 兑换记录API ====================

@app.post("/exchanges/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_exchange(exchange: ExchangeRecord):
    """创建兑换记录"""
    success = dm.add_exchange_record(
        exchange.couple_id,
        exchange.reward_id,
        exchange.points_used
    )
    if success:
        return {"message": "兑换记录创建成功"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="兑换记录创建失败"
    )

@app.get("/exchanges/", response_model=dict, status_code=status.HTTP_200_OK)
def get_all_exchanges():
    """获取所有兑换记录"""
    records = dm.get_all_exchange_records()
    return {
        "exchanges": [
            {
                "record_id": r.record_id,
                "couple_id": r.couple_id,
                "reward_id": r.reward_id,
                "points_used": r.points_used,
                "exchange_time": r.exchange_time
            }
            for r in records
        ]
    }

# ==================== 系统统计API ====================

@app.get("/stats/", response_model=dict, status_code=status.HTTP_200_OK)
def get_stats():
    """获取系统统计信息"""
    return dm.get_stats()

# ==================== 备份管理API ====================

@app.get("/backups/", response_model=dict, status_code=status.HTTP_200_OK)
def list_backups():
    """列出所有备份文件"""
    return {"backups": dm.list_backups()}

@app.post("/backups/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_backup():
    """创建新备份"""
    backup_file = dm.create_backup()
    if backup_file:
        return {"message": "备份创建成功", "backup_file": backup_file}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="备份创建失败"
    )

# ==================== 健康检查API ====================

@app.get("/health/", response_model=dict, status_code=status.HTTP_200_OK)
def health_check():
    """健康检查端点"""
    return {"status": "healthy", "message": "💕 心动积分系统运行正常"}
