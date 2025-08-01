# MetaLearnNavigator Windows PowerShell 设置脚本

Write-Host "🎯 MetaLearnNavigator Windows环境设置" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 检查conda是否安装
try {
    $condaVersion = conda --version 2>$null
    Write-Host "✅ Conda已安装: $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Conda未安装或未添加到PATH" -ForegroundColor Red
    Write-Host "请先安装Anaconda或Miniconda: https://docs.conda.io/en/latest/miniconda.html" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

$envName = "metalearn-navigator"

# 检查环境是否已存在
$envExists = conda env list | Select-String $envName
if ($envExists) {
    Write-Host "⚠️  环境 $envName 已存在" -ForegroundColor Yellow
    $choice = Read-Host "是否删除并重新创建? (y/N)"
    if ($choice -eq "y" -or $choice -eq "Y") {
        Write-Host "🔄 删除现有环境..." -ForegroundColor Yellow
        conda env remove -n $envName -y
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ 删除环境失败" -ForegroundColor Red
            Read-Host "按Enter键退出"
            exit 1
        }
    } else {
        Write-Host "使用现有环境" -ForegroundColor Green
        goto ActivateEnv
    }
}

# 创建conda环境
Write-Host "🔄 创建conda环境..." -ForegroundColor Yellow
conda create -n $envName python=3.9 nodejs=18 -y
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 创建环境失败" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}
Write-Host "✅ 环境创建成功" -ForegroundColor Green

# 安装Python依赖
Write-Host "🔄 安装Python依赖..." -ForegroundColor Yellow
conda run -n $envName pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 安装Python依赖失败" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}
Write-Host "✅ Python依赖安装完成" -ForegroundColor Green

# 安装前端依赖
if (Test-Path "frontend") {
    Write-Host "🔄 安装前端依赖..." -ForegroundColor Yellow
    Set-Location frontend
    conda run -n $envName npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 安装前端依赖失败" -ForegroundColor Red
        Set-Location ..
        Read-Host "按Enter键退出"
        exit 1
    }
    Set-Location ..
    Write-Host "✅ 前端依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "⚠️  frontend目录不存在，跳过前端依赖安装" -ForegroundColor Yellow
}

# 创建环境配置文件
if (!(Test-Path "backend\.env") -and (Test-Path "backend\.env.example")) {
    Write-Host "📝 创建环境配置文件..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✅ 已创建 backend\.env 文件" -ForegroundColor Green
}

:ActivateEnv
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🎉 环境设置完成!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "环境名称: $envName" -ForegroundColor White
Write-Host ""
Write-Host "📋 使用方法:" -ForegroundColor Yellow
Write-Host "1. 激活环境:" -ForegroundColor White
Write-Host "   conda activate $envName" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 启动开发服务器:" -ForegroundColor White
Write-Host "   python start_dev.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 或者手动启动:" -ForegroundColor White
Write-Host "   # 启动后端" -ForegroundColor Gray
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   uvicorn main:app --reload" -ForegroundColor Gray
Write-Host "   # 启动前端 (新终端)" -ForegroundColor Gray
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 测试后端API:" -ForegroundColor White
Write-Host "   python test_backend.py" -ForegroundColor Gray
Write-Host ""
Write-Host "📍 访问地址:" -ForegroundColor Yellow
Write-Host "   前端应用: http://localhost:3000" -ForegroundColor Gray
Write-Host "   后端API:  http://localhost:8000" -ForegroundColor Gray
Write-Host "   API文档:  http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Cyan

Read-Host "按Enter键退出"
