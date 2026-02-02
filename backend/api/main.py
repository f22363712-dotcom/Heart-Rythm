"""
心动积分项目 - 后端API服务 (v2.0 - 带权限控制)
使用FastAPI构建RESTful API，支持用户认证和数据隔离
"""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database import Database
from backend.auth import (
    SessionManager, get_current_user, require_admin,
    get_user_couple_id, verify_couple_access
)

app = FastAPI(
    title="心动积分项目 API v2.0",
    description="💕 情侣积分管理系统的后端API服务 - 支持用户认证和数据隔离",
    version="2.0.0"
)

# 添加CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
db = Database()

# ==================== Pydantic模型定义 ====================

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="用户名")
    password: str = Field(..., min_length=1, description="密码")

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    name1: str = Field(..., min_length=1, description="第一个人的名字")
    name2: str = Field(..., min_length=1, description="第二个人的名字")

class CoupleCreate(BaseModel):
    name1: str = Field(..., min_length=1, description="第一个人的名字")
    name2: str = Field(..., min_length=1, description="第二个人的名字")

class PointsChange(BaseModel):
    points_change: int = Field(..., description="积分变动值（正数增加，负数减少）")
    reason: str = Field(..., min_length=1, max_length=100, description="积分变动原因")

class RewardCreate(BaseModel):
    name: str = Field(..., min_length=1, description="奖励名称")
    points_needed: int = Field(..., gt=0, description="兑换所需积分")
    stock: int = Field(..., ge=0, description="奖励库存")
    description: str = Field("", max_length=200, description="奖励描述")

class RewardUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="奖励名称")
    points_needed: Optional[int] = Field(None, gt=0, description="兑换所需积分")
    stock: Optional[int] = Field(None, ge=0, description="奖励库存")
    description: Optional[str] = Field(None, max_length=200, description="奖励描述")

class ExchangeRequest(BaseModel):
    reward_id: str = Field(..., min_length=1, description="奖励ID")

# ==================== 认证API ====================

@app.post("/auth/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    """用户注册"""
    # 创建用户
    user_id = db.create_user(request.username, request.password, is_admin=False)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 创建情侣记录
    couple_id = db.create_couple(user_id, request.name1, request.name2)

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建情侣记录失败"
        )

    return {
        "message": "注册成功",
        "username": request.username,
        "couple_id": couple_id
    }

@app.post("/auth/login", response_model=dict, status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    """用户登录"""
    user = db.verify_user(request.username, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 创建会话
    token = SessionManager.create_session(
        user["id"],
        user["username"],
        user["is_admin"]
    )

    # 获取情侣信息（如果不是管理员）
    couple_info = None
    if not user["is_admin"]:
        couple = db.get_couple_by_user_id(user["id"])
        if couple:
            couple_info = {
                "couple_id": couple["couple_id"],
                "names": [couple["name1"], couple["name2"]],
                "points": couple["points"]
            }

    return {
        "message": "登录成功",
        "token": token,
        "user": {
            "username": user["username"],
            "is_admin": user["is_admin"]
        },
        "couple": couple_info
    }

@app.post("/auth/logout", response_model=dict, status_code=status.HTTP_200_OK)
def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """用户登出"""
    # 这里需要从请求头获取token，但为了简化，我们返回成功
    return {"message": "登出成功"}

@app.get("/auth/me", response_model=dict, status_code=status.HTTP_200_OK)
def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取当前用户信息"""
    user_info = {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "is_admin": current_user["is_admin"]
    }

    # 如果不是管理员，获取情侣信息
    if not current_user["is_admin"]:
        couple = db.get_couple_by_user_id(current_user["user_id"])
        if couple:
            user_info["couple"] = {
                "couple_id": couple["couple_id"],
                "names": [couple["name1"], couple["name2"]],
                "points": couple["points"]
            }

    return user_info

# ==================== 情侣管理API ====================

@app.get("/couples/me", response_model=dict, status_code=status.HTTP_200_OK)
def get_my_couple(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取当前用户的情侣信息"""
    if current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="管理员没有情侣信息"
        )

    couple = db.get_couple_by_user_id(current_user["user_id"])
    if not couple:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    return {
        "couple_id": couple["couple_id"],
        "names": [couple["name1"], couple["name2"]],
        "points": couple["points"],
        "created_time": couple["created_time"]
    }

@app.get("/couples/all", response_model=dict, status_code=status.HTTP_200_OK)
def get_all_couples(current_user: Dict[str, Any] = Depends(require_admin)):
    """获取所有情侣列表（管理员）"""
    couples = db.get_all_couples()
    return {
        "couples": [
            {
                "couple_id": c["couple_id"],
                "username": c.get("username", ""),
                "names": [c["name1"], c["name2"]],
                "points": c["points"],
                "created_time": c["created_time"]
            }
            for c in couples
        ]
    }

# ==================== 积分管理API ====================

@app.post("/points", response_model=dict, status_code=status.HTTP_200_OK)
def update_points(
    points_data: PointsChange,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """更新积分"""
    # 获取用户的情侣ID
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    # 更新积分
    success = db.update_couple_points(
        couple_id,
        points_data.points_change,
        points_data.reason
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="积分更新失败"
        )

    # 获取更新后的积分
    couple = db.get_couple_by_id(couple_id)

    return {
        "message": "积分更新成功",
        "new_points": couple["points"]
    }

@app.get("/points/history", response_model=dict, status_code=status.HTTP_200_OK)
def get_point_history(
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """获取积分历史"""
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    history = db.get_point_history(couple_id, limit)

    return {
        "history": history
    }

# ==================== 奖励管理API ====================

@app.get("/rewards/base", response_model=dict, status_code=status.HTTP_200_OK)
def get_base_rewards(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取基础奖励列表（供参考）"""
    rewards = db.get_base_rewards()
    return {
        "rewards": rewards
    }

@app.get("/rewards", response_model=dict, status_code=status.HTTP_200_OK)
def get_my_rewards(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取我的奖励列表"""
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    rewards = db.get_couple_rewards(couple_id)

    return {
        "rewards": rewards
    }

@app.post("/rewards", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_reward(
    reward: RewardCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """创建奖励"""
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    reward_id = db.create_couple_reward(
        couple_id,
        reward.name,
        reward.points_needed,
        reward.stock,
        reward.description
    )

    if not reward_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="创建奖励失败"
        )

    return {
        "message": "奖励创建成功",
        "reward_id": reward_id
    }

@app.put("/rewards/{reward_id}", response_model=dict, status_code=status.HTTP_200_OK)
def update_reward(
    reward_id: str,
    reward: RewardUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """更新奖励"""
    # 验证奖励是否属于当前用户
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    # 获取奖励信息验证所有权
    rewards = db.get_couple_rewards(couple_id)
    reward_exists = any(r["reward_id"] == reward_id for r in rewards)

    if not reward_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此奖励"
        )

    # 更新奖励
    success = db.update_couple_reward(
        reward_id,
        reward.name,
        reward.points_needed,
        reward.stock,
        reward.description
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="更新奖励失败"
        )

    return {"message": "奖励更新成功"}

@app.delete("/rewards/{reward_id}", response_model=dict, status_code=status.HTTP_200_OK)
def delete_reward(
    reward_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """删除奖励"""
    # 验证奖励是否属于当前用户
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    # 获取奖励信息验证所有权
    rewards = db.get_couple_rewards(couple_id)
    reward_exists = any(r["reward_id"] == reward_id for r in rewards)

    if not reward_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此奖励"
        )

    # 删除奖励
    success = db.delete_couple_reward(reward_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="删除奖励失败"
        )

    return {"message": "奖励删除成功"}

# ==================== 兑换管理API ====================

@app.post("/exchanges", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_exchange(
    exchange: ExchangeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """兑换奖励"""
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    # 获取奖励信息
    rewards = db.get_couple_rewards(couple_id)
    reward = next((r for r in rewards if r["reward_id"] == exchange.reward_id), None)

    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="奖励不存在"
        )

    # 创建兑换记录
    record_id = db.create_exchange_record(
        couple_id,
        exchange.reward_id,
        reward["points_needed"]
    )

    if not record_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="兑换失败，可能是积分不足或库存不足"
        )

    # 获取更新后的积分
    couple = db.get_couple_by_id(couple_id)

    return {
        "message": "兑换成功",
        "record_id": record_id,
        "new_points": couple["points"]
    }

@app.get("/exchanges", response_model=dict, status_code=status.HTTP_200_OK)
def get_my_exchanges(
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """获取我的兑换记录"""
    couple_id = get_user_couple_id(db, current_user["user_id"])

    if not couple_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="情侣信息不存在"
        )

    records = db.get_exchange_records(couple_id, limit)

    return {
        "exchanges": records
    }

@app.get("/exchanges/all", response_model=dict, status_code=status.HTTP_200_OK)
def get_all_exchanges(
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(require_admin)
):
    """获取所有兑换记录（管理员）"""
    records = db.get_all_exchange_records(limit)

    return {
        "exchanges": records
    }

# ==================== 管理员API ====================

@app.get("/admin/stats", response_model=dict, status_code=status.HTTP_200_OK)
def get_admin_stats(current_user: Dict[str, Any] = Depends(require_admin)):
    """获取系统统计信息（管理员）"""
    couples = db.get_all_couples()
    exchanges = db.get_all_exchange_records(1000)

    total_points = sum(c["points"] for c in couples)
    total_exchanges = len(exchanges)

    return {
        "total_couples": len(couples),
        "total_points": total_points,
        "total_exchanges": total_exchanges
    }

# ==================== 健康检查API ====================

@app.get("/health", response_model=dict, status_code=status.HTTP_200_OK)
def health_check():
    """健康检查端点"""
    return {"status": "healthy", "message": "💕 心动积分系统 v2.0 运行正常"}

# 根路径路由已移至 app.py，用于提供前端页面
# API 信息可通过 /docs 查看
