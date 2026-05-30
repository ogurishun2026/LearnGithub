# EverOS 研究总结

> 仓库地址：https://github.com/EverMind-AI/EverOS
> 研究日期：2026-05-30

## 一、仓库概述

EverOS 是一个**自进化 Agent 长期记忆系统**，为 AI Agent 提供构建、评估和集成长期记忆的统一基础设施。核心产品是 EverCore——一个受生物印迹启发的自组织记忆操作系统，可以让 Agent 记住、理解并持续进化。仓库目前拥有 **6K+ Stars**，是一个活跃的 AI 记忆基础设施项目。

## 二、核心内容

### 2.1 三大组成部分

| 模块 | 定位 | 说明 |
|------|------|------|
| **Use Cases** | 应用演示 | 展示记忆如何改变真实 Agent 工作流的示例 |
| **Architecture Methods** | 架构方法 | 可运行、扩展或对比的记忆系统和算法 |
| **Benchmarks** | 评估基准 | 记忆质量和 Agent 自进化评估的开放基准 |

### 2.2 核心架构：EverCore

**EverCore** 是 EverOS 的核心——一个自组织的记忆操作系统，受生物印迹（biological imprinting）启发。

**关键特性**：
- 从对话中提取、结构化并检索长期知识
- 支持多租户（multi-tenant），数据必须按租户隔离
- 全异步 I/O
- 提供 REST API（`/api/v1/memories`）
- 本地运行依赖 Docker + Python 3.12
- 服务端口：`http://localhost:1995`

**快速启动**：
```bash
cd methods/EverCore
docker compose up -d          # 启动基础设施
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
cp env.template .env          # 配置 API Keys
uv run python src/run.py      # 启动服务
curl http://localhost:1995/health  # 验证
```

**基础用法**：
```python
import os, requests
API_BASE = os.getenv("EVERCORE_API_BASE", "http://localhost:1995/api/v1")

# 存储记忆
add_payload = {
    "user_id": "user_001",
    "session_id": "quickstart_session",
    "messages": [{"message_id": "msg_001", "sender_id": "user_001", 
                  "sender_name": "User", "role": "user",
                  "timestamp": 1738404000000, 
                  "content": "I love playing soccer on weekends"}]
}
requests.post(f"{API_BASE}/memories", json=add_payload)

# 搜索记忆
search_payload = {
    "query": "What sports does the user like?",
    "method": "hybrid",
    "memory_types": ["episodic_memory"],
    "top_k": 5,
    "filters": {"user_id": "user_001"}
}
requests.post(f"{API_BASE}/memories/search", json=search_payload)
```

### 2.3 第二个架构：HyperMem

**HyperMem** 是一个基于超图（hypergraph）的层次记忆架构，通过超边（hyperedges）捕获高阶关联，包含 topic/event/fact 三层，用于从粗到细的对话检索。

### 2.4 评估基准

| 基准 | 用途 | 数据集 |
|------|------|--------|
| **EverMemBench** | 记忆质量三层评估：事实召回、应用推理、个性化泛化 | HuggingFace |
| **EvoAgentBench** | Agent 自进化评估：纵向生长曲线、迁移效率、错误规避、技能命中率 | HuggingFace |

支持的基准测试：
- **LoCoMo** — 长上下文记忆基准，支持单跳/多跳推理
- **LongMemEval** — 多会话对话评估
- **PersonaMem** — 基于人格的记忆评估

**运行评估**：
```bash
cd methods/EverCore
uv sync --group evaluation
uv run python -m evaluation.cli --dataset locomo --system everos --smoke
```

### 2.5 基准性能

| 方法 | LoCoMo | LongMemEval |
|------|--------|-------------|
| EverCore | 93.05% | 83.00% |
| HyperMem | 92.73% | - |

## 三、技术架构

### 3.1 目录结构

```
EverOS/
├── .github/              # 社区文件（贡献指南、行为准则、安全政策）
├── methods/
│   ├── EverCore/        # 核心记忆操作系统
│   │   ├── src/
│   │   │   ├── run.py              # 应用入口
│   │   │   ├── agentic_layer/
│   │   │   │   └── memory_manager.py  # 核心记忆管理器
│   │   │   ├── infra_layer/adapters/input/api/  # REST API控制器
│   │   │   └── memory_layer/prompts/  # 提示词（EN/ZH变体）
│   │   ├── docs/          # 安装、用法、架构文档
│   │   ├── evaluation/    # 评估运行器和报告
│   │   └── env.template   # 环境变量模板
│   └── HyperMem/         # 超图记忆架构
├── benchmarks/
│   ├── EverMemBench/      # 记忆质量评估
│   └── EvoAgentBench/     # Agent自进化评估
├── use-cases/
│   ├── claaude-code-plugin/      # Claude Code记忆插件
│   ├── game-of-throne-demo/      # 权游记忆演示
│   └── openher/                   # 记忆驱动人格引擎
├── CLAUDE.md              # Agent开发指南
├── AGENTS.md              # Agent工具指南
└── README.md
```

### 3.2 技术栈

| 层级 | 技术 |
|------|------|
| 主要语言 | Python（6.6M字节） |
| 前端相关 | TypeScript（142K）、JavaScript（131K）、HTML（84K）、CSS（24K） |
| 部署 | Docker、Docker Compose |
| 包管理 | uv（Astral出品的极速Python包管理器） |
| API框架 | REST API（FastAPI风格推断） |
| 数据库 | （未明确，从Docker配置看应该是PostgreSQL + 向量数据库） |
| 嵌入/重排 | 支持 VECTORIZE_API_KEY 配置 |

### 3.3 关键入口点

- `methods/EverCore/src/run.py` — EverCore 应用入口
- `methods/EverCore/src/agentic_layer/memory_manager.py` — 核心记忆管理器
- `methods/EverCore/src/infra_layer/adapters/input/api/` — REST API 控制器
- `methods/EverCore/docs/` — 完整文档
- `methods/EverCore/evaluation/` — 评估运行器

### 3.4 生态集成示例

README 列出了大量基于 EverOS 的集成案例：

- **Reunite** — 通过语义记忆连接失散家庭成员的记忆
- **Hive Orchestrator** — 浏览器原生的 CLI 编码 Agent 团队协作
- **Evermemos MCP** — 通用 AI 编码助手记忆层
- **AI Data Technician** — 持续从科学家交互中学习的时序数据分析 Agent
- **Claude Code Plugin** — 为 Claude Code 提供持久记忆
- **Ruminer Browser Agent** — 浏览器 Agent 的个人记忆
- **Earth Online** — 记忆驱动的生产力游戏

## 四、实际应用场景

### 4.1 适合的场景

1. **AI 编码助手记忆增强** — Claude Code、OpenCode、Aider 等通过 MCP 接入 EverOS，实现跨会话记忆
2. **多 Agent 协作系统** — 多个 Agent 共享长期记忆，实现真正的团队协作
3. **人形/角色 AI** — 为虚拟角色注入持续记忆，实现更真实的人格一致性
4. **垂直领域 Agent** — 医疗（阿尔茨海默记忆助手）、教育（自我进化的学习伙伴）、客服等

### 4.2 与现有工具链的关系

EverOS 定位为**记忆基础设施层**，可以与现有的 Agent 编排工具配合使用：

- 可以作为 **MCP Server** 接入各种 Agent（如 `evermemos-mcp`）
- 支持 Claude Code 插件形式直接集成
- 可以独立运行 REST API 服务，被任何应用调用

### 4.3 论文引用

项目已发表多篇学术论文：

```bibtex
# EverMemOS 论文
@article{hu2026evermemos,
  title={EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning},
  author={Chuanrui Hu et al.},
  journal={arXiv preprint arXiv:2601.02163},
  year={2026}
}

# HyperMem 论文
@article{yue2026hypermem,
  title={HyperMem: Hypergraph Memory for Long-Term Conversations},
  author={Juwei Yue et al.},
  journal={arXiv preprint arXiv:2604.08256},
  year={2026}
}

# 评估论文
@article{hu2026evaluating,
  title={Evaluating Long-Horizon Memory for Multi-Party Collaborative Dialogues},
  author={Chuanrui Hu et al.},
  journal={arXiv preprint arXiv:2602.01313},
  year={2026}
}
```

## 五、总结

EverOS 是一个**专注于 Agent 长期记忆**的专业项目，提供了从理论（论文）到实践（EverCore）再到评估（EverMemBench）的完整工具链。6K+ Stars 和 627 Fork 说明其在社区中有一定影响力。其架构设计强调自组织、多租户和可扩展性，适合需要为 AI Agent 添加持久记忆能力的开发者研究和使用。