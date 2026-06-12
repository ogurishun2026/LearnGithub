# lunel 研究总结

> 仓库地址：https://github.com/lunel-dev/lunel
> 研究日期：2026-06-13

## 一、仓库概述

**一句话定位**：AI 驱动的**移动 IDE + 云开发平台**——"在手机上写代码，跑在自己机器上或安全云沙盒里"。

**为什么值得看**：1.0K Stars / 112 Forks（MIT 协议），2026-02-04 创建，4 个月做到这个量级，节奏快；自带 Rust 实现的 PTY 后端（基于 wezterm fork），工程化诚意足。域名 https://lunel.dev，公共网关 gateway.lunel.dev。

**与 happy 的差异**：happy 是"已有 Claude/Codex CLI 的移动遥控"，lunel 是"完整的移动 IDE + 未来云沙盒"——一个是包装器，一个想做自有平台。

**主语言**：TypeScript（app/cli/manager/proxy）+ Rust（pty）+ 预留 Go（sandman 沙盒，未发）。

## 二、核心内容

### 2.1 两种使用模式

| 模式 | 说明 | 状态 |
|------|------|------|
| **Lunel Connect** | 用手机远程使用自己 PC，不用搞 SSH，专为编码场景设计 | ✅ 已就绪 |
| **Lunel Cloud** | 云端安全沙盒（猜测：Firecracker 类 microVM）| 🚧 Coming soon |

### 2.2 5 大组件（每个都是独立子目录）

```
lunel/
├── app/      — Expo/React Native 移动 app（iOS/Android/Web）
├── cli/      — lunel-cli（Node.js + TypeScript）
├── manager/  — Manager 服务（Bun，会话控制面）
├── proxy/    — Proxy 服务（Bun，WebSocket 数据面）
└── pty/      — Rust PTY 二进制（基于 wezterm 内部库做渲染）
```

### 2.3 各组件特性详解

**App（Expo）**
> "App is just a dumb client with most logic on cli"——APP 是哑客户端，主逻辑在 CLI 端

- 文件浏览与编辑
- Git 集成
- 终端模拟器
- 进程管理
- **22 种语言本地化**：en/zh/ja/ko/es/pt/de/fr/vi/ru/id/pl/tr/it/nl/sv/uk/fi/zh-TW/tw/ms/es-MX
- `app/` 内部还包含 `DESIGN.md` / `context.md` / `extra-design.md`、Hot Updater 配置（`.env.hotupdater.example`）、`eas.json`（Expo Application Services）

**CLI（`npx lunel-cli`）**

Node.js CLI 通过 WebSocket 把本地机器桥到 App，能力包括：
- 文件系统操作（read/write/grep…）
- Git 命令（status/commit/push/pull…）
- 终端 spawn
- 进程管理
- 端口扫描
- 系统监控（CPU/内存/磁盘/电池）

**Manager + Proxy（都用 Bun 写）**

Bun 的 WebSocket 中继服务，用 session code 连接 CLI 和 App。公共版部署于 `gateway.lunel.dev`：
- Session 管理（**10 分钟 TTL**）
- 双通道架构（control + data 分离）
- QR code 配对

**PTY（Rust）**

```
Rust binary for pseudo-terminal management
- Real PTY sessions via wezterm fork on github.com/sohzm/wezterm
- Screen buffer as cell grid (char + fg + bg per cell)
- 24fps render loop (only sends updates when content changes)
- JSON line protocol over stdin/stdout
```

亮点：
- 真实 PTY 会话基于 **wezterm fork**（一个真正的现代终端模拟器），不是简单的 readline
- 屏幕缓冲建模为单元格网格（字符 + 前景色 + 背景色）
- **24fps 渲染循环**（仅在内容变化时发更新，省带宽省电）
- 通过 stdin/stdout 的 JSON 行协议与 CLI 通信

**Sandman（未发）**

Makefile 预留了 `sandman-build/run/test/tidy` 目标（Go 语言），README 提到 "Not yet added"——这就是未来 **Lunel Cloud** 的沙盒底座。

## 三、技术架构

### 3.1 Makefile 编排（5 大组件一统）

```makefile
make install     # 装 app + cli + gateway + sandman 所有依赖
make dev         # 并行启动 gateway + app dev 服务
make build       # 编译 cli + sandman

# 各组件独立目标
make app-android | app-ios | app-web | app-start
make cli-build | cli-dev
make manager-dev | manager-start
make proxy-dev | proxy-start
make pty-build | pty-dev
```

### 3.2 关键工程决策

| 决策 | 用意 |
|------|------|
| App 设计为 dumb client | 业务逻辑集中在 CLI，更新 App 频率低 |
| Manager / Proxy 分离 | 控制面（session 配对、QR）与数据面（实际流量）独立扩展 |
| Bun 写后端 | 启动快、内存低、ts 原生 |
| Rust 写 PTY | 终端渲染性能/正确性强需求，wezterm 是黄金参考 |
| 24fps + diff-only 推送 | 移动网络省流量、省电 |
| 10 分钟 session TTL | 安全（短期凭证）但允许临时断网重连 |
| Go 预留 sandman | 容器/沙盒生态成熟（Firecracker/runc/gVisor 都 Go） |

### 3.3 部署与移动端更新

- `eas.json` + Expo Application Services — 走 Expo 的标准移动 CI/CD
- `hot-updater.config.ts` — OTA 热更新（绕过 App Store 审核做小修复）
- Bun manager/proxy 可独立部署或自托管，公共部署在 gateway.lunel.dev

## 四、实际应用场景

### 4.1 跟 happy 的对比（同赛道核心选型）

| 维度 | slopus/happy | lunel-dev/lunel |
|------|--------------|------------------|
| 定位 | Claude Code / Codex 的移动遥控 | 独立的移动 IDE + 云开发平台 |
| 是否绑定特定 Agent | 是（Claude/Codex 包装） | 不绑，自己是 IDE |
| 服务端 | happy-server（pnpm/TS） | manager + proxy（Bun） |
| 终端实现 | node-pty | Rust + wezterm fork（更强） |
| 端到端加密 | ✅ 零知识架构 | ❌ README 未提及（可能依赖 session 配对的对称密钥） |
| 云沙盒 | 无 | 🚧 Lunel Cloud（未发） |
| Stars / 创建 | 21.8K / 2025-07 | 1.0K / 2026-02 |
| 协议 | MIT | MIT |
| 桌面端 | 有 Electron（codium） | 无（聚焦移动 + Web） |

**选择建议**：
- 你已经天天用 Claude Code / Codex 且重视隐私 → **happy**
- 你想要更通用、跨任何编程场景、未来想用云沙盒 → **lunel**
- 想要顶级终端体验（Vim 等 TUI 应用流畅显示）→ **lunel**（wezterm-based PTY）

### 4.2 工程范式可借鉴

- **App = dumb client + CLI = brain**：移动端只做渲染，业务在本地——这种"控制反转"对很多移动应用都适用
- **Manager / Proxy 分离**：控制面 vs 数据面，是 Hashicorp/Tailscale 的经典 pattern，Bun 实现成本低
- **PTY 单独抽 Rust**：当某个组件性能/正确性要求远高于其他时，跨语言抽出来值
- **24fps diff-only**：远程屏幕推送的标准做法，对你做"AI 多 Agent 终端聚合面板"很有参考价值
- **Makefile + 多组件目录**：跨语言/跨包管理器（npm + Bun + Cargo + Go）的统一编排——这是个多语言项目模板的好范本

### 4.3 跟你已有研究的关联

- **序号 9 [opencode](../opencode/summary.md)** / **happy** — 都是 AI 编码 Agent 系生态，lunel 不绑 Agent 但可承载它们
- **序号 11 [Mexus](../Mexus/summary.md)** — 本地 Agent 管理面板，lunel 是这思路的移动 + 云版本
- **本批次的 happy** — 同赛道直接对比，参见上一节表格

### 4.4 风险与限制

- 1K Stars，4 个月新项目，**稳定性未经长期检验**
- **Lunel Cloud 未发**——目前只是"无 SSH 远控自家电脑"，云端能力还在路上
- README 没提端到端加密细节，敏感项目慎用 / 自托管 manager+proxy
- 22 种语言虽多但深度未知（可能机翻）

### 4.5 选型一句话

**想做"移动端写代码"工具的工程范本 + 想要 wezterm 级终端体验 + 愿意接受新项目** → 装 lunel 试一下；想等成熟 → 关注 Lunel Cloud GA。

---

## 五、与本研究库其他条目的关系

- **本次同批的 [happy](../happy/summary.md)** — 同赛道核心对比对象，必看
- **序号 9** [opencode](../opencode/summary.md) — AI 编码 Agent，是 lunel 这类移动 IDE 的可承载对象
- **序号 11** [Mexus](../Mexus/summary.md) — 本地 Agent 管理面板的桌面版
- **序号 32** [vibe-kanban](../vibe-kanban/summary.md) — 看板式 Agent 任务管理（可类比 lunel 想做的多任务视图）
