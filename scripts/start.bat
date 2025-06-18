@echo off
chcp 65001 >nul

:start
cls
echo.
echo ┌─────────────────────────────────────────────────────────────┐
echo │                  📱 通用套餐推荐系统                        │
echo │                  选择启动模式                               │
echo └─────────────────────────────────────────────────────────────┘
echo.
echo 请选择启动模式：
echo.
echo [1] 🖥️  GUI桌面应用（推荐）
echo [2] 🌐 API服务器模式  
echo [3] 📋 查看系统信息
echo [4] 🔧 安装依赖
echo [5] ❌ 退出
echo.
set /p choice="请输入选项 (1-5): "

if "%choice%"=="1" goto start_gui
if "%choice%"=="2" goto start_api
if "%choice%"=="3" goto show_info
if "%choice%"=="4" goto install_deps
if "%choice%"=="5" goto exit
echo 无效选项，请重新选择...
pause
goto start

:start_gui
echo.
echo 🚀 启动GUI应用...
cd /d %~dp0..
call scripts\start_gui.bat
goto end

:start_api
echo.
echo 🚀 启动API服务器...
cd /d %~dp0..
call scripts\start_api.bat
goto end

:show_info
echo.
echo 📋 系统信息：
echo ─────────────────────────────────────
echo 项目名称：通用套餐推荐系统
echo 版本：v2.0.0 模块化重构版
echo 架构：分层模块化设计
echo 核心模块：推荐引擎、数据源管理、API服务
echo 支持方式：GUI界面、REST API、Python模块
echo ─────────────────────────────────────
echo.
python --version 2>nul || echo Python：未安装
pip --version 2>nul || echo pip：未安装
echo.
pause
goto start

:install_deps
echo.
echo 📦 安装项目依赖...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python
    echo 📥 请先安装Python 3.7+：https://www.python.org/downloads/
    pause
    goto start
)
echo ✅ Python已安装
echo.
echo 正在安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
) else (
    echo ✅ 依赖安装完成
)
echo.
pause
goto start

:exit
echo.
echo 👋 再见！
timeout /t 2 >nul
exit

:end
echo.
echo 按任意键返回主菜单...
pause >nul
goto start 