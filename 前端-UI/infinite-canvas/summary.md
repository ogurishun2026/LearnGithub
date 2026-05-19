# infinite-canvas 研究总结

> 仓库地址：https://github.com/basketikun/infinite-canvas
> 研究日期：2026-05-19

## 一、仓库概述

**无限画布 (infinite-canvas)** 是一款面向 AI 图片创作的开源工作台，把无限画布编排、AI 图片生成、参考图编辑、对话助手、提示词库和素材管理集成在同一个界面里，适合用来探索视觉方案并连续迭代图片结果。

| 基础信息 | 值 |
|---------|-----|
| Stars | 134 |
| 主要语言 | TypeScript (前端) + Go (后端) |
| License | GNU Affero GPL v3.0 |
| 部署方式 | Docker |

## 二、核心功能

### 2.1 无限画布

- **画布操作**：拖拽、滚轮缩放、缩放滑杆、重置视图、小地图定位
- **背景模式**：点阵、网格线、空白三种背景
- **主题**：浅色/深色主题切换
- **选择**：框选、多选、全选、取消选择
- **编辑**：复制粘贴节点和连线、撤销重做（节点/连线/视口/背景/助手会话）
- **连线**：节点连线，高亮上下游关系
- **快捷键**：覆盖缩放、框选、复制粘贴、撤销重做、删除等

### 2.2 三类节点

| 节点类型 | 功能 |
|---------|------|
| **图片节点** | 展示上传图片、生成图片或素材库图片 |
| **文本节点** | 保存提示词、说明文案、AI 文字回答 |
| **生成配置节点** | 汇总上游文本/图片，统一配置模型、比例、数量后批量生成 |

节点通用能力：拖拽移动、四角缩放、等比/自由比例切换、查看信息/JSON、删除复制粘贴、建立上下游连接。

### 2.3 AI 生成

通过前端直连 OpenAI 兼容接口：
- `/v1/images/generations` — 文生图
- `/v1/images/edits` — 图生图/参考图编辑
- `/v1/chat/completions` — 文本问答和带图问答
- `/v1/models` — 读取模型列表

**可配置项：** Base URL、API Key、默认模型、图片质量、图片比例、生成数量。

### 2.4 画布助手

- 文本问答、生图
- 读取当前选中节点及上游节点作为引用
- 粘贴图片插入画布
- 历史会话管理（删除、重试）
- 将生成的文本/图片插入画布

### 2.5 提示词库

**前台：** 搜索、标签筛选、来源筛选、详情查看、复制、加入素材库

**后台管理：** 查询、新增/编辑/删除提示词、分组标签管理、远程提示词源同步

当前内置源包括多个 GPT Image / GPT-4o / Nano Banana Pro 相关提示词仓库。

### 2.6 素材管理

**"我的素材"（浏览器本地）：** 新增文本/图片素材、编辑元数据、搜索筛选、分页浏览、下载、从多来源加入素材、在画布中插入

**"素材库"（服务器端）：** 搜索筛选、查看详情、复制链接/文本、加入我的素材、在画布中插入

## 三、技术架构

### 3.1 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Next.js、React、TypeScript、Tailwind CSS、Ant Design、Zustand、TanStack Query |
| 后端 | Go、Gin、GORM |
| 数据库 | SQLite、MySQL、PostgreSQL |
| 部署 | Docker |

### 3.2 目录结构

```
infinite-canvas/
├── web/                      # Next.js 前端
│   ├── src/
│   │   ├── app/             # Next.js App Router
│   │   ├── components/      # React 组件
│   │   ├── stores/          # Zustand 状态管理
│   │   ├── services/        # API 服务
│   │   └── types/           # TypeScript 类型
│   └── public/              # 静态资源
├── service/                  # Go 后端业务逻辑
│   ├── assets.go            # 素材服务
│   ├── auth.go              # 认证服务
│   ├── context.go           # 上下文管理
│   ├── prompt_fetch.go      # 远程提示词抓取
│   └── prompts.go           # 提示词服务
├── handler/                  # Go HTTP 处理器
├── middleware/               # Go 中间件
├── model/                    # Go 数据模型
├── repository/               # Go 数据访问层
├── router/                   # Go 路由
├── config/                   # 配置文件
├── docs/                     # 项目文档
├── main.go                   # Go 入口
└── docker-compose.yml        # Docker 部署配置
```

### 3.3 架构特点

- **Go + Next.js 分离部署**：Go 提供 API 服务，非 `/api/*` 请求转发到内部 Next.js
- **浏览器本地存储**：画布项目和"我的素材"保存在浏览器 localStorage
- **JWT 会话认证**：支持用户认证，API Key 保存在浏览器本地
- **GORM 自动迁移**：数据库 schema 自动管理，支持多数据库

## 四、部署方式

### 4.1 Docker 一键部署

```bash
git clone git@github.com:basketikun/infinite-canvas.git
cd infinite-canvas
cp .env.example .env
# 修改默认账号密码等信息
docker-compose up -d
```

访问 `http://localhost:3000`

### 4.2 本地源码构建

```bash
cp .env.example .env
docker compose -f docker-compose.local.yml up -d --build
```

### 4.3 提示词初始化

部署后可选择拉取内置提示词：`http://localhost:3000/admin/prompts`

## 五、当前限制与注意事项

- 画布项目和"我的素材"仅保存在浏览器本地，不随账号同步
- AI API Key 保存在浏览器本地，直连配置的 OpenAI 兼容接口
- 服务器素材库主要保存 URL/文本，暂无文件上传接口
- 项目处于开发阶段，不保证数据兼容性
- 暂不支持稳定版本，建议个人/本地部署
- 画布更适合桌面端，移动端体验未完善

## 六、与游戏开发的关系

虽然 infinite-canvas 定位为 AI 图片创作工具，但在游戏开发场景中也有潜在价值：

| 用途 | 说明 |
|------|------|
| **游戏美术探索** | 用 AI 快速生成角色/场景概念图，在画布上编排对比 |
| **游戏策划** | 可视化关卡布局、流程图、素材关系图 |
| **素材迭代** | 对 AI 生成的素材进行多轮"图生图" refinement |
| **提示词管理** | 内置的提示词库可沉淀游戏美术风格 |

## 七、总结

**价值定位：**
无限画布是一个将 AI 生图与可视化画布结合的创作工具，适合需要频繁迭代 AI 生成内容的场景（如游戏美术概念设计）。其核心亮点是"画布+AI 生图+提示词库"的三合一体验。

**优势：**
- 开源、可自部署
- 支持 OpenAI 兼容接口，灵活切换生图后端
- 内置提示词库，降低生图调试成本
- Docker 一键部署

**劣势：**
- 社区规模小（134 Stars），成熟度有限
- 数据本地存储，协作能力弱
- 移动端体验差

---

> 更多信息请参考：
> - [官方仓库](https://github.com/basketikun/infinite-canvas)
> - [功能介绍](docs/features.md)
> - [部署说明](docs/deployment.md)
