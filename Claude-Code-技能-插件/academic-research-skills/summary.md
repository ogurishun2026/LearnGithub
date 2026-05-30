# academic-research-skills 研究总结

> 仓库地址：https://github.com/Imbad0202/academic-research-skills
> 研究日期：2026-05-30

## 一、仓库概述

academic-research-skills（ARS）是一套为 **Claude Code** 设计的学术研究技能套件，覆盖从研究到发表的完整流程——research → write → review → revise → finalize。24,203 Stars，采用 CC BY-NC 4.0 许可证（非商业用途可自由使用）。

核心定位：**AI 是副驾驶，不是自动驾驶**。工具处理繁琐工作（找参考文献、格式化引用、验证数据、检查逻辑一致性），研究者专注真正需要大脑的部分：定义问题、选择方法、解读数据、写出"我论证的是"那句话。

## 二、核心内容

### 2.1 四大技能模块

| 模块 | 规模 | 核心功能 |
|------|------|----------|
| **Deep Research** | 13 Agent | 13 智能体研究团队，含 Socratic 引导模式、PRISMA 系统评审、意图检测、对话健康监控、交叉模型验证 |
| **Academic Paper** | 12 Agent | 12 智能体论文写作，含风格校准、写作质量检查、LaTeX 优化、可视化、修改指导 |
| **Academic Paper Reviewer** | 7 Agent | 7 智能体多视角同行评审，0-100 质量评分表（EIC + 3 动态审稿人 + 魔鬼代言人） |
| **Academic Pipeline** | 10-stage | 10 阶段管道编排器，含自适应检查点、声明验证、两阶段评审、Socratic 辅导、协作评估 |

### 2.2 10 阶段论文管道

```
Stage 1: RESEARCH       → 研究问题 Brief + 方法论蓝图
Stage 2: WRITE          → 论文写作（基于验证的实验结果）
Stage 2.5: INTEGRITY    → 完整性验证（Fabrication 检测）
Stage 3: REVIEW         → 同行评审
Stage 3': RE-REVIEW     → 修改后复审
Stage 4: REVISION       → 作者修改
Stage 4.5: INTEGRITY     → 最终完整性验证
Stage 5: FINAL          → 终稿
Stage 6: SUMMARY        → 过程总结 + 协作质量评估（6 维度 1-100）
```

**关键设计**：每个阶段需要用户确认检查点；完整性验证（Stage 2.5 + 4.5）**不可跳过**。

### 2.3 引用验证体系（v3.7+）

基于 Zhao et al. (2026) 的研究——审计 1.11 亿条引用，发现 146,932 条虚假引用。ARS v3.7.3 起引入：
- **三层引用定位器锚（locator anchors）**：每条引用带定位锚点
- **声明审计（Claim Audit，v3.8）**：抓取被引用源验证声明是否得到支持
- 5 个 HIGH-WARN 类（声明不支持/负约束违反/伪造引用/无锚/约束违反未引用）作为硬门禁

### 2.4 核心问题发现与优化（v3.0）

| 问题 | 解决方案 |
|------|----------|
| **Frame-lock**：AI 在自己设定的框架内反驳，从不质疑前提 | 魔鬼代言人 concession threshold protocol： rebuttal 评分 1-5，≤3 分只能重述攻击，不可退让 |
| **谄媚倾向**：用户持续反驳时 AI 太快认输 | 反连续让步规则 + 让步率追踪 + 帧锁检测 |
| **意图误检测**：Socratic Mentor 在用户仍探索时就收敛 | 意图检测层：区分探索型 vs 目标导向型对话，5 轮/次自动健康评估 |

### 2.5 使用示例

```text
# 完整管道
"我想写一篇关于 AI 对高等教育影响的研究论文"

# Socratic 引导
"Guide my research on AI in educational evaluation"

# 论文写作
"Write a paper on X"

# 同行评审
"Review this paper"

# 引用检查
"/ars-citation-check"
```

### 2.6 支持的论文格式

- **格式**：APA 7.0（默认）、Chicago、MLA、IEEE、Vancouver
- **结构**：IMRaD（经验研究）、主题文献综述、理论分析、案例研究、政策简报、会议论文

## 三、技术架构

### 3.1 目录结构

```
academic-research-skills/
├── skills/
│   ├── deep-research/           # 13 Agent 研究套件
│   ├── academic-paper/         # 12 Agent 论文写作
│   ├── academic-paper-reviewer/ # 7 Agent 同行评审
│   └── academic-pipeline/      # 10 阶段管道编排器
├── commands/                   # 14 个独立命令（ars-plan/ars-review/ars-full 等）
├── agents/                     # 共享 Agent 角色定义
├── hooks/                      # 生命周期钩子
├── shared/                     # 共享模式（ground_truth_isolation 等）
├── evals/                      # 评估框架
├── examples/showcase/          # 完整管道输出示例
└── docs/                       # 文档（ARCHITECTURE.md 等）
```

### 3.2 数据访问层级（v3.3.2+）

每个技能声明 `data_access_level`（`raw` / `redacted` / `verified_only`），通过 `scripts/check_data_access_level.py` 强制执行。模式借鉴 Anthropic 的 automated-w2s-researcher。

### 3.3 成本估算

完整管道约 **$4-6**（15k 词论文），详见 [`docs/PERFORMANCE.md`](docs/PERFORMANCE.md)。

## 四、实际应用场景

### 4.1 适合的场景

- 学术研究者快速完成文献综述、论文写作、同行评审全流程
- 需要严格引用验证的研究（避免 Zhao et al. 发现的 14.6 万条虚假引用问题）
- 跨语言研究（中英文双语支持，意图检测不依赖关键词）

### 4.2 与 Experiment Agent 配合

```text
ARS Stage 1 RESEARCH  →  RQ Brief + Methodology Blueprint
        ↓
  experiment-agent     →  run/manage experiments → validate results
        ↓
ARS Stage 2 WRITE     →  write paper with verified experiment results
```

### 4.3 与 The AI Scientist 的区别

The AI Scientist（Lu et al., 2026）实现了**完全自主**的研究流程但继承了失败模式（实现 bug、幻觉结果、捷径依赖等）。ARS 选择**人机协作**模式，由人类定义问题、解读数据，AI 处理繁琐工作以规避这些失败模式。

## 五、总结

academic-research-skills 是一个**工程化程度极高的学术研究 Agent 工具链**，不是简单包装 LLM 生成内容，而是引入了完整性验证、两阶段评审、Socratic 对话、引用审计等多层机制来规避 AI 生成内容的系统性失败模式。CC BY-NC 4.0 许可证意味着非商业用途可自由使用，商业用途需联系作者。24K Stars 和完整的论文案例展示（同行评审报告、完整性验证报告等）说明其已经过实际验证。
