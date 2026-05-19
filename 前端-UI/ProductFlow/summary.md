# ProductFlow 研究总结

> 仓库地址：https://github.com/yuqie6/ProductFlow
> 研究日期：2026-05-19

## 一、仓库概述

**ProductFlow** 是面向单人或小团队商家的开源自托管商品素材工作台，核心链路覆盖商品资料、参考图、AI 文案、AI/模板海报、连续生图会话、生成图画廊和可视化工作流。

| 基础信息 | 值 |
|---------|-----|
| Stars | 152 |
| 主要语言 | Python (后端) + TypeScript (前端) |
| License | MIT |
| 部署方式 | Docker Compose |

## 二、核心功能

### 2.1 商品/工作台

- 单管理员访问密钥登录
- 商品列表分页浏览、创建商品、商品详情工作台
- 节点画布组织商品资料、参考图、文案节点和生图节点
- 桌面端：滚轮缩放、拖拽平移、节点拖拽定位、节点连线、Ctrl/Cmd/Shift 多选、Shift 框选
- 移动端：单指平移、点选节点、双指缩放、触控拖拽节点
- 完整画布模板创建商品，内置节点组模板

### 2.2 文/图生图

- 独立图片会话支持参考图上传、历史基图选择、连续生成
- 移动端主视图/抽屉/底部面板布局
- 会话列表从左侧抽屉打开，分支/候选历史从右侧窄抽屉打开
- 生成状态：排队位置、进度、失败原因、取消、重试
- 生成图可下载、投至画廊、保存为商品参考图

### 2.3 画廊

- `/gallery` 集中保存文/图生图结果
- 条目保留来源会话、关联商品、提示词、尺寸、模型信息

### 2.4 配置

- `/settings` 支持运行时业务配置：provider、模型、图片尺寸、图片工具参数、提示词模板、上传限制、全局并发
- Secret 字段不回显，配置页由独立令牌二次解锁
- 文案、海报、商品工作流由 Dramatiq + Redis 异步处理

## 三、技术架构

### 3.1 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.12、FastAPI、SQLAlchemy、Alembic、Dramatiq、Redis、PostgreSQL |
| 前端 | React 19、Vite、TypeScript、React Router、TanStack Query、Tailwind CSS 4 |
| 部署 | Docker Compose |

### 3.2 目录结构

```
ProductFlow/
├── backend/              # Python FastAPI 后端
│   ├── src/productflow_backend/
│   │   ├── main.py       # API 入口
│   │   └── workers.py    # Dramatiq worker
│   └── tests/
├── web/                  # React 前端
│   └── src/
├── docs/                 # PRD、用户指南、架构文档
├── .trellis/            # AI 协作工作流规范
├── .codex/              # Codex CLI 配置
├── docker-compose.yml   # Docker 部署配置
└── justfile             # 本地开发入口
```

### 3.3 部署架构

```
Docker Compose 启动:
├── productflow-postgres  (PostgreSQL, 端口 15432)
├── productflow-redis     (Redis, 端口 16379)
├── productflow-backend   (FastAPI API, 端口 29280)
├── productflow-worker    (Dramatiq worker)
└── productflow-web       (nginx 静态服务, 端口 29281)
```

### 3.4 AI 协作资产

本仓库还保留了一套面向 AI 协作的项目工作流资产：
- **Trellis** — 任务工作流、规范沉淀和上下文注入约定
- **OpenAI Codex** — AI coding agent 参与项目开发协作

## 四、快速开始

### Docker 一键部署

```bash
git clone git@github.com:yuqie6/ProductFlow.git
cd ProductFlow
cp .env.example .env
# 修改 ADMIN_ACCESS_KEY, SESSION_SECRET, POSTGRES_PASSWORD
docker compose up -d --build
# 访问 http://127.0.0.1:29281
```

### 本地开发

```bash
cp .env.example .env
cp .env.dev.example .env.dev
cp web/.env.example web/.env

# 仅启动数据库依赖
docker compose up -d productflow-postgres productflow-redis

# 安装依赖
just backend-install && just web-install && just backend-migrate

# 启动服务
just backend-run    # API: http://localhost:29282
just backend-worker # Dramatiq worker
just web-dev        # Web: http://localhost:29283
```

## 五、模型配置

- **文案供应商**：支持 `mock` 和 `openai`
- **图片供应商**：支持 `mock`、`openai_responses`(Responses API)、`openai_images`(Images API)
- `openai_responses` 使用 OpenAI Responses `image_generation` 工具，支持参考图输入
- 海报模式：`POSTER_GENERATION_MODE=template`（本地模板）或 `generated`（AI 生成）

## 六、与游戏开发的关系

ProductFlow 的商品工作台和画布编排思路可用于游戏开发中的：

| 用途 | 说明 |
|------|------|
| **游戏商品化素材管理** | 游戏内的道具/角色可以作为"商品"管理 |
| **美术资源流水线** | 参考图 → AI 生图 → 素材库的工作流可复用于游戏美术资源生产 |
| **提示词库** | 内置提示词库可沉淀游戏美术风格 |

## 七、总结

**价值定位：**
ProductFlow 是一个面向电商/商品场景的 AI 素材工作台，特色是将画布编排与 AI 生图、素材库结合。其架构规范完整，AI 协作资产（Trellis + Codex）是亮点。

**优势：**
- Docker Compose 一键部署，自托管友好
- 画布节点编排灵活，支持连续生图会话
- AI 协作工作流规范完整（Trellis/Codex）
- 支持 PostgreSQL/MySQL/Redis 多种数据库

**劣势：**
- Stars 较少（152），社区规模小
- 功能偏向电商场景，不完全适合游戏开发
- 单管理员模式，不支持多用户协作

---

> 更多信息请参考：
> - [官方仓库](https://github.com/yuqie6/ProductFlow)
> - [用户指南](docs/USER_GUIDE.md)
> - [架构说明](docs/ARCHITECTURE.md)