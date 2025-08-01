#!/usr/bin/env python3
"""
开发环境启动脚本
同时启动后端API服务器和前端开发服务器
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def check_conda_env():
    """检查是否在conda环境中"""
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env:
        print(f"✅ 当前conda环境: {conda_env}")
        return True
    else:
        print("⚠️  未检测到conda环境")
        return False

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    print(f"✅ Python版本: {sys.version}")

def check_node_version():
    """检查Node.js版本"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js版本: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js未安装")
            return False
    except FileNotFoundError:
        print("❌ Node.js未安装")
        return False

def install_python_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, cwd='.')
        print("✅ Python依赖安装完成")
    except subprocess.CalledProcessError:
        print("❌ Python依赖安装失败")
        sys.exit(1)

def install_node_dependencies():
    """安装Node.js依赖"""
    print("📦 安装Node.js依赖...")
    frontend_path = Path('frontend')
    if not frontend_path.exists():
        print("❌ frontend目录不存在")
        return False

    # 检查是否在conda环境中
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')

    try:
        if conda_env:
            # 在conda环境中使用conda run来确保正确的环境
            print(f"🔄 在conda环境 {conda_env} 中安装npm依赖...")
            subprocess.run(['conda', 'run', '-n', conda_env, 'npm', 'install'],
                          check=True, cwd=frontend_path)
        else:
            # 直接使用npm
            subprocess.run(['npm', 'install'], check=True, cwd=frontend_path)

        print("✅ Node.js依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Node.js依赖安装失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ npm命令未找到，请确保Node.js已正确安装")
        print("💡 尝试手动安装:")
        print(f"   cd {frontend_path}")
        print("   npm install")
        return False

def setup_environment():
    """设置环境变量"""
    env_file = Path('backend/.env')
    env_example = Path('backend/.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 创建环境配置文件...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ 已创建 backend/.env 文件，请根据需要修改配置")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    backend_path = Path('backend')
    
    # 设置环境变量
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_path.absolute())
    
    return subprocess.Popen(
        [sys.executable, '-m', 'uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
        cwd=backend_path,
        env=env
    )

def start_frontend():
    """启动前端服务"""
    print("🚀 启动前端服务...")
    frontend_path = Path('frontend')

    if not frontend_path.exists():
        print("❌ frontend目录不存在，跳过前端启动")
        return None

    # 检查是否在conda环境中
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')

    try:
        if conda_env:
            # 在conda环境中使用conda run
            return subprocess.Popen(['conda', 'run', '-n', conda_env, 'npm', 'start'],
                                  cwd=frontend_path)
        else:
            return subprocess.Popen(['npm', 'start'], cwd=frontend_path)
    except FileNotFoundError:
        print("❌ npm命令未找到，无法启动前端服务")
        print("💡 请手动启动前端:")
        print(f"   cd {frontend_path}")
        print("   npm start")
        return None

def main():
    """主函数"""
    print("🎯 MetaLearnNavigator 开发环境启动器")
    print("=" * 50)

    # 检查环境
    is_conda = check_conda_env()
    check_python_version()
    has_node = check_node_version()

    # 如果不在conda环境中，提示用户
    if not is_conda:
        print("\n💡 建议使用conda环境:")
        print("   python setup_conda_env.py  # 创建conda环境")
        print("   conda activate metalearn-navigator")
        print("   python start_dev.py")
        print("\n继续使用当前环境? (y/N): ", end="")
        response = input()
        if response.lower() != 'y':
            print("👋 请设置conda环境后再运行")
            sys.exit(0)
    
    # 安装依赖
    install_python_dependencies()
    if has_node:
        install_node_dependencies()
    
    # 设置环境
    setup_environment()
    
    # 启动服务
    backend_process = None
    frontend_process = None
    
    try:
        backend_process = start_backend()
        time.sleep(3)  # 等待后端启动
        
        if has_node:
            frontend_process = start_frontend()
        
        print("\n" + "=" * 50)
        print("🎉 服务启动完成!")
        print("📍 后端API: http://localhost:8000")
        print("📍 API文档: http://localhost:8000/docs")
        if has_node:
            print("📍 前端应用: http://localhost:3000")
        print("=" * 50)
        print("按 Ctrl+C 停止所有服务")
        
        # 等待用户中断
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
            print("✅ 后端服务已停止")
        
        if frontend_process:
            frontend_process.terminate()
            frontend_process.wait()
            print("✅ 前端服务已停止")
        
        print("👋 再见!")

if __name__ == '__main__':
    main()
