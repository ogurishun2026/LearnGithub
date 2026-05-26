# airi 研究总结

> 仓库地址：https://github.com/moeru-ai/airi
> 研究日期：2026-05-26

## 一、仓库概述

Project AIRI 是一个开源项目，旨在重现 Neuro-sama（AI 虚拟角色/虚拟主播）的灵魂，将 AI 虚拟角色带入现实世界。支持 Windows/macOS/Linux 多平台，可通过桌面应用或浏览器访问。能与用户对话、播放语音、玩 Minecraft/Factorio 等游戏。

## 二、核心能力

### 2.1 支持的平台

| 平台 | 安装方式 |
|---|---|
| **Windows** | 安装包 / Scoop |
| **macOS** | DMG 安装包 |
| **Linux** | AppImage |
| **浏览器** | Web 端访问 |
| **移动端** | 二维码访问 |

### 2.2 核心功能

| 功能 | 说明 |
|---|---|
| **语音对话** | STT 语音识别 + TTS 语音合成 |
| **VRM 角色** | 支持虚拟角色显示 |
| **记忆系统** | 基于 DuckDB-WASM 的记忆存储 |
| **游戏Agent** | 内置 Minecraft 和 Factorio 游戏Agent |
| **实时语音** | Realtime Audio 交互 |
| **提示词工程** | Playground 提示词调试工具 |

### 2.3 技术架构

```
Core（核心）
├── unspeech（语音处理）
├── Memory（记忆）
├── STT（语音识别）
├── Stage（舞台/场景）
├── ServerRuntime（服务端运行时）
└── xsAI（AI引擎）

Apps（应用）
├── Stage Web（网页端）
├── Stage Tamagotchi（电子宠物模式）
├── Realtime Audio（实时语音）
└── Prompt Engineering（提示词调试）

Game Agents（游戏Agent）
├── Factorio Agent（工业流水线游戏）
└── Minecraft Agent（我的世界）
```

### 2.4 技术栈

- **语言**：TypeScript/Node.js
- **数据库**：DuckDB-WASM
- **向量检索**：PGVector（可选）
- **游戏控制**：Mineflayer（Minecraft）、RCON API（Factorio）
- **UI**：React/现代前端框架
- **许可证**：MIT

## 三、项目生态

### 3.1 社区支持

| 渠道 | 链接 |
|---|---|
| Discord | discord.gg/TgQ3Cu2F7A |
| Telegram | t.me/+7M_ZKO3zUHFlOThh |
| Twitter | @proj_airi |
| QQ群 | 1058166697 |

### 3.2 多语言文档

支持简体中文、日语、俄语、越南语、法语、韩语等

### 3.3 相似项目对比

| 项目 | 特点 |
|---|---|
| kimjammer/Neuro | 7天完成的高还原度实现 |
| SugarcaneDefender/z-waif | 游戏能力强、自主性强 |
| semperai/amica | VRM、WebXR 支持优秀 |
| elizaOS/eliza | Agent 集成示例丰富 |

## 四、项目信息

- **许可证**：MIT
- **平台**：跨平台（Win/macOS/Linux/Web）
- **灵感来源**：Neuro-sama
- **社区**：活跃的 Discord/Telegram/QQ 社区

## 五、应用场景

1. **虚拟主播**：创建自己的 AI 虚拟角色
2. **游戏陪玩**：AI Agent 陪你玩 Minecraft/Factorio
3. **AI 助手**：有形象的语音对话助手
4. **研究学习**：LLM + 游戏Agent 的实现参考