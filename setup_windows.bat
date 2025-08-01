@echo off
echo 🎯 MetaLearnNavigator Windows环境设置
echo ================================================

REM 检查conda是否安装
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Conda未安装或未添加到PATH
    echo 请先安装Anaconda或Miniconda: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo ✅ Conda已安装

REM 检查环境是否已存在
conda env list | findstr "metalearn-navigator" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  环境 metalearn-navigator 已存在
    set /p choice="是否删除并重新创建? (y/N): "
    if /i "%choice%"=="y" (
        echo 🔄 删除现有环境...
        conda env remove -n metalearn-navigator -y
    ) else (
        echo 使用现有环境
        goto activate_env
    )
)

echo 🔄 创建conda环境...
conda create -n metalearn-navigator python=3.9 nodejs=18 -y
if %errorlevel% neq 0 (
    echo ❌ 创建环境失败
    pause
    exit /b 1
)

echo ✅ 环境创建成功

echo 🔄 安装Python依赖...
conda run -n metalearn-navigator pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 安装Python依赖失败
    pause
    exit /b 1
)

echo ✅ Python依赖安装完成

REM 检查frontend目录是否存在
if exist "frontend" (
    echo 🔄 安装前端依赖...
    cd frontend
    conda run -n metalearn-navigator npm install
    if %errorlevel% neq 0 (
        echo ❌ 安装前端依赖失败
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo ✅ 前端依赖安装完成
) else (
    echo ⚠️  frontend目录不存在，跳过前端依赖安装
)

REM 创建环境配置文件
if not exist "backend\.env" (
    if exist "backend\.env.example" (
        echo 📝 创建环境配置文件...
        copy "backend\.env.example" "backend\.env" >nul
        echo ✅ 已创建 backend\.env 文件
    )
)

:activate_env
echo.
echo ================================================
echo 🎉 环境设置完成!
echo ================================================
echo 环境名称: metalearn-navigator
echo.
echo 📋 使用方法:
echo 1. 激活环境:
echo    conda activate metalearn-navigator
echo.
echo 2. 启动开发服务器:
echo    python start_dev.py
echo.
echo 3. 或者手动启动:
echo    # 启动后端
echo    cd backend
echo    uvicorn main:app --reload
echo    # 启动前端 (新终端)
echo    cd frontend
echo    npm start
echo.
echo 4. 测试后端API:
echo    python test_backend.py
echo.
echo 📍 访问地址:
echo    前端应用: http://localhost:3000
echo    后端API:  http://localhost:8000
echo    API文档:  http://localhost:8000/docs
echo ================================================

pause
