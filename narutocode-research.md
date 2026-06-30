---
name: narutocode-research
description: NarutoCode 深度研究 —— 基于 Microsoft Agent Framework 的终端 AI 编程助手
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6aafdfcd-c3e4-495d-a2d3-5636278c31ab
---

**NarutoCode** 是一个基于 **.NET 10** 和 **Microsoft Agent Framework** 开发的终端 Agent 编程工具。用户启动后可以直接用自然语言让它分析项目、修改文件、执行命令、排查问题。

仓库地址：`https://github.com/NarutoAI/NarutoCode`

## 为什么重要（Why）

开发自动化 Agent 时，NarutoCode 展示了**如何基于微软官方 Agent Framework 构建一个完整的终端 AI 助手**。它的架构设计、工具注册方式、上下文压缩策略、多模式 Agent（plan/execute）都值得参考。特别是对中文开发者友好，系统 Prompt 和安全红线设计都很成熟。

## 关键能力

| 能力 | 说明 |
|------|------|
| **多模型支持** | OpenAI Chat / OpenAI Responses / Anthropic 三种协议，运行时 `/provider` 切换 |
| **多模式 Agent** | 支持 plan / execute 等模式，通过 `mode_get` / `mode_set` 工具切换 |
| **丰富工具集** | Shell、文件访问、文件记忆、Task/Todo、SVG 渲染、Skills 目录 |
| **三级上下文压缩** | 图片压缩(40%) → 工具结果压缩(60%) → 摘要压缩(80%) |
| **会话持久化** | SQLite 本地存储，按工作目录隔离会话 |
| **安全设计** | 工作目录隔离 + 敏感路径黑名单 + Shell 审批开关 |
| **AOT 发布** | 支持 Ahead-of-Time 编译、单文件、自包含、裁剪 |

## 架构要点

采用分层领域驱动架构：

```
NarutoCodeCli (TUI + 入口)
  └─ NarutoCode.Infrastructure (AI Agent、存储、ChatClient 工厂)
       └─ NarutoCode.Application (服务、接口)
            └─ NarutoCode.Domain (实体、配置、枚举)
```

### 核心技术依赖

- `Microsoft.Agents.AI` / `Microsoft.Agents.AI.Harness` — 微软 Agent 框架
- `Microsoft.Extensions.AI` (MEAI) — 统一 AI 抽象接口
- `Spectre.Console` — 终端 UI 渲染
- `Microsoft.Data.Sqlite` — 本地数据存储（纯 SQL，无 ORM，AOT 友好）

### 设计亮点

1. **Agent 工厂高度定制**：通过 `HarnessAgentOptions` 注入详细中文系统 Prompt，包含工程规范、安全红线、输出风格
2. **动态 ChatClient**：使用 `IChatClientFactory` + Keyed Service，运行时切换 Provider 无需重建依赖容器
3. **压缩策略协调器**：`CompactionStrategyCoordinator` 按阈值分级执行，优先压缩成本低的内容（图片 → 工具结果 → 摘要）
4. **AGENTS.md 项目信息注入**：自动读取工作目录下的 `AGENTS.md` 作为项目上下文注入 Agent

## 如何应用（How to apply）

1. **学习 Microsoft Agent Framework 的最佳实践**：NarutoCode 是国内较早使用该框架的开源项目，其 `AgentFactory`、`LoopEvaluators`、`AIContextProviders` 的用法可以直接参考
2. **构建自己的终端 Agent**：参考其 TUI 架构（`TuiChatApplication` 事件循环、`ChatScreenRenderer` 流式渲染）
3. **上下文管理策略**：三级压缩策略（图片 → 工具结果 → 摘要）可直接借鉴到自己的 Agent 系统中
4. **多模式工作流**：plan/execute 模式切换机制适合需要"先规划后执行"的复杂自动化任务
5. **与 CLIProxyAPI 组合**：CLIProxyAPI 提供多模型 API 网关，NarutoCode 提供终端交互层，两者可以组合构建完整的本地 AI 开发环境

## 相关记忆

- [[cliproxyapi-research]] — AI 代理网关，可与 NarutoCode 组合使用提供多模型 API 接入
- [[ai-workflow-discussion]] — AI 全自动化工作流探索
