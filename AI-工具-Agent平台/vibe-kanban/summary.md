# vibe-kanban 研究总结

> 仓库地址：https://github.com/BloopAI/vibe-kanban
> 研究日期：2026-05-26

## 一、仓库概述

Vibe Kanban 是一个为编码 Agent（Claude Code、Codex、Gemini CLI 等）设计的看板式任务管理平台，通过看板 issues 规划工作，在 workspace 中运行 Agent，最终通过 PR 提交代码。定位是"AI 时代的产品团队工具"——让工程师在规划和 review 编码 Agent 上花费的时间更少，交付更快。

**⚠️ 注意**：Vibe Kanban 官方已宣布即将停服（sunsetting），建议关注后续动态或考虑自托管。

## 二、核心能力

### 2.1 功能列表

| 功能 | 说明 |
|---|---|
| 看板 issues | 在看板上创建、优先级排序、分配任务 |
| Agent Workspace | 每个 workspace 提供一个分支、一个终端、一个 dev server |
| Diff review + 内联评论 | 不离开 UI 即可发送反馈给 Agent |
| 内置浏览器 | devtools、inspect mode、设备模拟 |
| 10+ 编码 Agent 支持 | Claude Code, Codex, Gemini CLI, GitHub Copilot, Amp, Cursor, OpenCode, Droid, CCR, Qwen Code |
| PR 创建和合并 | AI 生成 PR 描述，在 GitHub 审查并合并 |

### 2.2 工作流程

```
规划（看板） → 在 Workspace 运行 Agent → Review Diff → 创建 PR → Merge
```

一条命令完成：`npx vibe-kanban`

## 三、技术架构

### 3.1 技术栈

- **语言**：Rust（核心）
- **前端**：Node.js（>=20）+ pnpm（>=8）
- **架构**：Monorepo（packages/local-web, remote-web, web-core, ui）
- **分析**：PostHog（可选，build-time 配置）
- **部署**：Docker（自托管）、Cloud（官方）

### 3.2 目录结构

```
packages/
  local-web/      # 本地 Web 应用
  remote-web/     # 远程 Web 应用
  web-core/       # 共享 Web 核心
  ui/             # UI 组件库
  public/         # 公共资源
```

### 3.3 环境变量

| 变量 | 类型 | 说明 |
|---|---|---|
| `POSTHOG_API_KEY` | Build-time | PostHog 分析（留空则禁用） |
| `PORT` | Runtime | 服务器端口 |
| `BACKEND_PORT` | Runtime | 后端端口 |
| `MCP_HOST/PORT` | Runtime | MCP 服务器连接 |
| `VK_ALLOWED_ORIGINS` | Runtime | 允许的跨域来源 |
| `DISABLE_WORKTREE_CLEANUP` | Runtime | 禁用 git worktree 清理 |

### 3.4 自托管

支持 Docker 部署，可自托管 Vibe Kanban Cloud 实例，通过 `VK_ALLOWED_ORIGINS` 配置反向代理或自定义域名。

## 四、关键特点

1. **多 Agent 支持**：统一界面支持 10+ 编码 Agent，无需切换工具
2. **Workspace 隔离**：每个任务在独立分支和终端中运行
3. **内置 Dev Server**：预览应用 + devtools + 设备模拟
4. **Diff Review**：不离开看板界面直接评论 PR
5. **远程部署**：通过 SSH 打开远程服务器上的 VSCode

## 五、项目信息

- **Stars**：26,525（非常高🔥）
- **Forks**：2,777
- **语言**：Rust
- **许可证**：Apache 2.0
- **创建时间**：2025-06-14
- **主页**：https://www.vibekanban.com
- **⚠️ 状态**：即将停服（sunsetting）
- **Topics**：agent, ai-agents, kanban, management, task-manager

## 六、与 codedb-mcp 的潜在关联

两者都是 BloopAI 出品（vibe-kanban 仓库所属组织），且 codedb-mcp 此前由用户标记为⭐重点关注。vibe-kanban 的停服可能意味着 BloopAI 将资源集中到代码搜索/分析领域。