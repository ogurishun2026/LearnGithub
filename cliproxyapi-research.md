---
name: cliproxyapi-research
description: CLIProxyAPI 深度研究 —— AI 代理网关，用于将 CLI 订阅转为标准 API
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6aafdfcd-c3e4-495d-a2d3-5636278c31ab
---

**CLIProxyAPI** 是一个用 Go 1.26 编写的 AI 代理网关，核心能力是**把 Claude Code、OpenAI Codex、Gemini、Grok 等 CLI 工具的私有认证，翻译成标准的 OpenAI / Gemini / Claude 兼容 API**。

仓库地址：`https://github.com/router-for-me/CLIProxyAPI`

## 为什么重要（Why）

开发自动化 Agent 时，一个核心痛点是**如何低成本获取 LLM 调用能力**。直接购买 API Key 成本高，但很多人已经有 Claude Code / ChatGPT Plus / Gemini Pro 等 CLI/网页订阅。CLIProxyAPI 提供了一种将这些现有订阅转化为可编程 API 的完整方案，这对构建多 Agent 系统或自动化工作流非常有价值。

## 关键能力

| 能力 | 说明 |
|------|------|
| **协议转换** | 将各厂商私有协议翻译为标准 OpenAI/Gemini/Claude API |
| **OAuth 登录** | 内置浏览器 OAuth 流程获取 Claude/Codex/Gemini/Grok 等 token |
| **多账户轮询** | 同一厂商多组凭证自动轮询 + 失败冷却（cooldown） |
| **WebSocket 支持** | Codex 和 xAI 有专门 WebSocket 执行器 |
| **管理 API** | `/v0/management/*` 支持配置热更新、OAuth 会话管理 |
| **插件系统** | 支持 Go/C/Rust 动态库插件（C ABI + JSON 协议） |
| **存储后端** | 文件（默认）/ PostgreSQL / Git / 对象存储（S3/MinIO） |
| **TUI 管理界面** | `--tui --standalone` 启动终端管理 UI |
| **Home 控制平面** | 通过 `-home-jwt` 连接远程控制平面，实现集群配置下发 |

## 架构要点

- **分层清晰**：`cmd/` → `internal/`（api / runtime/executor / translator / auth / registry / store / tui）→ `sdk/`（可嵌入 Go SDK）
- **执行器模式**：每个上游厂商一个 executor（`claude_executor.go`、`codex_executor.go` 等），负责构造请求、处理响应、翻译格式
- **翻译器模式**：`internal/translator/` 按厂商分目录，遵循"先归一化 canonical 表示，再按厂商翻译输出"
- **Auth Manager + Store 抽象**：认证信息统一管理，Store 可替换为多种后端

## 如何应用（How to apply）

1. **作为 Agent 系统的 LLM 路由层**：在自己的自动化 Agent 中内嵌 CLIProxyAPI 的 Go SDK，实现多模型 failover 和负载均衡
2. **降低 LLM 调用成本**：用已有的 CLI 订阅代替 API Key，特别适合需要大量调用但预算有限的自动化场景
3. **多账户配额管理**：自动化 Agent 可以通过管理 API 监控各账户配额，实现智能调度
4. **学习其协议翻译设计**：`internal/translator/` 的"canonical → per-provider"架构值得借鉴，用于构建自己的多厂商适配层

## 相关记忆

- [[narutocode-research]] — 终端 Agent 编程工具，可与 CLIProxyAPI 组合使用（CLIProxyAPI 提供 API，NarutoCode 提供终端交互）
- [[ai-workflow-discussion]] — AI 全自动化工作流探索
