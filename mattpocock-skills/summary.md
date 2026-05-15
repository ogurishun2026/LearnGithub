# mattpocock-skills 研究总结

> 仓库地址：https://github.com/mattpocock/skills
> 研究日期：2026-05-15

## 一、仓库概述

这是 **Matt Pocock**（Total TypeScript 作者）的 Claude Code 技能集合，84000+ Stars。核心理念：**不是 vibe coding，而是用工程实践驱动 AI 编程**。与 ljg-skills 偏向个人知识管理不同，这套技能专注于**真实软件工程**——从需求对齐、TDD、调试到架构治理，覆盖完整的开发工作流。

### 核心哲学（四大问题 + 四个解法）

| 问题 | 解法 | 关键技能 |
|------|------|----------|
| AI 没理解我想要什么 | **Grilling Session**：让 AI 反复追问你，直到对齐 | `/grill-me`、`/grill-with-docs` |
| AI 太啰嗦，术语不统一 | **共享语言（Ubiquitous Language）**：建立项目术语表 CONTEXT.md | `/grill-with-docs`（自动维护） |
| 代码跑不起来 | **快速反馈循环**：TDD 红绿循环 + 诊断循环 | `/tdd`、`/diagnose` |
| 代码变成一团泥球 | **持续架构治理**：定期深化模块、垂直切片 | `/improve-codebase-architecture`、`/zoom-out` |

---

## 二、技能清单（14个）

### 工程类（engineering）—— 日常编码技能

| 技能 | 说明 | 核心方法 |
|------|------|----------|
| **setup-matt-pocock-skills** | 初始化配置：选 issue tracker（GitHub/Linear/本地）、triage 标签、文档路径 | 项目级配置，其他技能的前置依赖 |
| **grill-with-docs** | 带文档的拷问会话：挑战你的计划，同步更新 CONTEXT.md 和 ADR | 领域驱动设计的 Ubiquitous Language 实践 |
| **tdd** | 测试驱动开发：红绿重构循环 | 垂直切片（tracer bullet），反模式：水平切片 |
| **diagnose** | 纪律化调试：复现→最小化→假设→埋点→修复→回归测试 | 10种构建反馈循环的方式，强调2秒确定性循环 |
| **to-prd** | 将对话上下文转为 PRD 并发布到 issue tracker | 不采访用户，直接综合已有信息生成 |
| **to-issues** | 将 PRD/计划拆分为可独立抓取的 GitHub issues | 垂直切片，HITL（需人）/ AFK（全自动）分类 |
| **triage** | Issue 状态机管理：分类标签 + 状态标签流转 | 5个状态角色，每个 issue 恰好一个分类+一个状态 |
| **improve-codebase-architecture** | 发现架构摩擦点，提出深化模块建议 | 深模块理论（小接口+大实现），删除测试法 |
| **zoom-out** | 让 AI 跳出当前代码，给出模块全局地图 | 用项目领域术语描述模块关系 |
| **prototype** | 构建一次性原型来验证设计 | 逻辑原型（终端交互）或 UI 原型（多方案切换） |

### 生产力类（productivity）—— 通用工作流工具

| 技能 | 说明 | 核心方法 |
|------|------|----------|
| **grill-me** | 纯拷问会话（不带文档维护），逐一追问直到完全理解 | 逐个问题追问，不批量 |
| **caveman** | 极简通信模式：省略冠词/填充词/客套，减少 ~75% token | `[事物] [动作] [原因]` 格式，安全警告时自动切回正常模式 |
| **handoff** | 将当前对话压缩为交接文档，供下一个 agent 继续 | mktemp 生成临时文件，引用已有制品避免重复 |
| **write-a-skill** | 创建新技能的标准流程 | 需求收集→起草→审阅，渐进式披露 |

### 其他类

| 分类 | 技能 | 说明 |
|------|------|------|
| misc | git-guardrails-claude-code | 阻止危险 git 命令（push、reset --hard、clean） |
| misc | setup-pre-commit | 配置 Husky + lint-staged + Prettier + 类型检查 + 测试 |
| misc | scaffold-exercises | 创建练习目录结构 |
| misc | migrate-to-shoehorn | 迁移测试到 @total-typescript/shoehorn |

---

## 三、技术架构

### 目录结构

```
mattpocock-skills/
├── .claude-plugin/
│   └── plugin.json          # 技能注册清单
├── skills/
│   ├── engineering/         # 10个工程技能
│   ├── productivity/        # 4个生产力技能
│   ├── misc/                # 4个杂项技能
│   ├── personal/            # 个人技能（不发布）
│   ├── in-progress/         # 草稿
│   └── deprecated/          # 已废弃
├── docs/
│   └── adr/                 # 架构决策记录模板
├── scripts/                 # 辅助脚本
├── CLAUDE.md                # 仓库级指令
├── CONTEXT.md               # 领域术语表（示例）
└── README.md
```

### 核心文件约定

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 技能定义（YAML frontmatter + Markdown 指令） |
| `CONTEXT.md` | 项目领域术语表，AI 和人共享的语言 |
| `docs/adr/` | 架构决策记录（Architecture Decision Records） |
| `CONTEXT-MAP.md` | 多上下文项目的索引文件 |
| `plugin.json` | 注册所有可发布的技能 |

### 技能 SKILL.md 格式

```yaml
---
name: skill-name
description: "描述 + 触发条件 'Use when...'"
user_invocable: true|false
---

# 技能内容（指令、流程、参考）
```

### 设计模式：progressive disclosure

每个技能目录可包含：
- `SKILL.md` — 核心指令（必选）
- `REFERENCE.md` — 详细参考（可选，超过500行时拆出）
- `EXAMPLES.md` — 用法示例（可选）
- `scripts/` — 辅助脚本（可选）
- `*.md` 引用文件 — 被 SKILL.md 引用的补充文档

---

## 四、核心理念深度解析

### 1. 共享语言（CONTEXT.md）

这是整个技能集最核心的创新点。灵感来自 Eric Evans 的《领域驱动设计》：

- 项目中人和 AI 使用同一套术语
- `CONTEXT.md` 只记录**领域概念**，不记录实现细节
- `/grill-with-docs` 在拷问过程中实时更新术语表
- 效果：变量名一致、代码可导航、token 消耗减少

**示例**：
- 之前："课程里面某个课节被'正式化'（即给定文件系统位置）"
- 之后："materialization cascade"（一个词替代一句话）

### 2. 垂直切片（Vertical Slicing）

核心理念来自《务实程序员》的"tracer bullets"：

```
错误（水平切片）：写所有测试 → 写所有实现
正确（垂直切片）：测试1→实现1 → 测试2→实现2 → ...
```

应用于：
- `/tdd`：一个测试→一个实现→重复
- `/to-issues`：每个 issue 是一条贯穿所有层的垂直切片

### 3. 深模块（Deep Modules）

灵感来自 John Ousterhout 的《软件设计哲学》：

- **深模块** = 小接口 + 大实现（高杠杆）
- **浅模块** = 接口几乎和实现一样复杂（低杠杆）
- **删除测试法**：想象删掉这个模块，如果复杂度消失了，说明是 pass-through；如果复杂度分散到 N 个调用者，说明模块有价值

### 4. 反馈循环优先

`/diagnose` 技能列出 10 种构建反馈循环的方式，核心原则：
- **有确定性反馈循环 = bug 90% 已修复**
- 2秒确定性循环 > 30秒不稳定循环
- 花 disproportionate effort 构建循环本身

---

## 五、在游戏开发中的应用

### 直接可用的技能

| 技能 | 游戏开发场景 |
|------|-------------|
| **grill-me** | 开始设计新系统前，让 AI 拷问你："战斗系统的核心体验是什么？" |
| **grill-with-docs** | 建立游戏领域术语表：Player/Character/Skill/Quest/Inventory 的精确定义 |
| **tdd** | 游戏逻辑的 TDD：背包系统、战斗计算、任务状态机 |
| **diagnose** | 系统化排查游戏 bug：渲染异常、物理碰撞错误、AI行为异常 |
| **to-prd** | 将游戏设计讨论转化为 PRD（产品需求文档） |
| **to-issues** | 拆分大型功能（如"实现战斗系统"）为可独立完成的 issue |
| **triage** | 管理 GitHub issues：分类 bug/功能，标记优先级 |
| **improve-codebase-architecture** | 定期重构游戏代码：把 God Object 拆成深模块 |
| **zoom-out** | 不熟悉某个系统时，让 AI 给出全局模块地图 |
| **prototype** | 快速验证：战斗公式原型（终端交互）或 UI 布局原型（多方案对比） |
| **caveman** | 长时间编码时省 token，提高迭代速度 |
| **handoff** | 跨 session 继续开发，不丢失上下文 |

### 游戏开发工作流示例

**新系统开发流程**：
```
/grill-with-docs   → 拷问需求 + 建立领域术语（CONTEXT.md）
/to-prd            → 生成 PRD
/to-issues         → 拆分为垂直切片 issues
/tdd               → 逐个 issue 用 TDD 实现
/zoom-out          → 不懂某个模块时看全局地图
/diagnose          → 遇到 bug 时系统化调试
/improve-codebase-architecture → 定期架构治理
```

**Bug 排查流程**：
```
/diagnose → 构建反馈循环 → 最小化复现 → 修复 → 回归测试
```

---

## 六、与 ljg-skills 的对比

| 维度 | mattpocock-skills | ljg-skills |
|------|-------------------|------------|
| 定位 | 软件工程实践 | 个人知识管理 |
| Stars | 84000+ | 较少 |
| 核心方法论 | DDD + TDD + 深模块理论 | 费曼学习法 + 苏格拉底追问 |
| Issue 管理 | 有（triage + to-issues + to-prd） | 无 |
| 文档体系 | CONTEXT.md + ADR | org-mode / Markdown |
| 可视化 | 无 | 有（ljg-card 生成 PNG） |
| 适用场景 | 团队项目、工程化开发 | 个人学习、知识整理 |
| 互补性 | 偏"做"（工程执行） | 偏"想"（思维框架） |

**建议**：两者可以结合使用。用 mattpocock-skills 驱动开发流程，用 ljg-skills 做前期思考和后期知识沉淀。

---

## 七、安装方式

```bash
# 一键安装（交互式选择技能）
npx skills@latest add mattpocock/skills

# 安装后必须运行初始化
/setup-matt-pocock-skills
```

初始化会询问：
1. 使用哪个 issue tracker（GitHub / Linear / 本地文件）
2. triage 时使用哪些标签
3. 文档保存位置
