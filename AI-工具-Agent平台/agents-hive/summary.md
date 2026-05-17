# agents-hive 研究总结

> 仓库地址：https://github.com/chef-guo/agents-hive
> 研究日期：2026-05-15

## 一、仓库概述

agents-hive 是一个**基于 ReAct Agent 的多模态、多通道、企业级 Agent 编排和运行平台**。用一句话概括：**agents-hive = Agent Runtime + Agent Harness + Quality Control Plane + Ops Workbench**。

它不是单纯的模型调用工具，而是一套完整的 Agent 基础设施——解决"Agent 为什么失控"、"权限怎么管"、"失败怎么回滚"、"多路 IM 怎么统一"、"执行过程怎么追溯"这些生产级问题。

### 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Go 1.25+ |
| 前端 | React 19 + TypeScript 5.9 + Vite + Tailwind CSS |
| 数据库 | PostgreSQL 16（pgvector 扩展） |
| 容器化 | Docker Compose |
| AI SDK | OpenAI Go SDK（openai-go） |
| IM 集成 | 飞书 SDK + 企业微信 + 微信 wechatbot + 钉钉 |

---

## 二、核心能力

### 1. Agent Runtime（运行时）

- **ReAct 循环**：标准的 Thought→Action→Observation 循环，支持流式执行
- **Master Agent**：核心调度器，管理会话生命周期、工具调用、权限控制
- **Plan Runtime**：支持计划执行模式，可暂停/恢复/续接
- **Spec-Driven 模式**：规格驱动的 Agent 认知架构（feature flag 控制，默认 legacy）
- **HITL（Human-in-the-Loop）**：人在环路的审批机制，危险操作需人工确认
- **Session-scoped Todos**：会话级别的任务追踪

### 2. 多通道统一

所有通道共享同一套会话、权限、工具调用和执行轨迹：

| 通道 | 实现 |
|------|------|
| Web UI | React Chat 界面 |
| CLI | `./claw` 命令行工具 |
| HTTP API | RESTful + WebSocket |
| 飞书 | Lark SDK 集成 |
| 企业微信 | WeCom SDK 集成 |
| 微信 | wechatbot 全局控制 |
| 钉钉 | DingTalk 集成 |

### 3. 工具体系

| 工具类型 | 说明 |
|----------|------|
| Shell | 沙箱环境执行命令 |
| 文件操作 | 读写、编辑、多文件编辑（multiedit）、补丁（applypatch） |
| Web | WebFetch、WebSearch |
| LSP | 语言服务协议集成（代码补全/跳转） |
| Skill | 技能按需加载、搜索、安装 |
| IM API | 飞书/企微/钉钉消息发送 |
| Memory | 记忆注入、提取、搜索 |
| Task | 任务委派、并行调度 |
| TTS / 图片生成 / 视频生成 | 多模态输出 |
| 自定义工具 | 通过 CUSTOM_TOOLS_DIR 加载 |
| MCP Host | 完整的 MCP 协议支持（stdio/SSE/HTTP transport） |

### 4. 质量控制平面

这是 Hive 最独特的部分——一套完整的 Agent 质量工程体系：

| 能力 | 说明 |
|------|------|
| **Session Replay** | 回放 Agent 的每一步执行过程 |
| **Journal** | 结构化的执行日志 |
| **Trajectory** | 会话轨迹追踪，可视化每步决策 |
| **Eval Runner** | 评估运行器，自动评估 Agent 输出质量 |
| **Gate Runner** | 门控运行器，决定是否放行某次输出 |
| **Diff Eval** | 对比评估，量化 Prompt 变更的影响 |
| **Long Run Runner** | 长时间运行稳定性测试 |
| **Optimization** | Prompt/模型优化，自动建议改进 |
| **Rollback** | 不满意可回滚到之前的 Prompt 版本 |
| **Approval Workflow** | 变更审批流程，优化建议需人工批准 |

### 5. Memory 系统

基于 PostgreSQL + pgvector 的混合记忆系统：

| 能力 | 说明 |
|------|------|
| 持久化存储 | PostgreSQL 存储所有记忆 |
| 向量检索 | pgvector 支持语义搜索 |
| Embedding | 自动生成和索引 embedding |
| 冲突治理 | 记忆冲突检测和解决 |
| 注入/提取 | 智能注入上下文、提取关键信息 |
| 范围控制 | 按会话/用户/全局范围管理记忆 |
| 导入/导出 | 记忆数据的批量导入导出 |
| 夜间评估 | 定时运行记忆质量评估 |
| Backlog | 未索引记忆的异步处理队列 |

### 6. SubAgent / ACP 协议

| 能力 | 说明 |
|------|------|
| SubAgent | 从 Master Agent 派生子 Agent |
| ACP Server | Agent Communication Protocol 服务端 |
| ACP Client | 连接外部 ACP Agent |
| 用户 ID 继承 | 子 Agent 自动继承父 Agent 的用户身份 |
| Session 桥接 | ACP Agent 与 Hive Session 互通 |
| MCP 透传 | ACP Agent 可使用 Hive 的 MCP 工具 |

### 7. 安全体系

| 能力 | 说明 |
|------|------|
| SafeExecutor | 统一的安全执行器，原子替换策略 |
| BuiltinDangerousRules | 19 条内置危险命令规则 |
| AST 解析 | Shell 命令的 AST 级别分析 |
| LLM 分类器 | 用 LLM 判断命令是否危险 |
| 环境变量保护 | 敏感环境变量过滤 |
| 权限提示 | IM 通道的 HITL 卡点（`strings.HasPrefix(sessionID, "im-")`） |
| 模式匹配 | 正则 + glob 模式的命令匹配 |

---

## 三、技术架构

### 整体架构

```
             Web UI / CLI / HTTP API / IM Channel
                          |
                          v
                API Server / Gateway / Auth
                          |
                          v
             Master Agent <--- Scheduler / Scheduled Tasks
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
      Tool Runtime    Plan Runtime    SubAgents / ACP
      MCP Host        Todos/Resume    Remote Agents
          |
          v
  Files / Shell / LSP / Web / IM / Memory / Custom MCP

          PostgreSQL (sessions, config, prompts, skills,
                     memory, quality, trace, accounting)
```

### 后端目录结构（internal/）

| 目录 | 职责 | 文件数 |
|------|------|--------|
| `master/` | Master Agent 核心：ReAct 循环、会话管理、HITL、权限、流式 | 80+ |
| `tools/` | 工具实现：Shell、文件、Web、Skill、Memory、IM、TTS 等 | 80+ |
| `channel/` | IM 通道：飞书、企微、钉钉、微信 | 15+ |
| `mcphost/` | MCP 协议宿主：transport、schema 转换、HITL | 28 |
| `subagent/` | SubAgent 管理：注册、工厂、循环、压缩 | 20+ |
| `acpserver/` | ACP 服务端：权限、命令、流、桥接 | 18 |
| `acpclient/` | ACP 客户端 | 若干 |
| `agentquality/` | 质量工程：评估、门控、优化、回滚、审批 | 50+ |
| `memory/` | 记忆系统：存储、向量、注入、冲突治理 | 40+ |
| `specdriven/` | 规格驱动模式：intake、planner、continuation | 若干 |
| `security/` | 安全：规则、AST 解析、LLM 分类 | 16 |
| `store/` | PostgreSQL 存储层 | 若干 |
| `api/` | HTTP API 路由 | 若干 |
| `bootstrap/` | 启动初始化 | 若干 |
| `webui/` | Go embed 前端静态资源 | 若干 |
| 其他 | accounting、cache、config、i18n、journal、llm、lsp、observability、plugin、quota、resilience、router、sandbox、search、sessiontodo、trajectory... | — |

### 前端页面

| 页面 | 功能 |
|------|------|
| Chat | 会话交互：工具调用、HITL、Canvas、Todos |
| Sessions | 会话列表：归档、标签、fork、revert |
| SessionReplay | 会话回放和轨迹查看 |
| ReplayGallery | 回放画廊 |
| Settings | 运行时配置、MCP、权限、IM Channel、自定义 Agent |
| AdminSettings | LLM、Prompt、Skill、用户、Memory 管理后台 |
| Admin | 自定义优化工作台：回放、评估、优化、回滚 |
| ScheduledTasks | 定时任务管理 |
| Skills | 技能管理 |
| Dashboard | 仪表盘 |
| Guide | 使用指南 |

### 配置体系

两层配置：
1. **启动配置**：`config.json`（CLI flags / 环境变量），包含数据库、日志、服务器等
2. **运行时配置**：通过 Web UI/API 修改，存储在 PostgreSQL，包含 LLM、Prompt、Skill、Channel、权限、MCP 等

### 数据库迁移

使用 SQL 迁移文件（`migrations/`），主要覆盖飞书相关的去重、重试队列等。

---

## 四、关键设计模式

### 1. Lock 纪律

- `session.mu` 是 `sync.RWMutex`，非重入——任何持有锁时不允许再次获取
- `specCtx` 使用 `atomic.Pointer` 写入，仅 task ingress 路径可写，subagent/background 禁止写入
- `SpecState` 的 Load→Mutate→Save 必须在同一个任务入口内完成

### 2. CAS（Compare-And-Swap）

- `SpecChangeStore` 使用 `SELECT ... FOR UPDATE` + `WHERE revision = $expected` 实现乐观锁
- 冲突时返回 `ErrSpecChangeConflict`

### 3. Feature Flag 4 维控制

Spec-Driven 模式通过 4 个 feature flag 组合控制（16 种组合），`ValidateFlagCombination` 在启动时 fail-fast。

### 4. Skill 按需加载

- Public / Personal 双 scope
- 4 层 Overlay 优先级：`personal DB > personal FS > public DB > public FS`
- 未安装 skill 时自动提示安装（self-heal）

### 5. 质量工作台闭环

```
评估 → 发现问题 → 生成优化建议 → 人工审批 → 自动部署 → 不满意回滚
```

---

## 五、在游戏开发中的应用场景

### 1. 游戏内容生成 Agent

通过 IM 通道（飞书/企微）直接对话生成：
- NPC 对话脚本
- 任务描述文本
- 物品/技能描述
- 世界观设定

### 2. 游戏运维 Agent

- **定时任务**：通过 Scheduled Tasks 定时检查服务器状态、发送公告
- **IM 集成**：团队在飞书/企微中直接与 Agent 对话查数据、发公告
- **质量监控**：利用 Quality Control Plane 监控 Agent 输出质量

### 3. 代码开发助手

- **MCP 工具扩展**：接入游戏引擎相关的自定义工具
- **LSP 集成**：代码跳转和补全
- **Shell 沙箱**：安全执行构建/测试命令
- **Session Replay**：回放和审查 Agent 的代码修改过程

### 4. 知识管理

- **Memory 系统**：将游戏设计文档、GDD、技术规范注入记忆，Agent 自动检索相关上下文
- **向量搜索**：语义搜索游戏设计知识库
- **Skill 系统**：将常用的游戏开发流程封装为 Skill（如"生成角色卡"、"创建任务链"）

### 5. 多 Agent 协作

- **SubAgent**：主 Agent 派生子 Agent 分别处理不同模块（美术资源检查、代码审查、文档生成）
- **ACP 协议**：连接外部 Agent 服务
- **委派/并行调度**：将复杂任务分解并行处理

---

## 六、与同类项目对比

| 维度 | agents-hive | Dify | OpenHands |
|------|-------------|------|-----------|
| 定位 | Agent 运行平台 + 质量控制 | LLM 应用编排平台 | 软件开发 Agent |
| 语言 | Go + React | Python + React | Python + React |
| IM 集成 | 飞书/企微/微信/钉钉 | 有限 | 无 |
| 质量工程 | 完整（评估/优化/回滚） | 无 | 有限 |
| Agent 协议 | ACP + SubAgent + MCP | 自有 | 自有 |
| 规模 | 中型（~51 Stars） | 大型（100K+） | 大型（50K+） |
| 适合场景 | 企业内部 Agent 平台 | 对话应用构建 | 代码开发 |

### 核心差异化

agents-hive 的最大差异化在于：
1. **中国企业 IM 全覆盖**（飞书/企微/微信/钉钉）
2. **完整的 Agent 质量工程体系**（评估→优化→回滚→审批闭环）
3. **生产级的权限和安全体系**（SafeExecutor + AST 级 Shell 分析）
4. **Spec-Driven 认知架构**（规格驱动的 Agent 行为控制）

---

## 七、部署方式

### Docker Compose（推荐）

```bash
git clone https://github.com/chef-guo/agents-hive.git
cd agents-hive

# 配置环境变量
cat > .env <<EOF
POSTGRES_PASSWORD=your_strong_password
DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
TZ=Asia/Shanghai
HIVE_PORT=8080
EOF

# 构建 sandbox
docker build -t hive-sandbox:latest -f docker/sandbox/Dockerfile .

# 启动
docker compose up -d
```

访问 `http://localhost:8080`

### 本地开发

```bash
# 需要 Go 1.25+、Node.js 22+、PostgreSQL 16
cp config.example.json config.json
# 编辑 config.json

cd frontend && npm install && npm run build && cd ..
go build -o server ./cmd/server
./server --config config.json
```

### CLI 模式

```bash
./claw -c config.json "介绍一下当前项目结构"
./claw -c config.json -i  # 交互模式
```

---

## 八、值得关注的技术点

1. **ReAct Processor 的流式执行**：`react_processor.go` 实现了完整的流式 ReAct 循环
2. **Spec-Driven 的 Intake 决策**：`specdriven/intake/decide.go` 是唯一的 intake 决策入口
3. **质量评估的 Diff Eval**：可以量化对比两个 Prompt 版本的输出差异
4. **MCP 的 Schema 转换**：`mcphost/convert.go` 处理 MCP 工具到 Hive 内部工具的 schema 映射
5. **记忆的冲突治理**：`memory/conflict_governance.go` 检测和解决记忆冲突
6. **Feature Flag 组合验证**：4 维 flag 的 16 种组合启动时 fail-fast 校验
