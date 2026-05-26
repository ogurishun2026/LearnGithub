# OpenDerisk 研究总结

> 仓库地址：https://github.com/derisk-ai/OpenDerisk
> 研究日期：2026-05-26

## 一、仓库概述

OpenDeRisk 是一个 AI-Native 风险智能系统，定位为应用系统的智能管理器，提供 7×24 小时全面深入的保护。核心能力是基于多 Agent 协作的深度根因分析（RCA），支持可视化证据链、DeepResearch RCA、多角色 Agent 协同。底层使用微软开源的 OpenRCA 数据集（26GB）进行训练和验证。

## 二、核心能力

### 2.1 功能列表

| 功能 | 说明 |
|---|---|
| DeepResearch RCA | 通过深度分析日志、追踪、代码快速定位根因 |
| 可视化证据链 | 完全可视化诊断过程和证据链，清晰准确判断 |
| 多 Agent 协作 | SRE-Agent、Code-Agent、ReportAgent、Vis-Agent、Data-Agent 协同工作 |
| 开放架构 | 纯开源架构，框架和代码可在开源项目中复用 |

### 2.2 多 Agent 架构

| Agent | 角色 |
|---|---|
| SRE-Agent | SRE 专家，负责故障分析和根因定位 |
| Code-Agent | 动态编写代码进行最终分析 |
| ReportAgent | 生成诊断报告 |
| Vis-Agent | 可视化渲染整个处理流程和证据链 |
| Data-Agent | 数据处理和分析 |

### 2.3 使用模式

- **AI-SRE（OpenRCA）**：基于 OpenRCA 数据集的根因分析
- **Flame Graph 助手**：上传 Java/Python flame graph 进行分析
- **DataExpert**：上传指标/日志/追踪/Excel 数据进行对话式分析

## 三、技术架构

### 3.1 三层架构

```
可视化层（Vis 协议动态渲染）
    ↓
逻辑层（多 Agent 协作）
    ↓
数据层（OpenRCA 数据集 26GB）
```

### 3.2 技术栈

- **语言**：Python
- **依赖**：DB-GPT、GPT-Vis（可视化）、MetaGPT（多 Agent）、OpenRCA（数据集）
- **工具**：uv（包管理）、MCP（模型上下文协议）、Skills
- **数据库**：ChromaDB（向量存储）、OSS（对象存储）
- **通道**：钉钉（可选）

### 3.3 安装方式

```bash
# 一键安装
curl -fsSL https://raw.githubusercontent.com/derisk-ai/OpenDerisk/main/install.sh | bash

# 启动
openderisk-server

# 或从源码
git clone https://github.com/derisk-ai/OpenDerisk.git
cd OpenDerisk
uv sync --all-packages --frozen --extra "base" --extra "proxy_openai" ...
uv run derisk quickstart
```

启动后访问 http://localhost:7777 配置模型和设置。

## 四、数据集

使用微软 OpenRCA 数据集（Banking 数据集，约 26GB），通过 multi-agent 协作进行根因分析，Code-Agent 动态编写代码进行最终分析。

```bash
# 下载数据集
gdown https://drive.google.com/uc?id=1enBrdPT3wLG94ITGbSOwUFg9fkLR-16R
# 移动到 pilot/datasets/
```

## 五、项目背景

基于论文：
> OpenDerisk: An Industrial Framework for AI-Driven SRE, with Design, Implementation, and Case Studies
> arXiv:2510.13561

致谢项目：DB-GPT、GPT-Vis、MetaGPT、OpenRCA

## 六、项目信息

- **Stars**：935
- **Forks**：123
- **语言**：Python
- **许可证**：MIT
- **创建时间**：2025-04-23
- **Discord**：https://discord.com/invite/bgWkskhe
- **Topics**：agent, ai-sre, aigc, devops, mcp, multi-agent-systems, rag, risk, rl, sre