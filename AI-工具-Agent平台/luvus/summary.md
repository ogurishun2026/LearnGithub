# Luvus 研究总结

> 仓库地址：https://github.com/RizRiyz/luvus
> 研究日期：2026-08-30

## 一、仓库概述

**一句话定位**：Luvus 是一个纯 Rust 编写的 AI 编码 Agent “任务控制台”——它把持久终端、多 CLI Agent 状态监控、会话恢复、Git/Diff 审查、worktree 隔离编排和自动化协议整合进一个跨平台 TUI。

它不是新的模型或编码 Agent，而是运行在 Claude Code、Codex、opencode、Kimi、Gemini 等 CLI Agent 之上的**本地控制面**。可以把它理解成：

> tmux 的持久会话 + 多 Agent 监控 + Git 工作台 + worktree 编排器 + 可脚本化控制协议。

### 基本信息（2026-08-30 快照）

| 维度 | 数据 |
|------|------|
| Stars / Forks | 567 / 33 |
| 提交数 | 354 |
| 当前版本 | v0.13.2 |
| 主语言 | Rust 2021，最低 rustc 1.88 |
| 许可证 | Apache-2.0 |
| 平台 | macOS / Linux / Windows |
| 分发 | crates.io、Homebrew、安装脚本、Release 二进制、Nix |
| 官网 / 文档 | https://luvus.dev / https://luvus.dev/docs/ |

**为什么值得看**：项目体量不大，但边界很完整。它没有停留在“多开几个终端”的表层，而是继续做了 Agent 识别、会话语义、文件租约、质量门禁、隔离合并、协议发现、权限边界和跨平台 PTY，因此更像一个小型的本地 Agent Harness。

---

## 二、核心能力

### 2.1 持久工作区与终端复用

- 后台 server 持有真实 PTY、窗格、标签、布局和会话状态，关闭前端 client 不会结束任务
- 支持命名会话、重新附着、窗格拆分/缩放/移动/交换、标签重排和滚动历史
- 内置 Git 感知文件树、文件预览、全局搜索、Git 状态和 DIFF 审查界面
- 多个客户端可连接同一个 server，并保持各自的视口尺寸

它与 tmux 最关键的差异不是“会话常驻”，而是 Luvus 理解窗格中运行的是哪个 Agent、对应哪个会话、消耗了多少上下文，以及当前是 working、blocked、done 还是 idle。

### 2.2 多 Agent 识别、恢复与分叉

源码当前列出 18 种 Agent：

| 能力 | 支持情况 |
|------|----------|
| 无集成即可检测实时状态 | Claude Code、Copilot CLI、Codex、opencode、Kimi、Grok、Hermes、Pi、OMP、Muse、Fx、Cursor、Gemini、Aider、Amp、Droid、Qwen、Kiro |
| 会话恢复 | 前 11 种原生恢复；Cursor 使用 resume command |
| 原生分叉到新窗格 | Claude Code、Codex、Grok、Pi、Oh My Pi |
| 精确生命周期 Hook | Claude Code、Copilot CLI、Codex、opencode、Kimi、Grok、Oh My Pi |

Agent 检测与高权限集成是分开的：用户可以通过 manifest 添加“只检测”的新 Agent，但会话发现、恢复、分叉和配置写入必须由内置 adapter 明确实现。这种分层避免了自定义清单获得不必要的文件系统或命令权限。

### 2.3 多 Agent 编排

Luvus 内置任务看板和完整的并行开发闭环：

```text
任务 queued
  -> 声明依赖、文件路径和质量门禁
  -> 获取路径 lease
  -> 在独立 git worktree / luvus/<task> 分支启动 Agent
  -> Agent 执行并上报上下文占用
  -> 质量门禁通过后标记 done
  -> 在专用 integration worktree 合并
  -> 冲突则 blocked，不修改用户当前 checkout
```

核心保护有三层：

1. **路径租约**：重叠 glob 不能同时分配，先从任务层减少冲突。
2. **物理隔离**：每个 worker 使用独立 worktree，磁盘和分支互不覆盖。
3. **质量与合并门禁**：测试命令通过后才算完成，合并在专用 worktree 中执行。

它还提供 85% 上下文门槛：worker 上报的上下文占用过高时，`done` 会被阻止，提示先压缩上下文，减少 Agent 在“快失忆”时草率收尾。

### 2.4 Git、文件与审查

- Git 标签页展示状态、分支、提交、贡献者、PR、Issue 和仓库活动
- DIFF 视图支持逐项查看与本地审查笔记，但刻意不提供 stage、discard、commit、push 等高风险动作
- 文件树和全局查找器默认只读；索引文件名和路径，不扫描文件内容，也不跟随目录符号链接
- Agent handoff 会把源码上下文明示为不可信审查数据，并要求用户显式选择目标与发送动作

### 2.5 远程与移动窄屏

```bash
luvus --remote my-server
luvus --session api --remote my-server
```

远程模式直接复用 SSH，不开放 Luvus TCP 端口，也不需要中继服务。远端机器运行 server，本机终端只是 client；传输的是变化后的屏幕 cell diff，而不是整屏刷新。窄屏会切换到单窗格导航界面，但它仍是终端方案，不是 Happy/Lunel 那种原生手机 App。

### 2.6 模块、主题与 Agent Skill

- 模块使用 `luvus-module.toml` 声明 actions、events、settings、panes、docks 和 bar widgets
- 模块可以使用任意语言，通过命令行和环境变量接入，不要求 SDK
- 安装模块前会展示其声明的命令；构建时清理环境；安装后 manifest 不能静默变化
- 主题是纯 TOML 数据，不能携带脚本、命令、CSS、按键绑定或路径
- 二进制内置与版本匹配的 Luvus Skill，可让 Codex、Claude Code 等 Agent 学会控制 Luvus

---

## 三、技术架构

### 3.1 目录与技术栈

```text
luvus/
├── src/
│   ├── app/          # TUI 状态、输入、布局、Git、Diff、文件、任务板
│   ├── agent/        # 各 CLI Agent 的无状态 adapter 与统一 registry
│   ├── api/          # 能力、schema、错误和拓扑
│   ├── ipc/          # Unix socket / Windows named pipe 本地控制面
│   ├── orch/         # task、lease、quality gate、worktree 合并
│   ├── terminal/     # PTY、终端后端、VT/Alacritty 解析
│   ├── module/       # 模块发现、安装、manifest 和运行时
│   ├── diff/ git/    # 只读审查与 Git 数据模型
│   └── main.rs       # 单二进制入口
├── protocol/uhp/v1/ # UHP 1.0 JSON Schema、fixtures、conformance 契约
├── examples/modules/# Bash/Python/Node/Rust 等模块示例
├── skills/           # Luvus 控制 Skill
├── website/          # Astro 文档站
├── vendor/           # 定制 vte 与 alacritty_terminal
└── Cargo.toml
```

主要依赖：

| 技术 | 用途 |
|------|------|
| Ratatui + Crossterm | 跨平台 TUI 与输入输出 |
| portable-pty | 创建和管理 PTY |
| Alacritty Terminal + VTE | ANSI/终端状态解析；仓库维护了本地补丁 |
| interprocess | Unix socket / Windows named pipe IPC |
| serde / bincode / JSON Schema | 内部状态序列化与公开协议 |
| rusqlite | 只读解析部分 Agent 的本地会话/用量数据 |

### 3.2 Headless Server + Thin Client

```text
键盘输入 -> Thin Client -> 本地 IPC/SSH -> Headless Server
                                           |-- 单线程事件循环修改状态
                                           |-- worker 执行 Git/扫描/门禁等慢任务
                                           |-- PTY 与 Agent adapter
                                           `-- 离屏渲染 -> cell diff -> Client
```

server 是真实状态所有者，client 几乎无状态。每个命名会话拥有独立 server、启动锁、socket、快照、PTY 树和编排账本；停止的命名会话不占 CPU/内存。

所有状态修改集中在一个事件循环中，Git 获取、会话扫描、质量门禁等慢操作放到 worker，再以事件形式返回。这使 task claim 和 path lease 天然只有一个写入者，减少锁竞争和竞态。

### 3.3 差分渲染

server 离屏渲染完整 UI，但只发送发生变化的 cell，并把相同样式的相邻 cell 合并。项目文档给出的自测数据是：一次按键约 22 bytes，40 字符完整行约 100 bytes，本地渲染约 1 ms/帧；这些数字属于项目方性能声明，不是本次独立基准测试结果。

### 3.4 UHP 1.0：统一 Harness 协议

Universal Harness Protocol 是 Luvus 最有长期价值的设计之一。它不把自动化限制成若干 CLI 命令，而是公开一个有版本的能力面：

```text
UHP 1.0
├── server / config / events
├── workspace / tab / pane / layout
├── agent / orchestration
├── terminal inventory / capture / input / wait
├── files / Git / DIFF / worktree
└── modules / themes / bars / docks / notifications
```

关键协议设计：

- `uhp.capabilities` 是唯一握手，消费者按能力发现，而不是猜测版本功能
- JSON 请求严格校验未知字段、重复 key、参数类型和帧大小
- `server_generation + terminal_id + pane_id` 防止控制已替换或过期的 PTY
- 状态带 `revision`，写操作可用 `if_revision` 做乐观并发控制
- 复合操作先验证再原子提交
- 支持带序列号的事件重放和语义等待，鼓励 `agent.wait` / `wait_output`，避免轮询
- 委托 token 只存在内存中，有时限、有范围、有限长

这比“让 Agent 往 tmux send-keys”更可靠：调用方可以先发现能力、使用稳定 ID、等待语义事件，并检测并发修改。

### 3.5 工程质量

- `src/` 静态扫描约有 163 个 Rust 文件和 1,156 个 `#[test]` 标注
- CI 执行 fmt、Clippy `-D warnings`、锁定依赖测试、UHP fixtures/live conformance 和 RustSec audit
- Linux、macOS、Windows 都有流水线；Windows 单独验证 named pipe、ConPTY 和协议边界
- Release profile 启用 thin LTO 和 strip，并对 macOS 二进制大小设置门禁

这些证据说明项目对终端正确性、协议兼容与跨平台行为投入较多，但本次归档没有在本机完整编译运行 Luvus，不能把 CI 配置等同于本地实测通过。

---

## 四、安全与隐私模型

Luvus 明确定位为**单用户、本地信任**工具，安全边界是操作系统用户账户，而不是容器沙箱。

| 边界 | 做法 |
|------|------|
| 本地控制端点 | Unix state 目录 0700、socket 0600；Windows named pipe 仅当前用户和 LocalSystem，并验证进程所有者 |
| 网络 | 不开放 TCP listener；远程只走用户自己的 SSH |
| Telemetry | 项目声明无 telemetry |
| 模块 | 安装前展示命令并确认；manifest 固定；卸载只删 Luvus 管理的路径 |
| 主题 | 纯数据、HTTPS、64 KiB 上限、校验后原子写入 |
| Agent Hook | 只添加/删除自己的配置项，避免覆盖 API Key、注释和用户 Hook |
| Git / DIFF | 验证 ref；禁用 pager、外部 diff、textconv 和控制字符；审查界面不提供写操作 |
| 编排 | 显式启动；worker 和合并均在隔离 worktree 中 |

需要正确理解这个模型：Luvus 不是恶意代码沙箱。窗格和受信模块仍能以当前用户身份执行命令；它保护的是本地控制面、配置修改范围和误操作边界。

---

## 五、应用场景与同类对比

### 5.1 适合的场景

1. **同时使用多个 CLI Agent**：统一看 Claude Code、Codex、opencode、Kimi 等会话状态，不必逐窗格巡检。
2. **长时间任务**：客户端关闭或 SSH 中断后 server 与 PTY 继续运行，之后重新附着。
3. **多 Agent 并行开发**：用依赖、lease、worktree、质量门禁和隔离合并管理多个 worker。
4. **构建 Agent Harness**：通过 UHP 1.0 取得结构化快照、事件和语义等待，而非解析终端文本。
5. **学习工程架构**：研究 Rust TUI、终端复用、本地 IPC、协议版本化和跨平台安全。

### 5.2 与已有研究条目的对比

| 项目 | 核心定位 | 交互形态 | Agent 能力 | 并行隔离 | 远程方式 | 更适合谁 |
|------|----------|----------|------------|----------|----------|----------|
| **Luvus** | 本地多 Agent 任务控制台 / Harness | Rust TUI | 检测、恢复、分叉、Hook、UHP | worktree + lease + gate | 原生 SSH attach | 终端重度用户、多 Agent 本地编排 |
| **Warp** | 现代 Agentic Terminal + 自有 Oz Agent | 原生 GUI 终端 | 内置 Agent、云端编排、MCP | 云/本地工作流 | Warp 生态 | 想要成熟 GUI 和一体化 AI 终端的人 |
| **Mexus** | 多 CLI Agent 本地 Web 控制台 | React Web UI | 多窗格、状态、文件树、Diff | Git worktree | 本地 Web | 更喜欢浏览器看板和可视化审查的人 |
| **Happy** | Claude Code / Codex 移动遥控 | iOS/Android/Web/CLI | 远程查看、审批、推送、E2E 加密 | 不是核心 | 加密同步服务 | 离开电脑后用手机接管 Agent 的人 |
| **Lunel** | 移动 IDE + 本机开发桥接 | Expo 移动 App | 通用终端承载 Agent | 不是核心 | Manager/Proxy | 想在手机上获得完整 IDE 体验的人 |

**关键差异**：Warp 在“终端产品 + 自有 Agent”上更完整，Mexus 在“浏览器可视化”上更直观，Happy/Lunel 强在移动端；Luvus 的优势是**本地、轻量、Agent 中立、编排边界清晰，并且公开了结构化 Harness 协议**。

---

## 六、风险、限制与选型建议

### 6.1 风险与限制

- **仍是早期项目**：当前 v0.13.2，虽然 354 次提交且更新频繁，但 CLI、协议和配置仍可能变化
- **不是 Agent 本体**：需要自行安装各 CLI、准备账号/API Key，并承担对应厂商链路的隐私与费用
- **TUI 学习成本**：快捷键和终端操作比 Web/桌面 GUI 更偏工程用户
- **编排依赖 Git**：任务 worker 需要 Git 仓库；路径 lease 依赖正确声明 glob，不能识别所有逻辑冲突
- **远程不是云服务**：两端都要安装 Luvus 并配置 SSH；没有 Happy 式推送和原生移动 App
- **本地信任不是沙箱**：确认安装的模块可以以当前用户身份运行命令，仍需审查来源
- **一键安装脚本风险**：`curl | sh` / `irm | iex` 使用方便，但敏感环境应先下载检查或使用包管理器
- **本次未做运行实测**：结论来自源码、文档、CI 和仓库元数据分析，尚未验证实际终端兼容性与性能声明

### 6.2 对你的直接价值

你已经在研究多 Agent、Codex/Claude Code 协作、worktree 隔离和任务调度，Luvus 最值得借鉴的不是界面，而是下面五个工程决策：

1. **Agent adapter registry**：检测、恢复、分叉、Hook 分层授权，避免在 UI/CLI 到处写 Agent 名称分支。
2. **单写者事件循环**：把 task/lease 等一致性问题转化成架构约束，而不是依赖复杂锁。
3. **worktree + lease + gate**：把“多 Agent 并发安全”拆成任务、文件和合并三层保护。
4. **UHP 能力发现**：稳定 ID、revision、事件重放和语义 wait，是 Agent 控制终端的正确抽象方向。
5. **安全范围可证明**：Hook 卸载只删自己的条目，DIFF 只读，主题不执行代码，都是可验证的最小权限设计。

### 6.3 选型一句话

**你需要在本地终端里长期运行多个 Claude Code / Codex / opencode 会话，并希望把 worktree 隔离、质量门禁和结构化自动化统一起来**，Luvus 很值得试用；如果你的第一需求是 GUI、手机遥控或托管云 Agent，则分别优先看 Warp/Mexus、Happy/Lunel 或云端 Agent 平台。

---

## 七、与本研究库其他条目的关系

- [Warp](../warp/summary.md) — 同为 Rust 终端与 Agent 平台；Warp 更产品化和云化，Luvus 更轻、更本地、更偏 Harness
- [Mexus](../Mexus/summary.md) — 最直接的本地多 CLI Agent 控制台对比；Web UI 对 TUI
- [happy](../happy/summary.md) — 移动遥控和端到端加密更强，与 Luvus 的本地编排形成互补
- [lunel](../lunel/summary.md) — 移动 IDE/远程开发方案，侧重点不在多 Agent 编排
- [vibe-kanban](../vibe-kanban/summary.md) — 都管理 Agent 任务；Luvus 更强调终端会话与 worktree 执行闭环
- [Fusion](../Fusion/summary.md) — 都有 Mission/任务层级和 worktree 隔离，Fusion 更偏多节点平台，Luvus 更偏单机终端控制面
