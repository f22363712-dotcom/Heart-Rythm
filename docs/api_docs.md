# 心动积分项目 API 文档

## 1. 概述

这是心动积分项目的后端API文档，提供了情侣积分管理系统的所有API接口。

## 2. API基础信息

- **API Base URL**: `http://localhost:8000`
- **文档地址**: `http://localhost:8000/docs` (Swagger UI)
- **开发语言**: Python
- **框架**: FastAPI

## 3. API端点

### 3.1 情侣管理

#### 3.1.1 创建情侣

- **HTTP Method**: POST
- **URL**: `/couples/`
- **请求体**:
  ```json
  {
    "couple_id": "string",
    "name1": "string",
    "name2": "string"
  }
  ```
- **响应示例**:
  ```json
  {
    "message": "情侣创建成功",
    "couple_id": "001"
  }
  ```
- **状态码**:
  - 201 Created: 创建成功
  - 400 Bad Request: 情侣ID已存在
  - 422 Unprocessable Entity: 请求参数验证失败

#### 3.1.2 获取情侣信息

- **HTTP Method**: GET
- **URL**: `/couples/{couple_id}/`
- **响应示例**:
  ```json
  {
    "couple_id": "001",
    "names": ["张三", "李四"],
    "points": 100,
    "history": [
      {
        "timestamp": "2025-12-09T16:00:00",
        "points_change": 100,
        "reason": "完成任务",
        "new_balance": 100
      }
    ],
    "created_time": "2025-12-09T15:00:00"
  }
  ```
- **状态码**:
  - 200 OK: 获取成功
  - 404 Not Found: 情侣不存在

### 3.2 奖励管理

#### 3.2.1 创建奖励

- **HTTP Method**: POST
- **URL**: `/rewards/`
- **请求体**:
  ```json
  {
    "reward_id": "string",
    "name": "string",
    "points_needed": 50,
    "stock": 10,
    "description": "string"
  }
  ```
- **响应示例**:
  ```json
  {
    "message": "奖励创建成功",
    "reward_id": "reward001"
  }
  ```
- **状态码**:
  - 201 Created: 创建成功
  - 400 Bad Request: 奖励ID已存在
  - 422 Unprocessable Entity: 请求参数验证失败

### 3.3 积分变动

#### 3.3.1 更新积分

- **HTTP Method**: POST
- **URL**: `/points/`
- **请求体**:
  ```json
  {
    "couple_id": "string",
    "points_change": 50,
    "reason": "string"
  }
  ```
- **响应示例**:
  ```json
  {
    "message": "积分更新成功",
    "couple_id": "001",
    "new_points": 150
  }
  ```
- **状态码**:
  - 200 OK: 更新成功
  - 404 Not Found: 情侣不存在
  - 422 Unprocessable Entity: 请求参数验证失败

### 3.4 兑换记录

#### 3.4.1 创建兑换记录

- **HTTP Method**: POST
- **URL**: `/exchanges/`
- **请求体**:
  ```json
  {
    "couple_id": "string",
    "reward_id": "string",
    "points_used": 50
  }
  ```
- **响应示例**:
  ```json
  {
    "message": "兑换记录创建成功"
  }
  ```
- **状态码**:
  - 201 Created: 创建成功
  - 400 Bad Request: 创建失败
  - 422 Unprocessable Entity: 请求参数验证失败

### 3.5 系统统计

#### 3.5.1 获取系统统计信息

- **HTTP Method**: GET
- **URL**: `/stats/`
- **响应示例**:
  ```json
  {
    "total_couples": 2,
    "total_rewards": 3,
    "total_exchanges": 5,
    "total_points": 1500,
    "last_updated": "2025-12-09T16:00:00"
  }
  ```
- **状态码**:
  - 200 OK: 获取成功

### 3.6 备份管理

#### 3.6.1 列出所有备份

- **HTTP Method**: GET
- **URL**: `/backups/`
- **响应示例**:
  ```json
  {
    "backups": [
      "data/backups/backup_20251209_150000.json",
      "data/backups/backup_20251209_140000.json"
    ]
  }
  ```
- **状态码**:
  - 200 OK: 获取成功

## 4. 数据模型

### 4.1 情侣模型

```json
{
  "couple_id": "string",
  "names": ["string", "string"],
  "points": 0,
  "history": [
    {
      "timestamp": "string",
      "points_change": 0,
      "reason": "string",
      "new_balance": 0
    }
  ],
  "created_time": "string"
}
```

### 4.2 奖励模型

```json
{
  "reward_id": "string",
  "name": "string",
  "points_needed": 0,
  "stock": 0,
  "description": "string",
  "created_time": "string"
}
```

### 4.3 积分变动模型

```json
{
  "couple_id": "string",
  "points_change": 0,
  "reason": "string"
}
```

### 4.4 兑换记录模型

```json
{
  "couple_id": "string",
  "reward_id": "string",
  "points_used": 0
}
```

## 5. 错误处理

### 5.1 常见错误状态码

| 状态码 | 描述 |
|--------|------|
| 200 OK | 请求成功 |
| 201 Created | 创建成功 |
| 400 Bad Request | 请求参数错误 |
| 404 Not Found | 资源不存在 |
| 422 Unprocessable Entity | 请求参数验证失败 |
| 500 Internal Server Error | 服务器内部错误 |

### 5.2 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

## 6. 最佳实践

1. **使用Swagger UI**：通过 `http://localhost:8000/docs` 可以交互式测试所有API
2. **错误处理**：调用API时请妥善处理各种错误状态码
3. **数据验证**：API会验证请求参数的合法性，请确保输入格式正确
4. **并发操作**：系统支持并发操作，但请避免同时对同一情侣进行积分变动
5. **备份管理**：定期查看和管理备份文件，确保数据安全

## 7. 开发说明

### 7.1 启动后端服务

```bash
# 通过主程序菜单启动
python main.py
# 选择选项1启动后端服务
```

或者直接运行API文件：

```bash
python -m uvicorn backend.api.main:app --reload
```

### 7.2 测试API

```bash
# 运行集成测试
python -m pytest tests/integration_tests/test_api.py -v
```

## 8. 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2025-12-09 | 初始版本，实现了所有核心API |
