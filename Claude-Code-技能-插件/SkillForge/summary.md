# SkillForge 研究总结

> 仓库地址：https://github.com/tripleyak/SkillForge
> 研究日期：2026-05-26

## 一、仓库概述

SkillForge 是一个 AI Skill 创作方法论，从艺术到工程的转变。它将技能创建从 reactive testing 转变为 proactive engineering。核心是一个四阶段架构，通过 rigor 和多智能体 peer review 确保每个技能都经过全面分析、规范制定、清晰生成和客观验收。

## 二、核心能力

### 2.1 四阶段架构

| 阶段 | 说明 | 产物 |
|---|---|---|
| **Phase 0: Skill Trigger** | 分析输入确定最佳行动 | 判断：使用/改进/创建 |
| **Phase 1: Deep Analysis** | 系统化解构问题 | 11 个思维透镜 |
| **Phase 2: Specification & Generation** | 将分析转为规范 | XAML 规范 + 技能代码 |
| **Phase 3: Multi-Agent Synthesis** | 多智能体验收 | 4 个专家 Agent 评审 |

### 2.2 11 个思维透镜

1. First Principles（第一原理）
2. Inversion（反向）
3. Second-Order Effects（二阶效应）
4. Pre-Mortem（事前验尸）
5. Systems Thinking（系统思维）
6. Devil's Advocacy（魔鬼代言）
7. Constraints（约束）
8. Root Cause（根本原因）
9. Comparative（比较）
10. Opportunity Cost（机会成本）
11. Utility（效用）

### 2.3 核心功能

| 功能 | 说明 |
|---|---|
| **Context Skill Advisor** | v5.2 新增，主动基于证据的技能建议，含用户控制的主动级别 |
| **Advisor Commands** | configure-proactive、checkpoint、run-scheduled 等命令 |
| **Advisor Queue & State** | 建议队列和状态反馈 |
| **Context-Efficient Foundation** | SKILL.md 从 872 行简化到 313 行（64% 减少） |
| **Degrees of Freedom** | 高自由度（文本指导）、中自由度（参数化脚本）、低自由度（精确脚本） |
| **Scaffold Script** | `init_skill.py` 创建丰富技能模板 |
| **Iteration as Formal Step** | 迭代内置于 Phase 3，而非事后审查 |
| **Extended Frontmatter** | 支持 model、context、agent、hooks、user-invocable |
| **Hooks Integration** | PreToolUse、PostToolUse、Stop 钩子指南 |
| **Validation + Packing Safety** | 共享验证常量、改进解析和严格结构检查 |

## 三、技术架构

### 3.1 技术栈

- **语言**：Python + Shell
- **许可证**：MIT
- **版本**：v5.2.0

### 3.2 目录结构

```
skillforge/
├── SKILL.md              # 主 skill 定义（<500 行）
├── LICENSE               # MIT
├── CONTEXT.md            # Repo  glossary（not packaged）
├── docs/
│   └── adr/              # Repo architecture decisions（not packaged）
├── commands/             # Claude Code slash commands
├── skillforge.md          # Repo root only（not packaged）
├── references/           # Loaded into context when needed
├── regression-questions.md
├── specific-template.md
├── evolution-scorer.md
├── synthesis-protocol.md
├── script-patterns-catalogue.md
├── degrees-of-freedom.md
├── iteration-guide.md
├── evo-scorer.py
├── context_scorer.py
├── context_sources.py
├── init_skill.py
├── install_workshop.sh
├── skillforge_config.py
├── triage_skill_request.py
├── discover_skills.py
├── validate-skill.py
└── quick_validate.py
```

### 3.3 安装

**方式 1：Workspace Quick Install（一键）**
```bash
curl -fsSL https://raw.githubusercontent.com/tripleyak/SkillForge/main/scripts/install_workshop.sh | bash
```

**方式 2：手动安装**
```bash
git clone https://github.com/tripleyak/SkillForge.git /tmp/skillforge
cp -r /tmp/skillforge ~/.claude/skills/skillforge
rm -rf ~/.claude/skills/skillforge/{README.md,LICENSE,CONTEXT.md,docs,.git,.gitignore,.skillignore}
```

## 四、项目信息

- **Stars**：668
- **语言**：Python + Shell
- **许可证**：MIT
- **版本**：v5.2.0
- **创建者**：tripleyak
- **前置要求**：Codex CLI 或 Claude Code CLI，Python 3.8+

## 五、核心设计理念

> SkillForge transforms skill creation from an art into an engineering discipline.

1. **不要复制粘贴**：通过引导让你理解而非记忆
2. **模式识别**：将问题分解为可转移的技能模式
3. **渐进式提示**：5-级别提示系统，从观察线索到伪代码解决
4. **像高级工程师一样思考**：培养解决问题的思维方式

## 六、与 skill-router 的对比

| 维度 | SkillForge | skill-router |
|---|---|---|
| 定位 | Skill 创建方法论 | 低存在感运行时 |
| 目标 | 创建更好技能 | 减少浪费 |
| 核心 | 4-阶段架构 | 路由决策优化 |
| Stars | 668 | 40 |
| 风格 | 系统化工程 | 实用主义 |

两者互补：SkillForge 负责创建，skill-router 负责路由。