# Fusion 研究总结

> 仓库地址：https://github.com/Runfusion/Fusion
> 研究日期：2026-05-15

## 一、仓库概述

Fusion 是一个**多节点 AI Agent 编排平台**，核心理念是"从粗略想法到生产代码，全自动"。它用自然语言描述任务，AI 自动规划、执行、审查、合并，每个任务在独立的 git worktree 中运行，并行无冲突。类似"AI 版的 Trello 看板"。

### 技术栈

| 层 | 技术 |
|----|------|
| 语言 | TypeScript |
| 包管理 | pnpm 10.33（monorepo） |
| 存储 | SQLite |
| 前端 | Express + SPA（SSE 实时推送） |
| 桌面端 | Electron（macOS / Windows / Linux） |
| 移动端 | Capacitor（iOS / Android） |
| 构建工具 | esbuild、Bun（可编译为单文件可执行） |
| 模型支持 | Anthropic、OpenAI、Ollama、llama.cpp、Factory AI 等 |

---

## 二、核心特性

### 1. AI 驱动的任务生命周期

```
描述任务 → AI规划(PROMPT.md) → 待办 → 执行中 → 审查 → 完成 → 归档
```

每个步骤都有 AI 参与：
- **Planning Agent**：阅读项目代码，生成 `PROMPT.md`（步骤、文件范围、验收标准）
- **Execution Agent**：按步骤执行代码修改
- **Review Agent**：审查执行结果，不通过则回退重做

### 2. 工作流关卡（Workflow Gates）

每个任务步骤都经过：**Plan → Review → Execute → Review** 循环。

| 关卡类型 | 说明 |
|----------|------|
| Pre-merge Gate | 阻断合并，代码不达标就不能进下一步 |
| Post-merge Gate | 信息性检查，不阻断但会记录问题 |
| Manual Approval | 可选的人工审批点，插入任意位置 |

### 3. Git Worktree 隔离

- 每个任务运行在独立的 `fusion/{task-id}` 分支和 worktree 中
- **并行任务零冲突**
- 通过关卡后自动 squash merge 回主分支
- 支持手动审批合并

### 4. 多节点网格

所有设备都是对等节点，状态实时同步：

| 平台 | 形态 |
|------|------|
| 桌面端 | Electron 应用（macOS Intel/Apple Silicon、Windows 10/11、Linux） |
| 移动端 | Capacitor 应用（iOS/iPadOS、Android） |
| Web | 浏览器访问 Dashboard |
| CLI | `fn` 命令行工具 |

笔记本电脑、Mac mini、Linux 服务器、云 VM、手机——任意组合组成网格，任务看板随处可访问。

### 5. 任务层级（Missions）

**Mission → Milestone → Slice → Feature → Task** 五层结构：

```
Mission: 提升可靠性
  Milestone: 稳定执行流水线
    Slice: 重试和恢复强化
      Feature: 卡死任务恢复
        Task: FN-210
        Task: FN-214
```

- **Autopilot**：自动监控完成事件，激活下一个 Slice
- **验证契约**：每个 Feature 自动生成断言，验证实现是否达标
- **阻塞传递**：任务阻塞时自动上交（blocked-handoff）

### 6. Agent 公司

可导入预构建的 Agent 团队：

- **440+ Agent 跨 16 家公司**
- 支持 [companies.sh](https://github.com/paperclipai/companies) 标准
- Agent 之间有**内置邮箱**，可委派、协调、讨论
- 支持自主运行数周

```bash
npx companies.sh add paperclipai/companies/gstack
```

### 7. 模型系统

5 条独立模型通道，支持全局/项目/任务三级覆盖：

| 通道 | 用途 |
|------|------|
| Executor | 任务执行 |
| Planning | 任务规划 |
| Validator | 代码审查 |
| Title Summarization | 自动标题生成 |
| Workflow Step Refinement | AI Prompt 优化 |

优先级：**Per-Task → Project → Global Lane → Default → 自动选择**

### 8. 定时任务和自动化

| 功能 | 说明 |
|------|------|
| Automations | 定时执行 Shell 命令或多步骤工作流 |
| Routines | AI Agent 任务（cron / webhook / 手动触发） |
| Scope | 支持 Global（跨项目）和 Project（项目级）两种范围 |

### 9. Agent 权限策略

| 策略 | 说明 |
|------|------|
| `unrestricted` | 允许所有操作 |
| `approval-required` | 所有敏感操作需审批 |
| `locked-down` | 阻断所有敏感操作 |

5 类受控操作：`git_write`、`file_write_delete`、`command_execution`、`network_api`、`task_agent_mutation`

### 10. 研究功能

- 边界受限的研究运行（web 搜索、GitHub、本地文档、LLM 综合）
- 研究结果可直接转为任务

---

## 三、技术架构

### 包结构

| 包 | 职责 |
|----|------|
| `@fusion/core` | 领域模型：任务、看板列、SQLite 存储 |
| `@fusion/engine` | AI 引擎：规划、执行、调度、工作流步骤 |
| `@fusion/dashboard` | Web UI：Express 服务 + 看板界面 + SSE |
| `@runfusion/fusion` | CLI + Pi 扩展，发布到 npm |
| `@fusion/desktop` | Electron 桌面端 |
| `@fusion/mobile` | Capacitor 移动端 |
| `@fusion/plugin-sdk` | 插件 SDK |
| `@fusion/droid-cli` | Factory AI Droid CLI 集成 |
| `@fusion/pi-llama-cpp` | llama.cpp 本地模型集成 |
| `@fusion/pi-claude-cli` | Claude CLI 集成 |

### 插件生态

| 插件 | 说明 |
|------|------|
| Hermes Plugin | Nous Research 的开源自主 Agent |
| Paperclip Plugin | 人类控制面板 for AI 劳动力 |
| OpenClaw Plugin | OpenClaw 运行时支持 |

### CLI 命令速查

```bash
fn task create "描述"           # 创建任务 → 进入规划
fn task plan "描述"             # AI 引导规划
fn task import owner/repo       # 导入 GitHub issues
fn task show FN-001             # 查看任务详情
fn task logs FN-001 --follow    # 流式查看执行日志
fn task steer FN-001 "指引"     # 中途引导 Agent

fn project add my-app /path     # 注册项目
fn project list                 # 列出项目

fn mission create "名称" "描述"  # 创建任务层级
fn mission activate-slice <id>  # 激活 Slice

fn settings set maxConcurrent 4 # 配置并发数
fn skills search react          # 搜索 skills.sh
fn skills install firebase/...  # 安装 Agent 技能
fn chat <agent-id>              # 与 Agent 对话
```

---

## 四、实际应用场景

### 游戏开发中的用法

| 场景 | 怎么用 |
|------|--------|
| **功能开发** | "给设置面板加暗黑模式切换" → AI 自动规划 → 独立 worktree 执行 → review 后合并 |
| **Bug 修复** | 导入 GitHub issues → 自动分配给 Agent → worktree 隔离修复 → PR 合并 |
| **大型功能拆分** | Mission 层级拆分：Mission(战斗系统) → Milestone(核心战斗) → Slice(伤害计算) → Feature(暴击) → Task |
| **多平台协作** | 台式机提交任务，Mac mini 执行，手机查看进度 |
| **定时运维** | Routine 定时检查服务器状态、自动生成测试报告 |
| **Agent 团队** | 导入预构建团队，让多个 Agent 协作开发（前端 Agent + 后端 Agent + 测试 Agent） |
| **代码审查** | Validator Agent 自动审查每一步执行结果 |
| **研究方向** | 研究 Unreal Engine 最新 API 变更，结果转为开发任务 |

### 工作流示例

**从想法到合并的完整流程**：
```
1. 手机上输入："给角色加跳跃动画"
2. Planning Agent 自动分析项目，生成 PROMPT.md
3. 你在电脑上审查计划，确认
4. Execution Agent 在独立 worktree 中实现
5. Review Agent 审查代码质量
6. 通过所有关卡后自动 squash merge
7. 你在手机上看到"Done"
```

---

## 五、与其他工具对比

| 维度 | Fusion | Claude Code | Cursor | GitHub Copilot |
|------|--------|-------------|--------|----------------|
| 定位 | 多 Agent 编排平台 | 单 Agent CLI | IDE + Agent | IDE 插件 |
| 并行任务 | 原生支持（worktree 隔离） | 不支持 | 有限 | 不支持 |
| 任务看板 | Kanban 看板 | 无 | 无 | 无 |
| 多设备 | 桌面/移动/Web/CLI | CLI only | 桌面 only | IDE only |
| Agent 公司 | 440+ Agent / 16 公司 | 单 Agent | 单 Agent | 单 Agent |
| 自主运行 | 数周 | 单次会话 | 单次会话 | 单次会话 |
| 开源 | MIT | 部分 | 否 | 否 |

---

## 六、安装方式

```bash
# 一键启动（推荐）
npx runfusion.ai

# macOS / Linux 安装
curl -fsSL https://runfusion.ai/install.sh | sh

# Homebrew
brew install runfusion/fusion/fusion

# npm 全局安装
npm install -g @runfusion/fusion
fn dashboard
```

首次启动有引导向导：AI 配置 → GitHub 连接（可选） → 创建第一个任务。
