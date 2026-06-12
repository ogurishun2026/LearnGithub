# awesome-ai-gateway 研究总结

> 仓库地址：https://github.com/cuihuan/awesome-ai-gateway
> 研究日期：2026-06-13

## 一、仓库概述

**一句话定位**：全网唯一给 50+ AI 网关「打分 + 配可复现成本评测」的精选清单，CC0 协议，中英双语，每日 GitHub Actions 自动更新。

不同于一般 awesome-* 系列只罗列链接，这个项目主打三件事：

1. **按真实诉求分类，而非按厂商罗列**——9 大痛点导向板块（性价比、自托管、合规、原厂、国产、智能路由、可观测、MCP/Agent 网关、K8s）
2. **四维评分卡**（合规·价格·安全·稳定 ★1–5）+ 每周人工更新
3. **可复现的 106× 成本评测**——同一份 10 万 token 报告，DeepSeek $0.03 vs GPT-5.5 $3.01，由 Python 脚本从公开价格表计算，带单元测试，绝不手填

仓库自 2026-06-11 创建，目前 15 Stars，作者 cuihuan，主语言 Python（脚本部分），文档 95% 是 Markdown。明确目标：400+ Stars 后申请入选 `sindresorhus/awesome` 元清单。

## 二、核心内容

### 2.1 仓库精选的 50+ AI 网关（9 大类）

| 板块 | 痛点 | 代表项目 |
|------|------|---------|
| 💰 性价比优先 | 用最少钱接最多模型，不想运维 | OpenRouter（400+ 模型）· Vercel AI Gateway（0 加价）· Cloudflare AI Gateway（免费控制面）· Requesty · Eden AI · Helicone 云版 |
| 🔓 自托管开源 | Key 自管，跑自家机器，不交按量过路费 | **LiteLLM**（50.1k Stars，Python 生态默认之选，100+ 厂商）· **Portkey Gateway**（12k，TypeScript，1600+ 模型）· **TensorZero**（11.5k，Rust，全家桶）· **Bifrost**（5.7k，Go，号称比 LiteLLM 快 50×）· Helicone · Plano · APIPark · OptiLLM · aisuite |
| 🏢 企业合规 | 审计/PII脱敏/RBAC/欧盟 AI 法案 | **Kong AI Gateway**（43.6k Stars）· Apache APISIX · Envoy AI Gateway · kgateway · TrueFoundry · nexos.ai · Tyk · Gravitee · WSO2 · F5 · IBM API Connect · MuleSoft · Lunar.dev |
| ☁️ 原厂直连 | 已绑定某朵云的官方方案 | AWS Bedrock · Azure APIM GenAI · Google Apigee+Vertex · Cloudflare · Vercel · Databricks Unity |
| 🇨🇳 国内生态 | 国产模型、人民币、团队 Key 分发 | **new-api**（38.4k Stars）· **one-api**（34.9k）· **Higress**（8.6k，阿里）· GPT-Load · one-hub · simple-one-api · Veloera · uni-api · APIPark |
| 🧠 智能路由 | 每条 prompt 路由到能胜任的最便宜模型 | Not Diamond · Martian · Inworld Router · RouteLLM · OpenRouter Auto · Unify |
| 📊 可观测与成本 | 谁花多少钱？质量为什么降了？ | Helicone · TensorZero · Portkey · vLLora · Braintrust Proxy · MLflow AI Gateway |
| 🤖 MCP 与 Agent 网关 | 治理 Agent ↔ 工具流量（2025–2026 新品类） | agentgateway（CNCF）· Lunar MCPX · Tetrate Agent Router · Zuplo · NetFoundry · AWS AgentCore Gateway |
| ☸️ K8s 原生 | 集群内路由到 vLLM/Ollama，GPU 感知 | Gateway API Inference Extension · AIBrix（字节）· llm-d（红帽/谷歌/IBM）· Higress · Kong · Envoy · Traefik · Inference Gateway |

每个条目都标注：项目名/星数（HTML 注释自动占位）/类型/协议许可/多厂商/故障转移/缓存/护栏/成本核算等结构化字段。

### 2.2 决策树（README 开篇）

```text
要不要自己部署？
├─ 不部署 — 托管
│   ├─ 最低成本 ──────────▶ OpenRouter · Vercel AI Gateway
│   ├─ 自带 Key+免费 ─────▶ Cloudflare AI Gateway
│   ├─ 欧盟合规 ──────────▶ Requesty · Eden AI · nexos.ai
│   └─ 已绑某朵云 ────────▶ AWS Bedrock · Azure APIM · Vertex
└─ 要部署 — 自托管
    ├─ Python 功能最全 ───▶ LiteLLM
    ├─ 极致性能 ──────────▶ Bifrost · TensorZero · Portkey
    ├─ 自带评测/可观测 ───▶ TensorZero · Helicone
    ├─ 国产/Key 分发 ─────▶ new-api · one-api · GPT-Load
    ├─ 企业 K8s ──────────▶ Kong · Higress · APISIX · Envoy
    └─ Agent/MCP ─────────▶ agentgateway · Lunar.dev
```

### 2.3 评测集 BENCHMARKS.zh-CN.md（核心专业度证明）

4 部分组成：

1. **权威模型基准** — Artificial Analysis 智能指数排序，含 GPQA Diamond / SWE-bench Verified / AIME / Arena Elo / AA 指数，13 个主流模型（Claude Fable 5 65 分 🥇 / Opus 4.8 / GPT-5.5 / Gemini 3.1 Pro / Qwen3.7 Max / Kimi K2.6 / DeepSeek V4 Pro …）
2. **按场景选模型** — 把"智能体编码 / 长上下文 / 硬核推理 / 批量生成 / 最便宜对话 / 私有化 / 强合规"7 类任务映射到"能力之选"+"性价比之选"
3. **真实 Token 成本实测**（脚本计算）— 4 个具体场景：
   - 写 10 万 token 报告：DeepSeek V4-Flash $0.028 → GPT-5.5 $3.01（**106×**）
   - 总结 10 万 token 文档：DeepSeek $0.015 → GPT-5.5 $0.56（**38×**）
   - 编码 Agent 会话（带 30k 思考 token）：DeepSeek $0.021 → GPT-5.5 $1.75（**83×**）
   - 百万 token 聊天机器人月度：DeepSeek $0.21 → GPT-5.5 …（均衡场景）
4. **网关四维评分**：合规·价格·安全·稳定 ★1–5 评分卡 + 公开评分标准

### 2.4 一行接入示例（OpenAI 兼容 base_url 速查表）

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # 改一行就接入 400+ 模型
    api_key="sk-or-...",
)
```

附 7 个主流网关的 `base_url`（OpenRouter / Vercel / Cloudflare / Portkey / Helicone / Requesty / LiteLLM）。

### 2.5 自动更新区（GitHub Actions 维护）

- **最新版本发布**：每日抓取主流网关的 GitHub Release，时间倒序列出 12 条
- **行业动态**：人工每月更新；最近一次审阅 2026-06-12，记录了 Palo Alto Networks 收购 Portkey（标志网关成核心安全基础设施）、OpenRouter 1.13 亿美元 B 轮、Cloudflare 上线消费上限等

## 三、技术架构

### 3.1 目录结构

```
awesome-ai-gateway/
├── README.md              # 英文主文档 (31.9 KB)
├── README.zh-CN.md        # 简体中文镜像 (30.9 KB)
├── BENCHMARKS.md          # 英文评测集 (18.9 KB)
├── BENCHMARKS.zh-CN.md    # 中文评测集 (18.1 KB)
├── CONTRIBUTING.md        # 贡献指南 (2 KB)
├── index.html             # GitHub Pages 在线交互页 (8.4 KB)
├── assets/                # 图片资产（cost-spread.png 等）
├── data/                  # 机器可读数据 (CC0)
│   ├── cost_table.csv          # 成本表
│   ├── gateways_eval.json      # 网关评分卡快照
│   ├── gateways_scorecard.csv  # 评分卡 CSV
│   ├── models.json             # 模型与价格（成本表唯一真理源）
│   ├── projects.json           # CI 跟踪的项目清单
│   └── releases.json           # 最近 release 抓取结果
├── docs/
│   └── SPEC.md                 # 项目规范（仓库契约/原则/更新节奏）
├── scripts/                    # 纯标准库 Python 实现
│   ├── update_readme.py        # 刷星数 + 重写 RELEASES 区块
│   ├── cost_calc.py            # 从 models.json 重新计算所有成本
│   ├── export_csv.py           # 导出 CSV
│   ├── make_cost_chart.py      # 生成 cost-spread 图
│   ├── make_social_preview.py  # 生成社交预览图
│   └── test_*.py               # 配套单元测试（项目规则：接口必须配测试）
└── .github/
    └── workflows/
        ├── ci.yml              # 单测（阻塞）+ 成本表新鲜度（阻塞）+ awesome-lint（建议）
        └── daily-update.yml    # 每日 02:23 UTC cron，仅在内容变化时提交
```

### 3.2 仓库契约（来自 docs/SPEC.md）

明确的 4 大原则：

1. **痛点优先，不按厂商**——板块回答"用户需求"而非"厂商分类"
2. **可分享资产 = 对比表 + 决策树**，不是链接列表
3. **每次自动提交必须真有内容变化**——禁止只更新时间戳
4. **准确性 > 完备性**——星数是近似值（CI 每日刷新），停滞项目明确标注而非默默保留

### 3.3 设计模式：Markdown 标记驱动的数据-视图分离

仓库的工程亮点是用 HTML 注释做插槽：

- **星数占位**：`<!--s:owner/repo-->⭐ 50.1k<!--/s-->`，CI 用脚本批量正则替换
- **成本块**：`<!-- COST:email:START -->...<!-- COST:email:END -->` 由 `cost_calc.py` 整段重写
- **Release 块**：`<!-- RELEASES:START -->...<!-- RELEASES:END -->` 由 `update_readme.py` 拉 GitHub Release API 后整段重写

中英双语共享同一套脚本和数据源，通过 `LABELS = {"en":..., "zh":...}` 字典做本地化文案切换。

### 3.4 评测引擎设计（cost_calc.py 核心思想）

```python
SCENARIOS = [
    Scenario("email",     "Write a 100K-token report",     2_000, 100_000),
    Scenario("summarize", "Summarize a 100K-token document", 100_000, 2_000),
    Scenario("coding",    "Coding-agent session",            50_000, 20_000, thinking_tokens=30_000),
    Scenario("chatbot",   "1M-token chatbot month",          500_000, 500_000),
]
```

- 价格统一以**美元/百万 token**为单位
- 推理模型（`reasoning: true`）额外把 `thinking_tokens` 计入 output 计费
- 每个图表场景在 `models.json` 中用 `scenario_cost: true` 显式 opt-in
- **纯标准库**（stdlib only），不引入任何依赖，CI 跑得快

### 3.5 评测原则（来自 SPEC）

> Every figure is sourced + dated; costs are computed and reproducible, not asserted.

- 每个数字都标注来源 + 日期
- 成本计算 + 可复现，绝不"声称"
- 基准用"静态分 + 人类偏好（Arena）+ 抗污染集（SWE-bench Pro / HLE）"三角验证
- CVE 诚实披露——可信度 > 营销

### 3.6 更新节奏

- **每日（自动）**：星数、release 区块、`data/releases.json`
- **每周（人工）**：新项目、行业动态新闻、板块调整
- **明确 out-of-scope**：价格抓取（避免过期价格责任）、灰产逆向"free-api"

## 四、实际应用场景

结合用户当前的项目背景（人工智能试验场、AI Game Studio 深度研究、多 Agent 协作、Claude Code 技能体系）：

### 4.1 选型参考（最直接价值）

用户索引里已有的 [new-api](https://github.com/QuantumNous/new-api) 是这份清单的核心条目之一（38.4k Stars，国内生态板块头牌）。这次研究给出了更完整的对比视野：

- **如果要做"统一 AI 服务"层**——LiteLLM（Python，功能最全）或 Bifrost（Go，性能优先）做自托管入口
- **如果只是给 AI Game Studio / 多 Agent 平台接 LLM**——直接走 OpenRouter（一把 Key 通 400+ 模型，省去多厂商 SDK）
- **如果要做企业级**——Kong AI Gateway 或 Higress（阿里系，对国产模型友好）
- **如果做 Agent 工具治理**——agentgateway（CNCF，专门为 MCP 流量设计），对接 Claude Code MCP 体系
- **如果做可观测**——Helicone 或 TensorZero（带评测+实验优化）

### 4.2 成本省钱手册

评测集第三部分的实测数据可以直接复用：

- **批量生成场景（长输出）**优先 DeepSeek V4-Flash，比 GPT-5.5 便宜 106×
- **长文档总结（长输入）**优先 DeepSeek V4-Flash（38× 价差）
- **编码 Agent 会话**优先 Kimi K2.6 / DeepSeek，开源模型已经接近 80% SWE-bench Verified

适合做 AI 游戏开发工具或自动化 Agent 时控制账单。

### 4.3 工程范式可借鉴

这个项目的「**Markdown 标记 + 单测脚本 + 数据 JSON**」三件套，对用户自己维护的研究索引库（`研究的github库/README.md`）很有参考价值：

- 用 `<!--s:owner/repo-->` 这种自动刷新星数，避免手工维护过期
- CI 跑 `daily-update.yml` 抓最新数据，**只在内容变化时才提交**（节省 git 历史噪音）
- 用 `LABELS["en"|"zh"]` 共享脚本同时输出双语

这套做法可以套到自己的 `LearnGithub` 仓库上，做"每日自动刷新所有研究过的项目的星数 + 最新动态"。

### 4.4 MCP/Agent 网关板块直接对接 Claude Code

用户全局 CLAUDE.md 大量使用 MCP Server 和子 Agent（VIPER-5 / vc-* 体系）。MCP/Agent 网关板块（特别是 agentgateway、Lunar MCPX、Zuplo）正好是给"多 Claude Code Agent 并行调工具"做治理的层——值得跟进观察。

### 4.5 速查附录：选型一句话总结

| 需求 | 推荐 |
|------|------|
| 零运维最便宜 | OpenRouter |
| 完全 0 加价 | Vercel AI Gateway / Helicone 云版 |
| 自托管最全 | LiteLLM |
| 自托管最快 | Bifrost（Go）/ TensorZero（Rust）|
| 国内/AGPL 接受 | new-api |
| 企业 K8s | Kong / Higress / Envoy AI Gateway |
| 智能路由 | Not Diamond / OpenRouter Auto |
| 可观测 | Helicone / TensorZero |
| Agent/MCP 治理 | agentgateway / Lunar.dev |

---

## 五、附：与本研究库其他条目的关系

- **序号 20** [new-api](../new-api/summary.md) — 本清单"国内生态"板块头牌，38.4k Stars，CC0/AGPL-3.0
- **序号 25** [ai-game-devtools](../ai-game-devtools/summary.md) — 同为 awesome-* 系列工程化标杆，可对比两者的「Markdown 标记 + 自动更新」做法
- **序号 47/48/50** EverOS / DeepSeek-Reasonix / Understand-Anything — 都会用到 LLM 网关层做多厂商兜底
