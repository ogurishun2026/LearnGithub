# Gen-Image 研究总结

> 仓库地址：https://github.com/SummerSec/Gen-Image
> 研究日期：2026-05-19

## 一、仓库概述

**Gen-Image**（Image Studio）是一个基于 OpenAI GPT Image 模型的前端图像生成工作台，提供提示词库管理和多图生成功能。

| 基础信息 | 值 |
|---------|-----|
| Stars | 5 |
| 主要语言 | TypeScript |
| License | 未标明 |
| 状态 | 早期项目 |

## 二、核心功能

### 2.1 提示词库

- 从两个上游仓库同步提示词（作为 git submodules）：
  - `freestylefly/awesome-gpt-image-2`
  - `EvoLinkAI/awesome-gpt-image-2-API-and-Prompts`
- 提示词缩略图本地化存储
- 点击提示词：自动填充文本框 + 加载缩略图到预览区

### 2.2 图片生成

- 支持单次生成 1-4 张图片
- 参考图上传支持多选
- 预览支持缩放和重置
- API 设置保存在浏览器 localStorage

### 2.3 响应式设计

- 桌面端和移动端适配

## 三、技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | React 19 |
| 语言 | TypeScript |
| 构建工具 | Vite |
| 样式 | Tailwind CSS 4 |
| 状态管理 | Zustand |
| AI SDK | OpenAI JS SDK |

## 四、项目结构

```
Gen-Image/
├── src/
│   ├── components/       # React 组件
│   ├── data/
│   │   ├── prompts.ts     # 提示词入口
│   │   ├── prompts.manual.ts  # 手动维护的提示词
│   │   └── prompts.generated.ts  # 自动生成的提示词（勿手动编辑）
│   ├── services/         # API 服务
│   └── store/            # Zustand 状态管理
├── external/             # Git submodules
│   ├── awesome-gpt-image-2
│   └── awesome-gpt-image-2-api-prompts
├── public/
│   └── prompt-thumbs/    # 本地化的提示词缩略图
├── scripts/
│   ├── setup-prompt-submodules.ps1
│   └── sync-prompts.mjs  # 提示词同步脚本
├── package.json
└── vite.config.ts
```

## 五、快速开始

```bash
npm install
# 初始化 git submodules 并同步提示词
powershell -ExecutionPolicy Bypass -File scripts/setup-prompt-submodules.ps1
npm run sync:prompts
npm run dev
# 访问 http://localhost:5173
```

## 六、提示词同步流程

`npm run sync:prompts` 调用 `scripts/sync-prompts.mjs`：
- **EvoLinkAI**：提取 `cases/*_zh-CN.md` 中的简体中文案例
- **freestylefly**：提取 `docs/gallery-part-1.md` 和 `docs/gallery-part-2.md` 中的提示词

缩略图策略：
- 图片从 submodules 复制到 `public/prompt-thumbs/`
- 命名空间隔离避免冲突
- 生成的数据引用本地路径

## 七、与游戏开发的关系

Gen-Image 是一个轻量级的 AI 生图前端工具，可用于：

| 用途 | 说明 |
|------|------|
| **游戏美术提示词管理** | 内置的 GPT Image 提示词库可作为游戏美术风格参考 |
| **快速原型** | 简单的前端界面可用于快速测试 AI 生图效果 |
| **参考** | 项目结构可作为类似工具的参考模板 |

## 八、总结

**价值定位：**
Gen-Image 是一个非常早期的轻量级 GPT Image 前端工具，核心价值是提示词库管理和多图生成功能。

**优势：**
- 简单易用，适合快速测试 GPT Image 生成效果
- 内置丰富的提示词库（通过 submodules 同步上游）
- 响应式设计，支持移动端

**劣势：**
- Stars 极少（5），几乎是个人玩具项目
- 功能单一，不支持画布编排等高级功能
- 没有后端，所有数据存在浏览器 localStorage

**对比 ProductFlow：**
| 维度 | Gen-Image | ProductFlow |
|------|-----------|------------|
| 复杂度 | 轻量纯前端 | 全栈应用 |
| 功能 | 提示词库 + 生图 | 商品工作台 + 画布编排 + AI 生图 |
| 成熟度 | 早期项目 | 较完整 |
| Stars | 5 | 152 |

---

> 更多信息请参考：
> - [官方仓库](https://github.com/SummerSec/Gen-Image)