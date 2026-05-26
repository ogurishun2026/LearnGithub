# ccglass 研究总结

> 仓库地址：https://github.com/jianshuo/ccglass
> 研究日期：2026-05-26

## 一、仓库概述

ccglass（Claude Code Glass）是一个轻量级的本地日志记录反向代理 + Web 仪表板，用于查看编码 Agent（Claude Code、Codex、OpenCode 等）发送给模型的真实内容。无需配置，一行命令即可启动，支持多个 AI 客户端的实时监控。

## 二、核心能力

### 2.1 支持的客户端

| 客户端 | 说明 |
|---|---|
| `claude` | Claude Code |
| `codex` | Codex (OpenAI) |
| `deepseek` | DeepSeek-UI 调度器 |
| `deepseek-tui` | DeepSeek-UI 运行时 |
| `reasonix` | Reasonix |
| `dsnix` | Reasonix (dsnix 别名) |
| `kimi` | Claude Code via Moonshot |
| `opencode` | OpenCode |
| `ollama` | 任何 Ollama 后端客户端 |
| `lmstudio` | 任何 LLM Studio 后端客户端 |
| `openrouter` | 任何 OpenRouter 后端客户端 |
| `glm` | 任何 GLM/Zhipu 后端客户端 |
| `bedrock` | Claude Code via AWS Bedrock |
| `vertex` | Claude Code via Google Vertex AI |
| `run` | 任何通过通用 provider 的客户端 |

### 2.2 核心功能

| 功能 | 说明 |
|---|---|
| 实时请求流 | 每个请求实时出现在仪表板上 |
| 系统提示查看 | 展开查看完整系统提示、消息、工具调用 |
| 对话流视图 | 自上而下的序列图展示 Agent 循环 |
| Token/缓存/成本 | 精确统计输入/输出/缓存 Token 和预估成本 |
| 对比 Diff | 选择两个请求查看精确上下文差异 |
| 会话摘要 | 显示滚动累计的输入/输出 Token 和缓存命中率 |

### 2.3 仪表板功能

- **Per-Model 过滤器**：按模型筛选请求列表、会话摘要、错误计数
- **Per-Request 延迟**：显示每个请求的总时间、TTFT、生成窗口
- **延迟趋势**：图表显示平均延迟
- **复制为 cURL**：从概览 tab 复制代理请求的 shell 格式
- **浅色/深色主题**：系统偏好、浅色或深色

### 2.4 IDE 扩展支持

IDE 扩展（Cursor in BYOK 模式、Clione、Continue.dev 等）配置自定义 API base URL 可以通过代理检查。

## 三、技术架构

### 3.1 技术栈

- **语言**：Node.js
- **协议**：HTTP 代理 + WebSocket
- **前端**：Web 仪表板

### 3.2 工作原理

```
Client → ccglass 代理 → 真实 API
         ↓
      Web 仪表板（实时监控）
```

核心原理：Client 访问代理，代理转发到真实 API，同时记录所有请求用于监控。

### 3.3 安装和使用

```bash
# 安装
npm install -g ccglass
ccglass

# 选择客户端
Which client do you want to inspect?
1) Claude Code
2) Codex (OpenAI)
3) DeepSeek-UI
...
> 
```

### 3.4 选项

| 选项 | 默认 | 说明 |
|---|---|---|
| `--provider` | 来自命令 | 强制格式/环境 |
| `--upstream` | 每 provider 默认 | 覆盖上游 API |
| `--port` | 自动 | 仪表板端口 |
| `--proxy-port` | 自动 | 代理端口 |
| `--no-open` | false | 不在浏览器中打开仪表板 |

## 四、项目信息

- **Stars**：302
- **语言**：JavaScript
- **创建者**：jianshuo
- **前置要求**：Node.js >=18

## 五、与 codedb-mcp 的对比

| 维度 | ccglass | codedb-mcp |
|---|---|---|
| 用途 | 流量监控/日志 | 代码搜索/知识图谱 |
| 功能 | 查看 Agent → Model 请求 | 代码库语义搜索 |
| 协议 | 代理 + WebSocket | MCP |
| 关注点 | 可观测性 | 代码分析 |

ccglass 解决的是"Agent 实际发送了什么给模型"的问题，而 codedb-mcp 解决的是"如何在代码库中找到所需信息"的问题。两者互补。