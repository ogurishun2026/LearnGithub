# claude-image 研究总结

> 仓库地址：https://github.com/jiangmuran/claude-image
> 研究日期：2026-05-20

## 一、仓库概述

**教 Claude Code、Codex 等 Agent 真正用好 GPT Image 2 的 drop-in skill 包**。让 AI Agent 从「这是个 curl 命令，祝你好运」进化成一次到位地产出 pitch deck 幻灯片、中文海报、像素图块、写实产品图、外科手术级修图。

**核心定位**：解决 AI Agent 在 GPT Image 2 时代之前的训练数据过时问题，教会 Agent 正确的图像生成 prompt 技巧和自验证流程。

## 二、核心内容

### 2.1 项目结构

```
gpt-image-2/
├── SKILL.md                # 入口，Claude 自动加载
├── README.md               # 文档（中英双语）
├── LICENSE                 # MIT
├── install.sh              # Claude Code 一键安装脚本
├── .env.example            # 环境变量模板
├── references/
│   ├── prompting.md        # 7条习惯 + 意图优先框架 + 风格词表
│   ├── use-cases.md         # 10+ 复制即用模板
│   ├── api.md              # 完整参数 + 自定义分辨率约束
│   └── post-process.md     # 压缩、缩放、转码指南
└── scripts/
    └── gpt_image.py        # 零依赖 Python CLI（仅 urllib）
```

### 2.2 核心能力

| 功能 | 说明 |
|------|------|
| **Pitch-deck 幻灯片** | 真正的 Series A 董事会幻灯片风格，多页一致性 |
| **中文海报和招贴** | 春节海报、产品发布、活动封面，中日韩文字渲染正确 |
| **写实 UI mockup** | 桌面 dashboard、移动端，放在真实设备外框里 |
| **像素图和游戏素材** | 角色 sprite、俯视图块集、物品图标、角色三视图 |
| **信息图** | GPT Image 2 能正确渲染的密集文字 + 复杂结构 |
| **Logo 概念** | 2x2 变体网格，探索不同形状语言 |
| **写实产品图** | 真正的摄影术语而非"高品质" |
| **外科手术级修图** | `change ONLY X / preserve Y exactly` 模式 |

### 2.3 安装方式

#### Claude Code（一行命令）
```bash
git clone https://github.com/jiangmuran/claude-image.git ~/.claude/skills/gpt-image-2 \
  && bash ~/.claude/skills/gpt-image-2/install.sh
```

#### Codex（或其他 agent）
```bash
git clone https://github.com/jiangmuran/claude-image.git ~/.agents/skills/gpt-image-2 \
  && bash ~/.agents/skills/gpt-image-2/install.sh
```

#### 手动 / CLI 独立使用
```bash
git clone https://github.com/jiangmuran/claude-image.git
cd gpt-image-2

echo 'export OPENAI_IMAGE_API_KEY="sk-..."' >> ~/.zshrc
echo 'export OPENAI_IMAGE_BASE_URL="https://jmrai.net/v1"' >> ~/.zshrc

python3 scripts/gpt_image.py generate -p "..." -o ./output.png
```

### 2.4 环境变量

| 变量 | 必填 | 默认值 |
|------|-----|--------|
| `OPENAI_IMAGE_API_KEY` | 是 | — |
| `OPENAI_IMAGE_BASE_URL` | 否 | `https://jmrai.net/v1` |

回退到 `OPENAI_API_KEY` / `OPENAI_BASE_URL`。

## 三、核心设计理念

### 3.1 Prompt 工程变革

**旧方式（GPT Image 2 之前）**：
```
beautiful stunning ultra-detailed 4K 8K masterpiece trending on artstation
cinematic lighting professional photography premium quality
```

**新方式（GPT Image 2 奖励）**：
```
Create a pitch-deck slide titled "Q3 Revenue Performance" that looks
like a real Series A board-meeting slide. Layout (16:9): title top-left,
36pt Inter dark gray. Two-column body: left 60% chart, right 40% three
KPI cards. Chart: vertical bars, Q1–Q3 2026, y-axis $0–$8M...
```

**核心原则**：抛掉魔法咒语，使用指令式、具体、意图优先的 prompt。

### 3.2 七条习惯

1. **意图开头** — 以期望结果开头而非形容词开头
2. **所有文字加引号** — 精确控制文字内容
3. **用规格语言不用夸赞语言** — `50mm f/2.8` 而非 `高质量`
4. **修图永远 "change ONLY X / preserve Y exactly"** — 精准局部修改
5. **一个风格锚点不要五个** — 避免风格冲突
6. **抛掉魔法咒语** — 不用 `ultra detailed`, `4K`, `masterpiece`
7. **迭代不要堆砌** — 一次改一个维度然后重新生成

### 3.3 视觉自验证

Skill 明确告诉 Claude **自己 `Read` 生成的 PNG 并对照 prompt 判断**，然后再给用户看。

```
文字渲染对了吗？ → 对照 prompt 检查
构图在你说的位置吗？ → 检查布局
negative 听话了吗？ → 检查负面约束
```

如果不对，agent 会**一次只改一个维度**然后重新生成。

### 3.4 可发现的 description

frontmatter 里把所有触发词都列了：
- "海报"、"图标"、"ppt素材"、"改图"
- "draw me"、"make an image"、"generate an image"

让 agent 的 skill 选择器在收到图像请求时**真的会触发**，而不是退回去自己拼 curl。

## 四、技术架构

### 4.1 零 Python 依赖

CLI 只用 `urllib`、`concurrent.futures`、`argparse`。无 `requests`、无 `openai` SDK。任何 Python 3.7+ 都能跑。

### 4.2 客户端并行

`-n 4` 是发 4 个并行的 n=1 请求，而非请求 host 一次返回 4 张图。墙钟时间快、不用管 host 是否支持 n>1。

### 4.3 合理的默认值

- `--quality high`（此 host 各档质量同价）
- `--size 1024x1024`
- `--concurrency 4`

### 4.4 预先验证

分辨率约束（最长边 <3840px、比例 ≤3:1）在请求 API 之前检查——快速失败、信息明确。

### 4.5 CLI 子命令

```bash
GI="python3 ~/.claude/skills/gpt-image-2/scripts/gpt_image.py"

# 生成
$GI generate -p "..." -o ./output.png

# 4张并行变体
$GI generate -p "..." -n 4 --concurrency 4 -o ./out

# 修图/局部重绘
$GI edit -i ./photo.png -p "replace ONLY the sky with northern lights" -o ./aurora.png

# 帮助
$GI generate --help
$GI edit --help
```

## 五、Star 历史与社区

- **Stars**: 57 (截至 2026-05-20)
- **语言**: Python
- **许可**: MIT
- **更新**: 2026-05-20

## 六、总结

claude-image 是一个精巧的 **Claude Code skill 包**，专注于解决 AI Agent 在图像生成领域的"最后一公里"问题。

**核心价值**：
- 教 Agent 用正确的方式写 prompt（意图优先而非魔法咒语）
- 内置视觉自验证工作流
- 零依赖 Python CLI，可独立使用
- 支持生成/编辑/局部重绘/并行批处理

**设计亮点**：
- 可发现的 description 让 Agent 真正调用而非装饰
- "change ONLY X / preserve Y exactly" 模式实现精准修图
- 中文、日文、韩文文字渲染支持

**适用场景**：
- Claude Code / Codex 用户需要生成高质量图像
- 需要中文海报、PPT 素材的产品设计流程
- 需要精确修图而非"生成全新图"的场景

## 七、相关资源

- [GPT Image 2 API](https://order.jmrai.net) — credits 购买
- [Anthropic Skills](https://github.com/anthropics/skills) — 官方 skill 集合