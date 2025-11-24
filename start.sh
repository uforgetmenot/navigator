#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[INFO] 正在检查环境...${NC}"

# 检查是否需要创建虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[INFO] 未检测到虚拟环境，正在创建...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "创建虚拟环境失败，请检查 Python 是否安装。"
        exit 1
    fi
    echo -e "${GREEN}[SUCCESS] 虚拟环境创建成功。${NC}"
    
    echo -e "${BLUE}[INFO] 正在安装依赖...${NC}"
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install fastapi uvicorn sqlmodel jinja2 python-dotenv requests pydantic-settings
    if [ $? -ne 0 ]; then
        echo "依赖安装失败。"
        exit 1
    fi
    echo -e "${GREEN}[SUCCESS] 依赖安装完成。${NC}"
fi

# 检查数据库是否存在，不存在则初始化
if [ ! -f "navigator.db" ]; then
    echo -e "${BLUE}[INFO] 正在初始化数据库并填充默认数据...${NC}"
    export PYTHONPATH=$PYTHONPATH:.
    ./venv/bin/python app/services/seed.py
    echo -e "${GREEN}[SUCCESS] 数据库初始化完成。${NC}"
fi

echo -e "${BLUE}[INFO] 正在启动服务器...${NC}"
echo -e "${GREEN}[SUCCESS] 服务已启动! 请访问: http://localhost:8000${NC}"

# 启动 FastAPI 服务
./venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
