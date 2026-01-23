@echo off
REM 心动积分项目 - 测试运行脚本（使用全局Python）
echo ====================================
echo   心动积分项目 - 运行所有测试
echo ====================================
echo.

REM 切换到项目目录
cd /d "%~dp0"

echo 当前目录: %CD%
echo.

REM 使用全局Python运行测试（忽略虚拟环境）
set PYTHONPATH=%CD%
set PYTHONDONTWRITEBYTECODE=1

echo 开始运行测试...
echo.

REM 使用python命令直接运行pytest
C:\Python314\python.exe -m pytest tests/ -v --tb=short

echo.
echo ====================================
echo   测试完成！
echo ====================================
pause
