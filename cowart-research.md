---
name: cowart-research
description: Cowart 深度研究 —— 面向 Codex 的本地无限画布插件
metadata:
  type: reference
---

**Cowart** 是一个面向 **OpenAI Codex** 的本地无限画布插件，基于 [tldraw](https://github.com/tldraw/tldraw) 提供可视化画布，用于构思、标注、生成图片和根据标注图迭代图片。

仓库地址：`https://github.com/zhongerxin/cowart`

## 为什么重要（Why）

Cowart 是 **"AI 辅助创作工具"** 的典型范例。它展示了如何为 Codex 构建完整的插件生态（Skills + MCP + 前端），让 AI 编程助手不仅能写代码，还能画图、做标注、生成图片。对开发需要可视化交互的 Agent 工具很有参考价值。

## 技术栈

| 维度 | 详情 |
|------|------|
| 前端框架 | React 19 + tldraw 5.1 |
| 构建工具 | Vite 7 |
| MCP 服务器 | Node.js 原生模块（`server.mjs`） |
| 插件系统 | Codex 插件规范（`.codex-plugin/plugin.json`） |
| 数据持久化 | 本地 JSON 文件 + 静态资源目录 |

## 架构

Cowart 由四层组成，完整对接 Codex 的插件生态：

```
┌─────────────────────────────────────────┐
│  Codex 对话层（用户自然语言指令）           │
├─────────────────────────────────────────┤
│  Skills（3 个 SKILL.md）                 │
│  - cowart-open-canvas：打开画布           │
│  - cowart-image-gen：AI 生成图片          │
│  - cowart-image-edit：标注驱动图片编辑     │
├─────────────────────────────────────────┤
│  MCP 服务器（mcp/server.mjs）             │
│  - get_cowart_selection：读取选择状态      │
│  - insert_cowart_image：插入图片           │
├─────────────────────────────────────────┤
│  前端应用（React + tldraw）               │
│  - 本地服务 http://127.0.0.1:43217/      │
│  - SSE 事件广播画布变更                    │
└─────────────────────────────────────────┘
```

## 核心功能

| 功能 | 说明 |
|------|------|
| **打开画布** | Codex 中一句话打开本地 tldraw 无限画布，数据保存在项目 `canvas/` 目录 |
| **AI 图片生成** | 在画布中创建 AI image holder（支持多种宽高比预设），Codex 按 holder 比例生成图片并插入 |
| **标注驱动编辑** | 对图片做标注（箭头、文字），截图发给 Codex，Codex 生成去掉标注痕迹的新图 |

## 数据流

- 画布状态通过 Vite dev server 的 API 路由（`/api/canvas`、`/api/selection`、`/api/canvas-events`）管理
- 使用 **SSE（Server-Sent Events）** 广播画布变更，实现多端同步
- 图片资源通过 `/page-assets/<page-id>/` 路由提供
- MCP 服务器通过 stdio JSON-RPC 2.0 与 Codex 通信

## 如何应用（How to apply）

1. **AI 辅助可视化创作**：标注 → AI 生成 → 迭代的工作流，可复用到任何需要"视觉反馈"的自动化场景
2. **Codex 插件开发参考**：完整的 Skills + MCP + 前端实现，是学习 Codex 插件生态的最佳范例
3. **本地持久化设计**：数据保存在用户项目目录而非插件目录，避免了数据与插件耦合

## 相关记忆

- [[narutocode-research]] — 终端 Agent 编程助手，可与 Cowart 组合使用（Cowart 提供可视化，NarutoCode 提供终端编程）
- [[sql-manything-research]] — 代码库搜索记忆，可为 Cowart 提供项目代码上下文
