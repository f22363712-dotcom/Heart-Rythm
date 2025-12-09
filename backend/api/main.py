from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.data_manager import DataManager

app = FastAPI(
    title="心动积分项目 API",
    description="情侣积分管理系统的后端API服务",
    version="1.0.0"
)

# 初始化数据管理器
dm = DataManager()
dm.load_all_data()

# 模型定义
class CoupleBase(BaseModel):
    name1: str = Field(..., min_length=1, description="第一个情侣的名字")
    name2: str = Field(..., min_length=1, description="第二个情侣的名字")

class CoupleCreate(CoupleBase):
    couple_id: str = Field(..., min_length=1, description="情侣唯一标识符")

class Couple(CoupleBase):
    couple_id: str
    points: int
    history: list
    created_time: str

    class Config:
        from_attributes = True

class RewardBase(BaseModel):
    name: str = Field(..., min_length=1, description="奖励名称")
    points_needed: int = Field(..., gt=0, description="兑换所需积分")
    stock: int = Field(..., ge=0, description="奖励库存")
    description: str = Field("", max_length=200, description="奖励描述")

class RewardCreate(RewardBase):
    reward_id: str = Field(..., min_length=1, description="奖励唯一标识符")

class Reward(RewardBase):
    reward_id: str
    created_time: str

    class Config:
        from_attributes = True

class PointsChange(BaseModel):
    couple_id: str = Field(..., min_length=1, description="情侣ID")
    points_change: int = Field(..., description="积分变动值")
    reason: str = Field(..., min_length=1, max_length=100, description="积分变动原因")

class ExchangeRecord(BaseModel):
    couple_id: str = Field(..., min_length=1, description="情侣ID")
    reward_id: str = Field(..., min_length=1, description="奖励ID")
    points_used: int = Field(..., gt=0, description="使用的积分")

# 情侣管理API
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

# 奖励管理API
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

# 积分变动API
@app.post("/points/", response_model=dict, status_code=status.HTTP_200_OK)
def update_points(points_change: PointsChange):
    """更新情侣积分"""
    success = dm.add_points_history(
        points_change.couple_id,
        points_change.points_change,
        points_change.reason
    )
    if success:
        couple = dm.get_couple(points_change.couple_id)
        return {
            "message": "积分更新成功",
            "couple_id": points_change.couple_id,
            "new_points": couple.points
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="积分更新失败，情侣不存在"
    )

# 兑换记录API
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

# 系统统计API
@app.get("/stats/", response_model=dict, status_code=status.HTTP_200_OK)
def get_stats():
    """获取系统统计信息"""
    return dm.get_system_stats()

# 备份管理API
@app.get("/backups/", response_model=dict, status_code=status.HTTP_200_OK)
def list_backups():
    """列出所有备份"""
    backups = dm.list_backups()
    return {"backups": backups}

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return {
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "detail": f"服务器内部错误: {str(exc)}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
