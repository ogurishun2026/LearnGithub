# SkillClaw 研究报告

## 项目概述

| 项目 | 内容 |
|------|------|
| **仓库** | https://github.com/AMAP-ML/SkillClaw |
| **Star** | 1,665 ⭐ |
| **Fork** | 155 |
| **语言** | Python 3.10+ |
| **许可** | MIT |
| **论文** | arXiv:2604.08377 |
| **组织** | AMAP-ML（阿里巴巴地图出行团队） |

## 核心理念

**"Let Skills Evolve Collectively with Agentic Evolver"**

SkillClaw 让 AI Agent 的技能从每次真实交互中自动进化、去重、改进和验证。不改变用户工作流程，只需像平时一样对话，技能会在后台默默进化。

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 🚀 **快速安装** | Shell installer (macOS/Linux)，Python 手动安装 (Windows) |
| 💬 **只需对话** | 与 agent 正常交流即可，进化在后台静默进行 |
| 🔌 **广泛兼容** | Hermes、OpenClaw、Codex、Claude Code、QwenPaw、IronClaw、PicoClaw、ZeroClaw、NanoClaw、NemoClaw 等 |
| 🧬 **集体技能进化** | 跨会话、跨 agent、跨设备、跨用户，经验持续累积 |

---

## 架构设计

### 两个核心组件

1. **Client Proxy（客户端代理）**
   - 本地 API 代理（`/v1/chat/completions`、`/v1/messages`）
   - 拦截 agent 请求，记录会话数据，管理本地技能库
   - 用户安装后即可使用

2. **Evolve Server（进化服务器）** — 可选
   - 读取共享存储中的会话数据
   - 自动进化或创建技能
   - 支持两种引擎：
     - `workflow`：固定 3 阶段 LLM 管道（Summarize → Aggregate → Execute）
     - `agent`：OpenClaw 驱动的 agent 工作空间

### 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    SkillClaw Architecture              │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐ │
│  │  Hermes  │    │  OpenClaw│    │   其他 Agent      │  │
│  │  /Codex  │    │          │    │  (Claude等)       │  │
│  └────┬─────┘    └────┬─────┘    └────────┬─────────┘  │
│       │               │                   │             │
│       └───────────────┼───────────────────┘             │
│                       ▼                                 │
│             ┌────────────────┐                         │
│              │  Client Proxy│◄── 本地技能库           │
│              │  (port 30000)   │                         │
│              └───────┬────────┘                         │
│                      │                                  │
│                      ▼ │
│         ┌────────────────────────┐                      │
│         │   共享存储 (OSS/S3/本地)│                      │
│        └─────────────┬──────────┘                      │
│                       │                                  │
│                       ▼                                  │
│         ┌────────────────────────┐                      │
│         │   Evolve Server        │                       │
│         │   (技能自动进化)        │                      │
│         └────────────────────────┘                      │
└─────────────────────────────────────────────────────────┘
```

---

## 目录结构

```
SkillClaw/
├── skillclaw/              # 客户端核心代码
│   ├── __main__.py         # 入口点
│   ├── cli.py              # CLI 命令行工具
│   ├── api_server.py       # API 代理服务器
│   ├── config.py           # 配置管理
│   ├── skill_manager.py    # 技能管理器
│   ├── skill_bundle.py     # 技能包
│   ├── skill_hub.py        # 技能中心
│   ├── prm_scorer.py       # PRM 评分器
│   ├── validation_worker.py# 验证工作器
│   ├── dashboard_*        # Dashboard 相关
│   ├── protocols/         # 协议适配器
│   │   ├── anthropic_messages.py
│   │   ├── openai_responses.py
│   │   └── common.py
│   └── dashboard_assets/  # Dashboard 静态资源
│
├── evolve_server/          # 进化服务器
│   ├── __main__.py         # 服务入口
│   ├── core/               # 核心逻辑
│   ├── engines/            # 进化引擎
│   │   ├── workflow.py     # 工作流引擎
│   │   ├── agent.py        # Agent 引擎
│   │   └── openclaw_runner.py
│   ├── pipeline/           # 处理管道
│   │   ├── summarizer.py   # 摘要生成
│   │   ├── aggregation.py  # 聚合
│   │   ├── execution.py    # 执行
│   │   ├── session_judge.py# 会话判断
│   │   └── skill_verifier.py# 技能验证
│   └── storage/            # 存储层
│
├── scripts/                # 安装脚本
│   ├── install_skillclaw.sh
│   └── install_skillclaw_server.sh
│
└── tests/                  # 测试
```

---

## 支持的 Agent 框架

| Agent | 说明 |
|-------|------|
| [Hermes](https://github.com/NousResearch/hermes-agent) | NousResearch 的 Agent |
| [OpenClaw](https://github.com/openclaw/openclaw) | 开放 claw 框架 |
| [Codex](https://github.com/openai/codex) | OpenAI Codex |
| Claude Code | Anthropic 的 Claude Code |
| [QwenPaw](https://github.com/agentscope-ai/QwenPaw) | 阿里 Qwen Agent |
| [IronClaw](https://github.com/nearai/ironclaw) | Near AI 的 IronClaw |
| [PicoClaw](https://github.com/sipeed/picoclaw) | Sipeed 的 PicoClaw |
| [ZeroClaw](https://github.com/zeroclaw-labs/zeroclaw) | ZeroClaw Labs |
| [NanoClaw](https://github.com/qwibitai/NanoClaw) | Nano 版本的 Claw |
| [NemoClaw](https://github.com/NVIDIA/NemoClaw) | NVIDIA Nemo 版本 |

---

## 快速开始

### 安装（macOS/Linux）

```bash
git clone https://github.com/AMAP-ML/SkillClaw.git && cd SkillClaw
bash scripts/install_skillclaw.sh
source .venv/bin/activate
skillclaw setup              # 配置向导
skillclaw start --daemon     # 启动守护进程
skillclaw status             # 检查状态
```

### 快速验证

```bash
PROXY_PORT="$(skillclaw config proxy.port | awk '{print $2}')"
curl "http://127.0.0.1:${PROXY_PORT}/healthz"
# 应返回 {"ok": true}
```

---

## 核心功能命令

| 命令 | 说明 |
|------|------|
| `skillclaw setup` | 配置向导 |
| `skillclaw start --daemon` | 启动客户端代理 |
| `skillclaw status` | 查看状态 |
| `skillclaw config show` | 显示配置 |
| `skillclaw skills pull` | 下载共享技能 |
| `skillclaw skills push` | 上传本地技能 |
| `skillclaw skills sync` | 双向同步 |
| `skillclaw skills list-remote` | 浏览共享技能 |
| `skillclaw doctor hermes` | Hermes 诊断 |
| `skillclaw dashboard sync` | 同步 Dashboard 数据 |
| `skillclaw dashboard serve` | 启动 Dashboard 服务器 |

---

## 进化管道（3 阶段）

```
会话数据 → Summarizer（摘要） → Aggregation（聚合） → Execution（执行） → SKILL.md
```

1. **Summarizer**：从会话中提取关键信息
2. **Aggregation**：聚合多个会话中的相似技能
3. **Execution**：执行技能生成/改进

---

## 部署模式

| 模式 | 说明 |
|------|------|
| **单人本地** | 客户端 + 本地进化服务器 |
| **单人云端** | 客户端 + OSS/S3 共享存储 + 远程进化服务器 |
| **团队共享** | 多个客户端 + 共享存储 + 统一进化服务器 |

---

## 技术栈

- **核心框架**：Click (CLI)、FastAPI + Uvicorn (API 服务器)
- **存储**：Alibaba Cloud OSS、AWS S3、本地文件系统
- **可选依赖**：
  - `embedding`：numpy、sentence-transformers（基于向量的技能检索）
  - `evolve`：openai（技能进化）
  - `sharing`：boto3、oss2（云端技能共享）

---

## 相关项目

| 项目 | 说明 |
|------|------|
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | 与 agent 对话即可学习进化的基础项目 |
| [WildClawBench](https://github.com/InternLM/WildClawBench) | AI Agent 端到端工作能力评估基准 |
| [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) | 通过对话训练个性化 Agent |

---

## 总结

**SkillClaw** 是一个**技能自动进化框架**，让多个 AI Agent 能够：
1. 从真实交互中自动提取和进化技能
2. 跨 agent、跨设备、跨用户共享和累积经验
3. 自动去重、改进和验证技能质量

**核心价值**：不改变用户工作流程，只需正常与 Agent 对话，技能就会在后台自动进化和优化。类似于 AI Agent 的"集体学习"系统。

---

## 研究日期

2026-06-08