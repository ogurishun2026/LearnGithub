# mattpocock-skills 对比研究报告 v2

> 仓库地址：https://github.com/mattpocock/skills
> 本次研究日期：2026-05-17
> 上次研究日期：2026-05-15
> 对比版本：v1 → v2

## 一、变更概览

仓库自上次研究以来，Stars 从 84K 增长到 88K（+4K），Forks 从未记录到 7,693。技能数量保持不变（14个正式技能），但有 4 个技能移入 deprecated，3 个新技能处于 in-progress 草稿阶段。核心理念（四大问题 + 四个解法）未变，整体架构稳定。

## 二、新增内容

### 2.1 新增 in-progress 技能（3个草稿）

| 技能 | 说明 |
|------|------|
| **review** | 代码审查技能（草稿） |
| **writing-beats** | 写作节拍技能（草稿） |
| **writing-fragments** | 写作碎片技能（草稿） |
| **writing-shape** | 写作塑形技能（草稿） |

可以看出 Matt 正在将技能集从纯工程扩展到**写作/内容创作**方向。

### 2.2 skills.sh 安装器

README 中新增了 [skills.sh](https://skills.sh/mattpocock/skills) 徽章，这是一个独立的技能分发平台。安装命令变更为：

```bash
npx skills@latest add mattpocock/skills
```

相比之前的安装方式，现在支持：
- 交互式选择要安装的技能
- 选择安装到哪些编码 Agent（不限于 Claude Code）
- 更灵活的安装粒度

## 三、移除/变更内容

### 3.1 移入 deprecated 的技能（4个）

| 技能 | 原分类 | 原因推测 |
|------|--------|----------|
| **design-an-interface** | engineering | 可能被 `prototype` 技能覆盖 |
| **qa** | engineering | 功能可能合并到其他流程 |
| **request-refactor-plan** | engineering | 被 `improve-codebase-architecture` 替代 |
| **ubiquitous-language** | engineering | 功能已内建到 `grill-with-docs` 的 CONTEXT.md 维护流程 |

这些技能在 v1 研究时尚未出现，说明它们在上次研究和本次研究之间经历了添加和废弃的生命周期。

### 3.2 README 变更

README 增加了对 GSD、BMAD、Spec-Kit 等竞争方案的评价，强调这些方案"试图拥有流程，但会夺走你的控制权"。这一定位声明是新增的。

## 四、数据对比

| 维度 | v1（2026-05-15） | v2（2026-05-17） |
|------|------------------|------------------|
| Stars | 84,000+ | 88,185 |
| Forks | 未记录 | 7,693 |
| 正式技能数 | 14 | 14（不变） |
| Engineering 技能 | 10 | 10（不变） |
| Productivity 技能 | 4 | 4（不变） |
| Misc 技能 | 4 | 4（不变） |
| Deprecated 技能 | 未记录 | 4（新增追踪） |
| In-progress 技能 | 未记录 | 3（新增追踪） |
| 核心理念 | 四大问题+四个解法 | 不变 |
| 安装方式 | npx skills add | npx skills@latest add（更新） |

## 五、完整研究内容

### 5.1 仓库定位

Matt Pocock（Total TypeScript 作者）的 Claude Code 技能集合。核心理念：**不是 vibe coding，而是用工程实践驱动 AI 编程**。专注真实软件工程——从需求对齐、TDD、调试到架构治理，覆盖完整开发工作流。

当前定位更明确：与 GSD、BMAD、Spec-Kit 等"拥有流程"的方案区分，强调**小、可组合、可定制**。

### 5.2 技能清单（14个正式 + 4个废弃 + 3个草稿）

#### Engineering（10个）

| 技能 | 说明 |
|------|------|
| **setup-matt-pocock-skills** | 初始化配置：选 issue tracker、triage 标签、文档路径 |
| **grill-with-docs** | 带文档的拷问会话，同步更新 CONTEXT.md 和 ADR |
| **tdd** | TDD 红绿重构循环，垂直切片 |
| **diagnose** | 纪律化调试：复现→最小化→假设→埋点→修复→回归测试 |
| **to-prd** | 对话上下文转 PRD，发布到 issue tracker |
| **to-issues** | PRD 拆分为垂直切片 GitHub issues |
| **triage** | Issue 状态机管理 |
| **improve-codebase-architecture** | 发现架构摩擦点，提出深化模块建议 |
| **zoom-out** | 让 AI 给出模块全局地图 |
| **prototype** | 构建一次性原型验证设计 |

#### Productivity（4个）

| 技能 | 说明 |
|------|------|
| **grill-me** | 纯拷问会话，逐一追问 |
| **caveman** | 极简通信模式，省 ~75% token |
| **handoff** | 对话压缩为交接文档 |
| **write-a-skill** | 创建新技能的标准流程 |

#### Misc（4个）

| 技能 | 说明 |
|------|------|
| **git-guardrails-claude-code** | 阻止危险 git 命令 |
| **setup-pre-commit** | 配置 Husky + lint-staged |
| **scaffold-exercises** | 创建练习目录 |
| **migrate-to-shoehorn** | 迁移测试到 shoehorn |

### 5.3 技术架构

目录结构与 v1 一致，无变化：
```
mattpocock-skills/
├── .claude-plugin/plugin.json
├── skills/
│   ├── engineering/     # 10个
│   ├── productivity/    # 4个
│   ├── misc/            # 4个
│   ├── personal/        # 个人技能（不发布）
│   ├── in-progress/     # 草稿（新增3个写作相关）
│   └── deprecated/      # 已废弃（4个）
├── docs/adr/            # ADR 模板
├── scripts/
├── CLAUDE.md
├── CONTEXT.md
└── README.md
```

## 六、对比结论

**变化程度：微小**。两天内仓库无重大架构变更，核心技能集稳定。

值得关注的变化：
1. **写作方向拓展**：3 个 in-progress 写作技能暗示 Matt 计划将技能集扩展到内容创作领域
2. **4 个技能废弃**：说明技能集在持续迭代，合并功能、去除冗余
3. **skills.sh 平台**：安装器升级，支持多 Agent 选择，说明生态在成熟

**建议**：无需采取行动。下次关注 writing-* 技能是否正式发布。
