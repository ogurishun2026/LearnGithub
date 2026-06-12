# happy 研究总结

> 仓库地址：https://github.com/slopus/happy
> 研究日期：2026-06-13

## 一、仓库概述

**一句话定位**：Claude Code 和 Codex 的**移动 + Web + CLI** 客户端，端到端加密，让你随时随地从手机控制电脑上跑着的 AI 编码 Agent。

**为什么火**：21.8K Stars / 1.8K Forks，2025-07 创建仅一年达到该量级，是把"AI 编码体验"从桌面搬到移动端的代表项目。MIT 协议。已上架 iOS App Store / Google Play / Web，配套域名 https://happy.engineering。

**核心场景**：你在咖啡馆/通勤路上想看 Claude Code 跑得怎么样了——以前只能等回到电脑前；用 Happy 后，电脑上 Agent 还在跑，手机能实时看进度、批准/拒绝权限请求、收到错误推送。

**作者来历**：README 自述"散落在 Bay Area 咖啡馆和 hacker house 的工程师们，午饭时不停查自家 AI 在 side project 上跑到哪一步了"——典型 scratch-your-own-itch 项目。

## 二、核心内容

### 2.1 工作流（核心 3 步）

```bash
# 1. 下载 iOS/Android/Web App

# 2. 在电脑上装 CLI（包名从 happy-coder 迁移来的）
npm install -g happy

# 3. 用 happy 包装命令运行
happy claude        # 替代 claude
happy codex         # 替代 codex
```

启动后 Agent 在你电脑上正常跑；当你想从手机控制时，它会"重启会话进入 remote 模式"；想切回电脑——按任意键即可。

### 2.2 5 大产品差异点

| 卖点 | 说明 |
|------|------|
| 📱 移动访问 Claude Code / Codex | 离开桌子也能看 AI 在搞什么 |
| 🔔 推送通知 | Agent 需要批准权限或报错时推送告警 |
| ⚡ 一键设备切换 | 手机/桌面间瞬时切换控制权 |
| 🔐 端到端加密 | 代码离开设备前先加密，服务器看不到明文 |
| 🛠️ 开源可审计 | MIT，无 telemetry / tracking（仅匿名 PostHog 事件且可关） |

### 2.3 端到端加密（零知识架构，PRIVACY.md 摘要）

- **加密内容**：所有对话和代码片段在设备本地加密后才传输
- **密钥**：配对设备时**密钥本身也是加密传输**，服务器无能力解密
- **服务器看到的元数据**：消息 ID、时间戳、匿名设备 ID、会话 ID、Expo 推送 token（**无内容**）
- **分析**：PostHog 只收匿名事件（用密钥派生的匿名 ID），可在 App 内关闭
- **订阅**：Revenue Cat 管理（账户 ID 与 PostHog 匿名 ID **不互通**）

### 2.4 商业化与组织

- 订阅模型走 Revenue Cat
- 域名 `happy.engineering`，团队叫 **Happy Coder** / 组织 **slopus**
- 配套 Discord 社区、官方 Docs Site、独立的 docs 仓库 `slopus/slopus.github.io`

## 三、技术架构

### 3.1 仓库结构（pnpm Monorepo，7 个子包）

```
happy/
├── packages/
│   ├── happy-app/         # Expo（React Native + Web）UI 主体
│   ├── happy-agent/       # Remote agent 控制 CLI（创建、发送、监听 session）
│   ├── happy-cli/         # 命令行入口（happy claude / happy codex）
│   ├── happy-server/      # 后端服务（加密同步）
│   ├── happy-wire/        # 通信协议层（client ↔ server）
│   ├── happy-app-logs/    # 日志查看器
│   └── codium/            # VSCodium 桌面端集成（fork 自 VSCodium）
├── environments/          # tsx 环境管理器（new/list/use/up/down/seed/tailscale）
├── docs/                  # 贡献指南
├── Dockerfile             # 根 Dockerfile
├── Dockerfile.server      # 服务端镜像
├── Dockerfile.webapp      # Web 端镜像
├── PRIVACY.md             # 隐私政策（零知识加密说明）
├── AGENTS.md              # 子 Agent 配置
├── .agents/  .claude/  .codex/  .mcp.json  # 内嵌 AI Agent 体系
└── package.json           # pnpm@10.11.0，pnpm workspace
```

### 3.2 关键技术栈

| 技术 | 用途 |
|------|------|
| **Expo / React Native** | iOS + Android + Web 三端同构 |
| **electron** | 桌面端（codium 包，桌面 IDE） |
| **node-pty** | 在 Agent 进程中起伪终端，包装 claude/codex |
| **@more-tech/react-native-libsodium** | 端到端加密原语（NaCl/libsodium） |
| **@shopify/react-native-skia** | App 高性能渲染 |
| **prisma / better-sqlite3** | 服务端数据持久化 |
| **sharp** | 图像处理 |

### 3.3 内嵌 AI 工程化（值得抄）

仓库根目录就藏着完整的 AI 协作配置：
- `.agents/` 自定义子 Agent
- `.claude/` Claude Code 配置（含 skills/hooks）
- `.codex/` Codex 配置
- `.mcp.json` MCP（Model Context Protocol）配置
- `AGENTS.md` 子 Agent 文档

——**这家用 Claude Code 开发 Claude Code 的客户端，整个仓库是一份活的最佳实践参考**。

### 3.4 环境管理器（tsx 脚本）

`environments/environments.ts` 提供多环境隔离 CLI：

```bash
pnpm env:new        # 新建环境
pnpm env:use        # 切换
pnpm env:up         # 起完整本地栈（含 server）
pnpm env:tailscale  # 接入 Tailscale 私网
pnpm env:server / env:web / env:ios / env:android / env:cli
```

模板支持 `authenticated-empty` 等。对多端联调（iOS+Android+Web+server）很必要。

## 四、实际应用场景

### 4.1 直接价值——成为日常工作流

如果你已经用 Claude Code 或 Codex（你的全局 CLAUDE.md 大量使用 Claude Code + VIPER-5 体系），把 `claude` 替换成 `happy claude` 几乎零成本，立刻获得：

- 📱 通勤路上看任务进度
- 🔔 长任务（编译/测试/Agent 链）完成或卡住时推送提醒
- ⚡ 客厅笔电跑、卧室手机审批权限请求

特别适合**多个 VIPER-5 阶段串行跑很久**的场景：RESEARCH → INNOVATE → PLAN → EXECUTE 中途等很久时，手机上就能看到。

### 4.2 工程范式可借鉴

- **零知识加密客户端**的标准做法：libsodium + 设备配对 + 元数据/内容分离
- **pnpm monorepo 跨平台同构**：一份 TypeScript 代码出 iOS/Android/Web/Electron/Server 五端
- **环境管理器脚本**（tsx + Docker + Tailscale）：值得抄给你自己的多端项目
- **仓库自带 .claude/.codex/.mcp.json/AGENTS.md**：把 AI 协作配置作为代码资产纳入版本控制——这正是 vc-context-engineering 提倡的做法

### 4.3 跟你已有研究的关联

- 你的索引里 **opencode（序号 9，161K Stars）** 是 happy 的同类竞品但定位不同——opencode 是 CLI 本体，happy 是"已有 CLI 的移动遥控"
- 与 **vibe-kanban（序号 32）**、**Mexus（序号 11）** 互补——它们做"多 Agent 任务管理面板"，happy 做"移动遥控单 Agent 进度"
- **codedb-mcp（序号 27）** / **codegraph（序号 36）** 是 MCP 工具，happy 仓库的 `.mcp.json` 给了它们一个真实用例参考

### 4.4 风险与限制

- 仍依赖你电脑保持开机（happy 只是遥控器，**Agent 仍在你机器上跑**），不是云沙盒
- 商业模型偏 SaaS（Revenue Cat 订阅+服务端做同步），完全 self-host 需要自己跑 happy-server
- E2E 加密虽强，但 Claude/Codex 与官方厂商通信仍走它们自己的链路，不受 happy 加密保护

### 4.5 选型一句话

**你已经天天用 Claude Code / Codex + 想要移动端遥控 + 信端到端加密** → 没有理由不装 happy。

---

## 五、与本研究库其他条目的关系

- **序号 9** [opencode](../opencode/summary.md) — 同样是 AI 编码 Agent，但 opencode 是 CLI 本体，happy 是给现有 CLI 加移动遥控
- **序号 11** [Mexus](../Mexus/summary.md) — 本地多 CLI Agent 管理控制台，happy 是单 Agent 的移动延伸
- **序号 32** [vibe-kanban](../vibe-kanban/summary.md) — 看板式 Agent 任务管理，互补关系
- **序号 27** [codedb-mcp](../../Claude-Code-技能-插件/codedb-mcp/summary.md) — MCP 工具，可与 happy 仓库内嵌的 `.mcp.json` 一起看
