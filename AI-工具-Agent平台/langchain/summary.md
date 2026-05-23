# langchain 研究总结

> 仓库地址：https://github.com/langchain-ai/langchain
> 研究日期：2026-05-23

## 一、仓库概述

LangChain 是一个 **Agent（智能体）工程平台**，用于构建、部署和管理基于大语言模型的应用。仓库采用 monorepo（单一代码库）架构，将核心抽象层、实现层、第三方集成层、测试框架等拆分为多个独立版本管理的 Python 包。

描述已从早期的"LLM应用开发框架"演变为更精准的 **"the agent engineering platform"**（Agent工程平台）。

## 二、核心内容

### 2.1 包结构（libs/ 目录）

| 包 | 包名 | 说明 |
|----|------|------|
| `libs/core` | `langchain_core` | 核心抽象层：BaseChatModel、BaseRetriever、BaseTool 等基类和协议 |
| `libs/langchain` | `langchain_classic` | 经典 LangChain（遗留包，无新功能） |
| `libs/langchain_v1` | `langchain` | **当前活跃维护的主包**，含 Chains、Agents、Memory、Callbacks 等 |
| `libs/partners/*` | 各 partner 包 | 第三方服务集成（见下表） |
| `libs/text-splitters` | `langchain_text_splitters` | 文档分块工具 |
| `libs/standard-tests` | — | 各 partner 集成的标准化集成测试套件 |
| `libs/model-profiles` | — | 模型配置profiles（能力标志、上下文窗口等），通过 `langchain-profiles` CLI 管理 |

### 2.2 Partner 集成（第三方集成）

| Partner 包 | 集成方向 |
|------------|---------|
| `openai` | OpenAI 模型 + Embeddings |
| `anthropic` | Anthropic (Claude) |
| `ollama` | 本地模型支持 |
| `huggingface` | HuggingFace 模型 |
| `deepseek` | DeepSeek 模型 |
| `mistralai` | Mistral AI |
| `fireworks` | Fireworks AI |
| `groq` | Groq |
| `exa` | Exa 搜索 |
| `perplexity` | Perplexity |
| `openrouter` | OpenRouter |
| `xai` | xAI |
| `chroma` | Chroma 向量数据库 |
| `qdrant` | Qdrant 向量数据库 |
| `nomic` | Nomic |
| `...` | 其他集成（部分在独立仓库如 `langchain-ai/langchain-google`、`langchain-ai/langchain-aws`） |

### 2.3 核心模块（langchain_v1 / langchain_classic）

基于 `AGENTS.md` 和目录结构推断的核心组件：

- **Chains（链）**：将模型调用、工具调用、记忆等串联成有序流程
- **Agents（智能体）**：基于 LLM 的自主决策单元，可调用工具
- **Memory（记忆）**：对话上下文持久化机制
- **Callbacks**：事件回调系统，用于日志、跟踪、监控
- **Tool（工具）**：Agent 可调用的外部能力（搜索、API调用等）
- **Retrievers（检索器）**：RAG（检索增强生成）场景的文档检索
- **Documents（文档）**：文档加载和处理的抽象

## 三、技术架构

### 3.1 目录结构

```
langchain/
├── libs/
│   ├── core/                    # langchain_core（核心抽象）
│   │   └── langchain_core/
│   │       ├── _api/            # 内部API机制
│   │       ├── messages/         # 消息抽象
│   │       ├── output_parsers/   # 输出解析
│   │       ├── prompts/          # Prompt模板
│   │       ├── retrievers/       # 检索器基类
│   │       ├── runnables/        # 可运行对象抽象（Chain的核心）
│   │       ├── tools/            # 工具基类
│   │       └── vectorstores/     # 向量存储抽象
│   ├── langchain/                # langchain_classic（遗留）
│   │   └── langchain_classic/
│   ├── langchain_v1/             # 活跃维护的 langchain 包
│   ├── partners/                 # 第三方集成
│   │   ├── openai/
│   │   ├── anthropic/
│   │   ├── ollama/
│   │   └── ...（16+个）
│   ├── text-splitters/
│   ├── standard-tests/
│   ├── model-profiles/           # langchain-profiles CLI
│   └── Makefile
├── .github/                      # CI/CD 工作流
├── .vscode/                      # VSCode 配置
├── AGENTS.md                     # 开发者指南（核心架构文档）
├── CLAUDE.md                     # Claude Code 指南（同 AGENTS.md）
└── README.md
```

### 3.2 技术栈

| 层级 | 技术 |
|------|------|
| 语言 | Python（主语言，12.5MB 代码） |
| 包管理 | `uv`（Fast Python 包管理器和解析器，替代 pip/poetry） |
| 测试 | `pytest` |
| 代码质量 | `ruff`（linter+formatter）、`mypy`（类型检查） |
| CI/CD | GitHub Actions |
| 预提交 | pre-commit hooks |

### 3.3 依赖管理模型

- **uv** 作为统一包管理器，每个 `libs/*` 包有独立的 `pyproject.toml` + `uv.lock`
- 本地开发使用 editable install（`[tool.uv.sources]`）
- 依赖组（groups）：`test`、`lint` 等，按组同步
- 支持 Docker 开发环境（`dev.Dockerfile`）

### 3.4 语言统计

- Python：12,490,067 字节（约 12MB）
- Makefile：60,679 字节
- Shell：13,124 字节
- 其他（XSLT、HTML、Dockerfile、JavaScript）：约 30KB

## 四、实际应用场景

### 4.1 RAG（检索增强生成）系统

LangChain 的经典应用场景：通过 `Retrievers` 从向量数据库检索相关文档，结合 `Chains` 组装成 LLM 问答 pipeline。支持 Chroma、Qdrant 等多种向量存储集成。

### 4.2 Agent（智能体）应用开发

通过 `Agent` + `Tool` 抽象构建能够自主决策、调用外部工具的 LLM 应用。支持多 Partner 模型（OpenAI Claude、DeepSeek、Ollama 本地模型等），通过标准化的接口接入。

### 4.3 对本项目的参考价值

作为"人工智能试验场"，LangChain 的架构设计值得参考：

- **分层抽象思想**：`core` 层定义接口协议，`partners` 层按供应商拆分，核心逻辑与集成解耦
- **Runnable 协议**：`langchain_core/runnables` 提供的可组合抽象，是构建复杂 Agent pipeline 的基础
- **标准化测试**：`standard-tests` 对所有 Partner 集成提供统一测试规范

### 4.4 版本演进注意

该仓库经历了从早期单一 `langchain` 包到 monorepo 的演进。目前：
- `langchain_classic`（`libs/langchain`）已标记为"legacy, no new features"
- 活跃开发集中在 `langchain_v1`（`libs/langchain_v1`）
- Partner 集成在 `libs/partners/` 中，部分独立集成维护在外部仓库

### 4.5 与同类项目对比

| 维度 | LangChain | CrewAI | AutoGen |
|------|-----------|--------|---------|
| 定位 | Agent 工程平台（通用） | 多Agent角色编排框架 | 多Agent会话框架 |
| 维护活跃度 | 非常活跃 | 活跃 | 活跃 |
| 包管理 | uv + monorepo | pip | pip |
| Partner集成 | 丰富（16+官方） | 较少 | 较少 |
| 学习曲线 | 中等（模块多） | 较低 | 中等 |