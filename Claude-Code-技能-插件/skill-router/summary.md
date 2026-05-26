# skill-router 研究总结

> 仓库地址：https://github.com/Yuzc-001/skill-router
> 研究日期：2026-05-26

## 一、仓库概述

Skill Router v0.5 是一个低presence（存在感）的运行时，用于在 skill-hefty Agent 环境中减少 skill-selection 浪费。核心职责是减少：
- 重复的 skill 发现
- 重复的 skill 比较
- 因忘记已有内容而导致的重复安装
- 导致成本超过决策本身价值的路由争议
- 递归覆盖集群中的不稳定默认值

## 二、核心设计理念

### 2.1 它不是什么

- 不是统一普适的 taxonymy 引擎
- 不是包管理器
- 不是搜索引擎
- 不是 pre-step 清单
- 不是 meta-layer 来说应该在每个任务上发言
- 不是长表单解释器用于应该一行化的决策

如果它变成了以上任何一种，它就失败了。

### 2.2 v0.5 运行时路径

1. 判断路由是否真的需要
2. 偏好最强的已安装默认值
3. 测试当前环境是否确实不足
4. 仅在真正需要时发现
5. 评估不确定性候选后再推荐

**核心规则**：无默认值变更，无声音。

**经济规则**：无浪费减少，无价值。

**边界规则**：如果路由没有改变下一个动作，Skill Router 应该消失。

## 三、技术架构

### 3.1 技术栈

- **语言**：Shell（SKILL.md）
- **许可证**：MIT
- **版本**：v0.5

### 3.2 目录结构

```
skill-router/
├── SKILL.md           # 主运行时 skill
├── README.md          # 英文说明
├── README.zh-CN.md     # 中文说明
├── LICENSE            # MIT 许可证
├── VERSION            # 当前版本
├── CHANGELOG.md       # 变更历史
├── docs/
│   ├── why-skill-router.md    # 为什么需要
│   ├── how-it-works.md        # 工作原理
│   ├── use-cases.md           # 使用场景
│   ├── with-vs-without.md    # 对比
│   ├── public-surface.md      # 公开接口
│   ├── release-notes-v0.1.0.md
│   ├── release-notes-v0.4.0.md
│   ├── release-notes-v0.5.0.md
│   ├── skill-router-v0.4-product-milestone.md
│   ├── skill-router-v0.5-ruthless-reset.md
│   ├── partial-issues-plan.md
│   └── partial-re-evaluation.md
└── references/
    ├── capacity-taxonomy.md
    ├── resolution-order.md
    ├── publish-safe-runtime-contract.md
    ├── reminder-policy.md
    ├── micro-routing-examples.md
    └── local-overrides-example.md
```

## 四、项目信息

- **Stars**：40
- **语言**：Shell/Markdown
- **许可证**：MIT
- **版本**：v0.5
- **创建者**：Yuzc-001
- **邮箱**：zxyu24@outlook.com

## 五、与 SkillForge 的对比

| 维度 | skill-router | SkillForge |
|---|---|---|
| 定位 | 低存在感运行时 | Skill 创建方法论 |
| 目标 | 减少浪费 | 创建更好技能 |
| 核心 | 路由决策优化 | 4-阶段架构 |
| Stars | 40 | 668 |
| 风格 | 实用主义 | 系统化工程 |

Skill Router 关注的是"何时应该路由"，SkillForge 关注的是"如何创建好技能"。两者互补。