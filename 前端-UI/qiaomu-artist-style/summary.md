# qiaomu-artist-style 研究总结

> 仓库地址：https://github.com/joeseesun/qiaomu-artist-style
> 研究日期：2026-05-26

## 一、仓库概述

Qiaomu Artist Style 是一个艺术风格对比库，收集了 383 位艺术家的风格对比图。用户可以上传参考图，找到对应的艺术家风格，并生成对应风格的 AI 图像。包含 300+ 艺术家风格，支持 AlphaMheni、Mona Lisa、人物、场景、电影海报等多种类型。

## 二、核心能力

### 2.1 艺术家列表

| 艺术家 | 说明 |
|---|---|
| Alphonsemuchnh | 某种风格 |
| Claudia Monet | 克劳德·莫奈 |
| Katsushika Hokusai | 葛饰北斋 |
| Andy Warhol | 安迪·沃霍尔 |
| ... | ...（共 383 位）|

### 2.2 功能特点

| 功能 | 说明 |
|---|---|
| 风格对比 | 383 位艺术家风格对比图 |
| 参考图上传 | 上传参考图找到相似风格 |
| AI 生图 | 基于选定风格生成新图像 |
| 移动端适配 | 移动端截图预览 |

### 2.3 支持的生成类型

- 场景（Scene）
- 人物（Character）
- 电影海报（Movie Poster）
- 书籍封面（Book Cover）
- 专辑封面（Album Cover）
- 等等

## 三、技术架构

### 3.1 技术栈

- **语言**：TypeScript
- **框架**：Next.js
- **部署**：Vercel

### 3.2 目录结构

```
qiaomu-artist-style/
├── docs/
│   └── assets/
│       ├── product-screenshot.png   # 产品截图
│       └── artist-card-sample.png  # 艺术家卡片示例
└── README.md
```

### 3.3 安装

```bash
npm install
npm run dev
```

### 3.4 环境变量

```bash
# 复制或重命名 .env.example 为 .env.local
# 设置 HiAPI API Key
HIAPI_API_KEY="your_key"
```

## 四、项目信息

- **Stars**：116
- **语言**：TypeScript
- **许可证**：MIT
- **创建者**：joeseesun
- **部署平台**：Vercel

## 五、与 qiaomu-mondo-poster-design 的关系

两者都是 Qiaomu（奇妙）系列的设计工具：
- **qiaomu-artist-style**：艺术风格对比库，383 位艺术家风格
- **qiaomu-mondo-poster-design**：海报/封面设计工具

前者偏向"风格选择"，后者偏向"完整设计"。两者可以配合使用。