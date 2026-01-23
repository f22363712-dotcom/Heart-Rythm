@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║          💕 心动积分 v2.1 PWA版 - 快速验证工具 💕          ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [步骤 1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到Python
    echo    请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python环境正常

echo.
echo [步骤 2/4] 检查项目依赖...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ⚠ 警告: Flask未安装
    echo    正在安装依赖...
    pip install -r requirements.txt
)
echo ✓ 项目依赖正常

echo.
echo [步骤 3/4] 验证PWA配置...
python scripts/verify_pwa.py
if errorlevel 1 (
    echo.
    echo ❌ PWA配置验证失败
    echo    请查看上述错误信息并修复
    pause
    exit /b 1
)

echo.
echo [步骤 4/4] 检查关键文件...
if not exist "frontend\static\manifest.json" (
    echo ❌ 缺少: manifest.json
    exit /b 1
)
echo ✓ manifest.json 存在

if not exist "frontend\static\sw.js" (
    echo ❌ 缺少: sw.js
    exit /b 1
)
echo ✓ sw.js 存在

if not exist "frontend\static\icons\icon-192x192.png" (
    echo ❌ 缺少: 图标文件
    echo    运行: python scripts/generate_pwa_icons.py
    exit /b 1
)
echo ✓ 图标文件存在

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║                  ✅ 所有检查通过！                         ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🎉 恭喜！PWA配置完全正确
echo.
echo 📱 下一步操作:
echo    1. 运行 start_pwa.bat 启动服务
echo    2. 访问 http://localhost:5000
echo    3. 使用Chrome打开开发者工具(F12)
echo    4. 检查 Application → Manifest 和 Service Workers
echo    5. 尝试安装到主屏幕
echo.
echo 📚 相关文档:
echo    - PWA部署指南: PWA_GUIDE.md
echo    - 快速参考: PWA_QUICK_REFERENCE.md
echo    - 测试清单: PWA_TEST_CHECKLIST.md
echo.
echo 💡 提示:
echo    - 使用Chrome浏览器获得最佳体验
echo    - 生产环境需要HTTPS
echo    - iOS设备需使用Safari手动添加
echo.
pause
