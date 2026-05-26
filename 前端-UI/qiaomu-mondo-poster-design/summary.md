# qiaomu-mondo-poster-design 研究总结

> 仓库地址：https://github.com/joeseesun/qiaomu-mondo-poster-design
> 研究日期：2026-05-26

## 一、仓库概述

Qiaomu Mondo Poster Design 是一款 AI 海报设计工具，一句话生成大师级海报、书籍封面、专辑封面和各类设计作品。无需懂 PS、配色或艺术史，AI 自动选择最佳风格（基于 20 位传奇海报设计师）。支持电影海报、读书笔记、公众号封面、小红书配图等。默认 9:16 竖版，完美适配社交媒体。包含 AI 提示词优化、风格对比、图生图转换功能。触发词："Mondo风格"、"书籍封面" 等。

## 二、核心能力

### 2.1 支持的生成类型

| 类型 | 尺寸 | 说明 |
|---|---|---|
| 电影海报 | 21:9 | 2.35:1 比例 |
| 书籍封面 | 3:4 | 竖版图书 |
| 专辑封面 | 3:4 | 音乐专辑 |
| 公众号封面 | 16:9 | 9:16 竖版 |
| 小红书配图 | 16:9 | 9:16 竖版 |
| 艺术海报 | 多尺寸 | 通用海报 |

### 2.2 内置艺术家风格（部分）

| 艺术家 | 说明 |
|---|---|
| Saul Bass | 索尔·巴斯（著名电影海报设计师）|
| Kyle Lambert | 插画师 |
| Charley Harper | 查利·哈珀 |
| Hergé | 艾尔热（丁丁历险记作者）|
| Paula Scher | 宝拉·谢尔 |
| ... | ... |

### 2.3 核心功能

| 功能 | 说明 |
|---|---|
| AI 提示词优化 | 自动优化描述以获得最佳效果 |
| 风格对比 | 不同风格对比展示 |
| 图生图转换 | 参考图转换为目标风格 |
| 9:16 竖版 | 默认竖版格式，适配社交媒体 |
| 批量生成 | 一次生成多张 |

### 2.4 命令示例

```bash
# 安装
npmpx skills add joeseesun/qiaomu-mondo-poster-design

# 生成电影海报
python3 ~/.claude/skills/qiaomu-mondo-poster-design/scripts/generate_mondo_enhanced.py "阿尔丰斯·穆夏" movie -a "AI"
```

## 三、技术架构

### 3.1 技术栈

- **语言**：Python + TypeScript
- **框架**：Claude Code Skill
- **部署**：Vercel

### 3.2 目录结构

```
qiaomu-mondo-poster-design/
├── scripts/
│   └── generate_mondo_enhanced.py  # 增强生成脚本
├── examples/                         # 示例图片
├── docs/
│   └── adr/                         # 架构决策记录
├── SKILL.md                          # 主 skill 文件
├── README.md
└── ...
```

### 3.3 生成模式

- **单图生成**：指定艺术家 + 类型
- **批量生成**：列表指定多个类型
- **图生图**：AI 增强参考图

## 四、项目信息

- **Stars**：812
- **语言**：Python + TypeScript
- **许可证**：MIT
- **创建者**：joeseesun
- **版本**：v1.0.0
- ** Topics**：poster-design, ai-art, claude-code, skill

## 五、与 qiaomu-artist-style 的对比

| 维度 | qiaomu-mondo-poster-design | qiaomu-artist-style |
|---|---|---|
| 定位 | 完整海报/封面设计 | 艺术风格对比库 |
| 功能 | 生成完整设计作品 | 风格选择 + 参考图 |
| 触发词 | Mondo风格 | 艺术家名称 |
| Stars | 812 | 116 |
| 场景 | 社媒内容创作 | 风格研究/选择 |

两者配合：先用 artist-style 找到合适风格，再用 mondo-poster-design 生成完整作品。