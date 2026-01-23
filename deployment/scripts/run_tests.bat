@echo off
REM 心动积分项目 - 测试运行脚本
echo ====================================
echo   心动积分项目 - 运行所有测试
echo ====================================
echo.

REM 切换到项目目录
cd /d "%~dp0"

echo 当前目录: %CD%
echo.
echo 开始运行测试...
echo.

REM 运行测试
python -m pytest tests/ -v --tb=short

echo.
echo ====================================
echo   测试完成！
echo ====================================
pause
