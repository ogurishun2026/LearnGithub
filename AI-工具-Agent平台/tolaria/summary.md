# tolaria 研究总结

> 仓库地址：https://github.com/refactoringhq/tolaria
> 研究日期：2026-06-14

## 一、仓库概述

**16,162 Stars · 1,099 Forks · TypeScript · AGPL-3.0 开源协议**

Tolaria 是一个**桌面应用**（macOS/Windows/Linux），用于管理 **Markdown 知识库**。创始人 Luca（Refactoring.fm 主播）本人每天使用，管理着 10,000+ 笔记的个人知识库。

## 二、核心定位

> "Files-first, Git-first, Offline-first, Zero lock-in"

Tolaria 倡导的是**把你的数据还给你**——纯 Markdown 文件 + Git 版本控制，完全离线运行，不需要任何账号和订阅。

## 三、设计原则

| 原则 | 说明 |
|------|------|
| **Files-first** | 纯 Markdown 文件，任何编辑器都能打开，无需导出 |
| **Git-first** | 每个 vault 都是 Git 仓库，享受完整版本历史 |
| **Offline-first** | 无账号、无订阅、无云依赖 |
| **Open source** | AGPL-3.0 协议 |
| **Standards-based** | Markdown + YAML frontmatter，无专有格式 |
| **Types as lenses** | 类型是导航辅助，不是强制模式 |
| **AI-first** | 为 AI Agent 优化，支持 Claude Code/Codex/Gemini CLI |
| **Keyboard-first** | 键盘优先，为高级用户设计 |
| **Built from real use** | 作者自己每天使用，10,000+ 笔记实战验证 |

## 四、技术架构

### 4.1 技术栈

| 层级 | 技术 |
|------|------|
| **桌面框架** | Tauri 2（Rust 后端） |
| **前端框架** | React 19 + TypeScript |
| **构建工具** | Vite |
| **样式** | Tailwind CSS 4 |
| **编辑器** | BlockNote（Notion-like 块编辑器）+ CodeMirror 6 |
| **图标** | Phosphor Icons |
| **AI SDK** | Anthropic SDK |
| **画布** | tldraw |
| **国际化** | Vitepress + lara-cli |
| **测试** | Vitest + Playwright |

### 4.2 目录结构

```
tolaria/
├── src/                      # React 前端源码
│   ├── App.tsx              # 主应用
│   ├── components/         # 组件
│   ├── hooks/              # React Hooks
│   ├── lib/                # 库函数
│   ├── extensions/         # 扩展
│   ├── types/              # TypeScript 类型
│   └── utils/              # 工具函数
├── src-tauri/               # Tauri Rust 后端
│   ├── src/                # Rust 源码
│   ├── tauri.conf.json     # Tauri 配置
│   └── Cargo.toml          # Rust 依赖
├── site/                    # Vitepress 文档站点
├── mcp-server/             # MCP 服务器
├── e2e/                    # 端到端测试
├── tests/                  # 单元测试
├── docs/                   # 架构文档
│   ├── ARCHITECTURE.md     # 系统架构
│   └── ABSTRACTIONS.md     # 核心抽象
└── package.json           # Node 依赖
```

### 4.3 核心抽象

从 ARCHITECTURE.md 看Tolaria 的核心抽象：

1. **Vault（知识库）**
   - 文件系统上的一个文件夹
   - 纯 Markdown + YAML frontmatter 文件
   - 是唯一真实数据源

2. **Note（笔记）**
   - 单个 `.md` 文件
   - 包含 YAML frontmatter 元数据和 Markdown 内容

3. **Type（类型）**
   - 通过 `type:` 字段标记
   - 类型决定图标、颜色、属性布局
   - 约定字段：`status:`, `url:`, `Workspace:`, `belongs_to:`, `related_to:`, `has:`, `start_date:`, `end_date:`

4. **Relation（关系）**
   - `belongs_to:` 归属关系
   - `related_to:` 关联关系
   - `has:` 包含关系

### 4.4 四面板 UI

Tolaria 采用类似 Bear Notes 的四面板布局：
- **侧边栏**：笔记列表、类型过滤
- **编辑器**：BlockNote 块编辑器
- **属性面板**：YAML frontmatter 编辑
- **预览/其他**：可选面板

## 五、主要功能

### 5.1 笔记管理
- 块级编辑器（Notion-like）
- Markdown + YAML frontmatter
- 类型系统（图标 + 颜色）
- 双向链接（`[[wikilink]]`）
- 代码高亮（Shiki）
- 数学公式（KaTeX）
- Mermaid 图表

### 5.2 搜索与导航
- 全文搜索
- 类型过滤
- 关系导航（belongs_to / related_to / has）
- 快速打开（Command Palette）

### 5.3 AI 集成
- **AGENTS.md**：为 AI Agent 提供上下文
- 支持 Claude Code、Codex CLI、Gemini CLI
- MCP 服务器（`mcp-server/`）
- AI-first 但不 AI-only

### 5.4 同步与版本控制
- Git 集成
- 离线优先
- 零云依赖

### 5.5 国际化
- Vitepress 文档站点
- lara-cli 翻译工具

## 六、与 Obsidian/Logseq 的对比

| 特性 | Tolaria | Obsidian | Logseq |
|------|---------|----------|--------|
| **Stars** | 16K | 72K+ | 24K+ |
| **许可证** | AGPL-3.0 | Proprietary* | AGPL-3.0 |
| **桌面框架** | Tauri | Electron | Electron |
| **编辑器** | BlockNote | CodeMirror/Legacy | BlockNote |
| **Git 集成** | 内置 | 插件 | 插件 |
| **AI 优先** | ✅ 内置 | 插件 | 插件 |
| **离线优先** | ✅ | 插件 | 插件 |
| **移动端** | ❌ | ✅ | ✅ |
| **本地数据** | ✅ | ✅ | ✅ |

*Obsidian 核心免费，付费功能包括 Sync 和 Publish

## 七、开发者文档

| 文档 | 内容 |
|------|------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | 系统设计、技术栈、数据流 |
| [ABSTRACTIONS.md](docs/ABSTRACTIONS.md) | 核心抽象和模型 |
| [GETTING-STARTED.md](docs/GETTING-STARTED.md) | 代码库导航 |
| [ADRs](docs/adr) | 架构决策记录 |

## 八、本地开发

```bash
# 前提条件
# Node.js 20+, pnpm 8+, Rust stable

# 安装依赖
pnpm install

# 浏览器模式（快速预览）
pnpm dev

# 原生桌面应用
pnpm tauri dev

# 构建
pnpm build
```

**Linux 系统依赖**：
```bash
# Arch
sudo pacman -S --needed webkit2gtk-4.1 base-devel curl wget file openssl \
  appmenu-gtk-module libappindicator-gtk3 librsvg

# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \
  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev \
  libsoup-3.0-dev patchelf
```

## 九、MCP 服务器

Tolaria 内置 MCP 服务器，支持：
- 笔记读写
- 搜索
- Git 操作
- AI 工具调用

## 十、总结

Tolaria 是一个**专注于本地优先、隐私优先的 Markdown 知识库管理工具**。其独特之处在于：

- ✅ **Tauri 2** 构建，比 Electron 更轻量
- ✅ **BlockNote** 编辑器，现代 Notion-like 体验
- ✅ **内置 Git**，版本控制开箱即用
- ✅ **AI-first**，为 Agent 优化（AGENTS.md + MCP）
- ✅ **约定优于配置**，减少用户配置负担
- ⚠️ **无移动端**，目前只有桌面版
- ⚠️ **社区较小**（16K Stars vs Obsidian 72K）

适合人群：
- 注重隐私、不想用云服务的用户
- 需要 AI Agent 可读的笔记库
- 喜欢键盘操作、效率优先的开发者