# jcode 研究总结

> 仓库地址：https://github.com/1jehuang/jcode
> 研究日期：2026-05-20

## 一、仓库概述

**jcode** — 下一代编码 Agent Harness，主打多会话工作流、极致可定制化和高性能。

核心理念：提升 AI 编程的技能天花板（skill ceiling），让 Agent 在真实项目中能持续、高效地工作。

## 二、核心性能指标

### 2.1 RAM 对比（1 个活跃会话）

| 工具 | PSS | 对比 |
|------|-----:|------:|
| **jcode (local embedding off)** | 27.8 MB | 基线 |
| **jcode** | 167.1 MB | 6.0× |
| **pi** | 144.4 MB | 5.2× |
| **Codex CLI** | 140.0 MB | 5.0× |
| **OpenCode** | 371.5 MB | 13.4× |
| **GitHub Copilot CLI** | 333.3 MB | 12.0× |
| **Claude Code** | 386.6 MB | 13.9× |

### 2.2 启动速度对比（Time to first frame）

| 工具 | 耗时 | 对比 |
|------|-----:|------:|
| **jcode** | **14.0 ms** | 基线 |
| **Antigravity CLI** | 383.5 ms | 27.4× 更慢 |
| **pi** | 590.7 ms | 42.2× 更慢 |
| **Codex CLI** | 882.8 ms | 63.1× 更慢 |
| **OpenCode** | 1035.9 ms | 74.0× 更慢 |
| **Claude Code** | 3436.9 ms | **245.5× 更慢** |

### 2.3 多会话内存扩展

| 工具 | 每新增会话增量 | 对比 |
|------|---:|------:|
| **jcode** | ~10.4 MB | 基线 |
| **pi** | ~76.5 MB | 7.7× |
| **OpenCode** | ~318.4 MB | 32.2× |
| **Claude Code** | ~212.7 MB | 21.5× |

## 三、核心功能

### 3.1 Agent Memory（类人记忆系统）

- **语义向量嵌入**：每轮对话作为语义向量存储
- **图结构检索**：查询记忆图，通过余弦相似度高效检索相关记忆
- **自动提取**：定期（语义漂移、K 轮后、会话结束）通过 sideagent 提取记忆
- **主动搜索工具**：显式记忆工具，支持主动搜索/存储
- **会话检索**：传统 RAG 方式检索历史会话
- **自动整理**：Ambient 模式定期重组、检错、消重

### 3.2 Swarm（多 Agent 协作）

- **多 Agent 同一仓库**：自动管理，冲突通知
- **文件变更通知**：Agent A 编辑文件时，Agent B 收到通知
- **消息通道**：支持 DM、广播、按仓库分组
- **自主spawn**：Agent 可自主 spawn 团队成员，并行完成任务
- **Coordinator/Worker**：主 Agent 变协调者，spawn 的 Agent 变工作者

### 3.3 UI 特性

- **Side Panel**：实时加载文件、diff viewer、Mermaid 图表渲染
- **Info Widgets**：只在屏幕负空间显示，不遮挡主内容
- **高帧率渲染**：1000+ fps，无闪烁
- **自定义 Terminal**：Handterm 实现原生滚动 API
- **对齐模式**：支持左对齐和居中模式

### 3.4 Browser Automation（浏览器自动化）

内置 `browser` 工具，当前支持 Firefox Agent Bridge：

| 动作 | 说明 |
|------|------|
| `status` | 检查状态 |
| `setup` | 设置 |
| `open` | 打开 URL |
| `snapshot` | 快照 |
| `get_content` | 获取内容 |
| `interactables` | 获取可交互元素 |
| `click` | 点击 |
| `type` | 输入 |
| `fill_form` | 填表 |
| `select` | 选择 |
| `wait` | 等待 |
| `screenshot` | 截图 |
| `eval` | 执行 JS |
| `scroll` | 滚动 |
| `upload` | 上传 |
| `press` | 按键 |

### 3.5 Self-Dev（自开发模式）

Agent 可以修改自己的源代码：

- 迭代基础设施完备：编辑 → 构建 → 测试 → 重载二进制 → 继续工作
- 支持多会话同时 self-dev
- 推荐使用前沿模型（GPT 5.5 或最新 frontier 模型）

### 3.6 会话恢复

支持从不同 harness 恢复会话：Codex、Claude Code、OpenCode、Pi。

### 3.7 OAuth 与 Provider 支持

**内置登录支持**：
- Claude
- OpenAI / ChatGPT / Codex
- Google Gemini
- GitHub Copilot
- Azure OpenAI
- Alibaba Cloud Coding Plan
- Fireworks
- MiniMax
- LM Studio
- Ollama
- Custom OpenAI-compatible endpoint

**完整 Provider 列表**：
`openrouter`, `openai-compatible`, `opencode`, `opencode-go`, `zai`/`kimi`, `302ai`, `baseten`, `cortecs`, `deepseek`, `firmware`, `huggingface`, `moonshotai`, `nebius`, `scaleway`, `stackit`, `groq`, `mistral`, `perplexity`, `togetherai`, `deepinfra`, `minimax`, `xai`, `lmstudio`, `ollama`, `chutes`, `cerebras`, `cursor`, `antigravity`, `google`

**多账号切换**：快速切换不同平台的多个账号。

### 3.8 MCP 支持

- 全局 MCP：`~/.jcode/mcp.json`
- 项目级 MCP：`.jcode/mcp.json`
- 兼容 fallback：`.claude/mcp.json`

## 四、技术架构

### 4.1 技术栈

- **语言**：Rust（核心）
- **终端**：Handterm（自研终端，支持原生滚动 API）
- **图表渲染**：mermaid-rs-renderer（自研，比浏览器版本快 1800×）

### 4.2 项目结构

```
jcode/
├── src/
│   ├── agent.rs          # Agent 核心逻辑
│   ├── agent_tests.rs    # Agent 测试
│   └── agent/            # Agent 子模块
├── .jcode/              # 项目级配置
├── .claude/             # Claude 兼容配置
├── .cargo/              # Cargo 配置
├── docs/                # 架构文档
│   ├── AMBIENT_MODE.md
│   ├── MEMORY_ARCHITECTURE.md
│   ├── SWARM_ARCHITECTURE.md
│   ├── SERVER_ARCHITECTURE.md
│   └── SAFETY_SYSTEM.md
├── scripts/
│   ├── install.sh       # Linux/macOS 安装
│   ├── install.ps1      # Windows 安装
│   └── remote_build.sh   # 远程构建
└── AGENTS.md             # 开发工作流指南
```

### 4.3 安装方式

```bash
# macOS & Linux
curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.sh | bash

# Windows PowerShell
irm https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.ps1 | iex

# Homebrew
brew tap 1jehuang/jcode
brew install jcode

# 源码构建
git clone https://github.com/1jehuang/jcode.git
cd jcode
cargo build --release
```

## 五、Star 历史与社区

- **Stars**: 6,375（2026-05-20）
- **语言**: Rust
- **许可**: MIT（推测）
- **活跃度**: Commit 活跃

## 六、总结

jcode 是一个**极致性能的编码 Agent Harness**，用 Rust 编写，专为多会话、高并发场景优化。

**核心优势**：
- 启动速度比 Claude Code 快 245×
- 10 活跃会话仅需 260MB，比 Claude Code 的 2300MB 省 21 倍
- 内置类人记忆系统，自动检索相关上下文
- Swarm 多 Agent 协作，支持并行任务
- 自研 Handterm 终端，1000+ fps 渲染
- 支持 30+ LLM Provider，多账号切换

**与 Claude Code 对比**：

| 维度 | jcode | Claude Code |
|------|-------|------------|
| 性能 | 极致优化 | 较重 |
| 多会话 | 原生支持 | 资源消耗大 |
| 记忆系统 | 内置语义记忆 | 依赖外部 |
| 协作 | Swarm 原生 | 不支持 |
| Provider | 30+ | Anthropic Only |

**适用场景**：
- 需要多 Agent 并行协作的大型项目
- 对性能敏感（资源、延迟）的团队
- 需要在多个 LLM Provider 间切换的用户
- 需要持久化记忆的长期项目开发