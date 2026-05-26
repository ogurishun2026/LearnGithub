# Locus 研究总结

> 仓库地址：https://github.com/r1n7aro/Locus
> 研究日期：2026-05-26

## 一、仓库概述

Locus 是一个开源的 Unity Dev Agent（Rust + Tauri + Vue.js 独立桌面应用），运行在 Unity 编辑器外部的独立进程中。通过自有中间表示层、Roslyn JIT 编译、C# 状态机工具、知识系统和可视化版本控制，让 AI Agent 能够渐进式读取大型场景、语义化编辑 Unity 资源和代码、自动化分析和调试运行时状态。

## 二、核心能力

### 2.1 功能列表

| 能力 | 说明 |
|---|---|
| **编辑器内操作** | 编写 C# 代码，读写 Unity 对象和资源，完成全流程功能开发 |
| **运行时分析和调试** | 自主操作和捕获运行时状态，辅助修复 Bug 和性能优化 |
| **自动化知识系统** | 自动总结对话需求为设计文档，长期记忆保存项目理解 |
| **可视化版本控制** | Unity YAML 资产的语义 diff 分析和冲突处理界面 |
| **多模型支持** | 支持订阅账户登录，兼容多种 LLM API |
| **状态机调试** | 通过反射在特定帧或事件采样内部状态，输出逐帧表格 |
| **渐进式大场景读取** | 自有中间表示 + 检索工具快速定位目标对象 |
| **高速并行资产扫描** | 基于 Rust 并行生态，快速语义解析大型场景 |

### 2.2 技术差异化

| 特性 | 实现方式 |
|---|---|
| 独立进程架构 | Rust + Tauri + Vue.js，不嵌入 Unity Editor |
| 大型场景渐进读取 | 自有中间表示 + 检索工具 |
| 语义化资产编辑 | Roslyn JIT 编译执行 C# 代码 |
| 版本管理 | Agent 侧管理，用户可 review 和 revert |
| 并行资产扫描 | Rust rayon 并行生态 |
| 知识系统 | L0/L1/L2 注入控制，可配置 AI 维护模式和规则 |
| 运行时调试 | C# 状态机工具 + 反射 |
| 可视化版本控制 | Unity YAML 语义 diff + 冲突解决 |
| 现代前端体验 | Vue.js，通过 Windows API 嵌入 Unity 窗口 |

如果将 Locus 实现为 Unity Editor 内插件或 MCP 服务器，大部分能力将难以实现甚至技术上不可能实现。

## 三、技术架构

### 3.1 技术栈

- **核心**：Rust + Tauri 2（桌面应用框架）
- **前端**：Vue.js + Vite + TypeScript
- **Unity 集成**：C# + Roslyn（.NET 编译器即服务）
- **包管理**：bun
- **平台**：Windows（当前唯一支持，计划支持 macOS）

### 3.2 核心依赖

- **Tauri**：桌面应用容器
- **Roslyn**：C# JIT 编译和执行
- **three.js / ag-psd**：资产预览和可视化
- **Pinia**：Vue 状态管理
- **elkjs**：图可视化
- **vditor**：Markdown 编辑器
- **turndown**：HTML 转 Markdown

### 3.3 目录结构

```
Locus/
  src-tauri/         # Rust Tauri 后端
  src/               # Vue.js 前端
  locus_unity/       # Unity 端集成（含 Roslyn）
  agent/             # Agent 逻辑
  knowledge/         # 知识系统
  prompt/            # Prompt 模板
  tools/             # 工具集
  docs/              # 文档
  scripts/           # 构建脚本
```

## 四、安装和构建

### 4.1 安装

推荐从 [Releases](https://github.com/r1n7aro/Locus/releases) 下载安装程序（Windows NSIS installer）。

### 4.2 从源码构建

```powershell
# 开发模式
bun tauri dev

# 构建
bun tauri build
```

## 五、与 unity-mcp / unity-cli-loop 对比

| 维度 | Locus | unity-mcp | unity-cli-loop |
|---|---|---|---|
| Stars | 460 | 9.7K | 370 |
| 架构 | Rust+Tauri 独立应用 | Unity 插件+TS 服务 | Unity Package+Node CLI |
| 进程 | 独立于 Unity | 独立进程（MCP） | Unity 内/CLI 调用 |
| 嵌入方式 | Windows API 嵌入 Unity 窗口 | MCP 协议 | Unity Package |
| 核心能力 | 语义编辑+知识系统+版本控制 | 资源/场景/脚本/构建 | AI 自主循环+PlayMode 测试 |
| 技术亮点 | Roslyn JIT、状态机调试 | MCP Server | Skills 驱动循环 |

Locus 是三者中架构最重但能力最深的方案，unity-mcp 是最轻量的 MCP 方案，unity-cli-loop 专注于 AI 自主开发循环。

## 六、项目信息

- **Stars**：460
- **Forks**：54
- **语言**：Rust（核心）+ TypeScript/Vue.js（前端）+ C#（Unity 集成）
- **许可证**：GPL-3.0-or-later
- **版本**：v0.2.15（早期测试阶段 v0.2.8）
- **平台**：Windows（当前唯一支持）
- **创建时间**：2026-04-22
- **Topics**：ai, ai-agent, codex, gamedev, llm, rust, unity
- **文档**：https://unity.farlocus.com/en
- **Roadmap**：https://unity.farlocus.com/en/overview/roadmap