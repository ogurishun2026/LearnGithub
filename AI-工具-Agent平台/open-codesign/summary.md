# open-codesign 研究总结

> 仓库地址：https://github.com/OpenCoworkAI/open-codesign
> 研究日期：2026-05-20

## 一、仓库概述

**开源的 Claude Design 替代品**。通过自然语言提示词，一键生成交互式原型、幻灯片和营销素材。支持多模型（Claude、GPT、Gemini、Kimi、GLM、Ollama），本地优先，MIT 许可。

**核心定位**：让设计师和产品经理无需编程即可通过 AI 生成可交互的 UI 原型和演示文稿。

## 二、核心内容

### 2.1 主要功能

| 功能 | 说明 |
|------|------|
| **Prompt → 原型** | 将自然语言描述转换为可交互的 UI 原型 |
| **Prompt → 幻灯片** | 自动生成演示文稿 |
| **Prompt → PDF** | 导出为 PDF 格式 |
| **一键导入 API Key** | 支持 Claude Code / Codex API Key |
| **多模型支持** | Claude、GPT、Gemini、Kimi、GLM、Ollama |
| **BYOK** | Bring Your Own Key，自带 API Key |
| **本地优先** | 本地运行，数据不上传 |

### 2.2 技术架构 (Monorepo)

```
open-codesign/
├── apps/
│   └── desktop/              # 桌面应用 (Tauri?)
├── packages/
│   ├── artifacts/            # 工件生成
│   ├── core/                 # 核心逻辑
│   ├── exporters/            # 导出功能 (PDF/幻灯片)
│   ├── i18n/                 # 国际化
│   ├── providers/            # AI 模型提供者
│   └── runtime/              # 运行时
├── .claude/                  # Claude Code 配置
├── .Codex/                   # Codex 配置
└── turbo.json               # Turbo 构建配置
```

### 2.3 技术栈

| 层级 | 技术 |
|------|------|
| **语言** | TypeScript |
| **构建** | Turbo (Monorepo) |
| **包管理** | pnpm |
| **桌面** | Tauri (推测) |
| **Node** | >= 22 |

### 2.4 支持的 AI 模型

| 模型 | 来源 |
|------|------|
| Claude | Anthropic |
| GPT | OpenAI |
| Gemini | Google |
| Kimi | 月之暗面 (Moonshot) |
| GLM | 智谱 AI |
| Ollama | 本地模型 |

## 三、项目特点

### 3.1 vs Claude Design

| 维度 | Claude Design | open-codesign |
|------|---------------|---------------|
| **许可** | 专有 | MIT 开源 |
| **部署** | 云服务 | 本地优先 |
| **API Key** | 官方渠道 | 自带 (BYOK) |
| **数据** | 上传到云 | 本地处理 |

### 3.2 变体版本

- **v0 替代版**: 早期版本的重实现
- **Lovable 替代版**: 另一个设计工具的替代
- **Bolt.new 替代版**: Bolt.new 的替代方案
- **Figma AI 替代版**: Figma AI 功能替代

## 四、Star 历史与社区

- **Stars**: 6,190 (截至 2026-05-20)
- **语言**: TypeScript
- **许可**: MIT
- **更新活跃**: 最近更新于 2026-05-20
- **包管理**: pnpm 10.33.4
- **Node 要求**: >= 22

## 五、总结

open-codesign 是一个有前途的开源项目，旨在替代 Claude Design 的核心功能。它允许用户使用自己的 API Key（BYOK），在本地生成设计原型和幻灯片，避免了对云服务的依赖。

**亮点**：
- 开源透明，MIT 许可
- 多模型支持灵活切换
- 本地优先保护隐私
- Turbo Monorepo 架构清晰

**适用场景**：
- 设计师快速生成 UI 原型
- 产品经理制作演示文稿
- 需要本地化 AI 生成设计的工作流
