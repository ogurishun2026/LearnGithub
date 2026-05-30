# hyperframes 研究总结

> 仓库地址：https://github.com/heygen-com/hyperframes
> 研究日期：2026-05-30

## 一、仓库概述

HyperFrames 是 **HeyGen** 开源的视频生成框架，核心理念是"**Write HTML. Render video. Built for agents.**"——用 HTML/CSS/动画定义视频，框架负责在 headless Chrome 中 seek 到每一帧并用 FFmpeg 编码为 MP4。22,403 Stars，Apache 2.0 许可证。主要特点：无构建步骤、确定性渲染、Agent 友好、开放生态。

## 二、核心内容

### 2.1 核心工作流

```
编写 HTML（带 data 属性和 GSAP 等动画）→ npx hyperframes preview（浏览器预览）→ npx hyperframes render（渲染 MP4）
```

### 2.2 视频定义示例

```html
<div id="stage" data-composition-id="launch" data-start="0" data-width="1920" data-height="1080">
  <!-- 背景视频轨道 -->
  <video class="clip" data-start="0" data-duration="6" data-track-index="0"
    src="intro.mp4" muted playsinline></video>

  <!-- 文字轨道 -->
  <h1 id="title" class="clip" data-start="1" data-duration="4" data-track-index="1">Launch day</h1>

  <!-- 音频轨道 -->
  <audio data-start="0" data-duration="6" data-track-index="2" data-volume="0.5" src="music.wav"></audio>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 40, duration: 0.8 }, 1);
    window.__timelines = window.__timelines || {};
    window.__timelines.launch = tl;
  </script>
</div>
```

### 2.3 可构建内容

- 产品发布视频和功能公告
- PR 演示（动画代码 diff + 配音 + 字幕）
- 数据可视化、图表竞跑、地图动画
- 社交短视频（动态字幕、叠加层、音乐）
- Docs-to-video、PDF-to-video、网站-to-video 解释器
- 自动化内容管线的可复用动态图形

### 2.4 AI Agent 集成

```bash
# 安装 HyperFrames skills
npx skills add heygen-com/hyperframes
```

支持 Claude Code、Cursor、Gemini CLI、Codex 等主流编码 Agent。Skills 教会 Agent 视频制作模式：规划视频→写有效 HTML→接入 seekable 动画→添加媒体→检查→预览→渲染。

提供专门的：
- [Claude Design guide](https://hyperframes.heygen.com/guides/claude-design)
- [Open Design guide](https://hyperframes.heygen.com/guides/open-design)

### 2.5 本地 CLI 使用

```bash
npx hyperframes init my-video   # 初始化项目
cd my-video
npx hyperframes preview         # 浏览器预览（热重载）
npx hyperframes render          # 渲染 MP4
```

**环境要求**：Node.js 22+，FFmpeg

### 2.6 可用包一览

| 包 | 用途 |
|----|------|
| `hyperframes` (CLI) | 创建、预览、lint、检查、渲染 composition |
| `@hyperframes/core` | 类型、解析器、生成器、linter、运行时、帧适配器 |
| `@hyperframes/engine` | Puppeteer + FFmpeg 驱动的 seekable 页面→视频捕获引擎 |
| `@hyperframes/producer` | 捕获、编码、混音的完整渲染管线 |
| `@hyperframes/studio` | 浏览器端 composition 编辑器 UI |
| `@hyperframes/player` | 可嵌入的 `<hyperframes-player>` Web 组件 |
| `@hyperframes/shader-transitions` | WebGL shader 转场效果 |
| `@hyperframes/aws-lambda` | AWS Lambda SDK，支持分布式渲染部署 |

### 2.7 Catalog（可安装的块）

```bash
npx hyperframes add flash-through-white   # shader 转场
npx hyperframes add instagram-follow      # 社交叠加层
npx hyperframes add data-chart           # 动画图表
```

在线目录：[hyperframes.heygen.com/catalog](https://hyperframes.heygen.com/catalog/blocks/data-chart)

### 2.8 部署选项

- **本地渲染**：CLI 直接调用
- **Docker**：容器内渲染
- **AWS Lambda**：分布式渲染集群，支持从 CI/本地驱动

## 三、技术架构

### 3.1 渲染原理

1. 解析 HTML composition 中的 `data-*` 属性，构建时间轴
2. 使用 Puppeteer 驱动 headless Chrome，根据时间 seek 到每一帧
3. FFmpeg 编码视频帧 + 混音音频轨道
4. 输出确定性 MP4（相同输入→相同帧→相同输出）

### 3.2 动画支持

通过**帧适配器（frame adapters）** 接入多种动画库：
- GSAP
- CSS 动画
- Lottie
- Three.js
- Anime.js
- WAAPI（Web Animations API）
- 自定义运行时

### 3.3 仓库结构

```
hyperframes/
├── packages/
│   ├── cli/                 # CLI
│   ├── core/                # 核心库
│   ├── engine/              # 渲染引擎
│   ├── producer/            # 生产管线
│   ├── studio/              # 编辑器 UI
│   ├── player/              # Web 组件播放器
│   ├── shader-transitions/  # WebGL 转场
│   └── aws-lambda/          # Lambda 渲染
├── skills/                  # Agent skills 定义
├── registry/                # 组件注册表
├── docs/                    # 文档
├── examples/               # 示例
└── ADOPTERS.md             # 实际使用者列表（tldraw、TanStack 等）
```

### 3.4 开发注意

仓库使用 **Git LFS** 存储回归测试基线（`packages/producer/tests/**/output.mp4`，约 240 MB）。完整 clone 前需安装 git-lfs：

```bash
brew install git-lfs  # macOS
# 然后
git lfs install
git clone https://github.com/heygen-com/hyperframes.git
```

跳过 LFS 内容：
```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git
```

### 3.5 与 Remotion 对比

| 维度 | HyperFrames | Remotion |
|------|-------------|----------|
| 创作方式 | HTML + CSS + seekable 动画 | React 组件 |
| 构建步骤 | 无；`index.html` 直接播放 | 需要 Bundler |
| Agent handoff | 纯 HTML 文件 | JSX / React 项目 |
| 动画精度 | 通过 adapter 实现帧级 seek | wall-clock 动画需小心处理 |
| 分布式渲染 | 本地 + AWS Lambda | Remotion Lambda |
| 许可证 | Apache 2.0 | 源码可用 Remotion License |

## 四、实际应用场景

### 4.1 目标用户

- **AI 编码 Agent 用户**：通过 skills 让 Agent 自动生成视频内容
- **视频内容创作者**：用熟悉的 HTML/CSS 工作流替代专业视频软件
- **CI/CD 流水线**：自动化视频渲染，相同输入保证确定性输出
- **企业视频团队**：HeyGen 生产环境使用 + ADOPTERS.md 列出 tldraw、TanStack 等实际案例

### 4.2 典型使用模式

1. **纯 CLI**：本地快速渲染视频原型
2. **Agent 驱动**：编码 Agent 接收自然语言需求 → 输出 HTML → 渲染 MP4
3. **设计 handoff**：设计师提供 HTML 原型 → 开发者接入动画 → 渲染
4. **规模化渲染**：AWS Lambda 分布式处理大量视频任务

## 五、总结

HyperFrames 解决的核心问题是"让 AI Agent 和人类都能用同一种语言（HTML）创作视频"。相比 Remotion 的 React 路线，HTML-native + 无构建步骤的设计对 Agent 更友好，对非前端背景的创作者也更易上手。HeyGen 的生产环境背书 + 活跃社区（22K Stars、2K Forks）说明其工程成熟度足够。确定性渲染输出使其特别适合 CI 和自动化内容管线。
