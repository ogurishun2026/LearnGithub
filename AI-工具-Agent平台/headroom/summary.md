# headroom 研究总结

> 仓库地址：https://github.com/headroomlabs-ai/headroom
> 研究日期：2026-07-01
> Stars：54,483 ｜ Forks：3,913 ｜ 主语言：Python（Rust 核心）｜ License：Apache 2.0
> 创建于 2026-01-07，最近更新 2026-06-30（非常活跃）

## 一、仓库概述

**Headroom 是面向 AI Agent 的「上下文压缩层」（context compression layer）。**

它在数据进入大模型（LLM）之前，先压缩 Agent 要读的一切内容——工具输出、日志、RAG 检索块、文件、对话历史——号称能减少 **60–95% 的 token**，而答案保持一致。

核心卖点：
- **省钱**：真实 Agent 工作负载下平均省 47%–92% token。
- **本地优先（local-first）**：所有压缩在本机进行，数据不出本地。
- **可逆（reversible）**：原文缓存在本地，模型需要时通过 `headroom_retrieve` 取回（称为 CCR）。
- **零代码接入**：可作为代理（proxy）插在任意语言/任意 OpenAI 兼容客户端前面。

一句话定位：**给 AI Agent 加一层「token 减肥」中间件，省钱但不掉精度。**

## 二、核心内容

### 4 种使用形态（任选）

1. **库（Library）**：`from headroom import compress` —— Python / TypeScript 内联调用 `compress(messages)`。
2. **代理（Proxy）**：`headroom proxy --port 8787` —— 零代码改动，任何语言、任何 OpenAI 兼容客户端都能用。
3. **Agent 包装（wrap）**：一条命令包住编码 Agent，`headroom wrap claude|codex|cursor|aider|...`，`headroom unwrap <tool>` 撤销。
4. **MCP 服务器**：暴露 `headroom_compress`、`headroom_retrieve`、`headroom_stats` 三个工具给任意 MCP 客户端。

### 关键能力

| 能力 | 说明 |
|------|------|
| **跨 Agent 记忆** | Claude、Codex、Gemini 之间共享存储，自动去重 |
| **headroom learn** | 挖掘「失败会话」，把纠正写进 `CLAUDE.local.md`（默认，gitignored）/ `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` |
| **输出 token 削减** | 不只压缩「发送」内容，还削减模型「写回」的内容（去掉客套、重复代码，常规步骤降低 thinking effort）。`HEADROOM_OUTPUT_SHAPER=1` 开启 |
| **可逆压缩 CCR** | 原文按 TTL 缓存本地，模型按需取回 |

### 实测数据（来自 README）

省 token 效果：

| 工作负载 | 压缩前 | 压缩后 | 节省 |
|----------|-------:|-------:|-----:|
| 代码搜索（100 条结果） | 17,765 | 1,408 | **92%** |
| SRE 故障调试 | 65,694 | 5,118 | **92%** |
| GitHub issue 分类 | 54,174 | 14,761 | **73%** |
| 代码库探索 | 78,502 | 41,254 | **47%** |

精度保持（标准基准）：GSM8K 数学 ±0.000；TruthfulQA +0.030；SQuAD v2 在 19% 压缩下保 97%；BFCL 工具调用在 32% 压缩下保 97%。

## 三、技术架构

### 处理管线（核心流程）

```
Agent/App → Headroom（本地）→ LLM 提供商
            CacheAligner → ContentRouter → CCR
                            ├─ SmartCrusher   (JSON)
                            ├─ CodeCompressor (AST)
                            └─ Kompress-v2-base (文本，HuggingFace 自研模型)
```

- **ContentRouter**：检测内容类型，自动选对应压缩器。
- **SmartCrusher**：通用 JSON 压缩（数组/嵌套对象/混合类型）。
- **CodeCompressor**：AST 感知，支持 Python/JS/TS/Go/Rust/Java/C/C++/Perl。
- **Kompress-v2-base**：自研 HuggingFace 模型，在 Agentic 轨迹上训练的文本压缩模型。
- **CacheAligner**：稳定 prompt 前缀，让 Anthropic/OpenAI 的 KV 缓存真正命中。
- **图像压缩**：通过训练的 ML 路由器，减少 40–90%。

统一请求生命周期（11 阶段）：
`Setup → Pre-Start → Post-Start → Input Received → Input Cached → Input Routed → Input Compressed → Input Remembered → Pre-Send → Post-Send → Response Received`

### 目录结构（要点）

- **`headroom/`**：Python 核心包。子模块包括 `compression/`（detector/universal/masks/handlers）、`ccr/`（可逆压缩）、`proxy/`（代理服务器）、`providers/`（claude/codex/copilot/gemini/openclaw 等厂商适配）、`memory/`（跨 Agent 记忆）、`learn/`（失败挖掘）、`mcp_registry/`、`evals/`、`dashboard/` 等。
- **`crates/`**：Rust 核心，4 个 crate —— `headroom-core`、`headroom-parity`、`headroom-proxy`、`headroom-py`（PyO3 绑定）。性能敏感路径用 Rust。
- **`sdk/`**：TypeScript SDK（npm 包 `headroom-ai`，仅库，不含 CLI）。
- 还有 `benchmarks/`、`agent-evals/`、`docs/`、`examples/`、`e2e/`、`docker/`、`sql/`、`plugins/`、`.claude-plugin/`。

### 语言构成

Python 13.2M、Rust 2.6M、TypeScript 435K、HTML 175K，外加 Shell/PowerShell/C/PLpgSQL。

### 生态集成（开箱即用）

Python / TypeScript app、Anthropic/OpenAI SDK（`withHeadroom(...)`）、Vercel AI SDK 中间件、LiteLLM 回调、LangChain（`HeadroomChatModel`）、Agno、Strands、ASGI 中间件、多 Agent（`SharedContext`）、MCP。

Agent 兼容矩阵（`headroom wrap` 支持）：Claude Code、Codex、Cursor、Aider、Copilot CLI、OpenClaw、OpenCode、Cline、Continue、Goose、OpenHands、Mistral Vibe。

## 四、实际应用场景（结合你的项目背景）

你日常重度使用 Claude Code + 多种 CLI Agent（Mexus、CLIProxyAPI 等），Headroom 与你的场景高度契合：

1. **直接给 Claude Code 省钱**：`headroom wrap claude` 一条命令包住，自动压缩工具输出/日志/文件读取的 token，对话体验不变。你跑大量代码搜索、代码库探索时省得最多（47%–92%）。

2. **配合 CLIProxyAPI / 多账户网关**：Headroom 是「压缩层」，CLIProxyAPI 是「订阅转 API 网关」，二者职责正交，可叠加——Headroom 先压缩再经网关转发，进一步降低每次请求成本。

3. **跨 Agent 共享记忆**：你同时用 Claude / Codex / 多个 CLI Agent，Headroom 的 cross-agent memory 能让它们共享上下文并自动去重，省去重复喂同样信息。

4. **`headroom learn` 自动写 CLAUDE.local.md**：挖掘失败会话、自动把纠正经验写进你项目的 `CLAUDE.local.md`，符合你「先计划后编码、完成前验证」的工作流，能沉淀踩坑教训。

5. **可逆压缩兜底**：担心压缩丢信息？CCR 把原文按 TTL 留在本地，模型需要时自己 `headroom_retrieve` 取回，安全感更强。

**注意点**：
- CLI 只随 PyPI 包发布（`pip install "headroom-ai[all]"`），npm 包仅是 TS 库无 CLI。
- 需要 Python 3.10+；想看「省了多少美元」选 Python 3.13（LiteLLM 计价，3.14+ 不支持计价）。
- 沙箱/无法跑本地进程的环境不适用。
- 单一厂商原生压缩已够用、又不需要跨 Agent 记忆的，可以跳过。
