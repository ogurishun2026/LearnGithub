# open-design 研究总结

> 仓库地址：https://github.com/nexu-io/open-design
> 研究日期：2026-05-17

## 一、仓库概述

Open Design 是一个**开源的 AI 驱动设计工具**，定位为 Anthropic Claude Design / Figma 的开源替代品。Local-first 架构，支持 BYOK（自带 API Key），通过调用本地 CLI Agent（Claude Code、Codex、Cursor Agent、Gemini CLI 等 16 种）作为设计引擎，配合 131 个可组合 Skills 和 151 个品牌级设计系统，生成 Web/Desktop/Mobile 原型、演示文稿、图片、视频等设计产物。

- Stars: 43,201 | Forks: 4,924 | License: Apache-2.0
- 主语言：TypeScript（13.7M），辅以 HTML（8.7M）、CSS（1.2M）
- 版本：v0.7.0（当前），v0.8.0-preview 开发中
- 两周内获 40K Stars，增长极快

## 二、核心内容

### 2.1 产品形态

| 组件 | 说明 |
|------|------|
| **Web App** | Next.js 16 + React 18 的 Web 界面 |
| **Desktop App** | Electron 桌面客户端 |
| **Daemon** | 本地守护进程（`od` 命令），管理 Agent 调度、Skills、设计系统、产物 |
| **Packaged** | 打包版 Electron 运行时 |

### 2.2 核心能力

**多 Agent 驱动**：自动检测 PATH 上的 16 种 CLI Agent：
- Claude Code、Codex、Devin for Terminal、Cursor Agent
- Gemini CLI、OpenCode、Qwen、Qoder CLI、GitHub Copilot CLI
- Hermes、Kimi、Pi、Kiro、Kilo、Mistral Vibe、DeepSeek TUI
- 无 CLI 时回退到 OpenAI 兼容的 BYOK 代理

**131 个 Skills**（设计技能）：
- 设计类：canvas-design、frontend-design、swiftui-design、flutter-animating-apps
- 原型类：web-prototype、mobile-app、login-flow、faq-page
- 演示文稿：slides、ppt-keynote、pptx-generator、html-ppt-* 系列（20+ 模板）
- 图片/视频：imagegen、fal-* 系列（3D/图片/视频编辑/唇形同步/放大）、sora、remotion
- 设计系统：design-brief、design-review、brand-guidelines、color-expert
- Figma 集成：figma-generate-design、figma-create-design-system-rules 等
- 动效：gsap-core、gsap-react、gsap-scrolltrigger、shader-dev、threejs
- 文档：pdf、docx、minimax-docx、minimax-pdf
- 其他：brainstorming、copywriting、competitive-ads-extractor、domain-name-brainstormer

**151 个品牌设计系统**：从 Airbnb、Apple、BMW 到 Vercel、WeChat、小红书，覆盖主流品牌视觉规范。

**100+ 设计模板**：PPT、Landing Page、Dashboard、社交卡片、原型等即用模板。

### 2.3 产出格式

- Web 原型（HTML/CSS/JS）
- Desktop / Mobile 原型
- 演示文稿（PPTX、HTML 幻灯片）
- 图片（PNG/JPG/SVG）
- 视频（MP4、HyperFrames）
- PDF / DOCX 文档
- 沙盒化预览 + 导出

## 三、技术架构

### 3.1 项目结构（Monorepo）

```
open-design/
├── apps/
│   ├── web/              # Next.js 16 + React 18 Web 界面
│   ├── daemon/           # 本地守护进程（Express + SQLite + MCP）
│   ├── desktop/          # Electron 桌面客户端
│   ├── packaged/         # 打包版 Electron 入口
│   ├── landing-page/     # 落地页
│   └── telemetry-worker/ # 遥测 Worker
├── packages/
│   ├── contracts/        # Web/Daemon 共享契约层（纯 TS，无框架依赖）
│   ├── platform/         # OS 进程原语
│   ├── sidecar/          # Sidecar 通用运行时
│   ├── sidecar-proto/    # Sidecar 业务协议
│   ├── agui-adapter/     # AG-UI 适配器
│   ├── plugin-runtime/   # 插件运行时
│   └── registry-protocol/# 注册协议
├── tools/
│   ├── dev/              # 开发生命周期管理
│   ├── pack/             # 打包构建
│   └── pr/               # PR 审查工具
├── skills/               # 131 个设计技能
├── design-systems/       # 151 个品牌设计系统
├── design-templates/     # 100+ 设计模板
├── craft/                # 设计工艺规范（排版、色彩、动画、无障碍等）
├── plugins/              # 插件体系（官方 + 社区）
├── specs/                # 规范文档
├── docs/                 # 文档
└── e2e/                  # Playwright E2E 测试
```

### 3.2 关键技术栈

| 层 | 技术 |
|----|------|
| 前端 | Next.js 16, React 18, TypeScript |
| 后端 | Express, Better-SQLite3, MCP SDK |
| 桌面 | Electron |
| 构建 | pnpm workspace, Turbo-like monorepo |
| AI 集成 | MCP（Model Context Protocol）, AG-UI Adapter |
| 包管理 | Corepack, pnpm@10.33.2 |
| 运行时 | Node ~24 |
| 部署 | Vercel（Web）, Docker, Nix |

### 3.3 架构设计亮点

- **Daemon 架构**：本地守护进程管理 Agent 生命周期、技能调度、产物管理，Web 通过 HTTP API 通信
- **BYOK 全层**：每个 AI 调用点都支持自带 Key，不强制绑定任何服务商
- **MCP 集成**：通过 `@modelcontextprotocol/sdk` 接入 Model Context Protocol
- **Plugin 体系**：`plugins/` 下有官方插件和社区插件，通过 registry-protocol 管理
- **Sidecar 模式**：隔离的辅助进程处理特定任务（桌面端的 IPC 通信等）
- **严格的架构约束**：`packages/contracts` 保持纯 TS、无框架依赖；app 间不互相导入私有代码

### 3.4 发布渠道

| 渠道 | 说明 |
|------|------|
| stable | 正式发布，依赖 nightly 验证 |
| nightly | 内部验证，stable 的前置 |
| preview | 独立早期访问，preview 版本号 |
| beta | 每日 R&D 开发验证 |

## 四、实际应用场景

### 4.1 快速原型设计

- 通过自然语言描述 + AI Agent 自动生成 Web/Mobile/Desktop 原型
- 选择品牌设计系统（如 Apple、Airbnb），AI 自动遵循品牌规范
- 适合产品经理、独立开发者快速验证想法

### 4.2 演示文稿生成

- 20+ PPT 模板，涵盖技术分享、产品发布、周报、投行路演等
- AI 根据内容自动排版，导出 PPTX 或 HTML 幻灯片
- 支持演讲者模式（reveal.js）

### 4.3 设计系统学习

- 151 个品牌设计系统是学习 UI 设计规范的宝库
- 每个系统有 `DESIGN.md` 文件，描述品牌的色彩、排版、间距等
- `craft/` 目录提供通用的设计工艺规则（排版层级、色彩理论、动效规范等）

### 4.4 开发者参考

- **大型 Monorepo 架构**：pnpm workspace + 多 package 的依赖管理和边界约束
- **Agent 集成模式**：如何让 AI Agent 与设计工具深度集成
- **MCP 实践**：`@modelcontextprotocol/sdk` 的实际使用
- **Plugin 系统设计**：可扩展的插件注册协议和运行时
- **多平台分发**：Web + Desktop + Packaged 三端发布

### 4.5 与本项目的关联

- 作为**前端 / UI 设计工具**的代表，其 Skills 系统和 Plugin 架构值得参考
- 与 Warp 的 Skills 系统对比：Warp 的 Skills 面向终端 Agent，Open Design 的 Skills 面向设计生成
- 其品牌设计系统库和工艺规范可作为 UI 开发的参考资源
