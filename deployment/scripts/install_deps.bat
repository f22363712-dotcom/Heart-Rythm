@echo off
REM 在虚拟环境中安装依赖
echo ====================================
echo   安装测试所需依赖
echo ====================================
echo.

cd /d "D:\Obsidian知识库\知识库"

echo 激活虚拟环境...
call .venv\Scripts\activate.bat

echo.
echo 安装 httpx 和 pytest...
pip install httpx pytest

echo.
echo ====================================
echo   安装完成！
echo ====================================
pause
