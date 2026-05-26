# opik-openclaw 研究总结

> 仓库地址：https://github.com/comet-ml/opik-openclaw
> 研究日期：2026-05-26

## 一、仓库概述

`opik-openclaw` 是 Comet 公司出品的官方插件，将 OpenClaw（开源 AI Agent 编排框架）的 Agent 运行轨迹导出到 Opik（开源 LLM/Agent 可观测性平台）进行监控和追踪。本质上是一个 Node.js npm 包，安装在 OpenClaw Gateway 进程中，拦截 Agent 的 LLM 调用、工具调用、子 Agent 生命周期等事件并发送到 Opik。

## 二、核心能力

### 2.1 追踪的事件类型

| OpenClaw 事件 | Opik 实体 |
|---|---|
| `llm_input` | trace + llm span |
| `llm_output` | llm span 更新/结束（写入 usage/output） |
| `before_tool_call` | tool span 开始（捕获工具名+输入） |
| `after_tool_call` | tool span 更新/结束（捕获输出/错误/耗时） |
| `subagent_spawning` | subagent span 开始（在请求者 trace 上启动） |
| `subagent_spawned` | subagent span 更新（丰富元数据） |
| `subagent_ended` | subagent span 结束（finalize 结果/错误） |
| `agent_end` | trace finalize（关闭所有 pending spans） |

### 2.2 可观测性内容

- LLM 请求/响应 span
- 子 Agent 请求/响应 span
- 工具调用 span（含 inputs、outputs、errors）
- Run-level finalize 元数据
- Usage 和 cost 元数据

### 2.3 追踪的事件类型

- LLM 请求/响应 spans
- 子 Agent 请求/响应 spans
- 工具调用 spans（含输入、输出、错误）
- Run 级别 finalize 元数据
- Usage 和 cost 元数据

## 三、技术架构

### 3.1 技术栈

- **语言**：TypeScript
- **运行时**：Node.js >= 22.12.0
- **包管理**：npm
- **插件协议**：OpenClaw Plugin API

### 3.2 工作原理

```
OpenClaw Gateway（运行 Agent）
    ↓ 拦截 Native Hooks
@opik/opik-openclaw 插件
    ↓ 发送追踪数据
Opik（Comet LLM 可观测性平台）
```

### 3.3 安装方式

```bash
# 通过 OpenClaw CLI 安装
openclaw plugins install clawhub:@opik/opik-openclaw

# 交互式配置
openclaw opik configure

# 查看配置状态
openclaw opik status

# 发送测试消息验证
openclaw gateway run
openclaw message send "hello from openclaw"
```

## 四、配置项

```json
{
  "plugins": {
    "entries": {
      "opik-openclaw": {
        "enabled": true,
        "hooks": { "allowConversationAccess": true },
        "config": {
          "apiKey": "your-api-key",
          "apiUrl": "https://www.comet.com/opik/api",
          "projectName": "openclaw",
          "workspaceName": "default",
          "tags": ["openclaw"],
          "toolResultPersistSanitizeEnabled": false,
          "staleTraceCleanupEnabled": true,
          "staleTraceTimeoutMs": 300000,
          "staleSweepIntervalMs": 60000
        }
      }
    }
  }
}
```

环境变量fallback：`OPIK_API_KEY`、`OPIK_URL_OVERRIDE`、`OPIK_PROJECT_NAME`、`OPIK_WORKSPACE`

## 五、与 Opik 的关系

Opik（https://github.com/comet-ml/opik）是 Comet 公司的开源 LLM/Agent 可观测性平台，opik-openclaw 是将 OpenClaw Agent 的轨迹接入 Opik 的官方桥接插件。两者共同提供：
- Agent 行为追踪
- Token/成本统计
- 错误监控
- 性能分析

## 六、项目信息

- **Stars**：616
- **语言**：TypeScript
- **许可证**：Apache 2.0
- **依赖**：Opik（上游）、OpenClaw（宿主框架）
- **前提**：OpenClaw >= 2026.3.2, Node.js >= 22.12.0