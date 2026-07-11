# spine-animation-ai 研究总结

> 仓库地址：https://github.com/GenielabsOpenSource/spine-animation-ai
> 研究日期：2026-07-11
> Stars：252 · Forks：34 · 主要语言：Python · 许可证：PolyForm Noncommercial 1.0.0（非商业免费，商用需授权）

## 一、仓库概述

一个 **AI 驱动的 Claude Skill（Claude 智能体技能）**，专门把 Spine 2D 骨骼动画（Esoteric Software 出品的行业标准 2D 动画工具）的繁琐生产环节自动化。核心定位：**你提供角色美术素材，Claude 帮你算骨骼、定位、生成动画和预览**——相当于一个"Spine 绑骨副驾驶（rigging co-pilot）"。

由 **Genielabs**（一家研究 AI 驱动 2D 动画流水线的公司）开源，是其研究成果的直接产物。

## 二、核心功能

1. **自动定位身体部件**：用 SIFT + RANSAC 算法从参考图反推每个部件在角色上的位置
2. **构建骨骼 JSON**：生成带正确骨骼层级和绘制顺序（draw order）的 Spine skeleton.json
3. **生成动画**：内置 6 种预设（idle 待机 / walk 行走 / run 奔跑 / wave 挥手 / jump 跳跃 / attack 攻击），遵循"动画十二原则"
4. **HTML5 交互预览**：用官方 Spine Web Player 生成自包含的 HTML 预览文件，浏览器直接打开，无需服务器
5. **AI 辅助修正**：分析现有骨骼，输出可审查、可回退、可组合的偏移调整（offset adjustment）
6. **单图拆分（新）**：只有一张整图时，用 Google Gemini 生成拆解精灵图集，再用 OpenCV 连通域分析切成透明 PNG
7. **Reskin Studio（新）**：一句话给已绑骨角色换皮肤（详见下文）

## 三、技术架构

### 目录结构

```
spine-animation-ai/
├── SKILL.md                  ← 自动生成，内嵌全部脚本（勿手改）
├── SKILL.template.md         ← 人类可编辑的模板源
├── build_skill.py            ← 从模板+脚本构建 SKILL.md
├── scripts/
│   ├── split_character.py           单图 → 部件拆分（Gemini + OpenCV）
│   ├── position_parts.py            SIFT+RANSAC 自动定位
│   ├── build_spine_json.py          Spine JSON 构建器
│   ├── make_atlas.py                纹理图集打包
│   └── generate_spine_player.py     HTML 预览生成器
├── .github/workflows/build-skill.yml  推送时自动重建 SKILL.md
├── references/spine-json-spec.md      Spine 格式参考
├── examples/sombrero/                 完整可运行示例（10部件/16骨骼/2秒待机循环）
├── demo/                              预览 HTML + gif 演示
├── docs/                              入门/调整格式/prompt 指南
└── reskin-app/                        Reskin Studio 独立应用
```

### 自动定位算法（position_parts.py 的两阶段）

- **阶段一 SIFT + RANSAC（主）**：对每个部件（按 alpha 遮罩取可见像素）和拼装参考图各提取 SIFT 关键点 → FLANN 匹配 + Lowe 比率测试 → RANSAC 估计相似变换（平移+缩放+旋转）→ 4+ 内点匹配即接受。比全单应性（homography）更适合特征稀疏的风格化游戏美术。
- **阶段二 遮挡分析定 Z 序**：对每对重叠部件采样重叠区像素，与参考图比色，颜色更接近的在上层 → 构建有向遮挡图 → 拓扑排序得绘制顺序。
- **兜底 模板匹配**：部件太小无法 SIFT 时，用 alpha 遮罩的 `TM_CCORR_NORMED` 多尺度匹配 + 背景惩罚打分。

### SKILL.md 自动同步机制

SKILL.md 是自动生成的：编辑 `SKILL.template.md`（散文/说明）和 `scripts/`（真实代码）→ 推送 main → GitHub Actions 跑 `build_skill.py`，把 `<!-- EMBED:scripts/xxx.py -->` 标记替换成脚本真实内容，塞进可折叠 `<details>` 块并自动提交。这样 SKILL.md 永远是**自包含文档**——粘进 Claude Projects 时，Claude 手里直接就有全部脚本代码，无需克隆仓库。

### Reskin Studio（reskin-app/，TypeScript/HTML/CSS 主要来源）

AI 换皮子应用。加载已有 Spine 工程，用 `spine-pixi-v8` 实时渲染，一键换皮：
1. 快照实时画布 → 2. 补边到 Gemini 支持的最近宽高比 → 3. 送 Gemini "Nano Banana" 全局重绘 → 4. 裁回原尺寸 → 5. 通过切换 slot 可见性算每个 slot 的 bbox → 6. 调 SAM-3 服务器（一次 HTTP）拿每 slot 精确遮罩 → 7. 重打包每皮肤图集 + 写 `Spine-{skin}.json` → 8. 画布重载，渲染 AI 换皮后的角色。

还有遮罩编辑器（笔刷/橡皮/套索/SAM 魔术选择）、AI 终端（逐 slot 局部重绘 inpainting）、逐 slot 非破坏性 HSL/RGB/对比度/变换调节、导出回 Spine。

- **前端**：Vite + React + TypeScript + spine-pixi-v8（PixiJS 画布）
- **后端**：FastAPI，含 Gemini provider + SAM provider、compose/slice/pipeline、Spine parser/skin_writer/atlas_repack

### 依赖与技术栈

- Python 3.9+ / opencv-python ≥4.8 / Pillow ≥10.0 / numpy ≥1.24
- 语言占比：Python 229KB / TypeScript 127KB / HTML 47KB / CSS 40KB
- 外部服务：Google Gemini（拆图+换皮）、SAM-3（分割）
- 兼容 OpenClaw 智能体运行时

## 四、三种使用方式

- **A. Claude Projects（推荐）**：新建 Project → 把 SKILL.md 全文粘进 Project Knowledge → 上传素材 + 描述需求即可。因 SKILL.md 内嵌全部脚本，无需克隆。
- **B. Claude 自定义 Skill**：`git clone` 到 `/mnt/skills/user/spine-animation`，Claude 下次会话自动发现加载。
- **C. 手动流水线（无需 Claude）**：依次跑 split_character → position_parts → build_spine_json → make_atlas → generate_spine_player。

### AI 调整格式

Claude 分析骨骼后输出的修正记录同时保存三个值：`original_offset`（原偏移）、`user_offset`（AI 建议增量 dx/dy/drot）、`final_offset`（应用后最终值），并附 `draw_order`。这让每次调整可审查、可回退、可组合。

## 五、实际应用场景（结合用户项目背景）

用户记忆中有 **AI Game Studio / 序列帧动画生成工具** 的研究方向，本仓库高度相关：

1. **2D 游戏角色动画自动化**：适合独立游戏/小团队，把"美术出图 → 绑骨 → 出动画"里最耗时的绑骨定位环节交给 AI，用户只需提供分好层的 PNG。
2. **Claude Skill 编写范式参考**：其 `SKILL.template.md + build_skill.py + GitHub Actions` 的"模板+脚本内嵌自动生成自包含 SKILL.md"模式，非常值得借鉴到用户自己的 vc-* / module-development 技能生产流程中——解决了"skill 里如何携带可运行代码"的问题。
3. **AI 换皮流水线（Reskin）**：Gemini 全局重绘 + SAM 精确切片 + 按 slot 重装的思路，可复用到任何"给已绑骨角色批量换风格/换配色"的量产需求。
4. **传统 CV + LLM 混合**：SIFT/RANSAC/遮挡分析这类经典计算机视觉算法 + Gemini/SAM 大模型的混合管线，是 AI 时代美术工具的典型工程范式，可作为架构参考。

⚠️ **许可证注意**：PolyForm Noncommercial 1.0.0，仅非商业免费，商用需单独联系 genielabs.tech 授权。
