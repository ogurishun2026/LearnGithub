# SkillTree 研究总结

> 仓库地址：https://github.com/maipianworni/SkillTree
> 研究日期：2026-05-26

## 一、仓库概述

SkillTree 是一个为 AI coding agent（Claude Code / Codex CLI 等）打造的 Skill 分层路由树生成器。把臃肿的单体 Skill 拆分/聚合成 ROOT → ROUTER → SKILL 的树形结构，让 agent 根据用户意图按需加载子能力，避免一次性塞满上下文。支持单 Skill 拆树、多 Skill 聚合（含歧义消解）、增量扩展三种模式，兼容 .claude/skills 与 .agent/skills 双路径约定，纯 Markdown + Bash，零依赖。

## 二、核心能力

### 2.1 三种工作模式

| 模式 | 说明 |
|---|---|
| **Single Skill → Tree** | 把臃肿单体 Skill 拆成树 |
| **Multiple Skills → Tree** | 把多个 Skill 聚合成树（含歧义消解） |
| **Update Skill Tree** | 增量扩展已有 Skill 树 |

### 2.2 核心命令

| 命令 | 说明 |
|---|---|
| `/skill-tree-generator skill` | 单个 Skill 拆树 |
| `/skill-tree-generator --aggregate skill1,skill2,... [--domain domain-name]` | 多 Skill 聚合 |
| `/skill-tree-generator --update tree-path --add skill` | 更新 Skill 树 |

### 2.3 Agent 支持

| Agent | Skill 目录 | 安装命令 |
|---|---|---|
| Claude Code | `.claude/skills/` | `cp -r skill-tree-generator ~/.claude/skills/` |
| Codex CLI | `.agent/skills/` | `cp -r skill-tree-generator ~/.agent/skills/` |
| OpenClaw | `.openclaw/skills/` | 类似 |
| OpenCode | `.opencode/skills/` | 类似 |
| Hermes | `.hermes/skills/` | 类似 |
| Continue | `.continue/skills/` | 类似 |
| Cursor | `.cursor/skills/` | 类似 |

## 三、技术架构

### 3.1 技术栈

- **语言**：Shell + Markdown
- **依赖**：纯零依赖（Bash + Markdown）
- **协议**：无（直接文件操作）

### 3.2 设计理念

```
ROOT（根路由）
  └── ROUTER（按领域路由）
       └── SKILL（具体技能）
```

- **按需加载**：用户意图决定加载哪些子技能
- **歧义消解**：多 Skill 聚合时自动消解歧义
- **增量扩展**：已有 Skill 树可增量更新

## 四、项目信息

- **Stars**：49
- **语言**：Shell
- **创建者**：maipianworni
- **协议**：纯 Markdown + Bash，零依赖

## 五、与 SkillForge/skill-router 的对比

| 维度 | SkillTree | SkillForge | skill-router |
|---|---|---|---|
| 定位 | Skill 树结构 | Skill 创建方法论 | 路由决策 |
| 目标 | 拆分/聚合 | 创建更好技能 | 减少浪费 |
| 核心 | 树形结构 | 4-阶段架构 | 存在感低 |
| 场景 | 组织大量 Skill | 从零创建 | 选择时减少开销 |

SkillTree 解决的是"已有 Skill 如何组织"的问题，SkillForge 解决"如何创建 Skill"的问题，skill-router 解决"何时路由"的问题。三者互补。