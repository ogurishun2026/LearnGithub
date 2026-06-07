# PriceAI 研究报告

## 项目概述

| 项目 | 内容 |
|------|------|
| **仓库** | https://github.com/physics-dimension/PriceAI |
| **Star** | 399 ⭐ |
| **Fork** | 45 |
| **语言** | TypeScript |
| **框架** | Next.js |
| **许可** | MIT |
| **官网** | https://priceai.cc |
| **组织** | physics-dimension（个人开发者） |

## 核心理念

**"AI 订阅项目多平台价格比较工具"**

PriceAI 是一个聚合100+ 平台的价格比较工具，对比 ChatGPT、Claude、Gemini、Grok 等多平台订阅、API/CDK 等多类型产品的价格，展示会话图表、价格状态、到账时间等原始站点信息。

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **价格聚合** | 聚合 100+ 平台/来源的价格数据 |
| 📊 **多平台对比** | ChatGPT、Claude、Gemini、Grok、API/CDK 等多类型产品 |
| 📈 **会话图表** | 展示会话图表、价格状态、到账时间等历史走势 |
| 🔗 **跳转原站** | 可转换到原始站点购买 |
| 🛡️ **来源可信** | 提供"AI 订阅代充卡商是否可靠"等指南 |

---

## 产品解决的问题

### 用户痛点

1. **产品分散不统一** —相同产品在不同平台价格各异
2. **价格来源分散** — 官方价格、市场价格、散售、渠道价、OEM 等多种形式
3. **缺货问题普遍** — 好价经常缺货，用户需要持续关注
4. **信息来源不可靠** — Telegram 群、咸鱼、第三方平台，价格变动不透明

### PriceAI 的方案

```
用户访问聚合比价页面
  -> 自动采集原始报价、价格、到货、来源信息
  -> 归一化为 ChatGPT Plus / Gemini Pro / Super Grok 等标准产品
  -> 展示会话图表、缺货状态、到账时间历史走势
  -> 跳转原站点购买
```

###核心产品原则

- **归一化为标准产品**：将不同平台的产品归一化为 `ChatGPT Plus`、`Claude Pro`、`Gemini Pro` 等可比较条目
- **展示原始数据**：展示原始站点报价、产品名称、价格状态、到账时间等原始信息
- **自动采集机制**：定时采集原站同款报价和到货，解决人工录入问题
- **来源透明追踪**：PriceAI 采集任何来源信息，用户自行判断可信度

---

## 技术架构

### 目录结构

```
PriceAI/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx           # 首页
│   │   ├── platforms/         # 平台比价页
│   │   ├── products/          # 产品详情页
│   │   ├── api-models/        # API 模型页
│   │   ├── official-prices/    # 官方价格页
│   │   ├── guides/ # 指南页
│   │   ├── admin/             # 管理后台
│   │   └── api/               # API 路由
│   ├── components/ # React 组件
│   │   ├── PriceExplorer.tsx # 价格浏览器
│   │   ├── ProductOffersPanel.tsx # 产品供应面板
│   │   ├── AdminConsole.tsx    # 管理后台
│   │   └── ...
│   └── lib/                   # 工具库
├── supabase/                  # Supabase 配置
├── config/ # 配置文件
├── docs/                      # 文档
│   ├── configuration.md       # 配置说明
│   ├── deployment.md          # 部署说明
│   ├── collectors.md          # 采集器说明
│   └── architecture.md        # 架构说明
├── DESIGN.md                  # 设计系统文档
├── PRODUCT.md                 # 产品说明
└── package.json
```

### 技术栈

| 技术 | 说明 |
|------|------|
| **Next.js** | React 全栈框架 |
| **TypeScript** | 类型安全 |
| **Supabase** | 后端即服务（数据库/认证） |
| **CSS** | 自定义设计系统 |

### 设计系统亮点

**色彩系统**：
- 主色：墨绿 `#202829`、工作炭 `#2d3435`、品牌绿 `#45bf78`
- 语义色：库存绿（可用）、缺货红（不可用）、警告琥珀（注意）

**字体系统**：
- 展示字体：Noto Serif SC（标题）
- 正文字体：Manrope（正文）

**设计原则**：
-表格优先的信息层级
- 胶囊式圆角控件
- 状态永远配文字（不单独使用颜色）

---

## 核心页面路由

| 路由 | 说明 |
|------|------|
| `/` | 首页 |
| `/platforms/chatgpt` | ChatGPT 等级比价 |
| `/platforms/claude` | Claude 等级比价 |
| `/products/[id]` | 产品详情页 |
| `/api-models` | 模型 API 价格 |
| `/official-prices` | 官方价格参考 |
| `/guides` | 用户指南 |
| `/admin` | 管理后台 |

---

## 采集系统

支持多种采集方式：
- **Shop API** — API 接口采集
- **HTML 解析** — 网页爬虫
- **Browser 采集** — 浏览器自动化

---

## 快速开始

```bash
npm install
npm run dev
```

默认访问：
- 前端：`http://localhost:3000`
- 后台：`http://localhost:3000/admin`

---

## 相关文档

- [项目介绍](./docs/project-intro.md)
- [配置说明](./docs/configuration.md)
- [部署说明](./docs/deployment.md)
- [采集器说明](./docs/collectors.md)
- [架构说明](./docs/architecture.md)
- [数据政策](./docs/data-policy.md)
- [产品原理](./PRODUCT.md)
- [设计系统](./DESIGN.md)

---

## 总结

**PriceAI** 是一个 **AI 订阅价格聚合比价平台**：
1. 聚合 100+ 平台的价格数据
2. 归一化为标准产品方便对比
3. 展示会话图表和历史走势
4. 提供来源可信度指南
5. 支持跳转原站购买

**定位**：不做评测、不给推荐，只做透明的价格信息聚合，让用户自己判断。

---

## 研究日期

2026-06-08