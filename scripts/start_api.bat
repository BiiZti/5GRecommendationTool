@echo off
REM 切换到脚本上级目录（即项目根目录）
cd /d %~dp0..
echo 🚀 启动套餐推荐系统 - API服务器模式
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python，请先安装Python 3.7+
    echo 📥 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查并安装依赖
echo 📦 检查API服务器依赖...
pip install flask flask-cors requests >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告：依赖安装可能有问题，但继续启动...
) else (
    echo ✅ 依赖检查完成
)

echo.
echo 🌐 正在启动API服务器...
echo 📡 服务器将在 http://127.0.0.1:5000 启动
echo 📋 API文档访问：http://127.0.0.1:5000/api/health
echo.
echo 💡 按 Ctrl+C 停止服务器
echo.

REM 启动API服务器
python -m grec5.api_server

if errorlevel 1 (
    echo.
    echo ❌ API服务器启动失败
    echo 💡 请检查是否有错误信息或端口冲突
    pause
) else (
    echo.
    echo ✅ API服务器已停止
)

pause 