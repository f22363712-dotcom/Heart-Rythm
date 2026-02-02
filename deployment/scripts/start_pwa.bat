@echo off
chcp 65001 >nul
echo ========================================
echo   心动积分系统 PWA 版本启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖...
    pip install -r requirements.txt
)

echo.
echo [2/3] 启动后端服务...
start "心动积分-后端" cmd /k "cd backend && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 >nul

echo.
echo [3/3] 启动前端服务...
start "心动积分-前端" cmd /k "cd frontend && python main.py"
timeout /t 3 >nul

echo.
echo ========================================
echo   ✅ 服务启动成功！
echo ========================================
echo.
echo   💻 电脑访问地址:
echo      http://127.0.0.1:5000
echo      http://localhost:5000
echo.
echo   📱 手机访问地址（同一WiFi下）:
echo      http://192.168.10.17:5000
echo.
echo   🔧 后端服务:
echo      API地址: http://127.0.0.1:8000
echo      API文档: http://127.0.0.1:8000/docs
echo.
echo   📱 PWA 安装说明:
echo   1. 电脑端: 使用Chrome/Edge浏览器访问上述地址
echo      - 地址栏会出现安装图标（⊕）
echo      - 或等待页面底部弹出安装提示
echo.
echo   2. 手机端: 确保手机和电脑连接同一WiFi
echo      - 使用手机浏览器访问: http://192.168.10.17:5000
echo      - Chrome: 点击菜单 → "添加到主屏幕"
echo      - Safari: 点击分享 → "添加到主屏幕"
echo      - 安装后可离线使用！
echo.
echo   测试账号:
echo   - 情侣账号: couple_test001 / 123456
echo   - 管理员:   admin / admin123
echo.
echo ========================================
echo   按任意键打开浏览器...
echo ========================================
pause >nul

start http://127.0.0.1:5000

echo.
echo 提示: 关闭此窗口不会停止服务
echo 要停止服务，请关闭后端和前端的命令行窗口
echo.
pause
