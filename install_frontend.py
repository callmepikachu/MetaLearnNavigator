#!/usr/bin/env python3
"""
前端依赖安装脚本
专门用于解决Windows conda环境中npm路径问题
"""

import subprocess
import sys
import os
from pathlib import Path

def install_frontend_dependencies():
    """安装前端依赖"""
    print("🎯 前端依赖安装工具")
    print("=" * 40)
    
    frontend_path = Path('frontend')
    if not frontend_path.exists():
        print("❌ frontend目录不存在")
        return False
    
    # 检查conda环境
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env:
        print(f"✅ 检测到conda环境: {conda_env}")
    else:
        print("⚠️  未检测到conda环境")
    
    # 尝试不同的npm安装方法
    methods = [
        ("conda run", lambda: subprocess.run(['conda', 'run', '-n', conda_env, 'npm', 'install'], 
                                           check=True, cwd=frontend_path)),
        ("直接npm", lambda: subprocess.run(['npm', 'install'], check=True, cwd=frontend_path)),
        ("conda run (无环境名)", lambda: subprocess.run(['conda', 'run', 'npm', 'install'], 
                                                      check=True, cwd=frontend_path)),
    ]
    
    for method_name, method_func in methods:
        print(f"\n🔄 尝试方法: {method_name}")
        try:
            method_func()
            print(f"✅ {method_name} 成功!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {method_name} 失败: {e}")
        except FileNotFoundError as e:
            print(f"❌ {method_name} 命令未找到: {e}")
        except Exception as e:
            print(f"❌ {method_name} 异常: {e}")
    
    print("\n❌ 所有自动安装方法都失败了")
    print("\n💡 手动安装方法:")
    print("1. 打开新的命令提示符或PowerShell")
    print("2. 激活conda环境:")
    print(f"   conda activate {conda_env if conda_env else 'metalearn-navigator'}")
    print("3. 进入frontend目录:")
    print("   cd frontend")
    print("4. 安装依赖:")
    print("   npm install")
    print("5. 返回项目根目录:")
    print("   cd ..")
    print("6. 启动项目:")
    print("   python start_dev.py")
    
    return False

def check_npm_availability():
    """检查npm是否可用"""
    print("\n🔍 检查npm可用性...")
    
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    
    # 检查不同方式的npm
    commands = [
        ("直接npm", ['npm', '--version']),
        ("conda run npm", ['conda', 'run', '-n', conda_env, 'npm', '--version'] if conda_env else None),
        ("node版本", ['node', '--version']),
        ("conda run node", ['conda', 'run', '-n', conda_env, 'node', '--version'] if conda_env else None),
    ]
    
    for name, cmd in commands:
        if cmd is None:
            continue
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ {name}: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ {name}: 不可用")

def main():
    """主函数"""
    check_npm_availability()
    
    if install_frontend_dependencies():
        print("\n🎉 前端依赖安装成功!")
        print("现在可以运行: python start_dev.py")
    else:
        print("\n😔 自动安装失败，请按照上面的手动安装步骤操作")

if __name__ == "__main__":
    main()
