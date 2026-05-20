# new-api 研究总结

> 仓库地址：https://github.com/QuantumNous/new-api
> 研究日期：2026-05-20

## 一、仓库概述

**下一代 LLM 网关和 AI 资产管理系统** —— 聚合与分发的统一 AI 模型中心。支持跨格式转换各种 LLM 为 OpenAI-compatible、Claude-compatible 或 Gemini-compatible 格式。适用于个人和企业的集中式模型管理。

**核心定位**：统一网关 + 配额管理 + 费用计费 + 多渠道负载均衡

## 二、核心内容

### 2.1 核心功能

| 功能 | 说明 |
|------|------|
| **多格式兼容** | OpenAI ⇄ Claude ⇄ Gemini 格式互转 |
| **智能路由** | 渠道加权随机 + 失败自动重试 |
| **用户级限流** | Token 分组 + 模型限制 |
| **配额与计费** | 内部充值、额度分配、按量计费 |
| **缓存计费** | OpenAI, Azure, DeepSeek, Claude, Qwen 等模型 |
| **多渠道管理** | 统一管理多个 API Key |
| **Discord/LinuxDO/Telegram 授权** | 多种第三方登录方式 |
| **OIDC 统一认证** | 企业级认证支持 |

### 2.2 支持的模型类型

| 类型 | 说明 |
|------|------|
| **OpenAI-Compatible** | 兼容 OpenAI 格式的模型 |
| **OpenAI Responses** | OpenAI 新 Response 格式 |
| **Claude Messages** | Claude Messages 格式 |
| **Google Gemini** | Gemini 格式 |
| **Midjourney-Proxy** | 图片生成 |
| **Suno-API** | 音乐生成 |
| **Rerank Models** | Cohere, Jina 重排模型 |
| **Dify ChatFlow** | Dify 集成 |
| **自定义上游** | 支持配置任意授权端点 |

### 2.3 支持的接口

| 接口类型 | 说明 |
|----------|------|
| Chat Completions | 标准对话接口 |
| Response | OpenAI Responses 格式 |
| Image | 图片生成 |
| Audio | 音频处理 |
| Video | 视频生成 |
| Embeddings | 向量嵌入 |
| Rerank | 重排接口 |
| Realtime | 实时对话 |
| Claude Chat | Claude 专用格式 |
| Gemini Chat | Gemini 专用格式 |

### 2.4 格式转换能力

```
OpenAI Compatible ⇄ Claude Messages
OpenAI Compatible → Google Gemini
Google Gemini → OpenAI Compatible (仅文本，函数调用暂不支持)
支持 Thinking-to-content 功能
```

### 2.5 Reasoning 模型支持

**OpenAI 系列：**
- `o3-mini-high/medium/low`
- `gpt-5-high/medium/low`

**Claude Thinking：**
- `claude-3-7-sonnet-20250219-thinking`

**Google Gemini：**
- `gemini-2.5-flash-thinking/nothinking`
- `gemini-2.5-pro-thinking`
- 可在任意 Gemini 模型后加 `-low/-medium/-high` 请求对应推理强度

## 三、技术架构

### 3.1 项目结构

```
new-api/
├── web/
│   ├── default/              # 默认 Web UI
│   └── classic/              # 经典 UI
├── pkg/                      # Go 核心包
│   ├── billingexpr/          # 计费表达式
│   ├── cachex/               # 缓存扩展
│   ├── ionet/                # 网络 I/O
│   └── perf_metrics/         # 性能指标
├── .agents/
│   └── skills/               # Agent 技能
├── docs/                     # 文档
├── docker-compose.yml        # Docker 部署配置
└── go.mod                    # Go 依赖
```

### 3.2 技术栈

| 组件 | 技术 |
|------|------|
| **语言** | Go |
| **前端** | Web UI (多主题) |
| **数据库** | SQLite (默认) / MySQL / PostgreSQL |
| **缓存** | Redis |
| **部署** | Docker / Docker Compose |
| **基础项目** | One API (MIT) |

### 3.3 部署要求

| 组件 | 要求 |
|------|------|
| 本地数据库 | SQLite (需挂载 /data) |
| 远程数据库 | MySQL ≥ 5.7.8 或 PostgreSQL ≥ 9.6 |
| 容器引擎 | Docker / Docker Compose |

### 3.4 关键环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SESSION_SECRET` | Session 密钥（多机部署必须） | - |
| `CRYPTO_SECRET` | 加密密钥（Redis 必须） | - |
| `SQL_DSN` | 数据库连接字符串 | - |
| `REDIS_CONN_STRING` | Redis 连接字符串 | - |
| `STREAMING_TIMEOUT` | 流式超时（秒） | 300 |
| `MAX_REQUEST_BODY_MB` | 最大请求体大小 | 32 |

## 四、与 One API 的关系

| 维度 | One API | new-api |
|------|---------|---------|
| **定位** | 基础网关 | 增强版网关 + 资产管理 |
| **Stars** | 22K | **34K** |
| **许可** | MIT | AGPLv3 |
| **计费功能** | 基础 | 完整计费 + 缓存统计 |
| **UI** | 基础 | 现代化多主题 |
| **格式转换** | 有限 | 完整跨格式转换 |

**new-api 是 One API 的增强分支**，保留了原有的数据库兼容性，添加了大量企业级功能。

## 五、应用场景

### 5.1 个人用户
- 统一管理多个 API Key（OpenAI、Claude、Gemini 等）
- 一个 Key 失效时自动切换到备用渠道
- 额度查询和用量统计

### 5.2 企业用户
- **计费系统**：内部充值、额度分配、按量计费
- **权限管理**：Token 分组、模型限制、用户管理
- **多渠道负载均衡**：加权随机分发请求
- **OIDC 统一认证**：企业 SSO 集成

### 5.3 AI 应用开发者
- 一次接入，统一调用多种模型
- 格式转换兼容不同 SDK
- 降低模型供应商锁定风险

## 六、Star 历史与社区

- **Stars**: 34,381 (截至 2026-05-20)
- **许可**: GNU AGPLv3
- **语言**: Go
- **更新活跃**: 2026-05-20
- **官方文档**: docs.newapi.pro

## 七、总结

new-api 是一个功能全面的 **LLM 网关和 AI 资产管理平台**，在 One API 基础上增加了企业级功能：

**核心价值**：
- 统一网关：聚合多个 LLM 提供商，一次接入
- 智能路由：加权随机 + 失败重试 + 限流
- 完整计费：充值、额度分配、缓存计费
- 格式转换：OpenAI ⇄ Claude ⇄ Gemini 跨格式兼容
- 现代化 UI：多主题支持，多语言（中文/英文/法文/日文）

**技术亮点**：
- Go 语言，高性能
- Docker 一键部署
- SQLite/MySQL/PostgreSQL 多数据库支持
- Redis 缓存支持
- 兼容 One API 数据库，平滑迁移

**适用场景**：
- 需要统一管理多个 AI API 的个人或团队
- 需要计费和配额管理的企业
- 需要负载均衡和高可用性的 AI 服务部署
