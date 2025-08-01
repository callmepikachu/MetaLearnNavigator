#!/usr/bin/env python3
"""
Conda环境设置脚本
自动创建和配置MetaLearnNavigator的conda环境
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, check=True):
    """运行命令并显示进度"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}完成")
            return True
        else:
            print(f"❌ {description}失败: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        return False

def check_conda():
    """检查conda是否安装"""
    print("🔍 检查conda环境...")
    try:
        result = subprocess.run(['conda', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Conda已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Conda未安装")
            return False
    except FileNotFoundError:
        print("❌ Conda未安装或未添加到PATH")
        return False

def create_conda_env():
    """创建conda环境"""
    env_name = "metalearn-navigator"
    
    # 检查环境是否已存在
    result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
    if env_name in result.stdout:
        print(f"⚠️  环境 {env_name} 已存在")
        response = input("是否删除并重新创建? (y/N): ")
        if response.lower() == 'y':
            run_command(f'conda env remove -n {env_name}', f"删除现有环境 {env_name}")
        else:
            print("使用现有环境")
            return True
    
    # 创建环境
    if Path('environment.yml').exists():
        return run_command(f'conda env create -f environment.yml', "从environment.yml创建conda环境")
    else:
        # 手动创建环境
        commands = [
            f'conda create -n {env_name} python=3.9 nodejs=18 -y',
        ]

        for cmd in commands:
            if not run_command(cmd, f"执行: {cmd}"):
                return False

        # 激活环境并安装Python包
        pip_install_cmd = f'conda run -n {env_name} pip install -r requirements.txt'
        return run_command(pip_install_cmd, "安装Python依赖包")

def install_frontend_deps():
    """安装前端依赖"""
    frontend_path = Path('frontend')
    if not frontend_path.exists():
        print("⚠️  frontend目录不存在，跳过前端依赖安装")
        return True
    
    env_name = "metalearn-navigator"
    npm_install_cmd = f'conda run -n {env_name} --cwd frontend npm install'
    return run_command(npm_install_cmd, "安装前端依赖")

def setup_environment_file():
    """设置环境配置文件"""
    env_file = Path('backend/.env')
    env_example = Path('backend/.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 创建环境配置文件...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ 已创建 backend/.env 文件")
    
    return True

def print_usage_instructions():
    """打印使用说明"""
    env_name = "metalearn-navigator"
    print("\n" + "=" * 60)
    print("🎉 Conda环境设置完成!")
    print("=" * 60)
    print(f"环境名称: {env_name}")
    print("\n📋 使用方法:")
    print(f"1. 激活环境:")
    print(f"   conda activate {env_name}")
    print("\n2. 启动开发服务器:")
    print("   python start_dev.py")
    print("\n3. 或者手动启动:")
    print("   # 启动后端")
    print("   cd backend")
    print("   uvicorn main:app --reload")
    print("   # 启动前端 (新终端)")
    print("   cd frontend")
    print("   npm start")
    print("\n4. 测试后端API:")
    print("   python test_backend.py")
    print("\n5. 停用环境:")
    print("   conda deactivate")
    print("\n📍 访问地址:")
    print("   前端应用: http://localhost:3000")
    print("   后端API:  http://localhost:8000")
    print("   API文档:  http://localhost:8000/docs")
    print("=" * 60)

def main():
    """主函数"""
    print("🎯 MetaLearnNavigator Conda环境设置")
    print("=" * 50)
    
    # 检查conda
    if not check_conda():
        print("\n❌ 请先安装Anaconda或Miniconda:")
        print("   https://docs.conda.io/en/latest/miniconda.html")
        sys.exit(1)
    
    # 创建conda环境
    if not create_conda_env():
        print("❌ 创建conda环境失败")
        sys.exit(1)
    
    # 安装前端依赖
    if not install_frontend_deps():
        print("❌ 安装前端依赖失败")
        sys.exit(1)
    
    # 设置环境文件
    setup_environment_file()
    
    # 打印使用说明
    print_usage_instructions()

if __name__ == '__main__':
    main()
