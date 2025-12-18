# 心动积分项目 - 阅读理解指南

## 1. 项目概述

心动积分项目是一个专为情侣设计的积分管理系统，旨在帮助情侣记录和管理彼此的积分，促进感情发展。通过完成各种任务和挑战，情侣可以获得积分，然后用积分兑换奖励，增强彼此之间的互动和情感连接。

## 2. 目录结构

### 2.1 项目根目录

```
Heart-Rythm/
├── backend/            # 后端代码
├── data/               # 数据存储目录
├── docs/               # 文档
├── frontend/           # 前端代码
├── tests/              # 测试代码
├── 文本说明/           # 项目文本说明
├── CHANGELOG.md        # 版本日志
├── COMPREHENSION_GUIDE.md # 阅读理解指南
├── main.py             # 主入口文件
└── requirements.txt    # 依赖列表
```

### 2.2 后端目录

```
backend/
├── api/               # API层
│   └── main.py         # API入口文件
└── data_manager.py     # 数据管理模块
```

- **api/main.py**：FastAPI应用的入口文件，定义了所有API端点
- **data_manager.py**：数据管理模块，负责数据的存储、验证和管理

### 2.3 前端目录

```
frontend/
└── templates/          # HTML模板
    ├── base.html       # 基础模板
    ├── couples.html    # 情侣管理页面
    ├── index.html      # 首页
    └── rewards.html    # 奖励管理页面
```

- **main.py**：Flask应用的入口文件
- **templates/**：HTML模板目录，包含所有前端页面

### 2.4 数据目录

```
data/
├── backups/            # 备份文件目录
└── system_data.json    # 主数据文件
```

- **system_data.json**：存储系统的所有数据，包括情侣、奖励、积分变动等
- **backups/**：自动生成的备份文件目录

### 2.5 文档目录

```
docs/
├── api_docs.md         # API文档
├── example_usage.py    # 示例程序
└── user_guide.md       # 用户指南
```

- **api_docs.md**：详细的API端点说明和示例
- **example_usage.py**：使用实际API演示系统功能的示例程序
- **user_guide.md**：完整的安装、运行和使用说明

### 2.6 测试目录

```
tests/
├── integration_tests/  # 集成测试
└── unit_tests/         # 单元测试
```

- **integration_tests/**：API集成测试
- **unit_tests/**：数据管理模块的单元测试

## 3. 核心功能

### 3.1 情侣管理

- **添加情侣**：创建新的情侣记录
- **查询情侣**：获取情侣的详细信息和积分变动历史
- **积分变动**：记录情侣之间的积分变动

### 3.2 奖励管理

- **添加奖励**：创建新的奖励商品
- **库存管理**：管理奖励的库存
- **积分兑换**：记录奖励兑换情况

### 3.3 积分变动

- **增加积分**：为情侣添加积分
- **减少积分**：从情侣积分中扣除
- **变动原因**：记录积分变动的原因

### 3.4 兑换记录

- **创建兑换记录**：记录情侣兑换奖励的情况
- **积分扣除**：自动扣除兑换所需的积分

### 3.5 系统统计

- **情侣数量**：统计系统中的情侣数量
- **奖励数量**：统计系统中的奖励数量
- **总积分**：统计所有情侣的总积分
- **兑换次数**：统计奖励兑换的总次数

### 3.6 数据备份

- **自动备份**：系统自动备份数据
- **备份管理**：保留最近10个备份文件
- **恢复功能**：支持从备份文件恢复数据

## 4. 主要文件说明

### 4.1 main.py（主入口）

项目的主入口文件，提供了一个菜单界面，用于启动后端服务、前端应用、运行示例程序和测试。

### 4.2 backend/api/main.py（API入口）

FastAPI应用的入口文件，定义了所有API端点，包括：
- 情侣管理API
- 奖励管理API
- 积分变动API
- 兑换记录API
- 系统统计API
- 备份管理API

### 4.3 backend/data_manager.py（数据管理）

数据管理模块，负责：
- 数据的存储和读取
- 数据验证
- 数据的CRUD操作
- 自动备份和恢复

### 4.4 frontend/main.py（前端入口）

Flask应用的入口文件，定义了前端路由和视图函数。

### 4.5 frontend/templates/（前端模板）

包含所有前端页面的HTML模板，使用Jinja2模板引擎。

## 5. 技术栈

| 分类 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 后端框架 | FastAPI | 1.0.0 | 构建RESTful API |
| 前端框架 | Flask | 3.1.2 | 构建前端应用 |
| 数据验证 | Pydantic | 2.12.5 | 数据模型和验证 |
| API文档 | Swagger UI | - | 自动生成API文档 |
| 测试框架 | pytest | 9.0.2 | 编写和运行测试 |
| HTTP客户端 | httpx | 0.28.1 | API测试和请求 |
| 数据存储 | JSON | - | 存储系统数据 |

## 6. 如何运行

### 6.1 环境要求

- Python 3.10 或更高版本
- pip 包管理工具

### 6.2 安装依赖

```bash
pip install -r requirements.txt
```

### 6.3 启动系统

```bash
python main.py
```

### 6.4 选择运行选项

启动系统后，会出现以下菜单：

```
==================================================
🎯 心动积分项目 - 主入口
==================================================
1. 启动后端服务
2. 启动前端应用
3. 运行示例程序
4. 运行测试
0. 退出
==================================================
请输入您的选择 [0-4]: 
```

- **选项1**：启动后端服务（默认端口：8000）
  - API文档：http://localhost:8000/docs
  - API Base URL：http://localhost:8000

- **选项2**：启动前端应用（默认端口：5000）
  - 前端页面：http://localhost:5000

- **选项3**：运行示例程序
  - 演示系统的主要功能

- **选项4**：运行测试
  - 运行单元测试和集成测试

- **选项0**：退出系统

## 7. 功能使用指南

### 7.1 后端API使用

#### 7.1.1 创建情侣

```bash
curl -X POST "http://localhost:8000/couples/" -H "Content-Type: application/json" -d '{"couple_id": "001", "name1": "张三", "name2": "李四"}'
```

#### 7.1.2 获取情侣信息

```bash
curl -X GET "http://localhost:8000/couples/001/"
```

#### 7.1.3 添加奖励

```bash
curl -X POST "http://localhost:8000/rewards/" -H "Content-Type: application/json" -d '{"reward_id": "reward001", "name": "电影票", "points_needed": 50, "stock": 10, "description": "双人电影票"}'
```

#### 7.1.4 更新积分

```bash
curl -X POST "http://localhost:8000/points/" -H "Content-Type: application/json" -d '{"couple_id": "001", "points_change": 100, "reason": "完成任务"}'
```

#### 7.1.5 创建兑换记录

```bash
curl -X POST "http://localhost:8000/exchanges/" -H "Content-Type: application/json" -d '{"couple_id": "001", "reward_id": "reward001", "points_used": 50}'
```

#### 7.1.6 获取系统统计

```bash
curl -X GET "http://localhost:8000/stats/"
```

### 7.2 前端应用使用

#### 7.2.1 首页

- 展示系统统计信息
- 提供功能导航

#### 7.2.2 情侣管理

- **添加情侣**：输入情侣ID、姓名1和姓名2，点击"添加情侣"按钮
- **查询情侣**：输入情侣ID，点击"查询"按钮查看情侣信息和积分变动历史

#### 7.2.3 奖励管理

- **添加奖励**：输入奖励ID、名称、所需积分、库存和描述，点击"添加奖励"按钮
- **积分变动**：输入情侣ID、积分变动值和变动原因，点击"提交积分变动"按钮
- **创建兑换记录**：输入情侣ID、奖励ID和使用积分，点击"创建兑换记录"按钮

### 7.3 示例程序使用

运行示例程序演示系统功能：

```bash
python docs/example_usage.py
```

## 8. 测试和开发

### 8.1 运行测试

```bash
python main.py
# 选择选项4运行测试
```

或者直接使用pytest运行测试：

```bash
# 运行所有测试
python -m pytest

# 运行单元测试
python -m pytest tests/unit_tests/

# 运行集成测试
python -m pytest tests/integration_tests/
```

### 8.2 开发流程

1. **克隆项目**：
   ```bash
   git clone <项目仓库地址>
   cd Heart-Rythm
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **开发代码**：
   - 后端开发：修改`backend/api/main.py`或`backend/data_manager.py`
   - 前端开发：修改`frontend/main.py`或`templates/`下的HTML文件

4. **运行测试**：
   ```bash
   python -m pytest
   ```

5. **提交代码**：
   ```bash
   git add .
   git commit -m "提交信息"
   git push
   ```

## 9. 文档

### 9.1 API文档

API文档提供了详细的API端点说明和示例，可以通过以下方式访问：

- **在线文档**：启动后端服务后，访问 `http://localhost:8000/docs`
- **离线文档**：查看 `docs/api_docs.md` 文件

### 9.2 用户指南

用户指南包含完整的安装、运行和使用说明，查看 `docs/user_guide.md` 文件。

### 9.3 示例程序

示例程序演示了如何使用实际API调用系统功能，查看 `docs/example_usage.py` 文件。

## 10. 常见问题

### 10.1 如何启动系统？

运行 `python main.py` 命令，然后选择相应的运行选项。

### 10.2 如何访问API文档？

启动后端服务后，访问 `http://localhost:8000/docs`。

### 10.3 如何访问前端页面？

启动前端应用后，访问 `http://localhost:5000`。

### 10.4 数据存储在哪里？

数据存储在 `data/system_data.json` 文件中。

### 10.5 如何备份数据？

系统会自动备份数据到 `data/backups/` 目录，无需手动操作。

### 10.6 如何恢复数据？

系统支持从备份文件恢复数据，具体方法请参考用户指南。

### 10.7 如何添加新的API端点？

在 `backend/api/main.py` 文件中添加新的路由和处理函数。

### 10.8 如何添加新的前端页面？

1. 在 `frontend/templates/` 目录下创建新的HTML模板
2. 在 `frontend/main.py` 文件中添加新的路由和视图函数

## 11. 后续优化方向

1. **添加用户认证**：实现登录和权限管理
2. **增强数据可视化**：添加图表展示积分趋势
3. **实现实时通知**：积分变动时发送通知
4. **添加更多奖励类型**：支持不同类型的奖励
5. **优化移动端体验**：增强移动端适配
6. **添加数据分析功能**：分析积分变动趋势和兑换情况
7. **支持多人情侣**：支持三人或以上的情侣关系
8. **添加任务系统**：预设任务模板，自动计算积分

## 12. 联系方式

如果您在使用过程中遇到任何问题，可以通过以下方式联系我们：

- **项目负责人**：XXX
- **邮箱**：XXX@example.com
- **GitHub**：<项目GitHub地址>

## 13. 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。
