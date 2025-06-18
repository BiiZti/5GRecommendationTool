@echo off
REM 切换到脚本上级目录（即项目根目录）
cd /d %~dp0..
echo 🚀 启动套餐推荐系统 - GUI模式
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python，请先安装Python 3.7+
    echo 📥 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 启动GUI应用
echo 📱 正在启动图形界面...
python -m grec5.gui

if errorlevel 1 (
    echo.
    echo ❌ 应用启动失败
    echo 💡 请检查是否有错误信息
    pause
) else (
    echo.
    echo ✅ 应用已正常关闭
)

pause 