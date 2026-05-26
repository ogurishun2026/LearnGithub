# unity-cli-loop 研究总结

> 仓库地址：https://github.com/hatayama/unity-cli-loop
> 研究日期：2026-05-26

## 一、仓库概述

Unity CLI Loop 是一个让 AI Agent（Claude Code、Codex、Cursor 等）通过 CLI 驱动 Unity 项目的工具。核心价值是将 Unity 编辑器的编译、测试、日志检查、场景操作、截图验证等能力暴露为 LLM 可调用的工具，实现 AI 自主驱动的开发循环。原名 `uLoopMCP`，v1.0.0 起更名为 `unity-cli-loop`。

## 二、核心能力

### 2.1 四大核心功能

1. **AI 自主编译/测试循环**：AI 自动编译、测试、检查日志、修复问题
2. **AI 驱动 Unity 编辑器操作**：场景构建、对象操作、菜单执行、UI 截图布局验证
3. **PlayMode 自动化测试**：AI 点击按钮、拖拽元素、按键、录制重放输入、验证游戏行为
4. **最小化工具集**：专注核心能力，不做过度设计

### 2.2 工具列表（16 个 Bundled Skills）

| Skill | 功能 |
|---|---|
| `/uloop-launch` | 启动正确版本的 Unity |
| `/uloop-compile` | 执行编译 |
| `/uloop-get-logs` | 获取控制台日志 |
| `/uloop-run-tests` | 运行测试 |
| `/uloop-clear-console` | 清空控制台 |
| `/uloop-focus-window` | 将 Unity 窗口置于前台 |
| `/uloop-get-hierarchy` | 获取场景层级 |
| `/uloop-find-game-objects` | 查找 GameObject |
| `/uloop-screenshot` | 捕获 EditorWindow |
| `/uloop-simulate-mouse-ui` | 模拟鼠标点击/长按/拖拽 PlayMode UI |
| `/uloop-simulate-mouse-input` | 模拟鼠标输入（Input System） |
| `/uloop-simulate-keyboard` | 模拟键盘输入（Input System） |
| `/uloop-record-input` | 录制键盘和鼠标输入 |
| `/uloop-replay-input` | 重放录制的输入 |
| `/uloop-control-play-mode` | 控制 Play Mode |
| `/uloop-execute-dynamic-code` | 执行动态 C# 代码 |

### 2.3 使用示例

| 人类指令 | AI 调用的 Skill |
|---|---|
| "Launch Unity for this project" | `/uloop-launch` |
| "Fix the compile errors" | `/uloop-compile` |
| "Run the tests and tell me why they failed" | `/uloop-run-tests` + `/uloop-get-logs` |
| "Check the scene hierarchy" | `/uloop-get-hierarchy` |
| "Play the game and bring Unity to the front" | `/uloop-control-play-mode` + `/uloop-focus-window` |
| "Bulk-update prefab parameters" | `/uloop-execute-dynamic-code` |
| "Take a screenshot of Game View and adjust the UI layout" | `/uloop-screenshot` + `/uloop-execute-dynamic-code` |
| "Record my gameplay input" | `/uloop-record-input` |
| "Replay the recorded input" | `/uloop-replay-input` |

## 三、技术架构

### 3.1 技术栈

- **Unity 包**：C# Unity Package（`/Packages/src`）
- **CLI**：Node.js（需要 Node.js 22.0+）
- **可选依赖**：`com.unity.inputsystem`（Input System 功能）、`com.unity.test-framework`（Test Runner）
- **AI 集成**：Skills（Claude Code / Codex 兼容）

### 3.2 安装方式

**方式 1：Unity Package Manager**
```
Window > Package Manager > + > Add package from git URL
https://github.com/hatayama/unity-cli-loop.git?path=/Packages/src
```

**方式 2：OpenUPM（推荐）**
```
Name: OpenUPM
URL: https://package.openupm.com
Scope(s): io.github.hatayama.uloopmcp
```

### 3.3 MCP 集成

支持 MCP（Model Context Protocol），可通过 MCP 连接 AI 工具和 Unity 编辑器。

## 四、与 unity-mcp 的对比

| 维度 | unity-cli-loop | unity-mcp |
|---|---|---|
| Stars | 370 | 9.7K |
| 架构 | Unity Package + Node CLI | Unity 插件 + TypeScript 服务 |
| 关注点 | 编辑器操作 + PlayMode 测试 + AI 自主循环 | Editor 控制、资源/场景/脚本/构建 |
| MCP | 支持 MCP 工具 | 原生 MCP 服务器 |
| AI Skills | 有（16 个 bundled skills） | 无明确 Skills |

两者互补：unity-mcp 侧重 MCP 服务器架构，unity-cli-loop 侧重 AI 自主开发循环和 PlayMode 自动化测试。

## 五、项目信息

- **Stars**：370
- **语言**：C#（Unity Package）+ JavaScript（CLI）
- **许可证**：MIT
- **创建时间**：2025-06-15（非常新）
- **Topics**：ai, automation, cli, mcp, unity, unity3d
- **前置要求**：Unity 2022.3+, Node.js 22.0+