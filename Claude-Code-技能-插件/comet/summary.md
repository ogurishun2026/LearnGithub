# comet 研究总结

> 仓库地址：https://github.com/rpamis/comet
> 研究日期：2026-05-26

## 一、仓库概述

Comet（彗星）是一个结合 OpenSpec 和 Superpowers 双星开发工作流的工具。OpenSpec 处理 WHAT（轮廓、提案、规范生命周期、归档），Superpowers 处理 HOW（技术设计、规划、执行、wrap-up）。Comet 将两者整合成一个五阶段自动化管道，通过一个命令从想法到归档。

## 二、核心能力

### 2.1 五阶段开发流程

| 阶段 | 命令 | 所有者 | 产物 |
|---|---|---|---|
| 1. Open | `/comet-open` | OpenSpec | proposal.md, design.md, tasks.md |
| 2. Design | `/comet-design` | Superpowers | Design Doc, delta spec |
| 3. Plan & Build | `/comet-build` | Superpowers | Implementation plan, code commits |
| 4. Verify & Finish | `/comet-verify` | Both | Verification report, branch handling |
| 5. Archive | `/comet-archive` | OpenSpec | delta spec sync, status annotation |

### 2.2 核心功能

| 功能 | 说明 |
|---|---|
| 自动状态检测 | 自动识别当前 Spec 所处阶段 |
| 动态阶段路由 | 根据状态自动分发到下一阶段 |
| 子agent驱动开发 | 支持子agent驱动的开发方式 |
| 代码审查 | 内置代码审查能力 |
| 计划写作 | 支持计划文档编写 |
| 归档同步 | 自动同步状态到归档 |

### 2.3 主要命令

| 命令 | 说明 |
|---|---|
| `comet init [path]` | 初始化 Comet 工作流 |
| `comet status [path]` | 显示活动变更和下一工作流命令 |
| `comet doctor [path]` | 诊断 Comet 安装状态 |
| `comet update [path]` | 更新 Comet 包和 skills |
| `comet -h` | 显示帮助 |
| `comet -v` | 显示版本 |

## 三、技术架构

### 3.1 技术栈

- **语言**：TypeScript
- **包管理器**：npm
- **支持平台**：28 个 AI 编码平台

### 3.2 支持的平台

| 平台 | Skills 目录 | 平台 | Skills 目录 |
|---|---|---|---|
| Claude Code | `.claude/` | JetBrains | `.jetbrains/` |
| Codium | `.codium/` | LlamaIndex | `.llamaindex/` |
| Continue | `.continue/` | Lovable | `.lovable/` |
| Cursor | `.cursor/` | Qwen Code | `.qwen/` |
| Deepseek | `.deepseek/` | Roo Code | `.roo/` |
| GitHub Copilot | `.github/` | Continue | `.continue/` |
| Kilo Code | `.kilocode/` | Augment | `.augment/` |
| Junie | `.junie/` | CodeBuddy | `.codebuddy/` |
| Cospect | `.cospect/` | Crusht | `.crusht/` |
| Factory | `.factory/` | iFlow | `.iflow/` |
| Llum | `.llum/` | Pi | `.pi/` |
| Antrhopic | `.agents/` | Bob Shell | `.bob/` |
| ForgeCode | `.forge/` | Trae | `.trae/` |

### 3.3 状态管理

Comet 使用解耦的状态架构，YAML 文件分离：

| 文件 | 所有者 | 用途 |
|---|---|---|
| `.openspec.yaml` | OpenSpec | Spec 生命周期、变更元数据 |
| `.comet.yaml` | Comet | 工作流阶段、执行模式、验证状态 |

### 3.4 安装

```bash
npm install -g @rpamis/comet
cd your-project
comet init
```

## 四、项目信息

- **Stars**：216
- **语言**：TypeScript
- **许可证**：MIT
- **创建者**：rpamis
- **创建时间**：2025-06-14
- **Topics**：openspec, superpowers, agentic, workflow, claude-code

## 五、核心设计理念

1. **引导而非强制**：每个阶段验证前置条件才执行
2. **状态驱动**：Script 后端状态机保证相位转换可靠性
3. **双重规范结合**：OpenSpec（WHAT）+ Superpowers（HOW）
4. **Agent 循环自动化**：通过脚本实现状态更新、验证、归档同步