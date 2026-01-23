@echo off
echo ========================================
echo 心动积分系统 v2.0 - 启动脚本
echo ========================================
echo.

echo [1/3] 停止现有服务...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/3] 启动后端服务 (端口 8000)...
start /B python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
timeout /t 3 /nobreak >nul

echo [3/3] 启动前端服务 (端口 5000)...
start /B python frontend/main.py
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 服务启动完成！
echo ========================================
echo.
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 前端界面: http://localhost:5000
echo.
echo 默认账号:
echo   管理员: admin / admin123
echo   情侣账号: couple_test001 / 123456
echo.
echo 按任意键打开浏览器...
pause >nul
start http://localhost:5000
