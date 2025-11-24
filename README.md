# 个人导航网站

这是一个基于 **FastAPI** 和 **SQLModel** 构建的现代个人导航网站系统。它提供了一个干净、响应式的界面来管理和访问常用的工具、资源和链接。

## ✨ 功能特性

*   **分类管理**: 左侧侧边栏支持多级分类（AI、运营、本地服务等）。
*   **卡片式导航**: 清晰的网格布局展示导航卡片，包含图标、标题、描述和链接。
*   **搜索功能**: 集成 Google 搜索，支持快速检索。
*   **响应式设计**: 基于 Tailwind CSS，适配各种屏幕尺寸。
*   **状态监控**: 实时显示 API 系统运行状态。
*   **数据驱动**: 所有数据存储在 SQLite 数据库中，易于备份和迁移。

## 🛠️ 技术栈

*   **后端**: Python 3.10+, FastAPI, SQLModel (SQLAlchemy wrapper)
*   **数据库**: SQLite3
*   **前端**: HTML5, Jinja2 Templates, Tailwind CSS (CDN), Material Symbols
*   **依赖管理**: pip / venv

## 🚀 快速开始

### 1. 环境准备

确保你的系统中安装了 Python 3.10 或更高版本。

### 2. 安装与运行

你可以使用提供的启动脚本一键运行：

```bash
# 给予脚本执行权限 (首次运行)
chmod +x start.sh

# 启动服务
./start.sh
```

或者手动运行：

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install fastapi uvicorn sqlmodel jinja2 python-dotenv requests pydantic-settings

# 4. 初始化数据库并填充数据 (首次运行)
export PYTHONPATH=$PYTHONPATH:.
python app/services/seed.py

# 5. 启动服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2.1 Docker 部署

项目内已提供 `Dockerfile` 和 `docker-compose.yml`，可以通过容器方式快速启动：

```bash
# 首次构建镜像并启动服务
docker compose up --build

# 后续再次启动
docker compose up
```

默认会暴露 `8000` 端口到宿主机，并将 SQLite 数据库存储在名为 `navigator_data` 的卷中（挂载到容器 `/app/data`）。

> 提示：如果需要自定义环境变量（例如 `SECRET_KEY` 或 `DATABASE_URL`），可以在项目根目录创建 `.env` 文件，或者直接在 `docker-compose.yml` 中的 `environment` 块覆盖。

### 3. 访问应用

启动成功后，打开浏览器访问：

*   **主页**: [http://localhost:8000](http://localhost:8000)
*   **API 文档 (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **API 文档 (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📁 项目结构

```
navigator/
├── app/
│   ├── main.py              # 应用入口
│   ├── database.py          # 数据库连接
│   ├── models/              # 数据模型 (Category, Card, Config)
│   ├── routers/             # API 路由接口
│   ├── services/            # 业务逻辑与数据种子脚本
│   └── templates/           # 前端 HTML 模板
├── static/                  # 静态资源
├── docs/                    # 文档与原型
├── navigator.db             # SQLite 数据库 (自动生成)
├── .env                     # 环境变量配置
├── start.sh                 # 启动脚本
└── README.md                # 项目说明文档
```

## ⚙️ 配置

项目根目录下的 `.env` 文件包含了应用的配置信息：

```env
APP_NAME=个人导航网站
DEBUG=true
DATABASE_URL=sqlite:///./navigator.db
```

## 🛡️ 许可证

MIT License
