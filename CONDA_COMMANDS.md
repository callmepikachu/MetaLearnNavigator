# Conda环境管理命令参考

## 快速开始

### Windows用户（推荐）
```cmd
# 运行Windows批处理脚本
setup_windows.bat

# 激活环境
conda activate metalearn-navigator

# 启动项目
python start_dev.py
```

### 其他系统
```bash
# 运行自动设置脚本
python setup_conda_env.py

# 激活环境
conda activate metalearn-navigator

# 启动项目
python start_dev.py
```

## 手动Conda命令

### 创建环境

#### 方法1：使用environment.yml文件
```bash
# 从配置文件创建环境
conda env create -f environment.yml

# 激活环境
conda activate metalearn-navigator
```

#### 方法2：手动创建
```bash
# 创建新环境并安装基础包（注意：Windows上不包含npm）
conda create -n metalearn-navigator python=3.9 nodejs=18 -y

# 激活环境
conda activate metalearn-navigator

# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖（npm会随nodejs自动安装）
cd frontend
npm install
cd ..
```

### 环境管理

```bash
# 查看所有环境
conda env list

# 激活环境
conda activate metalearn-navigator

# 停用环境
conda deactivate

# 删除环境
conda env remove -n metalearn-navigator

# 导出环境配置
conda env export > environment.yml

# 更新环境
conda env update -f environment.yml
```

### 包管理

```bash
# 在环境中安装包
conda activate metalearn-navigator
conda install package_name

# 使用pip安装包
conda activate metalearn-navigator
pip install package_name

# 查看已安装的包
conda list

# 搜索包
conda search package_name
```

### 项目开发命令

```bash
# 激活环境
conda activate metalearn-navigator

# 启动开发服务器
python start_dev.py

# 或者分别启动
# 后端
cd backend
uvicorn main:app --reload

# 前端（新终端）
conda activate metalearn-navigator
cd frontend
npm start

# 测试后端
python test_backend.py
```

## 常见问题

### Q: 如何在不同操作系统上使用？

**Windows:**
```cmd
# 使用Anaconda Prompt或PowerShell
conda activate metalearn-navigator
python start_dev.py
```

**macOS/Linux:**
```bash
# 使用Terminal
conda activate metalearn-navigator
python start_dev.py
```

### Q: 如何更新依赖？

```bash
# 激活环境
conda activate metalearn-navigator

# 更新Python包
pip install -r requirements.txt --upgrade

# 更新前端包
cd frontend
npm update
```

### Q: 如何重置环境？

```bash
# 删除现有环境
conda env remove -n metalearn-navigator

# 重新创建
python setup_conda_env.py
```

### Q: 如何在IDE中使用conda环境？

**VS Code:**
1. 安装Python扩展
2. Ctrl+Shift+P -> "Python: Select Interpreter"
3. 选择conda环境中的Python解释器

**PyCharm:**
1. File -> Settings -> Project -> Python Interpreter
2. Add -> Conda Environment -> Existing environment
3. 选择conda环境路径

## 环境信息

- **环境名称**: metalearn-navigator
- **Python版本**: 3.9
- **Node.js版本**: 18
- **主要依赖**: FastAPI, React, SQLAlchemy, Material-UI

## 故障排除

### 环境创建失败
```bash
# 清理conda缓存
conda clean --all

# 更新conda
conda update conda

# 重新创建环境
python setup_conda_env.py
```

### 包安装失败
```bash
# 使用conda-forge频道
conda install -c conda-forge package_name

# 或使用pip
pip install package_name
```

### 端口占用问题
```bash
# 查看端口占用
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# 杀死占用进程
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # macOS/Linux
```
