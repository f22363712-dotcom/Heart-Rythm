"""
用户认证和会话管理
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
from functools import wraps
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# 会话存储（简单的内存存储，生产环境应使用Redis等）
sessions: Dict[str, Dict[str, Any]] = {}

# 会话过期时间（小时）
SESSION_EXPIRE_HOURS = 24

security = HTTPBearer()


class SessionManager:
    """会话管理器"""

    @staticmethod
    def create_session(user_id: int, username: str, is_admin: bool) -> str:
        """创建会话"""
        token = secrets.token_urlsafe(32)
        sessions[token] = {
            "user_id": user_id,
            "username": username,
            "is_admin": is_admin,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=SESSION_EXPIRE_HOURS)
        }
        return token

    @staticmethod
    def get_session(token: str) -> Optional[Dict[str, Any]]:
        """获取会话信息"""
        if token not in sessions:
            return None

        session = sessions[token]

        # 检查是否过期
        if datetime.now() > session["expires_at"]:
            del sessions[token]
            return None

        return session

    @staticmethod
    def delete_session(token: str) -> bool:
        """删除会话（登出）"""
        if token in sessions:
            del sessions[token]
            return True
        return False

    @staticmethod
    def refresh_session(token: str) -> bool:
        """刷新会话过期时间"""
        if token in sessions:
            sessions[token]["expires_at"] = datetime.now() + timedelta(hours=SESSION_EXPIRE_HOURS)
            return True
        return False

    @staticmethod
    def cleanup_expired_sessions():
        """清理过期会话"""
        now = datetime.now()
        expired_tokens = [
            token for token, session in sessions.items()
            if now > session["expires_at"]
        ]
        for token in expired_tokens:
            del sessions[token]


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """获取当前登录用户（依赖注入）"""
    token = credentials.credentials
    session = SessionManager.get_session(token)

    if not session:
        raise HTTPException(status_code=401, detail="未登录或会话已过期")

    # 刷新会话
    SessionManager.refresh_session(token)

    return {
        "user_id": session["user_id"],
        "username": session["username"],
        "is_admin": session["is_admin"]
    }


def get_current_user_optional(request: Request) -> Optional[Dict[str, Any]]:
    """获取当前用户（可选，不强制登录）"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    session = SessionManager.get_session(token)

    if session:
        SessionManager.refresh_session(token)
        return {
            "user_id": session["user_id"],
            "username": session["username"],
            "is_admin": session["is_admin"]
        }

    return None


def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """要求管理员权限"""
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user


def get_user_couple_id(db, user_id: int) -> Optional[str]:
    """获取用户的情侣ID"""
    couple = db.get_couple_by_user_id(user_id)
    if couple:
        return couple["couple_id"]
    return None


def verify_couple_access(db, couple_id: str, current_user: Dict[str, Any]) -> bool:
    """验证用户是否有权访问指定情侣的数据"""
    # 管理员可以访问所有数据
    if current_user.get("is_admin"):
        return True

    # 普通用户只能访问自己的数据
    user_couple_id = get_user_couple_id(db, current_user["user_id"])
    return user_couple_id == couple_id
