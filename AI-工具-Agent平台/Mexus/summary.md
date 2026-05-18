# Mexus 研究总结

> 仓库地址：https://github.com/yofine/Mexus
> 研究日期：2026-05-18

## 一、仓库概述

Mexus (M.E.X.U.S. = Multi-agent Execution Unified System) 是一个本地 Web 控制台，用于在单个浏览器界面中同时管理多个 CLI AI Agent 实例的并行协作。它将分散的 CLI AI Agent 统一成一个本地系统：运行、观察、审查工作，都在一个操作控制台完成。

### 基本信息

| 维度 | 数据 |
|------|------|
| 正式名称 | Mexus (原名 Nexus，已 rebranding) |
| Stars | 75 |
| Forks | 4 |
| 主要语言 | TypeScript |
| 许可证 | Apache License 2.0 |
| 创始人 | yofine |
| 创建时间 | 2026-03-07 |
| 网站 | https://mexus.ai |

### 标签

`agent` `agent-team` `agent-teams` `ai` `harness-engineering` `llm` `multiagent`

## 二、核心内容

### 主要功能特性

#### 1. 多 Agent 执行管理
- 支持多种 Agent：Claude Code、OpenCode、Aider、Codex、Gemini
- 每个 Agent 作为托管的执行面板运行
- 支持创建、关闭、重启、恢复 Agent 执行
- 实时状态指示器（running / waiting / idle / stopped / error）
- 浮动底部 shell 终端，随时可访问

#### 2. Git Worktree 隔离
- 每个 Agent 可以在独立的 Git worktree 中工作
- 并行开发独立分支，无冲突
- 面板标题显示分支名和文件变更数

#### 3. 运行时观察
- 自动解析 Claude Code statusline 获取运行时信息
- 实时显示模型名、上下文使用率、累计成本、会话 ID
- Agent 状态持久化到 `.nexus/` 目录，支持本地会话连续性

#### 4. 统一审查界面
- 实时文件树，带自动变更检测（chokidar）
- 内置代码查看器，支持 Shiki 语法高亮
- Git diff 面板，支持仓库级变更检查

#### 5. 快捷键与命令面板
- `Cmd/Ctrl+K` — 打开命令面板
- `Cmd/Ctrl+N` — 新建 Agent 面板
- `Cmd/Ctrl+1-9` — 切换面板
- `Cmd/Ctrl+G` — 打开 Git diff
- 主题切换通过命令面板

#### 6. 主题与布局
- 可调节四栏布局：侧边栏 / Agent 面板 / 编辑器 / 文件树
- 7 种内置主题：Dark IDE、GitHub Dark、Dracula、Tokyo Night、Catppuccin、Nord、Light IDE
- 响应式缩放适配大屏幕

#### 7. 配置系统
- 全局 (`~/.nexus/config.yaml`) 和项目级 YAML 配置驱动
- 每个 Agent 的工作目录和任务描述
- 会话启动模式：新会话或恢复先前会话

### 支持的 Agent 类型

| Agent | 类型 |
|-------|------|
| Claude Code | CLI |
| OpenCode | CLI |
| Aider | CLI |
| Codex | CLI |
| Gemini | CLI |

## 三、技术架构

### 技术栈

**后端**
- Node.js 22+
- TypeScript
- Fastify 5 + @fastify/websocket
- node-pty (终端进程管理)
- chokidar (文件监听)
- simple-git (Git 操作)

**前端**
- React 18
- TypeScript
- Vite 6
- Tailwind CSS v4
- xterm.js
- Zustand (状态管理)
- Shiki (语法高亮)
- react-diff-view
- cmdk (命令面板)

### 目录结构

```
Mexus/
├── packages/
│   ├── server/src/           # 后端 (~1530 行)
│   │   ├── cli.ts            # CLI 入口 (mexus start/init/status/stop)
│   │   ├── index.ts          # Fastify 服务编排，启动所有子服务
│   │   ├── types.ts          # 全局类型定义
│   │   ├── pty/
│   │   │   ├── PtyManager.ts     # node-pty 生命周期，滚动缓冲区 (512KB/pane)
│   │   │   └── StatuslineParser.ts # 从 Claude Code 输出提取 JSON 元数据
│   │   ├── workspace/
│   │   │   ├── WorkspaceManager.ts  # 状态中心，Set-based 多客户端事件分发
│   │   │   ├── ConfigManager.ts     # YAML 配置读写，Agent CLI 自动检测
│   │   │   └── AgentsYamlWriter.ts  # 防抖写 .nexus/agents.yaml (500ms)
│   │   ├── ws/handlers.ts    # WebSocket 事件路由
│   │   ├── fs/FsWatcher.ts   # chokidar 文件树监听 (depth 5, 防抖 300ms)
│   │   ├── git/GitService.ts # simple-git diff + .git/index 监听 (防抖 1s)
│   │   └── history/          # 终端历史管理
│   │
│   ├── web/src/              # 前端 (~2500 行)
│   │   ├── App.tsx           # 根组件，WebSocket→Store 事件路由
│   │   ├── types.ts          # 前端类型 (与 server 手动同步，无共享包)
│   │   ├── components/
│   │   │   ├── Layout.tsx         # 四栏布局 (Sidebar|AgentPanes|Editor|FileTree)
│   │   │   ├── Sidebar.tsx        # 左侧图标操作栏 (48px)
│   │   │   ├── AgentPane.tsx      # 单个 Agent 手风琴面板 (可折叠)
│   │   │   ├── Terminal.tsx       # xterm.js 封装
│   │   │   ├── BottomTerminal.tsx # 底部浮动 Shell (懒创建，agent='__shell__')
│   │   │   ├── EditorTabs.tsx     # 文件/Diff 标签页系统
│   │   │   ├── FileTree.tsx       # 递归文件树浏览器
│   │   │   ├── FileViewer.tsx     # Shiki 语法高亮代码查看器
│   │   │   ├── GitDiffPanel.tsx   # Git diff 展示 + 展开 hunks
│   │   │   ├── AddPaneDialog.tsx  # 新建 Agent Pane 弹窗
│   │   │   ├── CommandPalette.tsx # Cmd+K 命令面板 (cmdk)
│   │   │   ├── AgentIcon.tsx      # Agent 类型 SVG 图标
│   │   │   └── ResizeHandle.tsx   # 列拖拽分隔条
│   │   ├── stores/
│   │   │   ├── workspaceStore.ts     # Zustand 全局状态 (panes/tabs/files/diffs)
│   │   │   └── terminalRegistry.ts   # 全局 Map 终端写入注册表 (不走 React)
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts       # WS 连接 + 指数退避重连
│   │   │   └── useKeyboardShortcuts.ts # 全局快捷键
│   │   └── styles/globals.css        # 7 套主题 + CSS Variables + 响应式缩放
│   │
│   ├── diff-viewer/         # Diff 展示包
│   ├── file-tree/           # 文件树组件包
│   ├── mexus-plugin/        # 插件系统
│   ├── mexus-terminal/      # 终端封装包
│   ├── mexus-ui/            # UI 组件库
│   └── plugin-agent-team/   # Agent Team 插件
│
├── agent-team/              # Agent Team 相关
├── change-logs/            # 变更日志
├── design/                 # 设计文档
├── doc_site/               # 文档站点
├── docs/                   # 设计文档
├── observer_logs/          # 观察日志
│
├── .claude/                # Claude Code 配置
├── .codex                  # Codex 配置
├── AGENTS.md               # Agent 配置说明
├── BLUEPRINT.md            # 架构蓝图
├── CLAUDE.md               # Claude Code 指示
├── package.json            # pnpm monorepo 根配置
├── pnpm-lock.yaml          # 锁定文件
└── README.md               # 项目说明
```

### 关键设计决策

1. **Shell 套壳启动** — 不直接 spawn Agent CLI，而是先启动 shell，800ms 后发送命令。确保 .bashrc/.zshrc 环境变量正确加载。

2. **终端输出旁路 React** — `terminalRegistry.ts` 用全局 `Map<paneId, writeFn>` 存储 xterm 写入函数。WebSocket 数据直接写入 xterm，不经过 React state，避免高频输出导致的性能问题。历史缓冲区限制 10000 chunks。

3. **Set-based 多客户端事件** — WorkspaceManager 的每类事件维护 `Set<listener>`。每个 WebSocket 客户端连接时注册监听器，断开时只移除自己的，互不影响。

4. **agents.yaml 互感知** — 所有 Agent pane 的运行状态实时写入 `.nexus/agents.yaml`（防抖 500ms），Agent 可以读取此文件感知其他 Agent 的存在和状态。

5. **StatuslineParser** — Claude Code 的 statusline API 会在终端输出中插入 JSON 行。Parser 检测并提取 `model/session_id/cost_usd/context_used_pct` 等字段，从输出中剥离后广播为 `pane.meta` 事件。

6. **类型手动同步** — server 和 web 各有独立的 `types.ts`，没有共享包。修改协议时需同时更新两处。

### 数据流

```text
浏览器 ←──WebSocket──→ Fastify Server
  │                        │
  │  terminal.input ──→    │──→ PtyManager.write(paneId, data) ──→ node-pty
  │  ←── terminal.output   │←── PtyManager.onData callback
  │                        │
  │  pane.create ──→       │──→ WorkspaceManager.createPane()
  │  ←── workspace.state   │      → PtyManager.spawn() → Shell → Agent CLI
  │                        │      → ConfigManager.save()
  │  ←── fs.tree           │←── FsWatcher (chokidar)
  │  ←── git.diff          │←── GitService (simple-git)
  │  ←── pane.meta         │←── StatuslineParser (Claude Code JSON)
```

## 四、实际应用场景

### 场景 1：多 Agent 并行开发
当需要多个 AI Agent 同时处理不同任务时（如一个写前端、一个做后端、一个写测试），Mexus 提供统一界面管理和监控所有 Agent 的执行状态。

### 场景 2：Git Worktree 隔离开发
团队成员可以在独立分支上并行工作，每个分支由不同 Agent 处理，Mexus 显示分支状态和文件变更，避免相互干扰。

### 场景 3：代码审查与协作
通过内置的 diff 查看器和文件树，可以统一审查多个 Agent 的工作成果，适合需要 AI Agent 辅助编码的团队。

### 场景 4：大型项目的 Agent 协调
对于需要协调多个专业 Agent（前端、后端、DevOps、安全等）的大型项目，Mexus 提供了中央控制台来管理这些 Agent 的生命周期。

## 五、使用方法

### 安装

```bash
# 全局安装
npm install -g mexus-cli
```

### 常用命令

```bash
# 推荐：启动 Mexus Hub
mexus hub

# 直接启动单个工作区
mexus

# 指定项目路径启动
mexus ~/projects/my-app

# 初始化项目配置
mexus init ~/projects/my-app

# 检查工作区状态
mexus status

# 停止服务器
mexus stop

# 自定义端口
NEXUS_PORT=8080 mexus

# 自定义 Hub 端口
NEXUS_HUB_PORT=8081 mexus hub
```

### 开发模式

```bash
# 安装依赖
pnpm install

# 开发模式（构建前端，然后启动带 watch 的服务器）
pnpm dev

# 全开发模式（前端 + 后端热重载并行）
pnpm dev:full

# 生产构建
pnpm build

# 启动生产服务器
pnpm start
```

### 配置

配置文件位于：
- 全局配置：`~/.nexus/config.yaml`
- 项目配置：`.nexus/config.yaml`

## 六、版本信息

- **当前版本**：3.7.0
- **引擎要求**：Node.js >= 22
- **包管理器**：pnpm

## 七、注意事项

1. 项目从 Nexus 更名为 Mexus，但部分内部路径和兼容性标识符仍使用历史名称 Nexus，以保持现有项目和配置的兼容性。

2. "Mexus" 和 "M.E.X.U.S." 是 yofine 的商标。Apache License 2.0 不授予使用这些名称的权限，fork 版本需要重新命名。

3. 终端历史存储在 `.nexus/history/` 目录，agents.yaml 存储运行时状态，这两个目录都被 gitignore。
