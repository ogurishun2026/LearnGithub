# algo-sensei 研究总结

> 仓库地址：https://github.com/karanb192/algo-sensei
> 研究日期：2026-05-26

## 一、仓库概述

Algo Sensei 是一个为 Claude Code 和 Claude.ai 打造的 AI-powered LeetCode & DSA（数据结构与算法）导师。通过智能指导、渐进式提示和模式识别训练来掌握算法，而非简单复制粘贴解决方案。提供模拟面试、代码审查、多语言支持（Python、Java、C++、JS、Go）等功能。目标是教你像高级工程师一样思考。

## 二、核心能力

### 2.1 五大核心模式

| 模式 | 说明 |
|---|---|
| **Tutorial Mode** | 通过概念解释、逐步问题分解、可视化图表、构建理解来打下坚实基础 |
| **Hint Mode** | 5-级别渐进式提示系统：观察线索 → 模式识别 → 接近方向 → 特殊技巧 → 伪代码解决（最终手段） |
| **Review Mode** | 压缩代码审查覆盖：正确性验证、时间和空间复杂度分析、代码质量反馈、优化建议、边缘情况识别、介入阅读评估 |
| **Interview Mode** | 模拟真实面试：专业面试官角色扮演、实时反馈和提示、沟通评估、详细性能回顾、面试后改进计划 |
| **Pattern Mapper Mode** | 动态学习识别算法模式：教你看问题像专业人士而非死记硬背、将模式转化为可转移技能 |

### 2.2 核心功能

- **引导式学习**：不直接给答案，而是引导你自己思考
- **渐进式提示**：5-级别提示系统，从观察线索到伪代码解决
- **模式识别训练**：教你识别 TWo Pointers、DP、Graphs 等模式
- **多语言支持**：Python、Java、C++、JS、Go 等
- **代码审查**：验证正确性、分析复杂度、识别边缘情况
- **模拟面试**：与专业面试官角色扮演

### 2.3 使用示例

| 人类指令 | AI 调用的模式 |
|---|---|
| "我卡在 LeetCode #3 上了..." | 自动切换到 Hint Mode |
| "你能解释一下动态规划吗？" | 自动切换到 Tutorial Mode |
| "这是我 TwO Sum 的解法，请审查" | 自动切换到 Review Mode |
| "我们可以做个模拟面试吗？" | 自动切换到 Interview Mode |
| "我不确定应该用什么方法..." | 自动切换到 Pattern Mapper Mode |

## 三、技术架构

### 3.1 技术栈

- **语言**：Shell（Skill 格式）
- **许可证**：MIT
- **目标用户**：Claude Code / Claude.ai

### 3.2 文件结构

```
algo-sensei/
├── SKILL.md              # 主 skill 文件（路由）
├── README.md              # 你正在阅读的文档
├── modes/
│   ├── tutor-mode.md     # 概念解释模式
│   ├── hint-mode.md      # 渐进式提示模式
│   ├── review-mode.md    # 代码审查模式
│   ├── interview-mode.md # 模拟面试模式
│   └── pattern-mapper-mode.md  # 模式识别模式
├── templates/
│   └── solutions/
│       └── solution-template.md  # 多语言解决方案格式
└── docs/
    └── dsa-cheatsheet.md  # 快速参考
```

### 3.3 安装方式

**方式 1：安装到个人 Claude Code skills**
```bash
git clone https://github.com/karanb192/algo-sensei.git
cp -r algo-sensei ~/.claude/skills/
```

**方式 2：安装到项目（团队共享）**
```bash
git clone https://github.com/karanb192/algo-sensei.git
cp -r algo-sensei /path/to/your/project/.claude/skills/
git add .claude/skills/algo-sensei
git commit -m "Add Algo Sensei skill for DSA practice"
```

**方式 3：Claude.ai 用户**
将 SKILL.md 内容粘贴到对话中，或上传整个 algo-sensei 文件夹到项目 Knowledge。

## 四、项目信息

- **Stars**：69
- **语言**：Shell/Markdown
- **许可证**：MIT
- **创建者**：karanb192
- **Topics**：leetcode, algorithms, dsa, claude-code, skill

## 五、与其他学习资源的对比

| 维度 | Algo Sensei | LeetCode Premium | YouTube 教程 |
|---|---|---|---|
| 学习方式 | 引导式提问 | 自主解决 | 被动观看 |
| 提示系统 | 5-级别渐进 | 官方提示 | 无 |
| 反馈 | 即时互动 | 答案比对 | 无 |
| 模式训练 | 内置 | 无 | 需自己总结 |
| 面试模拟 | 有 | 部分 | 无 |

## 六、核心哲学

> 停止解决随机问题，开始识别模式。

Algo Sensei 的核心理念：
1. **不要复制粘贴**：教你理解而非记忆
2. **模式识别**：看到问题类型而非具体题目
3. **渐进式引导**：让你自己找到答案
4. **像高级工程师一样思考**：培养解决问题的思维方式