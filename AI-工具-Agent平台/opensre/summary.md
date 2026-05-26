# opensre 研究总结

> 仓库地址：https://github.com/Tracer-Cloud/opensre
> 研究日期：2026-05-26

## 一、仓库概述

`OpenSRE`（Open Site Reliability Engineering）是一个开源 AI SRE Agent 框架，用于在自有基础设施上解决生产环境故障。定位是 AI 时代的"SWE-bench"——为 AI SRE Agent 提供可训练的强化学习环境，包含端到端测试和合成故障模拟，让 AI 能够调查和响应真实的基础设施故障。

## 二、核心能力

### 2.1 功能列表

| 能力 | 说明 |
|---|---|
| 结构化故障调查 | 跨所有信号的关联根因分析 |
| Runbook 感知推理 | 自动读取并应用运维手册 |
| 预测性故障检测 | 在告警触发前捕获潜在问题 |
| 证据链根因分析 | 每个结论都关联到背后数据 |
| 全模型灵活性 | 支持 Anthropic/OpenAI/Ollama/Gemini/OpenRouter/NVIDIA NIM |

### 2.2 支持的 60+ 集成

| 类别 | 集成 |
|---|---|
| LLM | Anthropic · OpenAI · Ollama · Google Gemini · OpenRouter · NVIDIA NIM · Bedrock |
| 可观测性 | Grafana · Datadog · Honeycomb · CloudWatch · Sentry · Elasticsearch |
| 基础设施 | Kubernetes · AWS · GCP · Azure |
| 数据库 | MongoDB · ClickHouse · PostgreSQL · MySQL · Snowflake |
| 数据平台 | Airflow · Kafka · Spark · Prefect |
| 事件管理 | PagerDuty · Opsgenie · Jira · Alertmanager |
| 通信 | Slack · Discord · Telegram |
| Dev工具 | GitHub · GitLab · Bitbucket |

## 三、技术架构

### 3.1 工作流程

当告警触发时，OpenSRE 自动：
1. **获取** 告警上下文和关联的日志/指标/追踪
2. **推理** 跨连接系统识别异常
3. **生成** 结构化调查报告（含可能根因）
4. **建议** 下一步操作，可选执行修复
5. **推送** 摘要到 Slack 或 PagerDuty

### 3.2 测试体系

- **合成 RCA 测试**：检查根因准确性、所需证据、对抗性干扰项
- **端到端测试**：跨云场景（Kubernetes/EC2/CloudWatch/Lambda/ECS Fargate/Flink）
- 本地 vs 云端边界保持清晰

### 3.3 技术栈

- **语言**：Python
- **框架**：FastAPI
- **部署**：Docker / Railway / EC2 / ECS / Vercel
- **Agent**：支持多种 LLM Provider，可配置推理深度（low/medium/high/xhigh/max）

### 3.4 目录结构

```
opensre/
  tests/
    synthetic/    # 合成 RCA 测试
    e2e/          # 端到端测试
  docs/           # 文档
  docs/assets/     # 集成图标
```

## 四、安装和使用

### 4.1 安装

```bash
# Linux/macOS
curl -fsSL https://install.opensre.com | bash

# Windows (PowerShell)
irm https://install.opensre.com | iex

# Homebrew
brew tap tracer-cloud/tap
brew install tracer-cloud/tap/opensre
```

### 4.2 使用

```bash
# 首次配置
opensre onboard

# 交互式 Shell（描述故障，流式调查）
opensre

# 一次性调查
opensre investigate -i tests/e2e/kubernetes/fixtures/datadog_k8s_alert.json
```

### 4.3 部署

部署为标准 Python/FastAPI 应用，设置 `LLM_PROVIDER` 和对应的 API key，需要持久化的场景配置 `DATABASE_URI` 和 `REDIS_URI`。

## 五、项目定位

- **愿景**：成为 AI SRE Agent 的基准测试和训练环境
- **现状**：Pre-alpha 阶段（核心工作流可用但 API 可能变化）
- **使命**：在自有基础设施上构建 AI SRE Agent，扩展到数千个真实的基础设施故障场景

## 六、项目信息

- **Stars**：5899（非常高）
- **Forks**：770
- **语言**：Python
- **许可证**：Apache 2.0
- **创建时间**：2026-01-13
- **主页**：https://www.opensre.com
- **Discord**：https://discord.gg/7NTpevXf7w
- **Topics**：ai-sre, alerting, datadog, grafana, incident-management, observability, remediation, root-cause-analysis, sre