# planning-with-files 研究总结

> 仓库地址：https://github.com/OthmanAdi/planning-with-files
> 研究日期：2026-06-14

## 一、仓库概述

**23,276 Stars · 2,042 Forks · Python · MIT 协议**

planning-with-files 是一个**持久化基于文件的规划技能**，专为 AI 编码 Agent 设计。它将 `task_plan.md`、`findings.md` 和 `progress.md` 写入磁盘，让 Agent 在**上下文丢失**、`/clear` 和崩溃后仍能恢复，支持 60+ Agent 安装。

Meta 收购 Manus 花了 **$2 billion**，而 planning-with-files 让你用同样的方式工作。

## 二、核心概念

### 2.1 核心理念

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

→ Anything important gets written to disk.
```

### 2.2 三个核心文件

| 文件 | 用途 | 更新时机 |
|------|------|----------|
| `task_plan.md` | 阶段划分、进度追踪、决策记录 | 每阶段完成后 |
| `findings.md` | 研究发现、探索结果 | 任何发现后 |
| `progress.md` | 会话日志、测试结果 | 全程持续 |

### 2.3 v3.0.0 新增：Autonomous 和 Gated 模式

**Legacy 模式（默认）**：v2.43 行为，不改变现有工作流

**Autonomous 模式**：
- 降低 token 消耗（减少 per-tool-call 重复注入）
- 默认启用计划证明（attestation）
- 使用结构化账本摘要替代原始 progress.md

**Gated 模式**：
- 在 Autonomous 基础上增加完成门控
- 阻止 Agent 在计划真正完成前停止
- 支持 Opus 4.8、Fable 5、GPT 5.5 等强模型

### 2.4 完成门控机制

| Tier | 宿主 | 门控机制 |
|------|------|----------|
| 1: hard block | Claude Code, Codex CLI, OpenAI Codex API, Continue.dev | `{"decision":"block"}` / exit 2 |
| 2: follow-up inject | Cursor, Pi, Kiro | follow-up message + counter |
| 3: notify only | OpenCode, Gemini CLI | systemMessage only |

## 三、核心功能

### 3.1 上下文恢复
- Session Catchup：上下文丢失后从文件系统恢复
- 自动检测 unsynced context
- Git diff 对比实际代码变更

### 3.2 并行任务工作流
```bash
# 启动任务 A
./scripts/init-session.sh "Backend Refactor"
# → .planning/2026-01-10-backend-refactor/task_plan.md

# 启动任务 B
./scripts/init-session.sh "Incident Investigation"
# → .planning/2026-01-10-incident-investigation/task_plan.md

# 切换活动计划
./scripts/set-active-plan.sh 2026-01-10-backend-refactor
```

### 3.3 Claude Code 集成（v2.38.0+）

| 功能 | 说明 |
|------|------|
| `/plan-goal` | 与 `/goal` 组合，基于计划完成条件终止 |
| `/plan-loop` | 定时重读计划文件，检查进度 |
| `PreCompact` hook | 压缩前自动 flush 进度到 progress.md |

### 3.4 3-Strike 错误协议

```
ATTEMPT 1: 诊断并修复
ATTEMPT 2: 换一种方法（不重复同样失败的动作）
ATTEMPT 3: 重新思考（质疑假设、搜索解决方案、更新计划）

3次失败后：升级给用户
```

## 四、关键规则

1. **创建计划优先**：复杂任务开始前必须创建 `task_plan.md`
2. **2-action 规则**：每 2 次 view/browser/search 操作后立即保存关键发现
3. **决策前阅读**：重大决策前阅读计划文件
4. **行动后更新**：每个阶段完成后更新状态并记录错误
5. **记录所有错误**：错误记录 → 知识积累 → 避免重复

## 五、技术实现

### 5.1 SKILL.md 标准
planning-with-files 实现了 **SKILL.md 标准**，支持 60+ Agent：
- Claude Code、Codex CLI、Cursor、Kiro、OpenCode
- Gemini CLI、Continue.dev、F闭包、Pi、Mastra Code 等

### 5.2 Hooks 系统

| Hook | 时机 | 功能 |
|------|------|------|
| `UserPromptSubmit` | 用户提交前 | 注入计划头部 + 进度尾部 |
| `PreToolUse` | 工具调用前 | 注入计划内容（可通过 matcher 过滤） |
| `PostToolUse` | 工具调用后 | 提示更新 progress.md |
| `Stop` | 停止前 | 完成门控检查（gated 模式） |
| `PreCompact` | 压缩前 | flush 进度到 progress.md |

### 5.3 脚本工具

| 脚本 | 功能 |
|------|------|
| `init-session.sh` | 初始化计划文件 |
| `set-active-plan.sh` | 切换活动计划 |
| `resolve-plan-dir.sh` | 解析活动计划目录 |
| `check-complete.sh` | 验证所有阶段完成 |
| `session-catchup.py` | 从上次会话恢复上下文 |
| `attest-plan.sh` | SHA-256 计划证明 |
| `ledger-summary.sh` | v3 账本摘要合成 |

### 5.4 多 Agent 账本

在 autonomous/gated 模式下，每个 agent 有自己的 ledger 文件：
```
.planning/<id>/ledger-<agent>.jsonl
```

- 追加写入（append-only）
- Gate 通过账本检测进度，而非 progress.md 修改时间
- stall 检测：没有新账本条目 → 允许停止

## 六、评估数据

| 指标 | 结果 |
|------|------|
| Benchmark 通过率 | 96.7% (v2.21.0, sonnet-4-6) |
| A/B Blind 测试 | 3/3 wins |
| SkillCheck 验证 | ✅ Validated |
| 安全审计 | ✅ Audited & Fixed v2.21.0 |

## 七、与 Claude Code /goal 对比

| 特性 | `/goal` | `/plan-goal` |
|------|---------|--------------|
| 终止条件 | 用户定义 | 基于 `task_plan.md` 自动派生 |
| 上下文恢复 | 需手动 | 自动（文件系统持久化） |
| 多阶段追踪 | 无 | `task_plan.md` 结构化追踪 |
| 错误日志 | 无 | `progress.md` 记录 |

## 八、使用场景

1. **长期运行的 Agent 任务**：不怕上下文丢失
2. **多阶段项目**：清晰划分阶段和进度
3. **并行任务**：同一仓库多个任务同时进行
4. **研究任务**：保存发现，防止信息丢失
5. **Babysit 工作流**：`/plan-loop` + `/plan-goal` 组合实现自治运行

## 九、支持的 Agent（60+）

| 分类 | Agent |
|------|-------|
| **主流 IDE** | Claude Code, Codex CLI, Cursor, Kiro, OpenCode, Pi |
| **其他 IDE** | Continue.dev, Gemini CLI, Mastra Code |
| **国内** | 通义、百度 Comate、文心、Kimi |
| **其他** | Roo, Cline, Goose, CodeBuddy,Factory 等 |

## 十、总结

planning-with-files 是一个** Manus 风格的规划技能**，让 AI Agent 拥有持久化的工作记忆：

- ✅ **防崩溃**：上下文丢失后自动恢复
- ✅ **防遗忘**：重要发现立即写入磁盘
- ✅ **多任务**：并行处理多个任务，互不干扰
- ✅ **门控**：确保任务真正完成才停止
- ✅ **60+ Agent 支持**：SKILL.md 标准统一
- ⚠️ **配置成本**：需要理解 hooks 才能发挥全部能力
- ⚠️ **v3 新特性**：autonomous/gated 模式较新，部分宿主支持有限

适合场景：
- 长期运行的 AI 编码任务
- 需要多阶段规划和追踪的复杂项目
- 需要上下文恢复能力的生产环境
- 多 Agent 协作场景