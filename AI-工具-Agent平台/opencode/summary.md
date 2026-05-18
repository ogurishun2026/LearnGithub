# opencode 研究总结

> 仓库地址：https://github.com/anomalyco/opencode
> 研究日期：2026-05-18

## 一、仓库概述

opencode 是一个开源的 AI 编码 Agent，定位为"The open source coding agent"。它是一个基于 TypeScript 构建的全栈 AI 编码平台，支持多种 LLM 提供商，提供 CLI、桌面应用（Electron）、VS Code 扩展和 Zed 扩展等多种交互方式。拥有 161K+ Stars，是目前最受欢迎的开源编码 Agent 项目之一。

## 二、核心内容

### 核心功能

- **AI 编码 Agent**：支持多种 LLM 提供商（Anthropic、OpenAI、Azure、Cloudflare 等），内置智能体循环
- **多端交互**：CLI 终端、Electron 桌面应用、VS Code 扩展、Zed 编辑器扩展
- **MCP 协议支持**：完整的 Model Context Protocol 集成，支持外部工具扩展
- **Skill 系统**：内置技能发现与执行框架
- **LSP 集成**：语言服务协议客户端，支持代码诊断与补全
- **Worktree 管理**：Git worktree 隔离工作区
- **PTY 支持**：伪终端集成，支持 Shell 命令执行
- **权限系统**：细粒度的操作权限控制（shell 执行、文件写入、MCP 工具等）
- **会话管理**：完整的会话持久化、压缩（compaction）、重试、回滚
- **Plan 模式**：内置计划模式的进入/退出流程
- **企业版功能**：独立的企业版包，支持 SSO/AUTH 集成

### 内置工具清单

opencode 内置了丰富的工具集：

| 工具 | 功能 |
|------|------|
| read | 文件读取 |
| write | 文件写入 |
| edit | 文件编辑 |
| shell | Shell 命令执行 |
| glob | 文件模式匹配 |
| grep | 内容搜索 |
| lsp | LSP 诊断 |
| mcp-websearch | MCP 网页搜索 |
| plan | 计划模式 |
| question | 交互式提问 |
| apply_patch | 补丁应用 |
| webfetch | 网页获取 |
| websearch | 网页搜索 |
| skill | 技能调用 |
| task | 任务管理 |
| task_status | 任务状态 |
| todo | 待办管理 |
| repo_clone | 仓库克隆 |
| repo_overview | 仓库概览 |

### 插件系统

内置 GitHub Copilot 插件，同时支持 Azure、Cloudflare、DigitalOcean、Codex 等提供商插件。

## 三、技术架构

### 顶层目录结构

```
opencode/
├── packages/          # 核心包集合
│   ├── opencode/      # 主包：CLI + Agent 核心
│   ├── core/          # 核心共享库
│   ├── ui/            # Vite 前端 UI
│   ├── desktop/       # Electron 桌面应用
│   ├── llm/           # LLM SDK 封装
│   ├── enterprise/    # 企业版
│   ├── extensions/    # 编辑器扩展（Zed）
│   └── ...
├── sdks/              # 外部 SDK（VS Code 扩展）
├── infra/             # 基础设施配置
├── script/            # 构建脚本
└── specs/             # 规格文档
```

### 主包 (packages/opencode) 内部架构

```
src/
├── agent/        # Agent 核心循环与子 Agent 权限
├── cli/          # CLI 入口与命令
├── config/       # 配置系统（24+ 配置文件）
├── mcp/          # MCP 协议客户端与服务端
├── tool/         # 内置工具实现（40+ 工具）
├── session/      # 会话管理（持久化、压缩、重试、回滚）
├── provider/     # LLM 提供商适配层
├── permission/   # 权限评估系统
├── skill/        # 技能发现与执行
├── lsp/          # LSP 客户端/服务端
├── storage/      # SQLite 存储层
├── shell/        # Shell 命令执行
├── worktree/     # Git worktree 管理
├── plugin/       # 插件加载器
├── ide/          # IDE 集成
├── pty/          # 伪终端（Bun/Node 双实现）
├── format/       # 代码格式化
├── git/          # Git 操作
├── auth/         # 认证（OAuth）
├── server/       # HTTP 服务
├── sync/         # 同步机制
├── share/        # 分享功能
├── snapshot/     # 快照
├── reference/    # 引用系统
├── v2/           # V2 架构（渐进迁移）
└── ...
```

### 技术栈

| 维度 | 技术 |
|------|------|
| 语言 | TypeScript |
| 运行时 | Bun（主）+ Node.js（兼容） |
| 包管理 | Bun（bun.lock） |
| 构建 | Turborepo（monorepo） |
| 存储 | SQLite（drizzle-orm） |
| 前端 | Vite + React |
| 桌面 | Electron |
| 测试 | Bun test |
| CI/CD | SST（Serverless Stack） |
| 许可证 | MIT |

### 关键设计特点

1. **Monorepo 架构**：使用 Turborepo 管理多包，包含 20+ 子包
2. **Bun 优先**：运行时和包管理均基于 Bun，PTY/DB 有 Bun/Node 双实现
3. **SQLite 持久化**：会话和状态通过 SQLite（drizzle-orm）持久化
4. **V2 迁移**：src/v2/ 目录包含渐进式架构迁移，含 provider-parity-checklist
5. **Effect 系统**：cli/ 下有 effect-cmd.ts，使用 Effect-TS 风格的错误处理
6. **多语言 README**：支持 20+ 种语言的 README 文档

## 四、实际应用场景

1. **AI 编码助手**：作为日常编码的 AI Agent，支持代码生成、编辑、调试
2. **多 IDE 集成**：在 VS Code / Zed / 终端中统一使用
3. **MCP 工具扩展**：通过 MCP 协议连接外部工具和服务
4. **企业部署**：企业版支持 SSO 和自定义提供商
5. **技能系统**：自定义编码技能的发现和执行
6. **团队协作**：会话分享、快照、同步功能支持团队场景
