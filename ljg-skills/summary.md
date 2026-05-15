# ljg-skills 研究总结

> 仓库地址：https://github.com/lijigang/ljg-skills
> 研究日期：2026-05-15

## 一、仓库概述

lijigang/ljg-skills 是一个 **Claude Code 自定义技能插件集合**，共包含 17 个独立技能。每个技能是一个自包含目录，安装到 `~/.claude/skills/` 即可通过自然语言或 `/skill-name` 调用。

### 安装方式

```bash
# 全量安装（全局）
npx skills add lijigang/ljg-skills -g --all

# 单个安装
npx skills add lijigang/ljg-skills -g --skill ljg-card

# Markdown 格式版本（适用 Obsidian / VSCode / Notion）
npx skills add lijigang/ljg-skills#md -g --all
```

---

## 二、技能清单（17个）

### 知识处理类

| 技能 | 说明 | 关键方法 |
|------|------|----------|
| **ljg-read** | 深度阅读任意文本（翻译+结构化注释+深层提问） | 翻译（古文/英文/方言）+ 结构标注 + 深层追问 |
| **ljg-paper** | 学术论文分析管道 | 核心想法、关键贡献提取 |
| **ljg-paper-river** | 论文追踪：5层递进模型+历史溯源 | 当前前沿模型（5层）+ 新进展 + 源头 |
| **ljg-learn** | 从书/课程提取核心概念 | 验证→测试→形式→要素→压缩，五步法 |

### 写作与表达类

| 技能 | 说明 | 关键方法 |
|------|------|----------|
| **ljg-writes** | 写作引擎：一个观点→千字文（1000-1500字） | 观点扩写 |
| **ljg-plain** | 朴素重写：任何内容改写成十岁小孩也能懂 | 费曼学习法 |
| **ljg-qa** | 信息膏药：Q-A 结构化（问要刁钻，答要深刻） | 问答框架（可视化/图解/故事/边界） |
| **ljg-word** | 英语单词深度解析 | 汉语释义 + 时效 + 多种例句 |

### 可视化类

| 技能 | 说明 | 依赖 |
|------|------|------|
| **ljg-card** | 内容→PNG 视觉卡片（长卡/信息图/海报/简历/名言/卡片/壁纸） | Node.js + Playwright |
| **ljg-present** | 演示文稿生成（默认复古风格，`-s` 可切换现代风格） | 无 |
| **ljg-travel** | 旅行研究+便携片（org-mode + PNG） | 无 |

### 思维框架类

| 技能 | 说明 | 关键方法 |
|------|------|----------|
| **ljg-think** | 追问之箭：对一个观点追问到根本 | 苏格拉底式追问，追到百分百的根 |
| **ljg-rank** | 排名分析：不可逆的决策排序 | 强制排序，揭示真实优先级 |
| **ljg-roundtable** | 圆桌对话：多角色辩证（ASCII 思维图） | 多元视角碰撞 |
| **ljg-relationship** | 关系解剖：结构→对话→关系真相 | 人际关系结构分析 |
| **ljg-invest** | 投资分析：评估项目是否值得投入 | 投资决策框架 |

### 元技能

| 技能 | 说明 |
|------|------|
| **ljg-skill-map** | 扫描已安装技能并可视化渲染 |
| **ljg-push** | 同步技能到 GitHub（master + md 双分支） |

### 复合技能流

| 组合 | 效果 |
|------|------|
| **ljg-paper-flow** | ljg-paper + ljg-card -c → 论文分析 + 卡片一条龙 |
| **ljg-word-flow** | ljg-word + ljg-card -i → 单词解析 + 信息图一条龙 |

---

## 三、技术架构

### 技能定义格式

```yaml
---
name: skill-name
description: "What this skill does. Use when user says..."
user_invocable: true|false
version: "x.x.x"
---

# 技能内容（Markdown）...
```

### 内容处理管道

```
URL → WebFetch
文件路径 → Read 工具
原始文本 → 直接使用
```

### 输出规范

- org-mode 格式（master 分支）或 Markdown 格式（md 分支）
- 文件名：`{timestamp}--{title}__{type}.org`
- 输出目录：`~/Documents/notes/`
- ljg-card PNG 输出：`~/Downloads/`

---

## 四、在游戏开发中的应用

### 直接可用的场景

1. **ljg-card** — 生成角色卡、技能卡、道具卡、关卡概念图（PNG）
2. **ljg-think** — 追问核心设计："为什么用回合制？"→ 追问到根本决策依据
3. **ljg-roundtable** — 模拟玩家/策划/程序员/美术四方圆桌讨论游戏机制
4. **ljg-plain** — 把复杂战斗系统改写成"十岁能懂"的版本，验证设计清晰度
5. **ljg-writes** — 从一个核心概念扩展为完整游戏世界观
6. **ljg-relationship** — NPC 阵营、角色关系图谱、势力结构分析
7. **ljg-rank** — 对候选功能做不可逆排序，决定开发优先级
8. **ljg-learn** — 学新引擎/框架时提取核心概念并压缩记忆
9. **ljg-present** — 生成游戏概念提案演示文稿

### 游戏开发工作流示例

**新角色设计**：
```
ljg-think → 追问角色定位本质
ljg-writes → 扩展角色背景故事
ljg-relationship → 梳理角色关系网络
ljg-card → 生成角色视觉卡片
```

**机制决策**：
```
ljg-roundtable → 多角色辩论方案
ljg-rank → 候选方案排序
ljg-plain → 用最简语言验证机制自洽性
```

### 限制

这些技能不能直接写游戏代码、编辑场景、调试引擎。它们的价值在于**设计思考和文档输出**环节。
