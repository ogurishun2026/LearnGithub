# codegraph 研究总结

> 仓库地址：https://github.com/colbymchenry/codegraph
> 研究日期：2026-05-26

## 一、仓库概述

CodeGraph 是一个为编码 Agent（Claude Code、Cursor、Codex CLI、opencode、Hermes Agent）设计的预索引代码知识图谱工具。通过 MCP 协议暴露 `codegraph_search`、`codegraph_context`、`codegraph_callers`、`codegraph_callees`、`codegraph_impact` 等工具，让 Agent 在预建索引上查询而非扫描文件。核心价值是**减少 Token 消耗和工具调用次数，同时保持 100% 本地运行**。

## 二、核心能力

### 2.1 工具列表

| 工具 | 用途 |
|---|---|
| `codegraph_search` | 按名称跨代码库全文搜索（FTS5） |
| `codegraph_context` | 一次调用返回入口点、相关符号和代码片段 |
| `codegraph_callers` | 追溯任意符号的调用者 |
| `codegraph_callees` | 追溯任意符号的被调用者 |
| `codegraph_impact` | 符号变更的影响半径分析 |
| `codegraph_node` | 获取符号节点详情 |
| `codegraph_status` | 索引健康状态和统计 |
| `codegraph_files` | 文件列表 |

### 2.2 性能基准

在 7 个真实开源代码库上测试（Claude Opus 4.7，headless）：

> **平均：35% 更便宜 · 57% 更少 Token · 46% 更快 · 71% 更少工具调用**

| 代码库 | 语言/规模 | 成本节省 | Token 节省 | 工具调用减少 |
|---|---|---|---|---|
| VS Code | TypeScript ~10k files | 26% | 78% | 85% |
| Excalidraw | TypeScript ~640 | 52% | 90% | 96% |
| Django | Python ~3k | 12% | 36% | 53% |
| Tokio | Rust ~790 | 82% | 86% | 92% |
| OkHttp | Java ~645 | 2% | 13% | 45% |
| Gin | Go ~110 | 21% | 34% | 40% |
| Alamofire | Swift ~110 | 47% | 64% | 83% |

大规模代码库受益最大：Agent 直接从索引回答问题，通常**零文件读取**。

### 2.3 支持的语言（20+）

TypeScript、JavaScript、Python、Go、Rust、Java、C#、PHP、Ruby、C、C++、Objective-C、Swift、Kotlin、Dart、Lua、Luau、Svelte、Liquid、Pascal/Delphi

### 2.4 框架感知路由

识别 14 种 Web 框架的路由文件，将 URL 模式链接到处理器：

Django、Flask、FastAPI、Express、NestJS、Laravel、Drupal、 Rails、Spring、Gin/chi/gorilla/mux、Axum/actix/Rocket、ASP.NET、Vapor、React Router/SvelteKit

### 2.5 跨语言桥接

| 边界 | 说明 |
|---|---|
| Swift ↔ ObjC | `@objc` 自动桥接规则（Cocoa 前缀如 `With`/`For`/`By` 等） |
| React Native 传统 Bridge | `NativeModules.X.fn()` ↔ `RCT_EXPORT_METHOD` / `@ReactMethod` |
| React Native TurboModules | `NativeM.ts` spec → native 实现 |
| RN Native → JS 事件 | `new NativeEventEmitter(...).addListener` ↔ `sendEventWithName` |
| Expo Modules | `requireNativeModule('X')` ↔ `Module { Name("X"); AsyncFunction }` |
| Fabric/Paper 视图 | JSX `<MyView>` ↔ ObjC `RCT_EXPORT_VIEW_PROPERTY` / Kotlin `@ReactProp` |

## 三、技术架构

### 3.1 技术栈

- **语言**：TypeScript
- **桌面打包**：Node.js（bundled runtime，无需预装 Node）
- **协议**：MCP（Model Context Protocol）
- **存储**：SQLite（100% 本地，无外部服务）
- **全文搜索**：FTS5（SQLite 内置）
- **安装方式**：npm 全局 / npx 零安装 / curl 一键脚本

### 3.2 架构设计

```
CodeGraph MCP Server（独立进程）
    ↓ SQLite 索引（.codegraph/）
    ↓ FTS5 全文索引 + 符号关系图
Agent 查询 → 预建索引 → 直接返回
    ↓ 无需文件扫描
```

核心设计理念：**不要将探索委托给文件读取子 Agent**——CodeGraph 是预建的搜索索引，重新用 grep+Read 推导其已有答案是在浪费预算。

### 3.3 安装和初始化

```bash
# 安装（一键脚本）
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh

# 或 npm
npm i -g @colbymchenry/codegraph

# 初始化项目
cd your-project
codegraph init -i
```

安装后自动配置 Claude Code / Cursor / Codex CLI / opencode / Hermes Agent 的 MCP server。

## 四、与 codedb-mcp 的对比

| 维度 | codegraph | codedb-mcp |
|---|---|---|
| Stars | 26,954（🔥非常高） | 34 |
| 协议 | MCP | MCP |
| 语言覆盖 | 20+ | C#/Java/Python/C++ |
| 架构 | TS + SQLite | Rust + tree-sitter |
| 工具数 | 8 个 MCP 工具 | 14 个 MCP 工具 |
| 特色 | 框架路由感知、跨语言桥接 | BM25 + HNSW 混合搜索、Louvain 图 |
| Token 优化 | ~35% 节省（benchmark 实测） | 未提供 benchmark |
| 发布日期 | 2026-01（更成熟） | 2026-05（很新） |

两者功能有重叠但定位互补：codegraph 更通用和成熟，codedb-mcp 在 C#/Java 领域的语义分析更深度。

## 五、项目信息

- **Stars**：26,954（非常高 🔥）
- **Forks**：1,507
- **语言**：TypeScript
- **许可证**：MIT
- **创建时间**：2026-01-18
- **平台**：Windows/macOS/Linux
- **Agent 支持**：Claude Code、Cursor、Codex CLI、opencode、Hermes Agent
- **文档**：https://colbymchenry.github.io/codegraph/
- **核心价值**：~35% 更便宜 · ~71% 更少工具调用 · 100% 本地